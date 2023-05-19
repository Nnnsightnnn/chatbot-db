"""This module searches the vector_store for the best matching document content"""
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis
import config

load_dotenv()


def local_doc_search(query, index_name='knowledge', k=5):
    """this function searches the vector_store for the best matching document content"""
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    # Initialize Redis index
    rds = Redis.from_existing_index(index_name=index_name,
                                    embedding=embeddings, redis_url=config.REDIS_URL)
    # similarity search with Redis
    docs = rds.similarity_search(query, k=k)
    try:
        return docs
    except (IndexError, TypeError):
        return None

# Path: agents/db_search.py
