
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.document import Document
import os
from Config.settings import OPENAI_API_KEY


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

persist_directory = "outputs/embeddings"


embedding_model = OpenAIEmbeddings()

def store_in_chroma(docs: list[Document]):
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    vectordb.persist()
    retriever = vectordb.as_retriever(search_kwargs={"k": 7})
    return retriever

