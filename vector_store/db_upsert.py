"""This module creates an embedding utilizing an Ada-GPT model and uploads it to Pinecone."""

import os
from typing import List
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

import pinecone
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
    """Create an embedding and upload it to Pinecone."""
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    # Initialize Pinecone
    pinecone.init(api_key=config.PINECONE_API_KEY,
                  environment=config.PINECONE_ENVIRONMENT)
    print("Pinecone Initialized")

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    # Get the list of text loaders
    loaders = get_text_loaders(str(config.DATABASE_DIRECTORY))
    print(f"Found {len(loaders)} files in {config.DATABASE_DIRECTORY} directory.")

    # Process documents and upload to Pinecone
    docs = None
    num_iterations = 0
    for loader in loaders:
        documents = loader.load()
        num_iterations += 1
        print(f"{num_iterations} number of documents loaded")
        document_chunks = text_splitter.split_documents(documents)

        if docs is None:
            docs = Pinecone.from_documents(
                document_chunks, embeddings, index_name=config.INDEX_NAME, upsert=True)
        else:
            docs.add_documents(document_chunks, upsert=True)

    print("Finished uploading documents to Pinecone")


if __name__ == "__main__":
    print(f"Found files in {config.DATABASE_DIRECTORY}")
    embed_docs()

# Path agents/local_db_embedding.py
