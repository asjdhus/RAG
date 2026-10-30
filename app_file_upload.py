import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务")    #标题
#文件上传
uploaded_file = st.file_uploader(
    "请上传txt文件",
    type=["txt"],
    accept_multiple_files=False,   #不接受多个文件上传
)

if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()


if uploaded_file is not None:
    file_name=uploaded_file.name
    file_type=uploaded_file.type
    file_size=uploaded_file.size/1024    #KB
    st.subheader(f"文件名是{file_name}")
    st.write(f"文件类型是{file_type}")
    st.write(f"文件大小是{file_size:.2f}KB")
    
    #读取文件内容 getvalue->字节流->decode("utf-8")->str
    file_content=uploaded_file.getvalue().decode("utf-8")
    st.write(f"文件内容是:\n{file_content}")
    
    
    res = st.session_state["service"].upload_by_str(file_content,file_name)
