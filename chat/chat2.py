import sys

sys.path.append('../utils')

from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from utils.tongyi import tongyi_chat_model

human_prompt_template = HumanMessagePromptTemplate.from_template("{message}")

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你是一个翻译员，你的任务是将用户的文本翻译成英语。"
            )
        ),
        human_prompt_template
    ]
)

chain = chat_template | tongyi_chat_model
result = chain.invoke({"message": "我喜欢足球啊, 并且我还喜欢汽车"})
print(result)
