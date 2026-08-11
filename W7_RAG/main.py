"""
年报问答 RAG 系统（W7 版）—— 入口文件（填空版）

只负责四件事：路径配置、.env 加载、命令行参数、流程编排。
具体流程拆分到各模块：
  step01_loader.py      文档加载 + 切片
  step02_embedding.py   硅基流动 Embedding（文本 → 向量）
  step03_vectorstore.py Chroma 向量库（创建 / 复用 / 重建）
  step04_reranker.py    硅基流动 Rerank 重排序
  step05_llm.py         DeepSeek Chat 模型封装
  step06_chain.py       RAG 问答链 + 提问打印

【填空说明】
标了 填空N 的位置需要补全，上方有提示注释。
____________ 是合法的 Python 占位符，填完前语法能通过、运行会报错。
参考答案可以对照 E:\langchain-rag\main.py（原完整版）。
"""
import os                          # 标准库：路径拼接、环境变量读取
import sys                         # 标准库：命令行参数、控制台编码
from dotenv import load_dotenv     # 第三方库：从 .env 读取配置

from step01_loader import load_and_split_pdfs          # 模块：加载 + 切片
from step03_vectorstore import create_vectorstore, rebuild_vectorstore  # 模块：向量库
from step06_chain import create_qa_chain, ask          # 模块：问答链 + 提问

# 控制台输出改为 UTF-8，避免 Windows GBK 输出 emoji 报错
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ============================================================
# 路径配置：基于脚本自身位置，从任何目录运行都不受影响
# ============================================================
# 填空1：取本脚本所在目录
# 提示：os.path.dirname(os.path.abspath(__file__))
BASE_DIR = ____________

# 填空2：向量库目录 = BASE_DIR 下的 "chroma_db"
# 提示：os.path.join(BASE_DIR, "chroma_db")
CHROMA_DIR = ____________

# 填空3：资料目录 = BASE_DIR/data/documents
# 提示：os.path.join(BASE_DIR, "data", "documents")
DATA_DIR = ____________

# 加载 .env：先看 W7_RAG/.env，再看项目根目录 .env（兼容之前配好的 DEEPSEEK key）
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))


if __name__ == "__main__":
    # 命令行参数：--rebuild 强制重建；其余参数视为 PDF 路径
    args = sys.argv[1:]
    force_rebuild = "--rebuild" in args
    cli_pdfs = [a for a in args if a != "--rebuild"]

    if cli_pdfs:
        pdf_paths = cli_pdfs
    else:
        # 填空4：收集 DATA_DIR 下所有 .pdf 文件，排序后作为默认资料
        # 提示：os.listdir(DATA_DIR) 遍历 + endswith(".pdf") 过滤 + os.path.join 拼路径 + sorted
        pdf_paths = ____________
        if not pdf_paths:
            print(f"⚠️  {DATA_DIR} 下没有 PDF 文件，请把年报放进去或用命令行指定路径")
            sys.exit(1)

    # 填空5：需要强制重建时，删除旧向量库
    # 提示：if force_rebuild: rebuild_vectorstore(CHROMA_DIR)
    if force_rebuild:
        ____________

    # 填空6：第一步——加载 PDF + 切片，得到文本块
    # 提示：load_and_split_pdfs(pdf_paths)
    chunks = ____________

    # 填空7：第二步——向量化入库（已有向量库则复用）
    # 提示：create_vectorstore(chunks, CHROMA_DIR)
    vectorstore = ____________

    # 填空8：第三步——组装问答链
    # 提示：create_qa_chain(vectorstore)
    print("🔗 创建问答链...")
    qa = ____________
    print("✅ 就绪！输入问题开始对话（输入 q 退出）\n")

    # 交互式问答循环
    while True:
        question = input("💬 你的问题：")
        if question.lower() in ("q", "quit", "exit"):
            print("👋 再见！")
            break
        if question.strip():
            # 填空9：执行一次 RAG 问答并打印回答和来源
            # 提示：ask(qa, question)
            ____________
