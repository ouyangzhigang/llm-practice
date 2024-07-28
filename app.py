import streamlit as st
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import AIMessage, HumanMessage
from tongyi import tongyi_chat_model

st.title('Chat bot demo')

memory_key = 'history'

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'you are a helpful chat bot'),
        MessagesPlaceholder(variable_name=memory_key),
        ('human', '{input}')
    ]
)


class Message(BaseModel):
    content: str
    role: str


if "messages" not in st.session_state:
    st.session_state.messages = []


def to_message_place_holder(messages):
    return [
        AIMessage(content=msg['content']) if msg['role'] == 'bot' else HumanMessage(content=msg['content']) for
        msg in messages
    ]


model = tongyi_chat_model
parser = StrOutputParser()

chain = {
    'input': lambda x: x['input'],
    'history': lambda x: to_message_place_holder(x['messages'])
} | prompt | model | parser

left, right = st.columns([0.7, 0.3])

with left:
    container = st.container()
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.write(message['content'])

    prompt_input = st.chat_input('请输入内容')
    if prompt_input:
        st.session_state.messages.append(Message(content=prompt_input, role='human').model_dump())
        with container:
            with st.chat_message('human'):
                st.write(prompt_input)

        with container:
            res = st.write_stream(chain.stream({'input': prompt_input, 'messages': st.session_state.messages}))
        st.session_state.messages.append(Message(content=res, role='bot').model_dump())

with right:
    st.write('chat records')
    st.json(st.session_state.messages)
