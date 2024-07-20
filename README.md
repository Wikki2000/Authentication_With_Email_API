# User Authentication With Email
This documentation outlines the API endpoints used for user authentication through email verification. The process begins when the user submits their email address. A 6-digit confirmation code is sent to the provided email address to verify ownership. Once the email is verified, the user can complete their registration and then log in.

# [POST] /api/auth/send-confirmation-code
The primary functionality includes sending a confirmation code to the user's email to verify their identity. Below are the details for each endpoint, including request and response formats.
## Request Body:

```python
[POST] /api/send-confirmation-code
Content-Type: application/json
{
    "name": "Josh Bush",
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

#### Empty request body:
```python
{
    "status": "Bad Request",
    "message": "Empty request body",
    "status_code": 400
}
```

# [POST] /api/auth/register