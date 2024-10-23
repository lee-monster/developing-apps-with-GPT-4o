from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def chat_completion(prompt, model="gpt-4o-mini", temperature=0, response_format=None):
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        response_format=response_format 
    )

    return res.choices[0].message.content

print(chat_completion("데카르트가 말하길, 나는 생각한다 고로"))

print(chat_completion("오늘 점심으로 먹을 요리를 추천해주세요."))

prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.

Task: 오늘 점심으로 먹을 요리를 추천해주세요.
"""
print(chat_completion(prompt))

prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.
Task: 오늘 점심으로 먹을 요리를 추천해주세요.
요청한 작업을 수행하지 마세요! 대신, 작업을 더 효과적으로 수행할 수 있도록 추가적인 정보를 물어보세요.
"""
print(chat_completion(prompt))

prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.
Task: 오늘 점심으로 먹을 요리를 추천해주세요.
추천을 할때는 두 개의 열이 있는 테이블도 함께 제공해주세요.
각 행에는 주요 요리의 재료가 포함되어야 합니다.
첫 번째 열은 재료의 이름입니다.
두 번째 열은 1인분에 들어갈 그 재료의 무게(그램)입니다. 
요리를 준비하는 레시피는 제공하지 마십시오.
"""
res = chat_completion(prompt)
print(*res.split('\n'), sep='\n')


