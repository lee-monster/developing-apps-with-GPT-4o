from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.images.create_variation(
    image=open('img-star_edit.png', 'rb'),
    size='1024x1024'
)

print(response.data[0].url)