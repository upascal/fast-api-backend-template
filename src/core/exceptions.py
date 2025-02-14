from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs):
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class NotFoundException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not found"


class BadRequestException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad request"


class UnauthorizedException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Unauthorized"


class ForbiddenException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Forbidden"


class UnprocessableEntityException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = "Unprocessable entity"


# Auth exceptions
class AuthFailedException(UnauthorizedException):
    DETAIL = "Incorrect email or password"


class AuthTokenExpiredException(UnauthorizedException):
    DETAIL = "Token has expired"


class AuthTokenInvalidException(UnauthorizedException):
    DETAIL = "Token is invalid"


# User exceptions
class UserNotFoundException(NotFoundException):
    DETAIL = "User not found"


class UserAlreadyExistsException(BadRequestException):
    DETAIL = "User with this email already exists"
