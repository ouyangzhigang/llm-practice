from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
import json

with open('example.json', 'r', encoding='utf-8') as file:
    example = json.load(file)

example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="Question: {question}\n{answer}"
)

# example_prompt.format(**example[0])

all_examples_prompt = FewShotPromptTemplate(
    examples=example,
    example_prompt=example_prompt,
    prefix="参考下面的示例，回答问题：\n<example>",
    suffix="</example>\n\nQuestion:{input}\nAI:",
    input_variables=["input"]
)

question = "网络安全"
prompt = all_examples_prompt.format(input=question)

model = Tongyi(model_name='qwen-max', dashscope_api_key='sk-a70f6e7008314650acf4388068e04490', stream=True)
for message in model.stream(prompt):
    print(message, end='', flush=True)