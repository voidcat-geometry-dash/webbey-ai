import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Load configurations from .env
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# Environment and API mapping configuration settings
CONFIG = {
    "PROVIDER": os.getenv("PROVIDER", "gemini").lower().strip(),
    "AI_MODEL": os.getenv("AI_MODEL", "gemini-2.0-flash").strip(),
    "AI_API_KEY": os.getenv("API_KEY", "").strip(),
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "").strip(),
    "DEFAULT_REPO": os.getenv("GITHUB_REPO", "voidcat-geometry-dash").strip(),
    "ADMIN_PASSWORD": os.getenv("ADMIN_PASSWORD", "ChangeMeSecurely123!").strip()
}

@app.route("/")
def serve_index():
    """Serves index.html UI dashboard directly from app space."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/chat", methods=["POST"])
def chat():
    """Secure API routing mechanism with conditional server validation."""
    # Force security credential validation only if running in production server mode
    if "--server" in sys.argv:
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != f"Bearer {CONFIG['ADMIN_PASSWORD']}":
            return jsonify({"reply": "Unauthorized: Invalid Server Admin Token Verification"}), 401

    data = request.get_json() or {}
    user_query = data.get("message", "")
    target_repo = data.get("repo", CONFIG["DEFAULT_REPO"])

    if not CONFIG["AI_API_KEY"]:
        return jsonify({"reply": "System Engine Error: Missing AI API Key Context."}), 500

    github_context = ""
    
    # Process internal Git issue context parsing using token references
    if target_repo and CONFIG["GITHUB_TOKEN"]:
        try:
            headers = {
                "Authorization": f"token {CONFIG['GITHUB_TOKEN']}",
                "Accept": "application/vnd.github.v3+json"
            }
            url = f"https://github.com{target_repo}/issues?state=open"
            res = requests.get(url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                issues = res.json()[:5]
                github_context = f"\n\n[Live GitHub Feed for {target_repo}]:\n"
                for issue in issues:
                    github_context += f"- Issue #{issue['number']}: {issue['title']}\n"
        except Exception as e:
            github_context = f"\n(Failed to aggregate repo context profiles: {str(e)})"

    # Simulated production AI engine connector return statement
    ai_reply = f"Webbey-AI responding. Workspace: {target_repo}. Status: Online."
    return jsonify({
        "reply": ai_reply,
        "context_attached": bool(github_context),
        "environment": "production-server" if "--server" in sys.argv else "local-sandbox"
    })

if __name__ == "__main__":
    # Handle environment flags passed down via execution layers
    if "--server" in sys.argv:
        from waitress import serve
        print("\n🚀 [PRODUCTION] Booting Webbey-AI Engine via Waitress...")
        print("📍 Serving Admin UI & HTTP Server API on http://0.0.0")
        serve(app, host="0.0.0.0", port=8080)
        
    elif "--noserver" in sys.argv:
        print("\n💻 [LOCAL SANDBOX] Booting Webbey-AI Local Instance...")
        print("📍 Serving Sandbox UI & HTTP Local API on http://127.0.0.1:5000")
        app.run(host="127.0.0.1", port=5000, debug=True)
        
    else:
        print("\n❌ Error: Missing execution runtime parameter.")
        print("Usage command requirements:")
        print("  python3 main.py --server      (For Public VPS Infrastructure Deployment)")
        print("  python3 main.py --noserver    (For Local PC Development/Testing)")
        sys.exit(1)
