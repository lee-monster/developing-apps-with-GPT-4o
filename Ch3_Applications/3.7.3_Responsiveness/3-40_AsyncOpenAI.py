import asyncio
import time
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI()

async def async_call():
    stream =  await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": "5세 아이를 위한 20줄짜리 이야기를 작성해주세요."}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

async def countdown():
    for i in range(10, 0, -1):
        print(f"\nCountdown: {i}")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(async_call(), countdown())

asyncio.run(main())