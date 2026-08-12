"""
DeepSeek 大模型封装模块 —— 填空版

职责：把 DeepSeek Chat API 封装成 LangChain 聊天模型，
这样它就能直接接进 LangChain 的问答链（RetrievalQA）里。
"""
import os                         # 标准库：读取环境变量（API Key、接口地址）

from langchain_core.language_models import BaseChatModel
# ↑ LangChain 的聊天模型抽象基类：实现 _generate 就能接入生态

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# ↑ LangChain 统一的消息类型：系统 / 用户 / 助手

from langchain_core.outputs import ChatResult, ChatGeneration
# ↑ 模型返回值的封装：ChatResult 包含多个 ChatGeneration，每个含一条 AIMessage

from openai import OpenAI
# ↑ OpenAI SDK，DeepSeek 提供 OpenAI 兼容接口


class DeepSeekChat(BaseChatModel):
    """把 DeepSeek Chat API 封装成 LangChain 聊天模型。"""

    client: OpenAI = None              # 类属性声明：OpenAI 客户端（在 __init__ 里真正赋值）
    model_name: str = "deepseek-v4-flash"  # 使用的模型名

    class Config:
        arbitrary_types_allowed = True  # pydantic 配置：允许 client 这种非标准类型

    def __init__(self):
        super().__init__()              # 先完成 BaseChatModel 自身的初始化
        # 填空1：创建 DeepSeek 的 OpenAI 兼容客户端
        # 提示：api_key 从 DEEPSEEK_API_KEY 读，base_url 从 DEEPSEEK_BASE_URL 读
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL"),
        )

    @property
    def _llm_type(self) -> str:
        return "deepseek-v4-flash"      # 模型类型标识（主要用于日志/追踪）

    def _generate(self, messages, stop=None, **kwargs):
        """核心方法：接收 LangChain 消息列表，返回 ChatResult。"""
        msgs = []                       # 准备 OpenAI 风格的消息列表
        for msg in messages:            # 遍历 LangChain 消息，翻译成 OpenAI 格式
            # 填空2：三种消息分别转成 {"role": ..., "content": ...} 字典
            # 提示：SystemMessage → "system" / HumanMessage → "user" / AIMessage → "assistant"
            if isinstance(msg, SystemMessage):
                msgs.append({"role": "system","content":msg.content})
            elif isinstance(msg, HumanMessage):
                msgs.append({"role": "user","content":msg.content})
            elif isinstance(msg, AIMessage):
                msgs.append({"role": "assistant","content":msg.content})

        # 填空3：调用 DeepSeek 对话接口（temperature=0.3，回答更保守）
        resp = self.client.chat.completions.create(
            model=self.model_name,
            messages=msgs,
            temperature=0.3,
        )

        # 填空4：取出模型生成的文本
        # 提示：resp.choices[0].message.content
        content = resp.choices[0].message.content

        # 填空5：包回 LangChain 的标准结果格式
        # 提示：ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])
