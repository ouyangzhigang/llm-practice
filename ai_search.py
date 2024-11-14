import os
from serpapi import Client
from dataclasses import dataclass, field
from typing import List
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

os.environ['SERPAPI_KEY'] = 'xxx'
os.environ['TONGYI_KEY'] = 'sk-'
print(os.environ.get('SERPAPI_KEY'))


class SearchResultItem(BaseModel):
    title: str
    link: str
    snippet: str


class SearchResults(BaseModel):
    results: List[SearchResultItem]


# def search_prompt(query: str, search_results: SearchResults) -> str:
#     _prompt = f"""根据搜索引擎的结果，回答用户问题。
#     SEARCH_RESULTS: {search_results}
#     USER_QUERY: {query}
#     """
#     return _prompt

prompt = PromptTemplate.from_template("""根据搜索引擎的结果，回答用户问题。
    SEARCH_RESULTS: {search_results}
    USER_QUERY: {query}
""")


def get_search_result(query: str) -> SearchResults:
    params = {
        "engine": "google",
        "q": query
    }

    client = Client(api_key=os.environ.get('SERPAPI_KEY'))
    results = client.search(params)
    organic_results = results["organic_results"]
    print(organic_results)
    search_results = SearchResults(
        results=[
            SearchResultItem(
                title=organic_result['title'],
                link=organic_result['link'],
                snippet=organic_result['snippet']
            ) for organic_result in organic_results
        ]
    )

    return search_results


model = Tongyi(
    model_name='qwen-max',
    model_kwargs={'temperature': 0.05},
    dashscope_api_key='sk-')

# def chat(query: str) -> str:
#     response = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {"rule": "user", "content": query}
#         ],
#         stream=True
#     )
#
#     for chunk in response:
#         if chunk.choice[0].delta.content is not None:
#             print(chunk.choice[0].delta.content, end='', flush=True)


# search_result = get_search_result(query='易建联是什么时候退休的？')
# chat(search_prompt(query, search_results))

parser = StrOutputParser()

chain = {'search_results': lambda x: get_search_result(x), 'query': lambda x: x} | prompt | model

result = chain.invoke('易建联是什么时候退役的?')
print(result)
