"""This module searches the vector_store for the best matching document content"""
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

import config

load_dotenv()

def doc_search(query):
    """Search Pinecone Index"""
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    docs = Pinecone.from_existing_index(index_name=config.INDEX_NAME,
                                              embedding=embeddings)
    try:
        response = docs.similarity_search(query)
        print(response)
        return response
    except (IndexError, TypeError):
        return None

# Path: agents/db_search.py
