"""Configuration settings"""
import os
from dotenv import load_dotenv

load_dotenv()
### Credentials ###
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

### Pinecone settings ###
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
INDEX_NAME = os.environ.get("INDEX_NAME")

### Local database settings ###
CHUNK_SIZE = os.environ.get("CHUNK_SIZE")
CHUNK_OVERLAP = os.environ.get("CHUNK_OVERLAP")
DATABASE_DIRECTORY = os.environ.get("DATABASE_DIRECTORY")

### Local vector store settings ###
INDEX_FILE = os.environ.get("INDEX_FILE")
VECTOR_STORE_DIRECTORY = os.environ.get("VECTOR_STORE_DIRECTORY")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

### MODE Settings ###
MODE = os.environ.get("MODE")

### OpenAI Settings ###
OPENAI_MAX_TOKENS = os.environ.get("OPENAI_MAX_TOKENS")
OPENAI_TEMPERATURE = os.environ.get("OPENAI_TEMPERATURE")