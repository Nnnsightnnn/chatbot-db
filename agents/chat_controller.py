"""This module contains the code to communicate with the language model (e.g., GPT-4)"""
import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from .local_db_embedding import get_best_matching_document_contents
import config

load_dotenv()

def embed_text(elements):
    """Your code to embed the text into a vector space"""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    elements = openai.Embedding.create(
        input=elements,
        model="text-embedding-ada-002"
    )
    return elements


def generate_summary(document_content):
    """this function generates a summary from document content"""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo',
                    max_tokens=1000, api_key=openai.api_key)
    summary_prompt = (f"Please provide a brief summary of the"
                      f"following information:\n{document_content}")
    summary = llm.call_as_llm(summary_prompt)
    return summary


def communicate_with_llm(user_message):
    """Your code to communicate with the language model (e.g., GPT-4)"""
#initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo',
                     max_tokens=500, api_key=openai.api_key)
#create document content for llm
    document_content = get_best_matching_document_contents(user_message)
#logic for document content
    if document_content:
        summary = generate_summary(document_content)
        new_prompt = (f"{user_message}\n\nBased on the documents:"
                      f"\n{summary}\n\nPlease provide an informed and natural response: ")
        response = llm.call_as_llm(new_prompt)
#logic for no document content
    else:
        response = llm(user_message)
    print(response)
# Return the response string
    return response

class ChatController:
    """This class is the main controller for the chatbot"""
    def __init__(self, model):
        self.model = model
        self.template = f"You're in {config.MODE}-mode.  Assist accordingly"
        self.user_message = ""
        self.response = ""

    def get_user_message(self):
        """This function gets the user message"""
        self.user_message = input("Please enter your message: ")
        return self.user_message

    def get_response(self):
        """This function gets the response from the language model"""
        self.response = communicate_with_llm(self.user_message)
        return self.response

    def print_response(self):
        """This function prints the response"""
        print(self.response)

    def run(self):
        """This function runs the chatbot"""
        while True:
            self.get_user_message()
            self.get_response()
            self.print_response()


# Path: agents/chat_controller.py
