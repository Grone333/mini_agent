import re
import ast  
from tools.calculator import calculator
from tools.file_reader import file_reader
from tools.web_search import web_search
from tools.database_query import database_query
import os
import requests
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

#1.工具注册表
TOOLS={
    "calculator": calculator,
    "file_reader": file_reader,
    "web_search": web_search,
    "database_query": database_query
}

#2.系统提示词：规定输出格式
SYSTEM_PROMPT = """你是一个能调用工具回答问题的智能体。
规则：
1. 涉及计算的问题，必须调用 calculator 工具，禁止直接心算。
2. 每次只能输出一个 Action,参数要加引号,例如:Action: calculator("2+3*4")
3. 输出 Action 后必须等待 Observation,同一个回答里不能给出 Final Answer。
4. 看到 Observation 后，再输出：
Final Answer: 答案
需要工具时，必须严格按照以下格式输出：
Thought: 你的思考
Action: 工具名(参数)

知道答案时输出：
Final Answer: 答案
"""

#3.模型接口
DEEPSEEK_MODEL = "deepseek-v4-flash"
def ask_llm(message:list)->str:
    api_key=os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "请在环境变量中设置 DEEPSEEK_API_KEY"

    resp= requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization":f"Bearer {api_key}"},
        json={
            "model": DEEPSEEK_MODEL,
            "messages": message,
            "temperature": 0.3,
            "max_tokens": 1024,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

#4.解析并执行Action行
def run_tool(action: str) -> str:
    match = re.match(r"(\w+)\((.*)\)", action.strip())
    if not match:
        return f"Action 格式错误: {action}"
    name, args_str = match.group(1), match.group(2)
    if name not in TOOLS:
        return f"未知工具: {name}"
    try:

        parsed = ast.literal_eval(args_str)
    except (ValueError, SyntaxError):
        return f"参数解析失败: {args_str}"

    if isinstance(parsed, tuple):
        return str(TOOLS[name](*parsed))
    return str(TOOLS[name](parsed))


#5.ReAct循环
def react(question:str,max_steps:int=5)->str:
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":question}
    ]
    for step in range(max_steps):
        text =ask_llm(messages)
        print(f"---第{step+1}步---\n{text}\n")

        if "Final Answer" in text:
            return text
        if "Action:" in text:

            action = text.split("Action:")[1].split("\n")[0]
            obs=run_tool(action)
            messages.append({"role":"assistant","content":text})
            messages.append({"role":"user","content":f"Observation: {obs}"})
    return f"达到最大步数{max_steps}，仍未得到最终答案。"


if __name__=="__main__":
    question="2+3*4=?"
    answer=react(question)
    print(f"问题: {question}\n答案: {answer}")
