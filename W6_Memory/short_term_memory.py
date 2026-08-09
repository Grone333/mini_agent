from collections import deque#导入双向队列：支持maxlen参数自动淘汰最旧元素

class ShortTermMemory:
    """
    短期记忆类
    滑动窗口,只保留最近N条消息
    """

    def __init__(self,window_size:int=5):
        """
        初始化短期记忆
        :param window_size: 窗口大小,即保留最近N条消息
        """
        self.window_size = window_size
        self.messages = deque(maxlen=window_size)  # 使用双向队列实现滑动窗口

    def add(self,role:str,content:str)->None:
        """
        添加消息到短期记忆
        :param role: 消息角色,如"user"或"assistant"
        :param content: 消息内容
        """
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        """
        获取短期记忆中的所有消息
        :return: 消息列表
        """
        return list(self.messages)

    def clear(self)->None:
        """
        清空短期记忆(窗口)，换话题时用
        """
        self.messages.clear()#deque自带的clear方法
        
