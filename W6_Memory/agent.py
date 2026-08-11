import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding="utf-8")
W5_DIR = str(Path(__file__).resolve().parent.parent/"W5_ReAct")
sys.path.insert(0, W5_DIR)  # 将W5_ReAct目录添加到系统路径中，以便导入模块

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from tools.calculator import calculator
from short_term_memory import ShortTermMemory
from long_term_memory import LongTermMemory
from decision_router import decide




TOOLS={
    "calculator": calculator,
}


def ask_llm(messages:list)->str:
    """
    调用LLM接口,传入对话列表,返回LLM的输出
    :param messages: 对话列表,每条消息是字典,包含role和content
    :return: LLM的输出文本
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
    resp =requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "deepseek-v4-flash",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1024,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

short_mem = ShortTermMemory(window_size=5)  # 短期记忆,保留最近5条消息
long_mem = LongTermMemory()


def run_tool(tool_name:str, args_str:str)->str: #简化版工具执行
    if tool_name not in TOOLS:
        return f"未知工具:{tool_name}"
    return str(TOOLS[tool_name](args_str))


def build_messages(user_input: str)->list:# 组装发给模型的完整对话
    hits = long_mem.search(user_input,k=3)
    memory_text = "\n".join(hits) if hits  else "(无相关记忆)"# 命中的记忆拼成一段文本
    system = f"你是问答助手。以下是可能相关的长期记忆：\n{memory_text}"
    return ([{"role":"system","content":system}]# 第一条：系统消息（含记忆
            +short_mem.get_messages()           # 中间：滑动窗口里的历史对话
            +[{"role": "user", "content": user_input}])    # 最后：当前输入


def run() ->None: # 主循环：一问一答
    try:
        while True:
            user_input=input("你：")

            decision=decide(ask_llm,user_input)# 第一步：路由判定该干什么

            if decision["action"]=="save_memory":# 分支一：需要记住信息
                long_mem.add(decision["text"])
                reply ="记住了"


            elif decision["action"]=="tool":# 分支二：需要调用工具
                obs= run_tool(decision["tool"],decision["args"])
                reply= ask_llm(build_messages(f"工具返回: {obs}，请给出最终回答"))


            else: # 分支三：直接回答
                reply = ask_llm(build_messages(user_input))


            short_mem.add("user",user_input) # 这一轮用户输入写进短期窗口
            short_mem.add("assistant",reply)
            print("助手：",reply)
    except KeyboardInterrupt:
        print("\n已退出")

if __name__=="__main__":
    run()


