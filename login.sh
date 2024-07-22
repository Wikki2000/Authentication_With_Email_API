#!/bin/bash
# Test /login endpoint

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <email> <password>"
    exit 1
fi

EMAIL=$1
PASSWORD=$2

curl -X POST http://127.0.0.1:5000/api/auth/login -H "Content-Type: application/json" -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}"
