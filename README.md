# User Authentication With Email
This documentation outlines the API endpoints used for user authentication through email verification. The primary functionality includes sending a confirmation code to the user's email to verify their identity. Below are the details for each endpoint, including request and response formats.

# Request Body:

```python
POST /api/send-confirmation-code
Content-Type: application/json

{
    "email": "user@example.com"
}
```

# Response Body:
## Successful Response:
```python
{
    "status": 200
    "message": "User registered successfully"
}
```
### Failure Response:
```python
{
    "error": "Invalid confirmation code"
}
```