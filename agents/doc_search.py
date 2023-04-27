"""This module searches the vector_store for the best matching document content"""
import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.vectorstores import Chroma

import config

load_dotenv()

def pinecone_doc_search(query):
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

def local_doc_search(query):
    """Search Chroma Index"""
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    print(parent_dir)
    # Ensure the directory exists
    directory_path = os.path.join(parent_dir, f"{config.VECTOR_STORE_DIRECTORY}")
    print(directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    print(directory_path)
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    print(directory_path)
    # load Chroma index
    docs = Chroma(persist_directory=directory_path,
                  embedding_function=embeddings)
    try:
        response = docs.similarity_search(query)
        print(response)
        return response
    except (IndexError, TypeError):
        return None

# Path: agents/db_search.py
