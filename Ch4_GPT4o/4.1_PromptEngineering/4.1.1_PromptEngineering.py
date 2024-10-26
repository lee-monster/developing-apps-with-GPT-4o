from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# 예시 4-1 API 호출 함수
def chat_completion(prompt, model="gpt-4o-mini", temperature=0, response_format=None):
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        response_format=response_format 
    )

    return res.choices[0].message.content

# 예시 4-2 GPT API 호출 함수 테스트
print(chat_completion("데카르트가 말하길, 나는 생각한다 고로"))

# 예시 4-3 컨텍스트가 없는 프롬프트
print(chat_completion("오늘 점심에 먹을 메인 메뉴를 추천해 주세요."))

# 예시 4-4 컨텍스트를 포함한 프롬프트
prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.

Task: 오늘 점심에 먹을 메인 메뉴를 추천해 주세요.
"""
print(chat_completion(prompt))

# 예시 4-5 프롬프트를 보완할 정보 요청
prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.
Task: 오늘 점심에 먹을 메인 메뉴를 추천해 주세요.
요청한 작업을 수행하지 마세요! 대신, 작업을 더 효과적으로 수행할 수 있도록 추가적인 정보를 물어보세요.
"""
print(chat_completion(prompt))

# 예시 4-6 표 형식의 결과를 요청하는 프롬프트
prompt = """
Context: 저는 하루에 2시간 운동을 합니다.
채식주의자이며, 녹색 채소를 싫어합니다.
건강식에 관심이 많아요.
Task: 오늘 점심에 먹을 메인 메뉴를 추천해 주세요.
추천을 할때는 두 개의 열이 있는 표도 함께 제공해주세요.
각 행에는 주요 요리의 재료가 포함되어야 합니다.
첫 번째 열은 재료의 이름입니다.
두 번째 열은 1인분에 들어갈 그 재료의 무게(그램)입니다. 
요리를 준비하는 레시피는 제공하지 마십시오.
"""
res = chat_completion(prompt)
print(*res.split('\n'), sep='\n')


