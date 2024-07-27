from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

human_message_prompt_template = HumanMessagePromptTemplate.from_template("{text}")

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你喜欢讲笑话，特别幽默"
            )
        ),
        human_message_prompt_template
    ]
)

messages = chat_template.format_messages(text='今天天气真好')
print(messages)
