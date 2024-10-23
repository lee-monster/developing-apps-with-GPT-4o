from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

transcript = client.audio.transcriptions.create(
    model='whisper-1',
    file=open('dali.mp3', 'rb'),
    prompt='This is a description of a painting done by Salvador Dalí.'
)

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {
            'role': 'system',
            'content': '''Your task is to correct any spelling mistakes 
            in the text. The text is about a description of a painting done
            by Salvador Dalí.'''
        },
        {
            'role': 'user',
            'content': transcript.text
        }
    ]
)
print(response.choices[0].message.content)
