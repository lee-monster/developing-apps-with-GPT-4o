

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

with open('file.txt', 'r') as f:
    document = f.read()

prompt = '''당신은 문서 정리원입니다. 
문서를 분석하고, 주요 주제를 추출하고, 간단한 요약을 생성합니다.
정보는 JSON 형식을 사용하여 제공하며, 다음 구조를 사용합니다:{
        "topics": ["주요 주제1", "주요 주제2", "주요 주제3"],
        "summary": "문서의 요약"
    } 
'''

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": f'{prompt} Document: {document}'}],
    response_format={"type": "json_object"})

print(response.choices[0].message.content)