from langchain_community.llms.tongyi import Tongyi
from langchain.prompts import PromptTemplate
import dashscope

prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{topic}的笑话"
)
model = Tongyi(model_name='qwen-max', dashscope_api_key='sk-a70f6e7008314650acf4388068e04490', stream=True)
prompt = prompt_template.format(topic='公司压榨员工')
# messages = model.invoke(prompt_template.format(topic='军队'))
for message in model.stream(prompt):
    print(message, end='', flush=True)
