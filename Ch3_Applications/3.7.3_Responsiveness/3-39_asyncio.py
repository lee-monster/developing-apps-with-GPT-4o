import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI()

async def async_call():
    response= await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "5세 아이를 위한 20줄짜리 이야기를 작성해주세요."}]
    )
    print(response.choices[0].message.content)


asyncio.run(async_call())