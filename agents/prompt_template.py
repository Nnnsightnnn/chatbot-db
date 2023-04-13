"""This is a template for a prompt."""
from langchain import PromptTemplate

def get_prompt_template():
    """Return the prompt template."""
    prompt = PromptTemplate(
        input_variables=["product"],
        template=template,
)
    template = """
    I want you to act as a naming consultant for new companies.
    Here are some examples of good company names:

    - search engine, Google
    - social media, Facebook
    - video sharing, YouTube

    The name should be short, catchy and easy to remember.

    What is a good name for a company that makes {product}?
    """

    return prompt

# Path: prompt_template.py
