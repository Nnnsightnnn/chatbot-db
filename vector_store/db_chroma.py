"""This module upserts/loads data from local Chroma database"""
import os
import chromadb
from typing import List
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.indexes.vectorstore import VectorstoreIndexCreator

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

    # Get the absolute path of the parent directory
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

    # Ensure the directory exists
    directory_path = os.path.join(parent_dir, f"chatbot-db/{config.VECTOR_STORE_DIRECTORY}")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    # Get the list of text loaders
    loaders = get_text_loaders(str(config.DATABASE_DIRECTORY))
    print(f"Found {len(loaders)} files in {config.DATABASE_DIRECTORY} directory.")
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    # Process documents and embed with Chroma
#    for loader in loaders:
#        docs = VectorstoreIndexCreator().from_loaders([loader])
    num_iterations = 0
    docs = None
    for loader in loaders:
        documents = loader.load()
        document_chunks = text_splitter.split_documents(documents)
        num_iterations += 1
        print(f"{num_iterations} number of documents loaded")


        if docs is None:
            client_settings = chromadb.configure(chroma_db_impl="duckdb+parquet", 
                                                 persist_directory=directory_path, anonymized_telemetry=False)
            docs = Chroma(client_settings=client_settings,
                persist_directory=directory_path,
                embedding_function=embeddings, collection_name=config.COLLECTION_NAME)
        else:
            docs.add_documents(documents=document_chunks, embedding=embeddings)
            docs.persist()

    print("Finished uploading documents to LocalDB.")


if __name__ == "__main__":
    print(f"Found files in {config.DATABASE_DIRECTORY}")
    embed_docs()

# Path agents/local_db_embedding.py
