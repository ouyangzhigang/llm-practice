from langchain_community.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate

responses = ["foo", "bar"]

model = FakeListLLM(responses=responses)

prompt = PromptTemplate.from_template('测试')

model.invoke(prompt.format())
model.invoke(prompt.format())

print(model.invoke(prompt.format()))
print(model.invoke(prompt.format()))
