from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model='dall-e-3',
    prompt='An image with a cute spiny brittle star with distinct arms.',
    n=1,
    size='1024x1024',
    quality='hd'
)

print(response.data[0].url)
print(response.data[0].revised_prompt)
