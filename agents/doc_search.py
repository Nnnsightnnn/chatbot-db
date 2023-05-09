"""This module searches the vector_store for the best matching document content"""
import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis
import config

load_dotenv()


def local_doc_search(query):
    """Search Chroma Index"""
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    print(parent_dir)
    # Ensure the directory exists
    directory_path = os.path.join(parent_dir, f"{config.VECTOR_STORE_DIRECTORY}")

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    if not os.path.exists(directory_path):
        raise Exception(f"{directory_path} does not exist, nothing can be queried")

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    # Initialize Redis index
    rds = Redis.from_existing_index(index_name='knowledge',
                                    embedding=embeddings, redis_url="redis://localhost:6379")
    # similarity search with Redis
    docs = rds.similarity_search(query, k=5)
    try:
        print(docs)
        return (docs)
    except (IndexError, TypeError):
        return None

# Path: agents/db_search.py
