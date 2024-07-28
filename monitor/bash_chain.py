import os
from langchain_experimental.llm_bash.base import LLMBashChain
from langchain_community.llms.tongyi import Tongyi
from langchain.prompts import PromptTemplate
# from langchain_core.prompts import PromptTemplate
from langchain.chains import APIChain

os.environ['TONGYI_KEY'] = ''
print(os.environ.get('TONGYI_KEY'))

llm = Tongyi(
    model_name='qwen-max',
    model_kwargs={'temperature': 0.05},
    dashscope_api_key=os.environ.get('TONGYI_KEY')
)

bash_chain = LLMBashChain.from_llm(llm, verbose=True)

query = '查询操作系统的所有磁盘使用情况'
result = bash_chain.invoke(query)
print(result)

prompt = PromptTemplate.from_template("""{context}
    根据以上的巡检结果，判断是否需要告警，如果需要的话总结并返回告警内容；否则返回空字符串
""")

alarm_chain = {
    "context": lambda x: result['answer']
} | prompt | llm

warnings = alarm_chain.invoke({})
print(warnings)

HTTPBIN_DOCS="""
# API 使用文档

## 概述

此API用于向指定URL发送告警信息。当系统检测到特定的告警条件时，可以调用此API以通知管理员或记录系统的状态。

## API信息

- **URL**: http://httpbin.org/get
- **业务说明**: 发送告警信息至服务器，用于系统告警通知或日志记录
- **请求方式**: `GET`

## 请求参数

| 参数名 | 类型 | 描述 | 是否必填 | 示例值 |
|-------|------|-------------|-----|-----|
|alarm|string|具体的告警信息描述|是|"alarm information"|

"""
api_chain = APIChain.from_llm_and_api_docs(
    llm,
    api_docs=HTTPBIN_DOCS,
    limit_to_domains=['http://httpbin.org'],
    verbose=True
)

alarm_api_chain = alarm_chain | api_chain
alarm_api_chain.invoke({})
