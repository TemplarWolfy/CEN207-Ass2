import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests from the HTML client

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for API key

# Function to query ChatGPT using gpt-3.5-turbo
def query_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful virtual sales assistant for an e-commerce platform."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Root endpoint for health check and CORS preflight response
@app.route('/', methods=['GET', 'OPTIONS'])
def home():
    if request.method == 'OPTIONS':
        # CORS preflight response for the root URL
        return '', 200
    return "AI Virtual Assistant is running!"

# Route for handling user questions
@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    if request.method == 'OPTIONS':
        # CORS preflight response for the /ask endpoint
        return '', 200
    
    # Get JSON data from the request
    data = request.get_json()
    user_question = data.get("question", "")
    
    # Construct the prompt for ChatGPT
    prompt = f"Answer this question as a knowledgeable sales assistant: {user_question}"
    answer = query_chatgpt(prompt)
    
    # Return the assistant's response in JSON format
    return jsonify({"answer": answer})

# Start the server
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
