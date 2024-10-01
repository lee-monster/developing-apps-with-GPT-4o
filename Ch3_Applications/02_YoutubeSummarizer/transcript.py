from openai import OpenAI


with open("files/transcript.txt", "r") as f:
    transcript = f.read()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"Summarize the following video transcript.:\n{transcript}"
        }
    ]
)


print(response.choices[0].message.content)
