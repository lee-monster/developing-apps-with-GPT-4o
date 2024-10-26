from pathlib import Path
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA

from dotenv import load_dotenv

load_dotenv()

file_path = Path(__file__).parent.joinpath("files").joinpath("ExplorersGuide.pdf")
loader = PyPDFLoader(file_path)
pages = loader.load_and_split()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(pages, embeddings)

q = "링크의 전형적인 의상 색깔은 무엇인가요?"
print(db.similarity_search(q)[0])

llm = ChatOpenAI(model_name="gpt-4o-mini")
chain = RetrievalQA.from_llm(llm=llm, retriever=db.as_retriever())

print(chain.invoke(q, return_only_outputs=True)['result'])