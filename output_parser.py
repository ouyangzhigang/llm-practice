from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(
    model_name='qwen-max',
    dashscope_api_key='sk-a70f6e7008314650acf4388068e04490',
    model_kwargs={'temperature': 0.1},
    stream=True
)

parser = JsonOutputParser()

prompt = PromptTemplate(
    template='Answer the user query.\n{format_instructions}\n{query}\n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

chain = prompt | model | parser
for s in chain.stream({'query': '给我讲个1930年代的浪漫爱情故事'}):
    print(s)
