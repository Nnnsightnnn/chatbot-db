"""this module embeds everything in a directory into a vector space"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.redis import Redis


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

    # Initialize Redis


    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    # Get the list of text loaders
    loaders = get_text_loaders(str(config.DATABASE_DIRECTORY))
    print(f"Found {len(loaders)} files in {config.DATABASE_DIRECTORY} directory.")

    # Process documents and upload to Redis
    docs = None
    num_iterations = 0
    for loader in loaders:
        documents = loader.load()
        num_iterations += 1
        print(f"{num_iterations} number of documents loaded")
        document_chunks = text_splitter.split_documents(documents)

        if docs is None:
            docs = Redis.from_documents(redis_url="redis://localhost:6379",
                documents=document_chunks, embedding=embeddings,
                index_name='coding')
        else:
            docs.add_documents(documents=document_chunks, embedding=embeddings)


if __name__ == "__main__":
    print(f"{config.DATABASE_DIRECTORY} processing...")
    embed_docs()
    print(f"{config.DATABASE_DIRECTORY} processed")

# path: vector_store\db_redis.
