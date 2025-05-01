class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""

    detail = "User not found."


class UserNotCorrectPasswordException(Exception):
    """Exception raised when the password provided is incorrect."""

    detail = "Password is not correct."


class TokenExpired(Exception):
    detail = "Token has expired"


class TokenNotCorrect(Exception):
    detail = "Token is not correct or expired"


class TaskNotFound(Exception):
    """Exception raised when a task is not found in the database."""

    detail = "Task not found."
