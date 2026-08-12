"""
Rerank 重排序模块（检索后的精排环节）—— 填空版

职责：对向量检索召回的结果做二次精排——向量检索快但精度有限，
rerank 模型把 query 和每个候选片段一起打分，按分数取前 top_n 个。
"""
import os                          # 标准库：读取环境变量
import requests                    # 第三方库：调用硅基流动 Rerank API

from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
# ↑ 文档压缩器基类：实现 compress_documents 就能自定义"重排/过滤"逻辑


class SiliconFlowReranker(BaseDocumentCompressor):
    """使用硅基流动的 Rerank API 对检索结果重排序。"""

    model: str = "BAAI/bge-reranker-v2-m3"  # 重排模型
    top_n: int = 5                          # 重排后保留前几个
    api_key: str = ""                       # 硅基流动 API Key
    base_url: str = ""                      # 硅基流动接口地址

    def __init__(self, model: str = None, top_n: int = 5):
        # 填空1：调用父类初始化，把模型名/数量/Key/地址传进去
        # 提示：model 默认从环境变量 SILICONFLOW_RERANK_MODEL 读，没有就用默认值
        
        super().__init__(
            model=model or os.getenv("SILICONFLOW_RERANK_MODEL",""),
            top_n=top_n,
            api_key=os.getenv("SILICONFLOW_API_KEY", ""),
            base_url=os.getenv("SILICONFLOW_BASE_URL", ""),
        )

    def compress_documents(self, documents, query: str, **kwargs):
        """接收检索到的文档列表，按与 query 的相关度重排，返回前 top_n 个。"""
        if not documents:                        # 没有候选就直接返回空
            return []

        try:
            # 填空2：拼出 rerank 接口地址
            # 提示：base_url 以 /v1 结尾，后面拼 "/rerank"（f-string）
            url = self.base_url+f"/rerank"
            resp = requests.post(
                url,
                headers={
                    # 填空3：身份凭证请求头
                    # 提示：f"Bearer {self.api_key}"
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,                      # 重排模型
                    "query": query,                           # 用户问题
                    # 填空4：候选片段文本列表
                    # 提示：遍历 documents 取每个 d.page_content（列表推导式）
                    "documents": [d.page_content for d  in documents]  ,
                    "top_n": self.top_n,                      # 返回前几名
                },
                timeout=30,                        # 30 秒超时，避免一直卡住
            )
            resp.raise_for_status()               # HTTP 非 2xx 时抛异常
            results = resp.json().get("results", [])  # 官方接口：按分数从高到低排序
        except Exception as e:
            # rerank 失败时不阻塞问答：退回原始检索结果
            print(f"⚠️  Rerank 失败，退回原始检索结果：{e}")
            return documents

        # 填空5：按返回的 index 映射回原始 Document，保持新排序
        # 提示：遍历 results，取 item["index"] 作为 documents 的下标，
        #       把分数 item.get("relevance_score") 写进 doc.metadata["rerank_score"]
        reranked = []
        for item in results:
            idx = item["index"]
            if 0 <= idx < len(documents):
                doc = documents[idx]
                doc.metadata["rerank_score"]= item.get("relevance_score")
                reranked.append(doc)
        return reranked
