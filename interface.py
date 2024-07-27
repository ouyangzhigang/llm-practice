from langchain_openai import ChatOpenAI
from langchain_community.llms.tongyi import Tongyi

# model = ChatOpenAI(model_name='')
model = ChatOpenAI(model_name='')

model.invoke('hello')
