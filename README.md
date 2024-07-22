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
### Successful Response (200):
```json
{
    "status": "success",
    "message": "Confirmation code sent to email",
    "token": "12345",
}
```

### Failure Response:
##### Missing Fields (400):
```json
{
    "status": "Bad Request",
    "message": "{fields} required",
}
```

#### Empty request body (400):
```json
{
    "status": "Bad Request",
    "message": "Empty request body",
}
```


# [POST] /api/auth/register
The primary functionality of this endpoint includes registering a new user after verifying their email with a token. Below are the details for the request and response formats:
## Request Body:
```python
[POST] /api/auth/send-confirmation-code
Content-Type: application/json
{
    "first_name": "Josh",
    "last_name": "Bush",
    "email": "user@example.com",
    "password": "password12345",
    "token": "12345"
}
```

## Response Body:
### Successful Response (200):
```json
{
    "status": "Success",
    "message": "Registration successfully",
    "data": {
        "id": "21wrdtu65etf5ww3",
        "first_name": "John",
        "last_name": "Bush",
        "email": "user@example.com",
        "password": "password12345"
    }
}
```

### Failure Response:
##### Missing Fields (400):
```json
{
    "status": "Bad Request",
    "message": "{fields} required",
}
```
##### Empty request body (400):
```json
{
    "status": "Bad Request",
    "message": "Request body is empty"
}
```

##### Invalid token (400):
```json
{
    "status": "Validation Error",
    "message": "Invalid or expired token"
}
```

##### Registration Existing user (422):
```json
{
    "status": "Validation Error",
    "message": "Email is already registered"
}
```

# [POST] /api/auth/login
The primary functionality of this endpoint includes authenticating a user by verifying their credentials. Below are the details for the request and response formats:
## Request Body:
```python
[POST] /api/auth/login
Content-Type: application/json
  {
    "email": "user@example.com",
    "password": "password12345"
  }
  ```

  ## Response Body:
### Successful Response (200):
```json
{
  "message": "Login successful",
  "access_token": "jwt_token",
  "user": {
    "id": "user_id",
    "first_name": "John",
    "last_name": "Bush",
    "email": "user@example.com",

  }
}
```

### Failure Response:
##### Empty request body (400):
```json
{
    "status": "Bad Request",
    "message": "Request body is empty"
}
```

##### Missing Fields (400):
```json
{
    "status": "Bad Request",
    "message": "Request body is empty"
}
```

##### Invalid login credentials (401):
```json
{
    "status": "Unauthorized Access",
    "message": "Invalid email or password"
}
```

This documentation provides a clear overview of the API endpoints for user authentication, including the necessary request and response formats for sending a confirmation code, registering a new user, and logging in.

# Contribution
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

# Contact
For any inquiries or support, please contact via [Email](mailto:wisdomokposin@gmail.com) or [LinkedIn](https://www.linkedin.com/in/wisdom-okposin).
