from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

transcript = client.audio.transcriptions.create(
    model='whisper-1',
    file=open('speech.mp3', 'rb')
)
print(transcript.text)