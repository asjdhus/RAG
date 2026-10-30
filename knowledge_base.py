import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter
from datetime import datetime
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()
def check_md5(md5_str:str):#检查这份数据是否处理过
    if not os.path.exists(config.md5_path):
        open(config.md5_path,"w",encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path,"r",encoding="utf-8").readlines():
            line=line.strip()          #处理字符串的的空格和回车
            if line==md5_str:
                return True            #已经处理过
        return False
        


def save_md5(md5_str:str):           #保存这份数据的md5值
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str+"\n")
    


def get_string_md5(input_str:str,encoding="utf-8"):    #将传入的字符串转化为md5值
    #将字符串转换为字节流
    byte_str=input_str.encode(encoding)
    #计算md5值
    md5=hashlib.md5()
    md5.update(byte_str)
    md52=md5.hexdigest()
    return md52  


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)               #文件夹不存在则创建
        self.chroma=Chroma(                                               #向量存储的实例Chroma向量库对象
            collection_name=config.collection_name,                       #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,                   #数据库本地存储路径
        )
        #文本分割器对象
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,                      #每个文本块的字符数
            chunk_overlap=config.chunk_overlap,                #每个文本块之间的重叠字符数
            separators=config.separators,                       #自然段落划分的符号
            length_function=len,                                #计算文本块的长度的函数
            )
    def  upload_by_str(self,data:str,filename):
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "数据已经处理过"
        if len(data)>config.max_split_char_number:
            knowledge_chunks: list[str]=self.spliter.split_text(data)
        else:
            knowledge_chunks: list[str]=[data]
            
        metadata=   {   "source":filename,
                        "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "opreator":"AAAA"
                        }        
        self.chroma.add_texts(texts=knowledge_chunks,
                              metadatas=[metadata for chunk in knowledge_chunks])            #内容加载进向量库中了
        save_md5(md5_hex)
        return "数据上传成功"
        
                                                             
        
    
    
# if __name__=="__main__":
#     a=KnowledgeBaseService()
#     print(a.upload_by_str("你好","test.txt"))