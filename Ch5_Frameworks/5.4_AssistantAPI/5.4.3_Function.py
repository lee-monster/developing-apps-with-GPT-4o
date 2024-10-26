import time, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def waiting_assistant_in_progress(thread_id, run_id, max_loops=20):
    for _ in range(max_loops):
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if (run.status == 'requires_action'
            and run.required_action.type == 'submit_tool_outputs'):

            tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
            if tool_call.function.name == 'getCurrentTemperature':
                arguments = json.loads(tool_call.function.arguments)
                fct_output = getCurrentTemperature(arguments['city'])
            else:
                raise Exception('Unexpected function')

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[
                    {
                        'tool_call_id': tool_call.id,
                        'output': fct_output
                    }
                ]
            )
        time.sleep(1)
    return run



def getCurrentTemperature(city):
    return str(len(city)) + '°C'

function = {
    'name': 'getCurrentTemperature',
    'description': '도시의 현재 기온을 가져오는 함수',
    'parameters': {
        'type': 'object',
        'properties': {
            'city': {
                'type': 'string',
                'description':
                '기온을 가져올 도시의 이름.'
                '예: ‘뉴욕’, ‘런던’, 등'
            }
        },
        'required': ['city']
    }
}

tools = [{
    'type': 'function',
            'function': function
}]

client = OpenAI()
assistant = client.beta.assistants.create(
    name='Weather Assistant',
    instructions='당신은 외부 도구를 사용하여 도시의 현재 기온을 제공하는 어시스턴트입니다.',
    model='gpt-4o-mini',
    tools=tools
)

thread = client.beta.threads.create()

client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='베를린의 현재 기온은 얼마인가요?'
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

run = waiting_assistant_in_progress(thread.id, run.id)
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
