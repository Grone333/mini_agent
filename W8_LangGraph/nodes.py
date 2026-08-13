"""
工作流节点 —— 每个节点是一个普通函数 (state) -> dict

规则：函数接收整个状态字典，返回"要更新的字段"组成的字典。
复用 W7_RAG 的组件：向量库、重排、LLM 都直接 import。
"""
import os
import sys
from pathlib import Path

# 把 W7_RAG 目录加进搜索路径，才能 import 它的 step 模块
W7_DIR = str(Path(__file__).resolve().parent.parent / "W7_RAG")
sys.path.insert(0, W7_DIR)
CHROMA_DIR = os.path.join(W7_DIR, "chroma_db")   # 复用 W7 建好的向量库

from langchain_community.vectorstores import Chroma      # 向量库
from step02_embedding import SiliconFlowEmbeddings       # 文本 → 向量
from step04_reranker import SiliconFlowReranker          # 重排
from step05_llm import DeepSeekChat                      # DeepSeek 模型
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


_vectorstore = None   # 模块级缓存：向量库只加载一次


def get_vectorstore():
    """懒加载 W7 建好的向量库（首次调用时加载，之后复用）。"""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=CHROMA_DIR,                 # W7 的持久化目录
            embedding_function=SiliconFlowEmbeddings(),   # 检索问题时要向量化
        )
    return _vectorstore


def retrieve_node(state: dict) -> dict:
    """检索节点：问题 → 向量召回 20 个 → Rerank 精排 5 个 → 拼 context 和 sources。"""
    question = state["question"]                          # 从状态里取用户问题
    base = get_vectorstore().as_retriever(search_kwargs={"k": 20})  # 向量召回 20
    docs = SiliconFlowReranker(top_n=5).compress_documents(
        base.invoke(question), question                   # 再精排成 5 个
    )

    context = "\n\n".join(d.page_content for d in docs)   # 文档拼成一段文本
    sources = [                                           # 记录引用来源
        {"source": d.metadata.get("source", ""), "page": d.metadata.get("page", 0)}
        for d in docs
    ]
    return {"context": context, "sources": sources}       # 只返回要更新的字段


def generate_node(state: dict) -> dict:
    """生成节点：context + 历史 + 问题 → DeepSeek 回答。"""
    system = (
        "你是年报问答助手。只根据下面的文档内容回答，不要编造数据。\n\n"
        f"文档内容：\n{state['context']}"
    )
    messages = [SystemMessage(content=system)]            # 系统消息带检索结果

    # 多轮记忆：把最近 4 轮历史拼进对话（配合 checkpoint 持久化）
    for role, content in state.get("history", [])[-4:]:
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))
    messages.append(HumanMessage(content=state["question"]))  # 当前问题

    answer = DeepSeekChat().invoke(messages).content      # 调用模型拿回答
    history = state.get("history", []) + [                # 更新历史
        ("user", state["question"]),
        ("assistant", answer),
    ]
    return {"answer": answer, "history": history}
