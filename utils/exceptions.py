from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class BadRequestException(AppException):
    def __init__(self, detail: str = "Invalid request"):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail,
        )


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail,
        )


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"{resource} not found",
        )


class ConflictException(AppException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status.HTTP_409_CONFLICT,
            detail,
        )