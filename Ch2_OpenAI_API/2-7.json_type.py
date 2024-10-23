from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model='gpt-4o',
    response_format={'type': 'json_object'},
    messages=[
        {
            'role': 'system',
            'content': '사용자의 입력을 영문으로 된 JSON 형식으로 변환하세요.'
        },
        {
            'role': 'user',
            'content': '신발을 찾고 있습니다. 재질은 가죽이면 좋겠고, 색상은 파랑 아니면 빨강, 사이즈는 7입니다.'
        },
    ],
)

print(response.choices[0].message.content)
