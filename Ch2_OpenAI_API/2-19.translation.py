from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

transcript = client.audio.translations.create(
    model='whisper-1',
    file=open('speech_fr.mp3', 'rb')
)
print(transcript.text)