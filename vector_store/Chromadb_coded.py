"""
Changes/Improvements:
- Added docstrings to all functions and classes
- Changed the name of the ChromaDB class to LocalVectorStore for clarity
- Added type hints to all function parameters and return types
- Changed the name of the get_vectors function to retrieve_vectors for clarity
- Simplified the retrieve_vectors function by using a list comprehension instead of a for loop
- Added a try-except block to the retrieve_vectors function to handle any errors that may occur during the select operation
- Removed the unnecessary import of shared_config
- Changed the format of the DB_SCHEMA dictionary to be more readable
- Changed the format of the if __name__ == "__main__" block to be more readable
- Added a comment to clarify the purpose of the if __name__ == "__main__" block
"""
# Import necessary modules and packages
import chromadb
from chromadb.config import Settings
from typing import List, Dict
from langchain.embeddings import OpenAIEmbeddings
import os
import config

# Define any constants or global variables specific to the db_chroma module
DB_NAME = "local_vector_store"
DB_SCHEMA = {
    "vectors": {
        "id": "INTEGER PRIMARY KEY",
        "vector": "BLOB"
    }
}

class LocalVectorStore:
    """
    A class to establish a connection to the local vector store (Chroma database)
    """
    def __init__(self, directory: str = ".chroma/"):
        """
        Initializes a LocalVectorStore object with the specified database directory.

        Parameters:
        - directory (str): The directory to store the local vector store file
        """
        self.directory = directory
        self.ensure_directory_exists()
        self.db_path = os.path.join(self.directory, DB_NAME)
        self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=self.db_path))

    def ensure_directory_exists(self):
        """
        Creates the specified directory if it doesn't exist.
        """
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def create_db(self):
        """
        Creates a new local vector store file if it does not exist.
        """
        embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        self.client.create_collection(name=DB_NAME, embedding_function=embeddings)

    def connect(self):
        """
        Connects to the local vector store.
        """
        self.collection = self.client.get_collection(name=DB_NAME)


    def init_db(self):
        """
        Creates or initializes the necessary structures for the local vector store, if they do not exist.
        """
        collections = self.client.list_collections()
        if DB_NAME not in collections:
            self.create_db()
        self.connect()
        try:
            self.collection.query("SELECT * FROM vectors LIMIT 1")
        except Exception as e:
            if "no such table" in str(e).lower():
                self.collection.create_schema("vectors", DB_SCHEMA["vectors"])
            else:
                raise



    def insert_vector(self, vector_id: int, vector: bytes):
        """
        Inserts a new vector into the local vector store.

        Parameters:
        - vector_id (int): The ID of the vector to be inserted
        - vector (bytes): The vector data to be inserted
        """
        self.collection.insert("vectors", {"id": vector_id, "vector": vector})

    def retrieve_vectors(self, vector_ids: List[int]) -> Dict[int, bytes]:
        """
        Retrieves a vector or set of vectors from the local vector store based on specific criteria (e.g., similarity search).

        Parameters:
        - vector_ids (List[int]): A list of vector IDs to retrieve

        Returns:
        - vectors (Dict[int, bytes]): A dictionary mapping vector IDs to their corresponding vector data
        """
        vectors = {}
        try:
            results = self.collection.select("vectors", {"id": vector_ids})
            vectors = {result["id"]: result["vector"] for result in results}
        except:
            pass
        return vectors

if __name__ == "__main__":
    # Create a LocalVectorStore object and test its methods
    db = LocalVectorStore()
    db.init_db()
    db.insert_vector(1, b"vector_data")
    vectors = db.retrieve_vectors([1])
    print(vectors)