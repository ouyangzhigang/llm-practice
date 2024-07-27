from langchain.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain.output_parsers import PydanticOutputParser
from datetime import datetime

from langchain_core.pydantic_v1 import BaseModel, Field
# import utils.tongyi as ty


class LogModel(BaseModel):
    user_input: str = Field(description="用户输入的内容")
    llm_output: str = Field(description="大模型的输出")


prompt = PromptTemplate.from_template(
    "按照如下的格式回答用户的问题\n {format} \n{query}"
)

model = Tongyi(model_name='qwen-max', dashscope_api_key='sk-a70f6e7008314650acf4388068e04490', stream=True,
                      model_kwargs={'temperature': 0.03})
parser = PydanticOutputParser(pydantic_object=LogModel)

while True:
    user_input = input('user: ')
    if user_input == 'quit':
        break

    # res = model.stream(prompt.format(
    #     format=parser.get_format_instructions(),
    #     query=user_input
    # ))

    # for msg in res:
    #     print(msg)

    res = model.invoke(prompt.format(
        format=parser.get_format_instructions(),
        query=user_input
    ))
    log_model_obj = parser.parse(res)
    print(f"ai: {log_model_obj}")

    _time = datetime.now().strftime("%H:%M:%S")
    print(f'{_time} INFO - USER: {log_model_obj.user_input}, AI: {log_model_obj}')