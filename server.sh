#!/bin/bash

# Ensure the script stops executing immediately if a command fails
set -e

# Define color prompts for clean terminal reading
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print usage instructions if the user passes an invalid or missing flag
usage() {
    echo -e "${RED}Error: Invalid flag or missing argument.${NC}"
    echo -e "Usage options:"
    echo -e "  ${GREEN}./server.sh --server${NC}       -> Deploy on a Remote Server (VPS/VDS/Bare-Metal on Port 8080)"
    echo -e "  ${BLUE}./server.sh --nonserver${NC}   -> Deploy on a Local Machine (PC/Laptop on Port 5000)"
    exit 1
}

# Ensure at least one argument is given
if [ $# -eq 0 ]; then
    usage
fi

# Detect deployment environment flag
IS_SERVER=false

case "$1" in
    --server)
        IS_SERVER=true
        echo -e "${GREEN}[+] Mode Selected: Cloud VPS / VDS / Bare-Metal Linux Server Production${NC}"
        ;;
    --nonserver)
        IS_SERVER=false
        echo -e "${BLUE}[+] Mode Selected: Local Development PC / Laptop Sandbox Environment${NC}"
        ;;
    *)
        usage
        ;;
esac

# 1. Automatic Python Dependency Checklist Setup
echo -e "${YELLOW}[*] Validating python system dependencies...${NC}"
pip install -q flask flask-cors python-dotenv requests waitress

# 2. Dynamic Source Core Generation for main.py
echo -e "${YELLOW}[*] Writing main.py backend logic stack...${NC}"
cat << 'EOF' > main.py
import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# Fallback Configuration settings parsed via local .env file structures
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
    """Secure api routing mechanism supporting live token isolation protocols."""
    # Force access key check if running as a live public cloud server structure
    if sys.argv[-1] == "--server":
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != f"Bearer {CONFIG['ADMIN_PASSWORD']}":
            return jsonify({"reply": "Unauthorized: Invalid Server Admin Token Verification"}), 401

    data = request.get_json() or {}
    user_query = data.get("message", "")
    target_repo = data.get("repo", CONFIG["DEFAULT_REPO"])

    if not CONFIG["AI_API_KEY"]:
        return jsonify({"reply": "System Engine Error: Missing AI API Key Context."}), 500

    github_context = ""
    
    # Process internal Git context parsing using token references
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

    ai_reply = f"Webbey-AI responding. Target Repository: {target_repo}."
    return jsonify({
        "reply": ai_reply,
        "context_attached": bool(github_context),
        "environment": "production-server" if sys.argv[-1] == "--server" else "local-sandbox"
    })

if __name__ == "__main__":
    # Check execution flags passed from bash script engine layer
    mode_flag = sys.argv[-1]
    
    if mode_flag == "--server":
        from waitress import serve
        print("\n🚀 [PRODUCTION DEPLOYMENT] Initializing Webbey-AI Infrastructure Core...")
        print("📍 Server Endpoint: http://0.0.0")
        serve(app, host="0.0.0.0", port=8080)
    else:
        print("\n💻 [LOCAL DEVELOPMENT] Initializing Webbey-AI Local Sandbox Instance...")
        print("📍 Sandbox Endpoint: http://127.0.0.1:5000")
        app.run(host="127.0.0.1", port=5000, debug=True)
EOF

# 3. Environment Execution Router Configuration
if [ "$IS_SERVER" = true ]; then
    echo -e "${YELLOW}[*] Configuring Linux Network Firewall rules (Port 8080)...${NC}"
    if command -v ufw &> /dev/null; then
        sudo ufw allow 8080/tcp || true
    fi

    echo -e "${GREEN}[+] Booting persistent production background daemon...${NC}"
    # Launch in the background using nohup to prevent terminal logout dropouts
    nohup python main.py --server > server.log 2>&1 &
    
    echo -e "${GREEN}================================================================${NC}"
    echo -e " 🚀 WEBBY-AI CLOUD SERVER LIVE"
    echo -e " 📍 Listening on Address Port: http://<YOUR_VPS_IP>:8080"
    echo -e " 📋 Logs routing to file tracking path: server.log"
    echo -e "${GREEN}================================================================${NC}"
else
    echo -e "${BLUE}================================================================${NC}"
    echo -e " 💻 WEBBY-AI LOCAL SANDBOX MODE INITIALIZED"
    echo -e " 📍 Listening locally on target port: http://127.0.0.1:5000"
    echo -e " ⚠️ Close this shell workspace window to stop execution runtime."
    echo -e "${BLUE}================================================================${NC}"
    
    # Run synchronously on local machine so developers can see debugging traces live
    python main.py --nonserver
fi
