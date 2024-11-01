from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

template = """Question: {question} 단계별로 생각해봅시다.
Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

chain = prompt | ChatOpenAI(model_name="gpt-4o-mini") | StrOutputParser()

question = "2016년 올림픽이 열린 국가의 수도는 인구가 얼마인가요?"
print(chain.invoke(question))
