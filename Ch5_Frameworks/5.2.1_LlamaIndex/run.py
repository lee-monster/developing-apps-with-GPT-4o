from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
load_dotenv()

# 데이터 폴더의 문서를 로드 및 색인
llm = OpenAI(model_name="gpt-4o-mini")
documents = SimpleDirectoryReader("files").load_data()
index = VectorStoreIndex.from_documents(documents, llm=llm)

# 쿼리 작성
query_engine = index.as_query_engine()
response = query_engine.query("링크의 전형적인 의상 색깔은 무엇인가요?")
print(response)