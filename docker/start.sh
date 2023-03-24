#!/bin/bash

cd /app

if [ $# -eq 0 ]; then
  echo "Usage: start.sh [PROCESS_TYPE](server)"
else
  PROCESS_TYPE=$1
fi

function start_server() {
  echo "Start server..."
  python app/cmd/chatbot.py
  # uvicorn app.main:app --reload --host 0.0.0.0 --port 18080
}

function main() {
  case "$PROCESS_TYPE" in
    "server")
      start_server
      ;;
    *)
      echo "Usage: start.sh [PROCESS_TYPE](server)"
      ;;
  esac
}

main
