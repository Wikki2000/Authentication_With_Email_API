#!/bin/bash
# Test /registration endpoint

if [ "$#" -ne 5 ]; then
	echo "Usage: $0 <first_name> <last_name> <email> <password> <token>"
    exit 1
fi

FIRST_NAME=$1
LAST_NAME=$2
EMAIL=$3
PASSWORD=$4
TOKEN=$5

curl -X POST http://127.0.0.1:5000/api/auth/register -H "Content-Type: application/json" -d "{\"first_name\": \"$FIRST_NAME\", \"last_name\": \"$LAST_NAME\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"token\": \"$TOKEN\"}"
