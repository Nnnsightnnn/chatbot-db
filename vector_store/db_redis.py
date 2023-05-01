"""this module embeds chat history into a vector space"""

import os
import redis
import openai
import config
import json

from typing import List
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.redis import Redis
from agents.memory import DatabaseManager 
from dotenv import load_dotenv

load_dotenv()

filepath = "database/memory/"

def embed_docs():
    """Create an embedding and upload it to Redis."""
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    # Get the list of text loaders
    loaders = DatabaseManager().get_database()

    # Process documents and upload to Pinecone
    docs = None
    num_iterations = 0
    for loader in loaders:
        documents = loader.load()
        num_iterations += 1
        print(f"{num_iterations} number of documents loaded")
        document_chunks = text_splitter.split_documents(documents)

        if docs is None:
            docs = Redis.from_documents(docs, 
                                              embeddings, redis_url="redis://localhost:6379",  
                                              index_name='link')
        else:
            docs.add_texts(texts=document_chunks)
    

if __name__ == "__main__":
    print(f"{filepath} processing...")
    embed_docs()
    print(f"{filepath} processed")

# path: vector_store\db_redis.py