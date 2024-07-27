from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "your name is {name}"),
        ("human", "你好"),
        ("ai", "hello"),
        ("human", "{message}")
    ]
)

messages = chat_template.format_messages(name="老王", message="你叫啥？")

print(messages)
