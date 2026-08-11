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
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url=os.getenv("SILICONFLOW_BASE_URL"),
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量把多个文档文本转成向量（文档入库时调用）。"""
        # 填空2：把每段超长文本截断到前 500 字符
        # 原因：bge 输入上限约 512 token，超长会被 API 拒绝

        
        texts = [t[:500] for t in texts]
        """
        截断方式会导致剩余部分被丢弃，检索不到
        只要保证chunk_size<embedding上限就不会触发截断
        可加上截断触发警报
        或换为拆分方式
        """
        all_embeddings = []                       # 收集所有批次的向量
        batch_size = 64                           # 每批 64 条，避免一次提交太多

        # 填空3：用 range 按 batch_size 步进遍历 texts，实现分批
        for i in range(0,len(texts),batch_size):
            # 填空4：取出当前这一批文本
            batch = texts[i:i+batch_size]

            # 填空5：调用 embedding API 把这一批文本转成向量
            # 提示：模型名 "BAAI/bge-large-zh-v1.5"
            resp = self.client.embeddings.create(
                model="BAAI/bge-large-zh-v1.5",
                input=batch,
                encoding_format="float",
            )
            # 填空6：把本批所有向量收进 all_embeddings
            # 提示：遍历 resp.data，取每个 d.embedding
            all_embeddings.extend(d.embedding for d in resp.data)
            """
            resp.data是OPENAI SDK返回的结果列表，一个对象对应一个输入的文本
            每个元素实际返回结构为
            {
                "object": "list",
                "data": [
                    {"object": "embedding", "index": 0, "embedding": [0.012, -0.045, 0.098, ...]},
                    {"object": "embedding", "index": 1, "embedding": [-0.033, 0.021, ...]},
                    {"object": "embedding", "index": 2, "embedding": [0.077, ...]}
                ],
                "model": "BAAI/bge-large-zh-v1.5",
                "usage": {"prompt_tokens": 1200, "total_tokens": 1200}
            }
            每个元素 d 有两个关键字段：d.index：这是第几个输入（从 0 开始，和传入顺序一一对应）
            d.embedding：这个文本的向量，本质是 list[float]，几百个浮点数
            """
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
        return resp.data[0].embedding
