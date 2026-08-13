"""
StateGraph 组装（填空版）—— W8 的学习重点

LangGraph 核心概念：
  StateGraph(State)  创建状态图：节点 + 边组成的有向图
  add_node("名字", 函数)  添加节点（节点就是普通函数）
  add_edge(A, B)     添加边：A 执行完后轮到 B
  START / END        图的起点和终点（特殊标记）
  compile(checkpointer)  编译成可调用的 app（checkpointer 负责状态持久化）

条件路由（进阶，本周先不做）：用 add_conditional_edges 让图根据条件走分支。
"""
from langgraph.graph import StateGraph, START, END
# ↑ START/END 是图的入口和出口标记，不是真的节点

from state import RAGState          # 状态类型
from nodes import retrieve_node, generate_node   # 两个工作流节点

# 填空1：创建状态图
# 提示：StateGraph(RAGState)
graph = StateGraph(RAGState)

# 填空2：添加节点（retrieve 和 generate）
# 提示：graph.add_node()
#       graph.add_node()
graph.add_node("retrieve",retrieve_node)
graph.add_node("generate",generate_node)

# 填空3：起始边——从 START 进入 retrieve
# 提示：graph.add_edge()
graph.add_edge(START,"retrieve")

# 填空4：retrieve 执行完 → generate
# 提示：graph.add_edge()
graph.add_edge("retrieve","generate")

# 填空5：generate 执行完 → END
# 提示：graph.add_edge("generate", END)
graph.add_edge("generate",END)

# 填空6：编译成可调用对象
# 提示：graph.compile()
# 进阶：加上 checkpoint 实现多轮记忆——
#   from langgraph.checkpoint.memory import MemorySaver
#   app = graph.compile(checkpointer=MemorySaver())
app = graph.compile()
