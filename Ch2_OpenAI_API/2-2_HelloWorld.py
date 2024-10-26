import os
from openai import OpenAI

client = OpenAI(
    # 시스템에 설정된 API 키를 사용합니다
    api_key=os.environ.get('OPENAI_API_KEY')
)

# OpenAI API를 활용하며, GPT-4o의 최신 모델을 호출합니다
response = client.chat.completions.create(model='gpt-4o',
messages=[
      {'role': 'user', 'content': '안녕!'}
  ])


# 응답을 추출합니다
print(response.choices[0].message.content)