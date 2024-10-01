from openai import OpenAI
from typing import List

client = OpenAI()

prompt_role = '''You are an assistant for journalists.
Your task is to write articles, based on the FACTS that are given to you. 
You should respect the instructions: the TONE, the LENGTH, and the STYLE'''

def ask_chatGPT (messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
        )
    
    return response.choices[0].message.content

def assist_journalist(
    facts: List[str], tone: str, length_words: int, style: str
):
    facts = ", ".join(facts)
    prompt = f"{prompt_role} \
        FACTS: {facts} \
        TONE: {tone} \
        LENGTH: {length_words} words \
        STYLE: {style}"
    return ask_chatGPT ([{"role": "user", "content": prompt}])


print(
    assist_journalist(
        ["The sky is blue", "The grass is green"], "informal", 100, "blogpost"
    )
)

print(
    assist_journalist(
        facts=[
            "A book on ChatGPT  has been published last week",
            "The title is Developing Apps with GPT-4 and ChatGPT ",
            "The publisher is O’Reilly.",
        ],
        tone="excited",
        length_words=50,
        style="news flash",
    )
)
