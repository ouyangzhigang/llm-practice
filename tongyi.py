import os
from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi

os.environ['TONGYI_KEY'] = 'sk-a70f6e7008314650acf4388068e04490'
# print(os.environ.get('TONGYI_KEY'))

tongyi_model = Tongyi(
    model_name='qwen-max',
    dashscope_api_key=os.environ['TONGYI_KEY'],
    stream=True,
    model_kwargs={'temperature': 0.03}
)


tongyi_chat_model = ChatTongyi(
    model_name='qwen-max',
    dashscope_api_key=os.environ.get('TONGYI_KEY'),
    stream=True,
    model_kwargs={'temperature': 0.05}
)
