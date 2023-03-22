#!/bin/bash

cd /app

if [ $# -eq 0 ]; then
  echo "Usage: start.sh [PROCESS_TYPE](server)"
else
  PROCESS_TYPE=$1
fi

function start_server() {
  echo "Start api..."
  python app/cmd/main.py
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
