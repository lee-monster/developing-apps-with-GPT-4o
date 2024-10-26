
import weaviate
from dotenv import load_dotenv
from llama_index.core import (SimpleDirectoryReader, StorageContext,
                              VectorStoreIndex)
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.weaviate import WeaviateVectorStore

load_dotenv()

Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding()

# 위비에이트 클라이언트와 연결 및 벡터 저장소 생성
client = weaviate.connect_to_local()
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="BlogPost", text_key="content")

# 임베딩을 위한 스토리지 세팅
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 데이터 폴더 내의 문서를 로드 및 색인
documents = SimpleDirectoryReader("files").load_data()
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context)

# 쿼리 작성
query_engine = index.as_query_engine()
response = query_engine.query("링크의 전형적인 의상 색깔은 무엇인가요?")
print(response)

client.close()