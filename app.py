from flask import Flask, request, jsonify
from chatbot import generate_ai_response

app = Flask(__name__)

# Default route for testing
@app.route("/")
def home():
    return "✅ Flask server is running! Use /chat to talk to the chatbot."

# Chatbot API route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    bot_response = generate_ai_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
