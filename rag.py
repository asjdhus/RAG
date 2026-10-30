from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import os
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from file_history_store import get_history
from langchain_core.runnables import RunnableLambda

load_dotenv()
class RAGService(object):
    def __init__(self):
        self.vector_store_service=VectorStoreService()       #向量检索器
        self.prompt_template=ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知参考资料为主，回答我的问题。参考资料：{context}"),
            ("system", "并且我提供历史会话"),
            MessagesPlaceholder("history"),
            
            ("user", "请回答用户提问：{input}"),
        ])
        self.chat_model=ChatTongyi(model="glm-5")   
           
        self.chain=self.__get_chain()
    
    
    def Prompt1(self,prompt):
        print(prompt.to_string())
        return prompt
    
    def __get_chain(self):                     #创建链
        retriever=self.vector_store_service.get_retriever()
        
        def format_document(docs: list[Document]):
                if not docs:
                    return "无相关参考资料"
                format=""
                for doc in docs:
                    format+=f"文档片段：{doc.page_content}\n"
                return format
        
        def temp1(values):              #从字典中的key为input的值中提取他的值（str）输入给向量检索器
            return values["input"]
        
        def temp2(value):             #RunnablePassthrough会接收传入的字典，最终变成{"input":{"input":"怎么洗涤","history":[]},"context":"无相关参考资料"}
                                      #用temp2把他们提取出来变成{"input":"怎么洗涤","history":[],"context":"无相关参考资料"}传给prompt_template
            new_value={}
            new_value["input"]=value["input"]["input"]
            new_value["history"]=value["input"]["history"]
            new_value["context"]=value["context"]
            return new_value
        
        chain=(
            {
                "input": RunnablePassthrough(),"context": RunnableLambda(temp1) | retriever | format_document,
             } | RunnableLambda(temp2) | self.prompt_template | self.Prompt1 | self.chat_model | StrOutputParser()
        )
        
        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history,
            input_message_key="input",
            history_messages_key="history"
        )
            
                                   
        
        return conversation_chain

# if __name__ == "__main__":
#     #配置session_id
#     session_config={
#         "configurable":{
#             "session_id":"user1"
#         }
#     }
#     rag_service=RAGService()
#     print(type(rag_service.vector_store_service.vector_stores))
#     print(rag_service.chain.invoke({"input":"怎么洗涤"},session_config))
