import os
import config
from typing import List, Union
import pinecone
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


load_dotenv()


print(f"Found files in {config.DATABASE_DIRECTORY} and {config.CHUNK_SIZE} directory.")

def get_text_loaders(directory: str) -> List[TextLoader]:
    """Retrieve a list of TextLoader objects from a given directory."""
    return [
        TextLoader(os.path.join(directory, filename,))
        for filename in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, filename))
    ]

def main():
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    pinecone.init(api_key=config.PINECONE_API_KEY, environment=config.PINECONE_ENVIRONMENT)

    text_splitter = CharacterTextSplitter(chunk_size=int(config.CHUNK_SIZE), chunk_overlap=int(config.CHUNK_OVERLAP))
    loaders = get_text_loaders(config.DATABASE_DIRECTORY)
    print(f"Found {len(loaders)} files in {config.DATABASE_DIRECTORY} directory.")

    docsearch = None

    for loader in loaders:
        documents = loader.load()
        document_chunks = text_splitter.split_documents(documents)

        if docsearch is None:
            docsearch = Pinecone.from_documents(document_chunks, embeddings, index_name=config.INDEX_NAME, upsert=True)
        else:
            docsearch.add_documents(document_chunks, upsert=True)

    return docsearch


docsearch_instance = main()


def get_best_matching_document_content(question: str) -> Union[str, None]:
    """Return the best matching document content based on the user's query."""   
    matching_docs = docsearch_instance.similarity_search(question)

    if matching_docs:
        best_document = matching_docs[0]
        return best_document.page_content
    else:
        return None
