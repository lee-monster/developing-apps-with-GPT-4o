from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

url = 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Ophiopteris_antipodum.JPG'
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': '이미지 속 동물의 이름을 알려주세요.',
                },
                {'type': 'image_url', 'image_url': {'url': url}},
            ],
        }
    ],
)

print(response.choices[0].message.content)