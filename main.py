import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import litellm
from github import Github

app = Flask(__name__)
CORS(app)  # Allows your static website code to interact with this local port

# In-Memory Session Variables (No data is saved to disk/hard drive)
SESSION_DATA = {
    "PROVIDER": None,
    "AI_MODEL": None,
    "AI_API_KEY": None,
    "GITHUB_TOKEN": None
}

@app.route("/api/initialize", methods=["POST"])
def initialize():
    """Securely capture keys directly into active RAM."""
    data = request.get_json() or {}
    
    SESSION_DATA["PROVIDER"] = data.get("provider", "").lower().strip()
    SESSION_DATA["AI_MODEL"] = data.get("ai_model", "").strip()
    SESSION_DATA["AI_API_KEY"] = data.get("ai_api_key", "").strip()
    SESSION_DATA["GITHUB_TOKEN"] = data.get("github_token", "").strip()
    
    # Dynamically inject the key into temporary environment space for LiteLLM
    prov = SESSION_DATA["PROVIDER"]
    if prov:
        os.environ[f"{prov.upper()}_API_KEY"] = SESSION_DATA["AI_API_KEY"]
        
    return jsonify({"status": "Success", "message": "Credentials loaded safely into RAM. Zero disk storage used."})

@app.route("/api/chat", methods=["POST"])
def chat():
    """Injects live GitHub context straight to your AI model context without logging."""
    if not SESSION_DATA["GITHUB_TOKEN"] or not SESSION_DATA["AI_API_KEY"]:
        return jsonify({"reply": "Error: Run initialization inside the UI first to pass your RAM tokens."}), 400

    data = request.get_json() or {}
    user_query = data.get("message", "")
    repo_name = data.get("repo", "") # Format example: "username/repository"

    github_context = ""
    
    # 1. Securely fetch context directly from GitHub using your runtime token
    if repo_name:
        try:
            g = Github(SESSION_DATA["GITHUB_TOKEN"])
            repo = g.get_repo(repo_name)
            
            # Grabbing recent issues to feed to the AI assistant
            issues = repo.get_issues(state="open")[:5]
            github_context = f"\n\nLive GitHub Context for {repo_name}:\n"
            github_context += "Recent Open Issues:\n"
            for issue in issues:
                github_context += f"- #{issue.number}: {issue.title}\n"
        except Exception as ge:
            github_context = f"\n(Could not read GitHub Repo data: {str(ge)})"

    # 2. Hand off the combined query directly to your chosen AI model
    try:
        system_instruction = "You are a secure coding assistant. Help the user with their question using the provided GitHub data."
        full_user_prompt = f"{user_query}{github_context}"
        
        response = litellm.completion(
            model=SESSION_DATA["AI_MODEL"],
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": full_user_prompt}
            ]
        )
        
        return jsonify({"reply": response.choices.message.content})
        
    except Exception as e:
        return jsonify({"reply": f"AI Engine Connection Error: {str(e)}"}), 500

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" WEB-AI SECURE RUNTIME ACTIVE")
    print(" Warning: Closing this window wipes all active memory tokens instantly.")
    print("="*60 + "\n")
    app.run(debug=False, port=5000)
