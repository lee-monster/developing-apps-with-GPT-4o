from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import OpenAI


loader = PyPDFLoader("files/ExplorersGuide.pdf")
pages = loader.load_and_split()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(pages, embeddings)

q = "What is Link's traditional outfit color?"
db.similarity_search(q)[0]

llm = OpenAI()
chain = RetrievalQA.from_llm(llm=llm, retriever=db.as_retriever())
q = "What is Link's traditional outfit color?"

print(chain(q, return_only_outputs=True))