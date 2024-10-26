from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "5세 아이를 위한 20줄짜리 이야기를 작성해주세요."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
