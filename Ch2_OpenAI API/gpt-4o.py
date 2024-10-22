# 파이썬 파일에서 환경 변수를 설정합니다.
from dotenv import load_dotenv
load_dotenv()

# 파이썬에서 OpenAI를 불러오고 클라이언트를 만듭니다.
from openai import OpenAI
client = OpenAI()

# chat.completions 엔드포인트를 호출합니다.
response = client.chat.completions.create( model='gpt-4o',
    messages=[{'role': 'user', 'content': '프롬프트를 입력하세요'}], )

# 응답을 확인합니다.
print(response.choices[0].message.content)
