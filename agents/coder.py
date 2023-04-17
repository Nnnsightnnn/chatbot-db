"""this module will take user input and return Python script"""

import os
import config
import openai
from dotenv import load_dotenv
#from template_module  import TemplateClass
from write_file import write_input_to_py_file
from local_db_embedding import get_best_matching_document_content
from langchain.chat_models import ChatOpenAI
from tqdm import tqdm

load_dotenv()




#initialize smart_llm
def generate_code_alpha(user_message):
    """this function utilizes document content to generate code"""
#create document content for llm
    document_content = get_best_matching_document_content(user_message)
#initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo', max_tokens=1000, api_key=openai.api_key)
    code_prompt = (f"Please generate code in Python to produce {user_message}"
                      f"utilize these {document_content} as a primary reference when generating code")
    code_response = llm.call_as_llm(code_prompt)
    return code_response

def generate_code_beta(user_message):
    """this function utilizes document content to generate code"""
#create document content for llm
#    document_content = get_best_matching_document_content(user_message)
#initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo', max_tokens=1000, api_key=openai.api_key)
    code_prompt = (f"Please review/improve this code {user_message}"
                      f"Respond with the changes/improvements encapsulated with triple quotation marks and then the corrected version of the code")
    code_response = llm.call_as_llm(code_prompt)
    return code_response


def generate_code_release(user_message):
    """this function utilizes document content to generate code"""
#create document content for llm
#    document_content = get_best_matching_document_content(user_message)
#initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo', max_tokens=1000, api_key=openai.api_key)
    code_prompt = (f"Please review/improve this code {user_message}"
                      f"Respond with the changes/improvements encapsulated with triple quotation marks and then the corrected version of the code")
    code_response = llm.call_as_llm(code_prompt)
    return code_response

def long_running_operation():
    # Do some long-running operation here
    for i in range(1000000):
        pass

def main(user_message):
    """this function will take user input and return Python script"""

    with tqdm(total=1) as progress:
        long_running_operation()
        progress.update(1)

        #generate code_alpha
        code_alpha = generate_code_alpha(str(user_message))
        #json_description_of_code = smart_llm.call(template_class.generate_json(user_input))

        ### template_class.beta
        code_beta = generate_code_beta(str(code_alpha))
        ### template_class.release
        code_release = generate_code_release(str(code_beta))

        write_input_to_py_file(code_alpha, "test_alpha.py")
        write_input_to_py_file(code_beta, "test_beta.py")
        write_input_to_py_file(code_release, "test_release.py")

    print("Finished")
#Path: agents\coder.py
