"""

Changes/Improvements:
- Removed duplicate import statements
- Removed unused import statements
- Added comments to explain each section of the code
- Renamed variables to be more descriptive
- Added whitespace to improve readability
- Removed duplicate definition of input_text variable

Corrected Code:
"""

# Import necessary modules
from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.cache import RedisCache
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import redis
from langchain.memory import ConversationBufferMemory
from typing import List

import config

embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
rds = redis.Redis(index_name="cache", redis_url=config.REDIS_URL,
                  embedding_function=embeddings)

# Define the tools
search_tool = Tool(
    name="Search",
    func=SerpAPIWrapper(serpapi_api_key="32b62f7c52f9ab2b8cabc1471c6b5e95ced2ec03172471fc6586dcb2e0ac6130").run,
    description="Useful for answering questions about current events. Ask targeted questions."
)

calculator_tool = Tool(
    name="Calculator",
    func=LLMMathChain(llm=OpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)).run,
    description="Useful for answering math questions."
)

database_tool = Tool(
    name="RedisCache",
    func=RedisCache(redis_=rds.from_existing_index(embedding=embeddings, index_name="cache")),
    description="Useful for storing and retrieving information."
)

tools = [search_tool, calculator_tool, database_tool]

# Initialize the zero-shot agent
zero_shot_agent = initialize_agent(tools, ChatOpenAI(temperature=0), agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Define the input for the zero-shot agent
zero_shot_input = "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"

# Run the zero-shot agent
zero_shot_agent.run(zero_shot_input)

# Define the memory for the conversation
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the conversational agent
conversational_agent = initialize_agent(tools, OpenAI(temperature=0), agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

# Define the input for the conversational agent
conversational_input = "Hi, I am Bob."

# Run the conversational agent
conversational_agent.run(conversational_input)