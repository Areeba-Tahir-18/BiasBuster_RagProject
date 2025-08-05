
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI  
from db.chromedb import store_in_chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import Document


def get_doc_qa_chain(retriever):
    
    llm = ChatOpenAI(temperature=0.3)  
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain


def process_llm_response(llm_response: dict):
    
    print("\n Answer:\n")
    print(llm_response['result'])
    print('\n Sources:')
    for source in llm_response.get("source_documents", []):
        print(f"- {source.metadata.get('source', 'No metadata available')}")

