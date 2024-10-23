from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from intentservice import IntentService
from responseservice import ResponseService
from dataservice import DataService

# PDF 파일 불러오기
pdf_path = Path(__file__).parent.joinpath("files").joinpath("ExplorersGuide.pdf")
data_service = DataService()

# 레디스 데이터 삭제
data_service.drop_redis_data()

# PDF 파일을 임베딩으로 변환
data = data_service.pdf_to_embeddings(pdf_path)
data_service.load_data_to_redis(data)

intent_service = IntentService()
response_service = ResponseService()

# 질문하기 
question = '보물 상자는 어디서 찾을 수 있나요?'

# 의도 분류
intents = intent_service.get_intent(question)

# 사실 찾기
facts = data_service.search_redis(intents)

# 답변 생성
answer = response_service.generate_response(facts, question)
print(answer)
