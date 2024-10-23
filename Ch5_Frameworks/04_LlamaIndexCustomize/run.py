
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

# Connect to Weaviate client and create a vector store
client = weaviate.connect_to_local()
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="BlogPost", text_key="content")

# Setting up the storage for the embeddings
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# Load and index the documents in the data folder
documents = SimpleDirectoryReader("files").load_data()
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context)

# Query your data
query_engine = index.as_query_engine()
response = query_engine.query("링크의 전형적인 의상 색깔은 무엇인가요?")
print(response)

client.close()