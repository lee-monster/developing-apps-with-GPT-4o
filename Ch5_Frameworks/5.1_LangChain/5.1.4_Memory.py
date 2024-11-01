from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from dotenv import load_dotenv
import uuid

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini")

# 상태 그래프 정의
workflow = StateGraph(state_schema=MessagesState)

# llm 호출 함수 정의
def call_llm(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": response}

# 그래프에 llm 추가
workflow.add_edge(START, "llm")
workflow.add_node("llm", call_llm)

# 메모리 저장
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 스레드 ID 생성
thread_id = uuid.uuid4()

# 스레드 ID 지정
config = {"configurable": {"thread_id": thread_id}}

# 대화 시작
query = "안녕하세요. 저는 홍길동입니다."

input_messages = [
    {
        "role": "system",
        "content": """당신은 상점을 운영하는 상인입니다. 
        고객의 질문에 성실히 답하세요.""",
    },
    {"role": "user", "content": query},
]
for event in app.stream({"messages": input_messages}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# 새로운 대화
new_query = "제 이름을 기억하나요?"
new_input_messages = [
    {"role": "user", "content": new_query},
]

for event in app.stream({"messages": new_input_messages}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()
