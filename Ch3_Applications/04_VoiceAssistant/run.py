# ffmpeg이 설치되어 있지 않을 시 오류가 발생할 수 있음

import whisper
import gradio as gr
from openai import OpenAI


client = OpenAI()
model = whisper.load_model("base")

prompts = {
    "START": "Classify the intent of the next input. \
                Is it: WRITE_EMAIL, QUESTION, OTHER? Only answer one word.",
    "QUESTION": "If you can answer the question: ANSWER, \
                    if you need more information: MORE, \
                    if you cannot answer: OTHER. Only answer one word.",
    "ANSWER": "Now answer the question",
    "MORE": "Now ask for more information",
    "OTHER": "Now tell me you cannot answer the question or do the action",
    "WRITE_EMAIL": 'If the subject or recipient or message is missing, \
                    answer "MORE". Else if you have all the information, \
                    answer "ACTION_WRITE_EMAIL |\
                    subject:subject, recipient:recipient, message:message".',
}

actions = {
    "ACTION_WRITE_EMAIL": "The mail has been sent. \
    Now tell me the action is done in natural language."
}

def transcribe(file):
    transcription = model.transcribe(file)
    return transcription["text"]


def generate_answer(messages):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages)
    return (response.choices[0].message.content)


def start(user_input):
    messages = [{"role": "user", "content": prompts["START"]}]
    messages.append({"role": "user", "content": user_input})
    return discussion(messages, "")


def discussion(messages, last_step):
    answer = generate_answer(messages)
    if answer in prompts.keys():
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": prompts[answer]})
        return discussion(messages, answer)
    
    elif answer in actions.keys():
        do_action(answer)

    else:
        if last_step != 'MORE':
            messages=[]
        last_step = 'END'
        return answer


def do_action(action):
    print("Doing action " + action)
    return ("I did the action " + action)


def start_chat(file):
    input = transcribe(file)
    return start(input)


if __name__ == '__main__':
    gr.Interface(
        fn=start_chat,
        live=True,
        inputs=gr.Audio(sources="microphone", type="filepath"),
        outputs="text",
    ).launch()