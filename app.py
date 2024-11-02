from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests from the HTML client

# Configure OpenAI API key
openai.api_key = "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"

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

# Route for handling user questions
@app.route('/ask', methods=['POST'])
def ask():
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
    app.run(debug=True)
