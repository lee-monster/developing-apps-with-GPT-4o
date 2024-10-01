import asyncio
import time
from openai import AsyncOpenAI
client = AsyncOpenAI()

async def async_call():
    response= await client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": "Write a 10 line story for my 5 year old."}]
    )
    print(response.choices[0].message.content)

asyncio.run(async_call())

async def countdown():
    for i in range(10, 0, -1):
        print(f"\nCountdown: {i}")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(async_call(), countdown())

asyncio.run(main())
