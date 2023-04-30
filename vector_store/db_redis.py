"""this module embeds chat history into a vector space"""

import os
import redis
import openai

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.redis import Redis

from dotenv import load_dotenv

load_dotenv()



