from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice='echo',
    input='I won’t be home tonight. Could you please take the dog for a walk?'
)

response.stream_to_file(speech_file_path)