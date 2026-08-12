"""
向量库模块（流程第 2 步）—— 填空版

职责：
  1. create_vectorstore：把文本块向量化写入 Chroma；已存在则直接复用
  2. rebuild_vectorstore：删除旧向量库目录（带路径安全校验）
"""
import os                          # 标准库：路径拼接、判断文件是否存在
import shutil                      # 标准库：递归删除目录（--rebuild 时用）

from langchain_community.vectorstores import Chroma
# ↑ langchain-community 的 Chroma 向量数据库封装

from step02_embedding import SiliconFlowEmbeddings
# ↑ 复用 step02 里的中文向量化实现


def create_vectorstore(chunks, persist_dir):
    """创建或复用向量存储。

    如果 persist_dir 里已有 Chroma 数据（chroma.sqlite3），就直接从磁盘加载，
    跳过向量化；否则才重新向量化并写入。
    """
    # 填空1：创建嵌入模型实例（加载和写入都需要）
    # 提示：SiliconFlowEmbeddings()
    embeddings = SiliconFlowEmbeddings()

    # 判断向量库是否已存在：目录里出现 chroma.sqlite3 就说明建过库
    # 填空2：拼出 chroma.sqlite3 的完整路径
    # 提示：os.path.join(persist_dir, "chroma.sqlite3")
    chroma_db_file = os.path.join(persist_dir,"chroma.sqlite3")

    if os.path.exists(chroma_db_file):
        print(f"♻️  检测到已有向量库 {persist_dir}，直接复用（跳过向量化）")
        try:
            # 填空3：从磁盘加载已有向量库（不重新 embedding）
            # 提示：Chroma(persist_directory=persist_dir, embedding_function=embeddings)
            return Chroma(persist_directory=persist_dir,embedding_function=embeddings)
        except Exception as e:
            # 万一库损坏加载失败，就降级为重新构建
            print(f"⚠️  已有向量库加载失败（{e}），重新构建")

    print("🧠 正在向量化文本块...")
    # 填空4：向量化 + 入库一步完成
    # 提示：Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_dir)
    vectorstore = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory=persist_dir)
    print(f"   已存入 {persist_dir}")
    return vectorstore                          # 返回向量库对象（自带检索能力）


def rebuild_vectorstore(persist_dir):
    """删除已有的向量库目录，用于更换资料后强制重建。"""
    abs_dir = os.path.abspath(persist_dir)                    # 转为绝对路径
    project_dir = os.path.abspath(os.path.dirname(__file__))  # 本模块所在目录

    # 填空5：路径安全校验——防止误删别的目录，三个条件同时满足才允许删：
    #   1) 目标确实是目录（os.path.isdir(abs_dir)）
    #   2) 它的父目录就是项目目录（os.path.dirname(abs_dir) == project_dir）
    #   3) 目录名是 "chroma_db"（os.path.basename(abs_dir) == "chroma_db"）
    is_safe = (os.path.isdir(abs_dir) and os.path.dirname(abs_dir)==project_dir
               and os.path.basename(abs_dir)=="chroma_db")
    
    if is_safe:
        print(f"🗑️  删除旧向量库 {abs_dir}（--rebuild）")
        # 填空6：递归删除该目录
        # 提示：shutil.rmtree(abs_dir)
        shutil.rmtree(abs_dir)
    else:
        print(f"⚠️  跳过删除：{abs_dir} 不是项目内的 chroma_db 目录")
