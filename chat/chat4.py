import sys

sys.path.append('../utils')

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, AIMessage
from utils.tongyi import tongyi_chat_model

memory_key = 'chat_history'

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个友好的答疑者'),
    MessagesPlaceholder(variable_name=memory_key),
    ('human', '{input}')
])

memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)
# memory.chat_memory.add_user_message('您好')
# memory.chat_memory.add_ai_message('你好')
# message_placeholder = MessagesPlaceholder(variable_name=memory_key)
# message_placeholder.format_messages(**memory.load_memory_variables({}))

chain = ConversationChain(
    llm=tongyi_chat_model,
    prompt=prompt,
    memory=memory
)

while True:
    user_input = input('user: ')
    if user_input == 'quit':
        break
    print('ai: ', end='')
    for chunk in chain.stream({'input': user_input}):
        print(chunk['response'], end='')
    print()
