"""
Gradio 网页界面：把 LangGraph 工作流变成可对话的网页

运行：python app.py → 浏览器自动打开本地页面
"""
import gradio as gr                       # 网页界面库
from graph import app                     # 编译好的状态图（graph.py 填完才能跑）


def chat(message, history):
    """Gradio 回调函数：message=本轮输入，history=网页端已显示的对话。"""
    # thread_id 是"会话身份证"：同一个 id 的多次调用共享 checkpoint 记忆
    config = {"configurable": {"thread_id": "user-1"}}

    # 调用工作流：只传入问题，其余字段由 checkpoint 从上次状态恢复
    state = app.invoke({"question": message}, config=config)
    return state["answer"]


if __name__ == "__main__":
    # ChatInterface 是最简单的聊天组件：传入回调函数即可
    demo = gr.ChatInterface(fn=chat, type="messages", title="年报问答 Agent（LangGraph 版）")
    demo.launch()                          # 启动本地网页服务
