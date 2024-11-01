import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def waiting_assistant_in_progress(thread_id, run_id, max_loops=20):
    for _ in range(max_loops):
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status != 'in_progress':
            break
        time.sleep(1)
    return run

# 파일 추가 완료 함수
def waiting_file_batch_in_progress(file_batch, max_loops=20):
    for _ in range(max_loops):
        if file_batch.status != 'in_progress':
            break
        time.sleep(1)
    return file_batch

# 벡터 저장소 "Explorers Guide" 생성
vector_store = client.beta.vector_stores.create(name="Explorers Guide")
 
# PDF 파일 업로드
file_streams = [open('ExplorersGuide.pdf', "rb")]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

# 파일 업로드 완료 대기
file_batch = waiting_file_batch_in_progress(file_batch)

# 어시스턴트 생성
zelda_expert_assistant = client.beta.assistants.create(
    name='Zelda expert',
    instructions='''당신은 비디오 게임 젤다의 전문가이며, 제가 드린 파일을 사용하여 게임에 대한 질문에 답해 주셔야 합니다.''',
    model='gpt-4o',
    tools=[{'type': 'file_search'}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)


# 스레드 생성
thread = client.beta.threads.create()

# 스레드에 메시지 추가
client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='링크의 전형적인 의상 색깔은 무엇인가요?'
)

# 스레드 실행
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=zelda_expert_assistant.id
)

# 스레드 실행 완료 후 결과 출력
run = waiting_assistant_in_progress(thread.id, run.id)
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
