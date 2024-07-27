from langchain_community.vectorstores import Chroma
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
import json

from utils import tongyi

with open('example.json', 'r', encoding='utf-8') as file:
    examples = json.load(file)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v1", dashscope_api_key='sk-a70f6e7008314650acf4388068e04490')

# print(examples)
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    Chroma,
    k=1
)

question = "网络安全"
selected_examples = example_selector.select_examples({"question": question})
# for example in selected_examples:
#     for k, v in example.items():
#         print(f"{k}, {v}")
# 以上是值返回向量数据库查找的返回， 下面是配合大模型
# --------------------------------------------
example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="Question: {question}\n{answer}"
)
all_examples_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="参考下面的示例，回答问题：\n<example>",
    suffix="</example>\n\nQuestion:{input}\nAI:",
    input_variables=["input"]
)

prompt = all_examples_prompt.format(input=question)
# print(prompt)

for message in tongyi.tongyi_model.stream(prompt):
    print(message, end='', flush=True)
