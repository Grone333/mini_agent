import chromadb #导入向量数据库客户端

class LongTermMemory:
    """
    长期记忆,向量化嵌入Chroma
    跨会话可检索
    """
    def __init__(self,persist_dir:str="W6_Memory/chroma.db",collection_name:str="memories"):
            """
            初始化长期记忆
            :param persist_dir: 持久化目录,用于存储向量数据库
            :param collection_name: 集合名称,用于存储消息
            """
            self.client = chromadb.PersistentClient(path=persist_dir)  # 连接磁盘上的库，重启不丢
            self.collection = self.client.get_or_create_collection(collection_name)  # 获取或创建集合
            self.next_id=self.collection.count()  # 已有条数作为起始ID,避免覆盖已有数据

    def add(self,text:str)->None:
        """
        添加消息到长期记忆
        :param text: 消息内容
        """
        self.collection.add(
            documents=[text],
            ids=[str(self.next_id)]
        )#向量化写入集合
        self.next_id += 1  

    def search(self,query:str,top_k:int=3):
        """
        检索长期记忆
        :param query: 查询内容
        :param top_k: 返回最相似的前K条消息
        :return: 最相似的消息列表
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )#向量化查询集合
        return results['documents'][0]  # 返回最相似的消息列表
