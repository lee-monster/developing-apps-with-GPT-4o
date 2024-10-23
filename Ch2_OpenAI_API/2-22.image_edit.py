from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.images.edit(
    model='dall-e-2',
    image=open('img-star.png', 'rb'),
    mask=open('img-star_alpha.png', 'rb'),
    prompt='''An image with a cute spiny brittle star with distinct arms 
        and with a cute smiling face in the center.''',
    n=1,
    size='1024x1024'
)

print(response.data[0].url)