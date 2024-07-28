from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from langchain_community.llms.tongyi import Tongyi

model = Tongyi(
    model_name='qwen-max', dashscope_api_key='', model_kwargs={'temperature': 0.8}
)


class Joke(BaseModel):
    content: str = Field(description='内容')
    reason: str = Field(description='说说深层次原因')
    custom: str = 'i love you, guangzhou'


parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template='参考下面格式回答用户问题.\n{format_instructions}\n{query}\n',
    input_variables=['query'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

data = model.invoke(prompt.format(query='给我讲个皇上笑话'))

joke_obj = data
# str类型，需要转成dict
print(data)
print(parser.parse(data).content)
