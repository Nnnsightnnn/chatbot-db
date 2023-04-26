"""This module contains the code to communicate with the language model (e.g., GPT-4)"""
import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from agents.doc_search import pinecone_doc_search
from agents.doc_search import local_doc_search

import config

load_dotenv()

def generate_summary(document_content):
    """this function generates a summary from document content"""
    
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                    max_tokens=config.OPENAI_MAX_TOKENS, api_key=config.OPENAI_API_KEY)
    summary_prompt = (f"Please explain"
                      f"following information:\n{document_content} in depth.\n\n")
    summary = llm.call_as_llm(summary_prompt)
    return summary

def communicate_with_llm(user_message):
    """Your code to communicate with the language model (e.g., GPT-4)"""
#initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                     max_tokens=config.OPENAI_MAX_TOKENS, api_key=config.OPENAI_API_KEY)
#create document content for llm
    document_content = local_doc_search(user_message)
#logic for document content
    if document_content:
        summary = generate_summary(document_content)
        new_prompt = (f"{user_message}\n\nBased on the summary of the relevant information:"
                      f"\n{summary}\n\nPlease provide an informed and detailed response: ")
        response = llm.call_as_llm(message=new_prompt)
#logic for no document content
    else:
        response = llm.call_as_llm(message=user_message)

# Return the response string
    return response

# Path: agents/chat_controller.py
