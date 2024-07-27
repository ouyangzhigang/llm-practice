import streamlit as st

container = st.container()

messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input('请输入你要问的问题')
if prompt:
    st.session_state.messages.append(prompt)

with container:
    with st.session_state.chat_message('user'):
        for message in messages:
            st.write(message)
