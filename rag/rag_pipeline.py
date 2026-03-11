from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from llm.llm_config import embeddings 

loader = PyPDFLoader("knowledge.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = splitter.split_documents(docs)

vector_store = Chroma.from_documents(
    documents=chunks, embedding=embeddings, persist_directory="chroma_db"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})
