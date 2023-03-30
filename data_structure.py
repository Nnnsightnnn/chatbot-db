"""This module splits data.txt then loads into Pinecone"""
import os
import pinecone

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# initialize loader and load split text
# loader = TextLoader("static/split.txt")
# documents = loader.load()

# add openai_api_key to environment variables
api_key = os.environ.get("OPENAI_API_KEY")


# load and split text and send to docs variable

from langchain.document_loaders import TextLoader
loader = TextLoader('static/elements.pdf')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# initialize of embeddings which transforms text into vectors
embeddings = OpenAIEmbeddings(openai_api_key="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")

# initialize pinecone vector store
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"),
              environment="	us-central1-gcp"
              )

# create variable for index name
INDEX_NAME = "slatebook001"

docsearch = Pinecone.from_documents(docs, embeddings, index_name=INDEX_NAME)

# create a variable for the query
#query = "What are employee rights?"

# search for the query
#docs = docsearch.similarity_search(query)

# print the results of the query and page content
#print(docs[0])

# data_structure.py
