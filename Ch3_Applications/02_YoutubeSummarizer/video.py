from openai import OpenAI
import base64
import cv2


video = cv2.VideoCapture("files/video.mp4")
base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()

client = OpenAI()

images = [{"image": frame, "resize":768} for frame in base64Frames[0::50]] # 토큰 초과 에러 발생 시 프레임 간격을 늘려서 재시도
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user", 
            "content": ["These are the frames from a video. Generate a two sentence summary.", *images]
        }
    ]
)

print(response.choices[0].message.content)
