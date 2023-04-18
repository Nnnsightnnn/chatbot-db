# GitHub Codespaces

# GPT-4 Chatbot
A simple chatbot application that uses Flask and GPT-4 to generate conversational responses.

## Requirements
- Python 3.6 or higher
- Flask

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nnnsightnnn/nnnsightnnn_chatbot-db.git

2. Change directories into the repository:
   ```bash
   cd nnnsightnnn_chatbot-db

3. Install the required packages:
   ```bash
   pip install -r requirements.txt

4. Run the application:
   ```bash
    python app.py

## Usage
1. Open a browser and navigate to http://localhost:5000
2. Type a message into the text box and click the "Send" button
3. The chatbot will respond with a message


## File Structure
```
application/
│
├── app.py                              # Main application entry point
├── requirements.txt                    # Dependencies for the application
├── config.py                           # Configuration settings
├── directory.txt                       # Base directory
├── .env.temp                           # Template for environment variables
│
├── database/                           # Database related modules
│   ├── __init__.py
|   ├── config.py                       # Configuration settings
│   ├── local_db.py                     # Local database (cached data)
│   ├── long_term_db.py                 # Long-term database
│   └── user_input_db.py                # User-input database
│
├── vector_store/                       # Vector store related modules
│   ├── __init__.py
|   ├── config.py                       # Configuration settings
│   ├── conversion.py                   # Convert databases to vector store
│   └── llm.py                          # Efficient LLM logic
│
├── agents/                             # Agent-related modules
│   ├── __init__.py
|   ├── config.py                       # Configuration settings
│   ├── base_agent.py                   # Base class for all agents
│   ├── write_file.py                   # Agent for writing data to file
│   ├── local_db_embedding.py           # Embeds files from database folder
│   ├── code_analysis_agent.py          # Agent for analyzing code
│   ├── coder.py                        # Agent for writing code
│   ├── search_agent.py                 # Agent for browsing the internet via Google Search
│   ├── plan_builder_agent.py           # Agent for interpreting user input to build a plan
│   └── self_reflection_agent.py        # Agent for self-reflecting on plans
│
├── chat_controller.py                  # Module for handling user input and delegating tasks to agents
│
├── templates/                          # HTML templates for Flask
│   ├── index.html                      # Base template for all pages
│
├── static/                             # Static files for Flask/React (CSS, JS, images, etc.)
│   ├── css/
│   ├── js/
│   └── img/
│
└── frontend/                           # React application directory
    ├── node_modules/
    ├── package.json
    ├── package-lock.json
    ├── public/
    │   ├── index.html
    │   ├── favicon.ico
    │   └── manifest.json
    └── src/
        ├── index.js
        ├── App.js
        ├── components/
        │   └── ...
        ├── containers/
        │   └── ...
        ├── utils/
        │   └── ...
        └── styles/
            └── ...

``` 
