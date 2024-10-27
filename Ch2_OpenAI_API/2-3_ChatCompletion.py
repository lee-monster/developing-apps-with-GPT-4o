from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

# chat.completions 엔드포인트 사용

response = client.chat.completions.create(
    #  GPT-4o mini 모델 지정 및 채팅 완성 기능 호출
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': '당신은 친절한 교사입니다.'},
        {
            'role': 'user',
            'content': '시간 복잡도 외에도 알고리즘의 다른 측정 방법이 있나요?',
        },
        {
            'role': 'assistant',
            'content': '네, 알고리즘의 성능을 측정하는 다른 방법으로는\
                  공간 복잡도가 있습니다.',
        },
        {'role': 'user', 'content': '그게 뭐죠?'},
    ],
)

# 응답출력
print(response.choices[0].message.content)
