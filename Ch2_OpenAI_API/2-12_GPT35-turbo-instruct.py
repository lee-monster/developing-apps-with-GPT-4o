from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

# 오픈AI 모델 호출
response = client.completions.create(
    model='gpt-3.5-turbo-instruct', 
    prompt='Hello World!'
)
# 생성된 출력값 확인
print(response.choices[0].text)
