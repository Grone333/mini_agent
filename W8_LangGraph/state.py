"""
LangGraph 状态定义

State 是节点之间传递的"共享笔记本"：
每个节点读取它需要的字段，往里面写入新字段，然后交给下一个节点。
"""
from typing import TypedDict, List


class RAGState(TypedDict):
    """RAG 工作流的状态。"""

    question: str        # 用户问题（起始输入）
    context: str         # 检索后拼接的文档内容（给 LLM 看）
    sources: List        # 引用来源列表（文件名 + 页码）
    answer: str          # 最终回答（输出）
    history: List        # 多轮对话历史（配合 checkpoint 持久化）
