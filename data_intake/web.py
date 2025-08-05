from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import requests

def load_web(url):
    
    loader = WebBaseLoader(url)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])

