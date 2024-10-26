from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini")
tools = load_tools(["wikipedia", "llm-math"], llm=llm)

agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=hub.pull("hwchase17/react"),
)

question = "2023 럭비 월드컵에서 우승한 나라의 인구의 제곱근은 얼마인가요?"
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": question})

