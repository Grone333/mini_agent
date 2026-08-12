"""
RAG 问答链模块（流程第 3~5 步）—— 填空版

职责：
  1. PROMPT_TEMPLATE：RAG 的核心提示词（只根据文档回答，减少幻觉）
  2. create_qa_chain：把 向量检索 + Rerank + 提示词 + LLM 串成一条链
  3. ask：执行一次问答并打印回答和引用来源
"""
import os                          # 标准库：取文件名（打印参考来源时用）

from langchain.chains import RetrievalQA
# ↑ 经典的检索问答链：内部自动完成「检索 → 拼 prompt → 调用 LLM」

from langchain.prompts import PromptTemplate
# ↑ 提示词模板：用 {context} 和 {question} 两个占位符拼接最终 prompt

from langchain.retrievers import ContextualCompressionRetriever
# ↑ 包装检索器：先用基础检索器召回候选，再用 compressor 压缩/重排

from step05_llm import DeepSeekChat          # 复用 step05 里的 DeepSeek 封装
from step04_reranker import SiliconFlowReranker  # 复用 step04 里的重排实现

# 填空1：写 RAG 核心提示词模板（多行字符串）
# 要求：
#   - 告诉模型"只根据提供的文档内容回答，不要编造数据，信息不足要明确说明"
#   - 必须包含两个占位符：{context}（文档内容）和 {question}（用户问题）
#   - 结尾要求"请用中文回答"
PROMPT_TEMPLATE = """
请根据以下年报内容回答用户问题。只使用提供的文档信息，
不要编造数据。如果信息不足，请明确说明。

文档内容：{context}

用户问题：{question}

请用中文回答：

"""
def create_qa_chain(vectorstore):
    """创建问答链：向量库 + Rerank + 提示词 + LLM，串成一条链。"""
    # 填空2：创建大模型实例
    # 提示：DeepSeekChat()
    llm = DeepSeekChat()

    # 填空3：创建提示词模板
    # 提示：PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

    # 填空4：基础检索——向量检索先召回 20 个候选
    # 提示：vectorstore.as_retriever(search_kwargs={"k": 20})
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    # 填空5：创建重排器，精排后保留 5 个
    # 提示：SiliconFlowReranker(top_n=5)
    reranker = SiliconFlowReranker(top_n=5)

    # 填空6：用 ContextualCompressionRetriever 包装成"召回 → 重排"两阶段检索
    # 提示：ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
    retriever = ContextualCompressionRetriever(base_compressor=reranker,base_retriever=base_retriever)

    # 填空7：组装问答链
    # 提示：RetrievalQA.from_chain_type(
    #          llm=llm, chain_type="stuff", retriever=retriever,
    #          chain_type_kwargs={"prompt": prompt}, return_source_documents=True)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever,
        chain_type_kwargs={"prompt": prompt}, return_source_documents=True
        )
    return qa


def ask(qa, question: str):
    """提问并打印结果：执行一次完整的 RAG 流程。"""
    # 填空8：调用问答链并得到结果字典
    # 提示：qa.invoke({"query": question})
    result = qa.invoke({"query": question})
    # result["result"] 是答案；result["source_documents"] 是引用的文本块

    print(f"\n🤖 回答：\n{result['result']}\n")
    print("📎 参考来源：")
    seen = set()                                  # 用集合去重，避免同一页重复打印
    for doc in result["source_documents"]:        # 遍历检索到的每个片段
        source = doc.metadata.get("source", "未知")  # 从元信息取文件名
        page = doc.metadata.get("page", "?")         # 从元信息取页码
        key = f"{source}-{page}"                     # 用「文件-页码」作为去重键
        if key not in seen:
            # 填空9：打印来源（带页码，页码从 0 开始所以 +1），并记录到 seen 去重
            # 提示：print(f"   - {os.path.basename(source)} 第 {page+1} 页") + seen.add(key)
            print(f"   - {os.path.basename(source)} 第 {page+1} 页") 
            seen.add(key)
