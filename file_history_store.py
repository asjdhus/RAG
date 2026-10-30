import os
import json
from typing import Sequence
from langchain_core.messages import BaseMessage, message_to_dict,messages_from_dict
#message_to_dict:单个消息对象（BaseMessage(AIMessage,HumanMessage,SystemMessage)）转换为字典（dict[str, Any]）
#messages_from_dict:[字典，字典]->[消息，消息]
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory



def get_history(session_id,storage_path='./chat_history'):
    return FileChatMessageHistory(session_id,storage_path)


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id,storage_path):
        self.session_id=session_id                 #会话id
        self.storage_path=storage_path             #不同会话id的存储文件所在的文件夹路径
        self.file_path=os.path.join(self.storage_path,self.session_id)    #完整的文件路径
        
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:         #Sequence类似list,tuple
        all_messages=list(self.messages)          #已有的消息列表
        all_messages.extend(messages)             #添加新的消息融合成一个list
        
        #将数据同步写入到文件中,类对象写入文件->一堆二进制,为了方便，可以将BaseMessage转换为字典(借助json模块以json字符串写入文件)
        #message_to_dict:单个消息对象（BaseMessage(AIMessage,HumanMessage,SystemMessage)）转换为字典（dict[str, Any]）
        
        
        # new_messages=[]
        # for message in all_messages:
        #     d=message_to_dict(message)
        #     new_messages.append(d)
        
        new_messages=[message_to_dict(message) for message in all_messages]    #列表推导式，和上面写法一样
        #将数据写入文件
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f)
            
    @property       #属性装饰器，将方法转换为属性  self.messages相当于执行messages方法
    def messages(self) -> Sequence[BaseMessage]:
        #从文件中读取数据，当前文件中是list[字典]
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                data=json.load(f)          #返回值是list[字典]
                messages=messages_from_dict(data)
                return messages
        except FileNotFoundError:
            return []
        #将字典转换为消息对象
        
    
    def clear(self) -> None:
        #清空文件
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f)
                 
        
        
        