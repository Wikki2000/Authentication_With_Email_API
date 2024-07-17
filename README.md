# User Authentication With Email
This documentation outlines the API endpoints used for user authentication through email verification. The primary functionality includes sending a confirmation code to the user's email to verify their identity. Below are the details for each endpoint, including request and response formats.

# [POST] /api/send-confirmation-code
## Request Body:

```python
POST /api/send-confirmation-code
Content-Type: application/json
{
    "email": "user@example.com"
}
```

## Response Body:
### Successful Response:
```python
{
    "status": "success",
    "message": "Confirmation code sent to email",
    "status_code": 200
}
```
### Failure Response:
##### Missing Fields:
```python
{
    "status": "Bad Request",
    "message": "{fields} required",
    "status_code": 422
}
```

#### Invalid email:
```python
{
    "status": "Bad Request",
    "message": "Wrong email address",
    "status_code": 422
}
```

#### Empty request body:
```python
{
    "status": "Bad Request",
    "message": "Empty request body",
    "status_code": 400
}
```