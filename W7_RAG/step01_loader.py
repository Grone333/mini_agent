"""
文档加载与切片模块（流程第 1 步）—— 填空版

职责：
  1. 用 PyPDFLoader 把 PDF 的每一页读成一个 Document 对象
  2. 用 RecursiveCharacterTextSplitter 按语义切分成小文本块
"""
from langchain_community.document_loaders import PyPDFLoader
# ↑ langchain-community 提供的 PDF 加载器

from langchain.text_splitter import RecursiveCharacterTextSplitter
# ↑ 递归字符文本分割器：按 separators 优先级从粗到细切分，尽量保住语义


def load_and_split_pdfs(pdf_paths: list[str]):
    """加载多份 PDF 并按语义分块。

    参数 pdf_paths: PDF 文件路径列表（可以传一份或多份年报）
    返回值: list[Document]，即分割后的文本块列表
    """
    documents = []                       # 收集所有 PDF 的页面
    for pdf_path in pdf_paths:           # 逐份加载
        print(f"📄 加载 PDF: {pdf_path}")

        # 填空1：创建 PDF 加载器（此刻还没真正读文件）
        # 提示：PyPDFLoader(pdf_path)
        loader = ____________

        # 填空2：真正读取 PDF，返回一页一个 Document
        # 提示：loader.load()
        docs = ____________
        print(f"   共 {len(docs)} 页")
        documents.extend(docs)           # 把这一份的页面并进总列表
    print(f"   合计 {len(documents)} 页")

    # 填空3：创建分割器，参数含义：
    #   chunk_size=400   每块目标约 400 字符
    #   chunk_overlap=80 相邻块重叠 80 字符，防止跨块信息被切断
    #   separators=["\n\n", "\n", "。", "；", "，", " ", ""] 段落→行→句→词→字符
    splitter = ____________

    # 填空4：对全部页面统一切分成文本块
    # 提示：splitter.split_documents(documents)
    chunks = ____________
    print(f"   分割成 {len(chunks)} 个文本块")
    return chunks
