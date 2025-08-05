


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from typing import List

def split(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,          
        chunk_overlap=200        
    )
    return splitter.split_documents(docs)
