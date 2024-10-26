from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

# 파일에서 스크립트 읽기
with open("transcript.txt", "r") as f:
    transcript = f.read()

# 오픈AI의 채팅 완성 엔드포인트 호출, GPT-4o 모델 사용
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"다음 영상 스크립트를 요약하세요.\n{transcript}"
        }
    ]
)

# 결과 출력
print(response.choices[0].message.content)
