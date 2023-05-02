"""this module embeds chat history into a vector space"""

import os
# import json
# import sqlite3
from typing import List
from dotenv import load_dotenv

# import redis
# import openai

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.redis import Redis
from llama_index import download_loader
from memory import Memory

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
    # initialize Memory
    Memory(file_path=config.MEMORY_FILE_PATH)

    json_reader = download_loader("JSONReader")
    # Get the list of text loaders
    loaders = json_reader()
    loaders.load_langchain_documents(config.MEMORY_FILE_PATH)
    print(loaders)
    # Embed memory into Redis
    docs = None
    num_iterations = 0
    for loader in loaders:
        documents = loaders.load_data(config.MEMORY_FILE_PATH)
        num_iterations += 1
        document_chunks = text_splitter.split_documents(documents)

        if docs is None:
            docs = Redis.from_documents(redis_url="redis://localhost:6379",
                documents=document_chunks, embedding=embeddings,
                index_name='memory')
        else:
            docs.add_documents(document_chunks, embeddings)


if __name__ == "__main__":
    print(f"{config.MEMORY_FILE_PATH} processing...")
    embed_docs()
    print(f"{config.MEMORY_FILE_PATH} processed")

# path: vector_store\db_redis.
