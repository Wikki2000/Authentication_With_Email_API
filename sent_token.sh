#!/bin/bash
# Test /sent-confirmation-code endpoint

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <name> <email>"
    exit 1
fi

NAME=$1
EMAIL=$2

curl -X POST http://127.0.0.1:5000/api/auth/sent-confirmation-token -H "Content-Type: application/json" -d "{\"name\": \"$NAME\", \"email\": \"$EMAIL\"}"
