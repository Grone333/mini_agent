"""
Embedding 模块（流程第 2 步的一部分）—— 填空版

职责：把文本变成向量（embedding），供 Chroma 入库和检索使用。
实现：封装硅基流动的 Embedding API（OpenAI 兼容接口）。
"""
import os                         # 标准库：读取环境变量（API Key、接口地址）

from langchain_core.embeddings import Embeddings
# ↑ LangChain 的 Embeddings 抽象基类：规定嵌入模型必须实现哪些方法

from openai import OpenAI
# ↑ OpenAI SDK。硅基流动提供 OpenAI 兼容接口，可直接复用


class SiliconFlowEmbeddings(Embeddings):
    """使用硅基流动的 Embedding API（OpenAI 兼容接口）。"""

    def __init__(self):
        # 填空1：创建 OpenAI 客户端，但把 base_url 指向硅基流动的服务器
        # 提示：api_key 从环境变量 SILICONFLOW_API_KEY 读
        #       base_url 从环境变量 SILICONFLOW_BASE_URL 读
        self.client = OpenAI(
            api_key=____________,
            base_url=____________,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量把多个文档文本转成向量（文档入库时调用）。"""
        # 填空2：把每段超长文本截断到前 500 字符
        # 原因：bge 输入上限约 512 token，超长会被 API 拒绝
        # 提示：[t[:500] for t in texts]
        texts = ____________

        all_embeddings = []                       # 收集所有批次的向量
        batch_size = 64                           # 每批 64 条，避免一次提交太多

        # 填空3：用 range 按 batch_size 步进遍历 texts，实现分批
        # 提示：range(0, len(texts), batch_size)
        for i in ____________:
            # 填空4：取出当前这一批文本
            # 提示：texts[i:i + batch_size]
            batch = ____________

            # 填空5：调用 embedding API 把这一批文本转成向量
            # 提示：模型名 "BAAI/bge-large-zh-v1.5"，input 传 batch
            resp = self.client.embeddings.create(
                model=____________,
                input=____________,
                encoding_format="float",
            )
            # 填空6：把本批所有向量收进 all_embeddings
            # 提示：遍历 resp.data，取每个 d.embedding
            all_embeddings.extend(____________)
        return all_embeddings

    def embed_query(self, text: str) -> list[float]:
        """把单个查询文本（用户问题）转成向量（检索时调用）。"""
        text = text[:500]                         # 同样截断，防止超长
        resp = self.client.embeddings.create(
            model="BAAI/bge-large-zh-v1.5",
            input=text,
            encoding_format="float",
        )
        # 填空7：返回第一个（也是唯一一个）向量
        # 提示：resp.data[0].embedding
        return ____________
