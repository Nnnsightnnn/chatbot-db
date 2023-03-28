import os
from flask import Flask, request, jsonify, render_template
from llm_handler import communicate_with_llm

api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '')
    
    # Call your GPT-4 model here to generate a response
    response = generate_gpt4_response(message)
    
    return jsonify(response=response)

def generate_gpt4_response(message):
    # Add your GPT-4 model code here
    message = communicate_with_llm(message)
    return message

if __name__ == '__main__':
    app.run(debug=True)


#...
