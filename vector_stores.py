import os
import config_data as config
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter
from datetime import datetime
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

class VectorStoreService(object):
    def __init__(self):
        #创建向量存储对象指定模型，路径，集合名称
        self.vector_stores = Chroma(
            persist_directory=config.persist_directory,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            collection_name=config.collection_name,
        )
    def get_retriever(self):
        #返回创建向量检索器
        return self.vector_stores.as_retriever(search_kwargs={"k": config.search_numbers})
    
    

# if __name__ == "__main__":
#     a=VectorStoreService()
#     retriever=a.get_retriever()
#     print(retriever.invoke("我的体重180斤，尺码推荐"))
#     print(VectorStoreService().get_retriever().invoke("我的体重180斤，尺码推荐"))
    
        