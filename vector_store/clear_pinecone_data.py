import os
import pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = "us-central1-gcp"
INDEX_NAME = "auto-gpt"

def clear_pinecone_data(index_name: str):
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    pinecone.deinit()
    
    with pinecone.deployment.PineconeIndex(index_name=index_name, api_key=PINECONE_API_KEY) as index:
        index.delete()

if __name__ == "__main__":
    clear_pinecone_data(INDEX_NAME)
