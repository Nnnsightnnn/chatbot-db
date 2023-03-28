"""This module gets user input and returns answer from OpenAI API"""

import os
from langchain.llms import OpenAI

def communicate_with_llm(user_message):
    # Your code to communicate with the language model (e.g., GPT-4)
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(temperature=0.9, max_tokens=100, api_key=api_key)

    response = llm(user_message)

    # Return the response string (replace 'response' with the actual response variable if different)
    return response
