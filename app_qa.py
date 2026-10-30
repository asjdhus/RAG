import streamlit as st
from rag import RAGService
import time
import config_data as config

#标题

st.title("智能客服")
st.divider()               #分隔符

if "rag_service" not in st.session_state:
    st.session_state["rag_service"] = RAGService()

if "message" not in st.session_state:                      #存储历史记录
    st.session_state["message"] = []
    st.session_state["message"].append({"role": "assistant", "content": "我是智能客服，您好，有什么我可以帮助您的吗？"})

for message in st.session_state["message"]:                #显示历史记录
    st.chat_message(message["role"]).write(message["content"])
#提供用户输入栏
prompt = st.chat_input("请输入您的问题")
if prompt:                #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    res_list=[]
    with st.spinner("思考中..."):
        time.sleep(1)
        response = st.session_state["rag_service"].chain.stream({"input": prompt},config.session_config) 
        def capture_response(generator,res_list=res_list):
            for chunk in generator:
                res_list.append(chunk)
            yield chunk
        st.chat_message("assistant").write_stream(capture_response(response))
        # st.session_state["message"].append({"role": "assistant", "content": response})
        st.session_state["message"].append({"role": "assistant", "content": "".join(res_list)})
