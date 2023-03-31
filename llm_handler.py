import os
import openai
from langchain.llms import OpenAI
from data_structure import get_best_matching_document_content


def embed_text(elements):
    """Your code to embed the text into a vector space"""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    elements = openai.Embedding.create(
        input=elements,
        model="text-embedding-ada-002"
    )
    return elements


def generate_summary(user_message, document_content):
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(temperature=0.5, max_tokens=100, api_key=api_key)

    summary_prompt = f"Please provide a brief summary of the following information:\n{document_content}"
    summary = llm(summary_prompt)
    return summary


def communicate_with_llm(user_message):
    """Your code to communicate with the language model (e.g., GPT-4)"""
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(temperature=0.9, max_tokens=100, api_key=api_key)

    document_content = get_best_matching_document_content(user_message)

    if document_content:
        summary = generate_summary(user_message, document_content)
        new_prompt = f"{user_message}\n\nBased on the summary of the relevant information:\n{summary}\n\nPlease provide an informed and natural response: "

    else:
        new_prompt = user_message


response = llm(new_prompt)


# Return the response string (replace 'response' with the actual response variable if different)
return response

response = llm(user_message)

# Return the response string (replace 'response' with the actual response variable if different)
return response

# Path: llm_handler.py
