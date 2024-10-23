from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

# 오픈AI 모더레이션 모델 최신 버전 호출
response = client.moderations.create(
    model='text-moderation-latest',
    input='I want to kill my neighbor.',
)

print(response)

