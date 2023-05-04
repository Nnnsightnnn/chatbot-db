"""this module embeds chat history into a vector space"""

import os
# import json
# import sqlite3
from pathlib import Path
from typing import List
from dotenv import load_dotenv
#import redis
#import openai

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.redis import Redis
from llama_index import download_loader


import config

load_dotenv()


def get_text_loaders(directory: str) -> List[TextLoader]:
    """Retrieve a list of TextLoader objects from a given directory."""
    return [
        TextLoader(os.path.join(directory, filename,))
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename))
    ]


def embed_docs():
    """Create an embedding and upload it to Redis."""
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    json_reader = download_loader("JSONReader")
    # Get the list of text loaders
    loader = json_reader()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    memory_file_path = os.path.join(script_dir,
                                    "database/memory/memory.json")
    documents = loader.load_data(Path(memory_file_path))

    # Convert Document objects to strings
    texts = [doc.text for doc in documents]

    # Embed memory into Redis
    document_chunks = text_splitter.create_documents(texts)
    docs = Redis.from_documents(documents=document_chunks,
                                index_name='memory',
                                embedding=embeddings, redis_url="redis://localhost:6379")
    
    #docs = Redis.from_existing_index(index_name='memory', embedding=embeddings, redis_url="redis://localhost:6379")
    #docs.add_documents(documents=document_chunks, embedding=embeddings)

if __name__ == "__main__":
    print(f"storing {config.MEMORY_FILE_PATH} in Redis...")
    embed_docs()
    print(f"{config.MEMORY_FILE_PATH} processed")

# path: vector_store\db_redis_memory
