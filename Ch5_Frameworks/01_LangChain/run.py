from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, create_react_agent, AgentExecutor
from langchain import hub


template = """Question: {question} Let's think step by step.
Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

llm = ChatOpenAI(model_name="gpt-4o-mini")
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = """ What is the population of the capital of the country where the
Olympic Games were held in 2016? """
llm_chain.invoke(question)

tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=hub.pull("hwchase17/react"),
)

question = """What is the square root of the population of the country that won 
the 2023 Rugby World Cup?
"""
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": question})

chatbot = ConversationChain(llm=llm , verbose=True)
chatbot.invoke(input='Hello')

