"""this module tests memory class"""
import os
from dotenv import load_dotenv
from memory import Memory

import config

load_dotenv()

#memory = Memory("/workspaces/chatbot-db/vector_store/database/memory/memory.json")


print(os.path.abspath(__file__))
file_path = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(file_path, f"{config.MEMORY_FILE_PATH}"))
# path = "vector_store/print.py"
