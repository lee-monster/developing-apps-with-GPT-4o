from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()

documents = SimpleDirectoryReader("files").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("What color is Link's outfit?")
print(response)