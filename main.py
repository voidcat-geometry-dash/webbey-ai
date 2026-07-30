import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import litellm

# Load configurations from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enables your static website to connect from any local origin

# Read config from .env
PROVIDER = os.getenv("PROVIDER", "").lower()
MODEL_NAME = os.getenv("AI_MODEL", "")
API_KEY = os.getenv("API_KEY", "")

# Dynamically map the generic API_KEY variable to what LiteLLM expects based on your provider
if PROVIDER == "gemini":
    os.environ["GEMINI_API_KEY"] = API_KEY
elif PROVIDER == "openai":
    os.environ["OPENAI_API_KEY"] = API_KEY
elif PROVIDER == "anthropic":
    os.environ["ANTHROPIC_API_KEY"] = API_KEY
elif PROVIDER == "cohere":
    os.environ["COHERE_API_KEY"] = API_KEY
else:
    # Fallback default: set a direct provider variable if needed
    os.environ[f"{PROVIDER.upper()}_API_KEY"] = API_KEY

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"reply": "Error: Empty message provided."}), 400
        
    if not MODEL_NAME:
        return jsonify({"reply": "Error: AI_MODEL not specified in .env file."}), 500

    try:
        # LiteLLM automatically detects the provider route by looking at the model prefix 
        # or the environment variables we mapped above.
        response = litellm.completion(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Safely extract text from the standard OpenAI-style response format
        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        return jsonify({"reply": f"Backend Error processing AI request: {str(e)}"}), 500

if __name__ == "__main__":
    # Start the backend server on port 5000
    print(f"Backend active. Routing traffic to Provider: [{PROVIDER}] | Model: [{MODEL_NAME}]")
    app.run(debug=True, port=5000)
