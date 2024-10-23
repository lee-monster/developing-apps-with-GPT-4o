from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

transcript = client.audio.transcriptions.create(
    model='whisper-1',
    file=open('dali.mp3', 'rb'),
    prompt='This is a description of a painting done by Salvador Dalí.'
)
print(transcript.text)