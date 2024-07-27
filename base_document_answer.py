from typing import List

from langchain.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_core.output_parsers import StrOutputParser

model = Tongyi(
    model_name='qwen-max',
    model_kwargs={'temperature': 0.01},
    dashscope_api_key='sk-a70f6e7008314650acf4388068e04490'
)


def get_docs(roles: str = 'student') -> List[Document]:
    docs = []
    if roles == 'student':
        docs = [
            Document(page_content='李明喜欢红色但不喜欢黄色'),
            Document(page_content='丽华喜欢绿色但他更喜欢但是橙色')
        ]

    else:
        docs = [
            Document(page_content='李老师喜欢红色但不喜欢紫色'),
            Document(page_content='西老师欢绿色但他更喜欢但是紫色'),
            Document(page_content='皮老师欢青但他更喜欢但是蓝色')
        ]

    return docs


prompt_st = PromptTemplate.from_template("每个人喜欢但颜色是什么：\n\n{context}")
prompt_tr = PromptTemplate.from_template("哪两位老师喜欢同样但颜色：\n\n{context}")

doc_chain = create_stuff_documents_chain(llm=model, prompt=prompt_tr, output_parser=StrOutputParser)

# res = doc_chain.invoke({"context": get_docs()})
# print(res)

# res_chain = {'context': get_docs} | doc_chain
# res = res_chain.invoke('teacher')
# print(res)

chain = {
            'context': RunnablePassthrough(lambda x: x['role']) | doc_chain,
            'color': RunnablePassthrough(lambda x: x['color'])
        } | prompt_tr | model
chain.invoke({'role': 'student', 'color': '蓝色'})
