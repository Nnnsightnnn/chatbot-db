import os
from dotenv import load_dotenv
import openai
from langchain.chat_models import ChatOpenAI
from agents.doc_search import local_doc_search
from vector_store.memory import Memory
from vector_store import memory_snippet_generator

import config

load_dotenv()

def generate_summary(document_content):
    """Generate a summary from document content."""
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                    max_tokens=config.OPENAI_MAX_TOKENS, api_key=config.OPENAI_API_KEY)
    summary_prompt = f"""Please explain the following information:
    \n{document_content} in depth.\n\n
    """

    summary = llm.call_as_llm(summary_prompt)
    return summary

def communicate_with_llm(user_message):
    """Communicate with the language model (e.g., GPT-4)."""
    # Get the path to memory.json
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_path, config.MEMORY_FILE_PATH)

    # Initialize Memory
    memory = Memory(file_path=file_path)

    # Initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                     max_tokens=config.OPENAI_MAX_TOKENS, api_key=config.OPENAI_API_KEY, streaming=True)

    # Choose which index to search
#    index_name = llm.call_as_llm(f"""
#    Based on {user_message}, should we utilize coding 
#    or fantasy gaming knowledge? 
#    Respond with all lowercase coding, knowledge, or 
#    """)

#    if index_name == "neither":
#        response = f"""
#        Based on my database, I will need to search the internet
#        """
#        return response
#    recall = local_doc_search(user_message, index_name="memory", k=4)
#    recall_prompt = f"""
##        Summarize {recall} and in less than 3 sentences.
#        Then with that in mind, answer {user_message}
    
#    creative_search_prompt = f"""
#        You're a dungeon master for a dnd campaign,
#        pick one of the following list
#        to develop an encounter for the campaign: The Book of Dragons,
#        Drow the Underdar, Elder Evils, Fiend Folio,
#        Libris Mortis, Lords of Madness, Monster Manual, Monster Manual II, 
#   """

        # Search for content in index_name for llm
    document_content = local_doc_search(user_message, index_name="knowledge", k=5)

    # Logic for document content
    if document_content:
#        encounter = llm.call_as_llm(creative_search_prompt) 
        summary = generate_summary(document_content)
        new_prompt = f"""Answer {user_message}\n\n
        based on the following:
        \n{summary}\n\nPlease provide an informed and detailed response in beautiful prose.: 
        """
        response = llm.call_as_llm(message=new_prompt)
    else:
        response = llm.call_as_llm(message=user_message)

    # Add memory to memory.json
    memory.add_memory(user_message, response)

    # Retrieve and check the last chat record
    last_chat_record = memory.retrieve_memory(memory.get_memory_count() - 1)

    if last_chat_record:
        memory_snippet_generator.main()
        print("Saved the last chat record")
    else:
        print("Failed to save the last chat record")

    # Return the response string
    return response