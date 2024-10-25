from langchain.chains import LLMChain, ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

template = """Question: {question} 단계별로 생각해봅시다.
Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

llm = ChatOpenAI(model_name="gpt-4o-mini")
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "2016년 올림픽이 열린 국가의 수도는 인구가 얼마인가요?"
print(llm_chain.invoke(question)['text'])

tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=hub.pull("hwchase17/react"),
)

question = "2023 럭비 월드컵에서 우승한 나라의 인구의 제곱근은 얼마인가요?"
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": question})

chatbot = ConversationChain(llm=llm , verbose=True)
chatbot.invoke(input='안녕하세요.')

