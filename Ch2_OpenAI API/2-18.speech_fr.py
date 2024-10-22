from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech_fr.mp3"
response = client.audio.speech.create(
    model='tts-1',
    voice='echo',
    input='Les mathématiques sont une science fondamentale.'
)
response.stream_to_file(speech_file_path)
