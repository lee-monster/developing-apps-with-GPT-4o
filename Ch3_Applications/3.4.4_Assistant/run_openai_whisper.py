import gradio as gr
import whisper
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

starting_prompt = """당신은 어시스턴트입니다.
사용자와 토론하거나 이메일 작업을 수행할 수 있습니다. 이메일은 제목, 수신자 및 본문이 필요합니다.
지시 사항은 [Instruction]으로 시작하고 사용자 입력은 [User]로 시작합니다. 지시에 따르십시오.
"""

prompts = {'START': '[Instruction] 사용자가 이메일을 작성하고 싶다면 "WRITE_EMAIL", 질문을 입력했다면 "QUESTION", 그 외의 요구를 했다면 "OTHER"를 답변합니다. 딱 한 단어만 답변하세요.',
           'QUESTION': '[Instruction] 질문에 답할 수 있다면 "ANSWER", 추가적인 정보가 필요하다면 "MORE", 답변할 수 있다면 "OTHER"를 답변합니다. 딱 한 단어만 답변하세요.',
           'ANSWER': '[Instruction] 사용자의 질문에 답변하세요.',
           'MORE': '[Instruction] 사용자의 앞선 지시에 따라 추가 정보를 요청하세요.',
           'OTHER': '[Instruction] 사용자가 예의바르게 대화를 나누고 있다면 예의바르게 대답하거나 인사를 건네세요. 그렇지 않다면 사용자에게 답변할 수 없다고 알려주세요.',
           'WRITE_EMAIL': '[Instruction] 제목이나 내용이 누락된 경우 "MORE"를 답변하세요. 모든 정보가 있다면 "ACTION_WRITE_EMAIL | subject:subject, recipient:recipient, message:message"를 답변하세요.',
           'ACTION_WRITE_EMAIL': '[Instruction] 메일이 전송되었습니다. 사용자에게 작업이 완료되었다고 알려주세요.'}
actions = ['ACTION_WRITE_EMAIL']


class Discussion:
    """
    어시스턴트와의 대화를 나타내는 클래스입니다.

    Attributes:
        state (str): 대화의 현재 상태
        messages_history (list): 대화의 메시지 이력을 나타내는 딕셔너리 리스트
        client: 오픈AI 클라이언트의 인스턴스
        stt_model: 오디오를 전사하는 데 사용되는 음성 인식 모델

    Methods:
        generate_answer: 입력된 메시지를 기반으로 답변을 생성
        reset: 대화를 초기 상태로 재설정
        do_action: 지정된 작업을 수행
        transcribe: 주어진 오디오 파일을 전사
        discuss_from_audio: 전사된 오디오 파일을 기반으로 대화 시작
        discuss: 주어진 입력을 기반으로 대화 계속
    """

    def __init__(
            self, state='START',
            messages_history=[{'role': 'user',
                               'content': f'{starting_prompt}'}]) -> None:
        self.state = state
        self.messages_history = messages_history
        self.client = OpenAI()
        self.stt_model = whisper.load_model("base")
        pass

    def generate_answer(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages)
        return (response.choices[0].message.content)

    def reset(self, start_state='START'):
        self.messages_history = [
            {'role': 'user', 'content': f'{starting_prompt}'}]
        self.state = start_state
        self.previous_state = None

    def reset_to_previous_state(self):
        self.state = self.previous_state
        self.previous_state = None

    def to_state(self, state):
        self.previous_state = self.state
        self.state = state

    def do_action(self, action):
        """
        특정 작업을 수행합니다.

        Args:
            action (str): 수행할 작업
        """
        print(f'DEBUG perform action={action}')
        pass

    def transcribe(self, file):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=open(file, 'rb'),
        )
        return transcription.text

    def discuss_from_audio(self, file):
        if file:
            # 오디오 파일을 전사하고 입력을 사용하여 토론 시작
            return self.discuss(f'[User] {self.transcribe(file)}')
        # 파일이 없는 경우 빈 출력
        return ''

    def discuss(self, input=None):
        if input is not None:
            self.messages_history.append({"role": "user", "content": input})

        # 대화를 계속
        completion = self.generate_answer(
            self.messages_history +
            [{"role": "user", "content": prompts[self.state]}])

        # 응답 내용이 작업인지 확인
        if completion.split("|")[0].strip() in actions:
            action = completion.split("|")[0].strip()
            self.to_state(action)
            self.do_action(completion)
            # 대화를 계속
            return self.discuss()
        # 응답 내용이 새로운 상태인지 확인
        elif completion in prompts:
            self.to_state(completion)
            # 대화를 계속
            return self.discuss()
        # 응답 내용이 사용자에게 전달할 내용인지 확인
        else:
            self.messages_history.append(
                {"role": "assistant", "content": completion})
            if self.state != 'MORE':
                # 재시작
                self.reset()
            else:
                # 이전 상태로 돌아가기
                self.reset_to_previous_state()
            return completion


if __name__ == '__main__':
    discussion = Discussion()

    gr.Interface(
        theme=gr.themes.Soft(),
        fn=discussion.discuss_from_audio,
        live=True,
        inputs=gr.Audio(sources="microphone", type="filepath"),
        outputs="text").launch()
