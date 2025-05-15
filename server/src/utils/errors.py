from typing import Any, Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class LaaiException(Exception):
    """This is the base class for all bookly errors"""

    pass

class InvalidToken(LaaiException):
    """User has provided an invalid or expired token"""

    pass

class RevokedToken(LaaiException):
    """User has provided a token that has been revoked"""

    pass

class AccessTokenRequired(LaaiException):
    """User has provided a refresh token when an access token is needed"""

    pass

class RefreshTokenRequired(LaaiException):
    """User has provided an access token when a refresh token is needed"""

    pass

class InvalidCredentials(LaaiException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(LaaiException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class UserAlreadyExistsError(LaaiException):
    """Raised when a user already exists in the database"""
    pass

class AccountNotVerified(Exception):
    """Account not yet verified"""
    pass

def create_exception_handler(status_code: int, detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    """
    Create an exception handler for a specific status code and detail.
    """
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": detail},
        )
    return exception_handler

def register_all_errors(app: FastAPI):
    """
    Register all error handlers with the FastAPI application.
    """
    app.add_exception_handler(
        UserAlreadyExistsError, 
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "User already exists.", 
                "error_code": "user_already_exists"
                },
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution":"Please check your email for verification details"
            },
        ),
    )