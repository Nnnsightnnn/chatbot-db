"""this module embeds chat history into a vector space"""

import os
import json
import sqlite3
#from typing import List
from dotenv import load_dotenv
#from io import StringIO

#import redis
#import openai

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from langchain.vectorstores.redis import Redis
#from agents.memory import DatabaseManager

import config

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"BASE_DIR: {BASE_DIR}")
FILEPATH = "/workspaces/chatbot-db/database/memory/memory.sqlite3"
print(f"FILEPATH: {FILEPATH}")

class Document:
    def __init__(self, text):
        self.page_content = text
        self.metadata = text

def get_all_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [table[0] for table in cursor.fetchall()]

def embed_docs():
    """Create an embedding and upload it to Redis."""
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

    # Initialize the text splitter
    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE),
                                          chunk_overlap=int(config.CHUNK_OVERLAP))

    # Connect to the SQLite database and extract data
    data = sqlite3.connect(FILEPATH)
    cursor = data.cursor()
    
    # Get all tables in the database
    tables = get_all_tables(cursor)

    docs = None
    num_iterations = 0

    # Iterate through all tables
    for table_name in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        loaders = cursor.fetchall()

        # Process documents and upload to Redis
        for loader in loaders:
            num_iterations += 1
            print(f"{num_iterations} number of documents loaded")
            # Create a Document object with the text_to_process and pass it to the text_splitter
            document = Document(loader)
            document_chunks = text_splitter.split_documents([document])


            if docs is None:
                docs = Redis.from_documents(docs,
                                              embeddings, redis_url="redis://localhost:6379",
                                              index_name='link')
            else:
                docs.add_texts(texts=document_chunks)

    # Close the database connection
    data.close()

if __name__ == "__main__":
    print(f"{FILEPATH} processing...")
    embed_docs()
    print(f"{FILEPATH} processed")

# path: vector_store\db_redis.
