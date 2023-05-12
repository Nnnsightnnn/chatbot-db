"""this module tests memory class"""
import os
from dotenv import load_dotenv
#from vector_store import memory
from vector_store import memory_snippet_generator

import config

load_dotenv()

#memory = Memory("/workspaces/chatbot-db/vector_store/database/memory/memory.json")


print(os.path.abspath(__file__))
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.join(file_path, f"{config.MEMORY_FILE_PATH}"))
memory_snippet_generator.main(max_words=20)

# path = "vector_store/print.py"
