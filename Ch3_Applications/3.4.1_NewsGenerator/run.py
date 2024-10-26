from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from typing import List

client = OpenAI()

prompt_role = '''당신은 기자를 도와주는 어시스턴트입니다.
당신의 임무는 주어진 사실을 기반으로 기사(FACTS)를 쓰는 것입니다.
다음 지시 사항을 준수해야 합니다: TONE, LENGTH, STYLE'''

def ask_chatGPT (messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
        )
    
    return response.choices[0].message.content

def assist_journalist(
    facts: List[str], tone: str, length_words: int, style: str
):
    facts = ", ".join(facts)
    prompt = f"{prompt_role} \
        FACTS: {facts} \
        TONE: {tone} \
        LENGTH: {length_words} 단어 \
        STYLE: {style}"
    return ask_chatGPT ([{"role": "user", "content": prompt}])


print(
    assist_journalist(
        ["하늘은 파랗다.", "풀은 푸르다."], "비격식", 100, "블로그글"
    )
)

print(
    assist_journalist(
        facts=[
            "이번주 챗GPT 관련 도서가 출간되었습니다.",
            "제목은 오픈AI API를 활용한 인공지능 앱 개발입니다.",
            "출판사는 한빛미디어입니다.",
        ],
        tone="흥분됨",
        length_words=50,
        style="뉴스 소식",
    )
)
