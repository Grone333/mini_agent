import json

ROUTER_PROMPT="""
你是路由决策器。根据用户输入,只输出一行JSON,不要输出任何其他内容。
可用工具:calculator(数学计算)、search_memory(检索长期记忆)、save_memory(保存长期记忆)。
输出格式三选一：
{"action": "tool", "tool": "calculator", "args": "2+3*4"}
{"action": "save_memory", "text": "要记住的信息"}
{"action": "answer"}
"""

def decide(ask_llm,user_input:str)->dict:
    """
    决策器,根据用户输入决定使用哪个工具
    :param ask_llm: 调用LLM的函数,传入prompt和user_input,返回LLM的输出
    :param user_input: 用户输入
    :return: 决策结果,字典格式
    """
    messages=[# 构造发给模型的对话列表
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": user_input}
    ]
    text=ask_llm(messages)# 调用LLM,期望返回一行JSON
    try:#尝试解析输出
        return json.loads(text)
    except json.JSONDecodeError:
        return {"action": "answer"}#解析失败,默认返回答案
