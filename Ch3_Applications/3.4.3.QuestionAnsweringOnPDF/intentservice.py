from openai import OpenAI

client = OpenAI()

class IntentService():
     def __init__(self):
        pass
     
     def get_intent(self, user_question: str):
         # 오픈AI 채팅 완성 엔드포인트 호출
         response = client.chat.completions.create(model="gpt-4o",
         messages=[
               {"role": "user", "content": f'다음 질문에서 키워드를 영어로 찾으세요: {user_question}'+
                 '다른 건 대답하지 말고 키워드만 답하세요.'}
            ])

         # 응답 추출
         return (response.choices[0].message.content)