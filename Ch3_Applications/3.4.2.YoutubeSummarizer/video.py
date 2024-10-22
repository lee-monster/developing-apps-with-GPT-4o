import base64
import cv2

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

video = cv2.VideoCapture("video.mp4")
base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()

client = OpenAI()

images = [{"image": frame, "resize":768} for frame in base64Frames[0::50]]
# 토큰 초과 에러 발생 시 프레임 간격을 늘려서 재시도

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user", 
            "content": ["다음은 비디오 파일의 프레임입니다. \
                두 문장으로 요약하세요.", *images]
        }
    ]
)

print(response.choices[0].message.content)
