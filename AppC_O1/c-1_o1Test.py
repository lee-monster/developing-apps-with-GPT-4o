from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model='o1-mini',
    messages=[{
            'role': 'user', 
            'content': '‘[1,2],[3,4],[5,6]’ 형식의 문자열로 표현된 행렬을 받아 전치 행렬을 같은 형식으로 출력하는 bash 스크립트를 작성합니다.'
        }
    ]
)
print(response.choices[0].message.content)
