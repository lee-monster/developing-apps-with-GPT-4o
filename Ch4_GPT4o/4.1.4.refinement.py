import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
def chat_completion(prompt, model="gpt-4o", temperature=0, response_format=None):
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        response_format=response_format 
    )
    return(res.choices[0].message.content)




def the_reviewer(prompt_initialization, current_prompt):
    
    prompt_reviewer = prompt_initialization + "\n\n"
    prompt_reviewer += f"현재 프롬프트입니다.: {current_prompt}\n\n"
    prompt_reviewer += """작업: 현재 프롬프트를 상세하고 철저하게 평가하세요.
    먼저 현재 프롬프트에 0점에서 5점 사이의 점수를 매겨주세요(0은 매우 나쁨, 5는 매우 좋음).
    그 후, 프롬프트를 5점짜리 완벽한 프롬프트가 되기 위해 개선할 점들을 간략한 문단으로 설명하세요."""
    
    reviews= chat_completion(prompt_reviewer)

    print(reviews)
    
    return reviews


def the_questioner(prompt_initialization, current_prompt, reviews, questions_answers):
        
        prompt_questioner = prompt_initialization + "\n\n"
        prompt_questioner += f"현재 프롬프트입니다: {current_prompt}\n\n"
        prompt_questioner += f"현재 프롬프트에 대한 평가입니다:{reviews}\n\n"
        prompt_questioner += """
        작업: 프롬프트를 개선하기 위해 반드시 필요한 최대 4개의 질문 목록을 작성하세요(각 질문에 대한 예시 답변도 괄호 안에 제공하세요).
        출력 형식: JSON 형식으로 출력하세요. 
        출력은 json.loads로 읽을 수 있어야 합니다. JSON 형식은 다음과 같습니다:
        {'Questions': ['Question 1', 'Question 2', 'Question 3', 'Question 4']}
        """
        
        questions_json = chat_completion(prompt_questioner, model="gpt-4-1106-preview", response_format={"type": "json_object"})

        try:
            questions = json.loads(questions_json).get('Questions', [])
        except json.JSONDecodeError:
            print("모델에서 반환된 JSON 형식이 잘못되었습니다.")
            questions = []
        
        for i, question in enumerate(questions, start=1):
            answer = input(f"질문 {i}: {question} ")
            questions_answers = questions_answers + f"질문: {question}\n답변: {answer}\n\n"
        
        return questions_answers


def the_prompt_maker(prompt_initialization, current_prompt, reviews, questions_answers):
     
    prompt =  prompt_initialization + "\n\n"
    prompt += f"현재 프롬프트입니다: {current_prompt}\n\n"
    prompt += f"해당 프롬프트에 대한 평가 결과입니다:{reviews}\n\n"
    prompt += f"현재 프롬프트를 개선하는 데 필요한 질문과 답변입니다:{questions_answers}\n\n"
    prompt += """
    작업: 이 모든 정보와 프롬프트 엔지니어링 전문 지식을 최대한 활용하여
    현재 프롬프트를 최적의 방식으로 다시 작성해 주세요.
    GPT로 실행할 5점 만점의 완벽한 프롬프트를 생성하는 것이 목표입니다.
    질문과 답변에 포함된 모든 정보를 새 프롬프트에 반드시 포함시켜 주세요.
    프롬프트는 GPT에게 하나 이상의 역할을 부여하고, 컨텍스트와 작업을 정의하는 것으로 시작하세요.
    출력: 당신이 작성한 새로운 GPT용 프롬프트(한국어)만 반환하세요. 그 외의 것은 포함하지 마세요.
    """

    new_prompt = chat_completion(prompt)
    return(new_prompt)

def promptor(initial_prompt, max_nb_iter=3):

    print(f"기존 프롬프트: {initial_prompt}")

    prompt_initialization = """
    당신은 프롬프트 엔지니어링과 대형 언어 모델에 대한 전문가입니다.
    좋은 프롬프트는 GPT에게 하나 이상의 역할을 부여하고, 명확한 컨텍스트와 작업을 정의하며, 기대되는 출력을 명확히 해야 합니다.
    당신은 퓨샷 러닝, 프롬프트 체이닝, 섀도우 프롬프팅 등 다양한 프롬프트 기술을 알고 활용할 수 있습니다.
    저는 당신이 저의 개인 프롬프트 제작 전문가입니다.
    당신의 이름은 이제 '프롬프터'이며, 앞으로 당신을 그렇게 부를 것입니다.
    프롬프터와 GPT는 별개이자 독립된 존재입니다.
    프롬프터(당신)는 GPT에 적합한 프롬프트를 만들어야 합니다.
    """
    
    current_prompt = initial_prompt
    questions_answers = ""
    for i in range(max_nb_iter):

        print(f"{i+1}회차")
        reviews = the_reviewer(prompt_initialization, current_prompt)
        questions_answers = the_questioner(prompt_initialization, current_prompt, reviews, questions_answers)
        current_prompt = the_prompt_maker(prompt_initialization, current_prompt, reviews, questions_answers)
        
        print(f"\n새로운 프롬프트: {current_prompt}\n\n")
        keep = input(f"이 프롬프트를 유지할까요(y/n)?: ")
        if keep == 'y':
            break

    return current_prompt


prompt = promptor("오늘 점심으로 먹을 메인 코스를 제안해주세요",  max_nb_iter=3)
res = chat_completion(prompt)
print(res)