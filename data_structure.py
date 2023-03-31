"""this module structures and splits the data then embeds it into Pinecone"""
import os
import pinecone
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
api_key_pinecone = os.environ.get("PINECONE_API_KEY")

loader = TextLoader('static/restrict_act.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
document_chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
INDEX_NAME = "restrict-act"

pinecone.init(api_key=api_key_pinecone, environment="us-central1-gcp")

docsearch = Pinecone.from_documents(document_chunks, embeddings, index_name=INDEX_NAME)

def get_best_matching_document_content(query):
    """This function returns the best matching document content based on the user's query."""
    matching_docs = docsearch.similarity_search(query)

    if matching_docs:
        best_document = matching_docs[0]
        return best_document.page_content
    else:
        return None
