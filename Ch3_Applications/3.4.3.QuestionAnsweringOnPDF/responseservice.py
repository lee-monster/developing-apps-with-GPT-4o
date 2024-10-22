from openai import OpenAI

client = OpenAI()

class ResponseService():
     def __init__(self):
        pass
     
     def generate_response(self, facts, user_question):
         response = client.chat.completions.create(model="gpt-4o",
         messages=[
               {"role": "user", "content": 'FACTS를 기반으로 QUESTION에 한국어로 답하세요.'+ 
                f'QUESTION: {user_question}. FACTS: {facts}'}
            ])

         # extract the response
         return (response.choices[0].message.content)