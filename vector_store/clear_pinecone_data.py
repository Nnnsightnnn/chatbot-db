"""Clear the Pinecone index."""
import pinecone
from dotenv import load_dotenv

import config

load_dotenv()

def clear_pinecone_data():
    """Clear the Pinecone index."""
    pinecone.init(api_key=config.PINECONE_API_KEY, environment=config.PINECONE_ENVIRONMENT)
    pinecone.delete_index(config.INDEX_NAME)
    print(f"Deleted index {config.INDEX_NAME}")

if __name__ == "__main__":
    clear_pinecone_data()
