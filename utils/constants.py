class ResponseDataKey:
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"
    ACCESS_TOKEN_EXPIRES = "at_expires"
    REFRESH_TOKEN_EXPIRES = "rt_expires"
    DATA_KEY = "data"
    ERROR_KEY = "error"
    MESSAGE_KEY = "message"
    ERROR_KEY = "error"
    USER_ID = "user_id"


class ResponseMessage:
    SUCCESSFULL_ACCOUNT_CREATED = "Your account was created successfully"
    ACCOUNT_SIGNIN_SUCCESS = "Signing in successfully"
    ERROR_EMAIL_AND_PASS_REQUIRED_MESSAGE = "Email and password are required."
    INVALID_EMAIL_AND_PASS_MESSAGE = "Invalid email or password"
    USER_ACCOUNT_DISABLED_MESSAGE = "Your account is disabled"
