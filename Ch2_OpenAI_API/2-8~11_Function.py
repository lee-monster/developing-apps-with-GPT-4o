from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

import json


def find_product(sql_query):
    # 쿼리를 실행
    results = [
        {"name": "pen", "color": "blue", "price": 1.99},
        {"name": "pen", "color": "red", "price": 1.78},
    ]
    return results


function_find_product = {
        "name": "find_product",
        "description": "sql 쿼리에서 상품 목록을 찾습니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "sql_query": {
                    "type": "string",
                    "description": "A SQL query",
                }
            },
            "required": ["sql_query"],
        },
    }



def run(user_question):
    # 정의된 함수 활용, chat.completions 호출
    messages = [{"role": "user", "content": user_question}]

    response = client.chat.completions.create(model='gpt-4o', messages=messages, tools=[{"type": "function", "function": function_find_product }])
    response_message = response.choices[0].message

    # 메시지에 어시스턴트의 응답 추가
    messages.append(response_message)
    

    # 함수를 호출하고 결과를 가져옴
    function_name = response_message.tool_calls[0].function.name

    if function_name == "find_product":
        function_args = json.loads(
            response_message.tool_calls[0].function.arguments
        )
        products = find_product(function_args.get("sql_query"))
    else:
        # 에러 처리
        products = []
    # 메시지에 함수의 응답을 추가
    messages.append(
        {
            "role": "tool",
            "content": json.dumps(products),
            "tool_call_id": response_message.tool_calls[0].id,
        }
    )
    # 함수 응답을 자연어로 변환
    second_response = client.chat.completions.create(model='gpt-4o',
    messages=messages)
    return second_response.choices[0].message.content


print(run("가격이 2달러 이하인 제품 2개를 찾아주세요."))