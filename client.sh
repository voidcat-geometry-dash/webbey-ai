#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Terminal visual helpers
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Display clean usage instructions if wrong flags are entered
show_usage() {
    echo -e "${RED}Error: Missing or invalid parameter choice.${NC}"
    echo -e "Usage examples:"
    echo -e "  ${GREEN}./client.sh --server${NC}     -> Launches python3 main.py --server"
    echo -e "  ${BLUE}./client.sh --noserver${NC}   -> Launches python3 main.py --noserver"
    exit 1
}

# Require exactly one parameter
if [ $# -ne 1 ]; then
    show_usage
fi

# Route flag commands
case "$1" in
    --server)
        echo -e "${GREEN}[+] Client starting core system in Remote Server Mode...${NC}"
        echo -e "${GREEN}[+] Executing: python3 main.py --server${NC}\n"
        
        # Start in background using nohup to protect the VPS process from terminal logout
        nohup python3 main.py --server > server.log 2>&1 &
        
        echo -e "${GREEN}====================================================${NC}"
        echo -e " 🚀 Production Core is now running silently in background."
        echo -e " 📍 Listening on remote access interface port: 8080"
        echo -e " 📋 Track runtime details with command: tail -f server.log"
        echo -e "${GREEN}====================================================${NC}"
        ;;
        
    --noserver)
        echo -e "${BLUE}[+] Client starting core system in Local PC/Laptop Sandbox Mode...${NC}"
        echo -e "${BLUE}[+] Executing: python3 main.py --noserver${NC}\n"
        
        # Start synchronously inside the foreground shell for live terminal debugging updates
        python3 main.py --noserver
        ;;
        
    *)
        show_usage
        ;;
esac
