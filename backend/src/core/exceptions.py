from fastapi import Request, status
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger(__name__)

class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 500, name: str = "InternalServerError"):
        self.message = message
        self.status_code = status_code
        self.name = name
        super().__init__(self.message)

class AIProviderException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=502, name="AIProviderError")

class GraphAPIException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=502, name="GraphAPIError")

class AuthenticationException(BaseAppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, name="AuthenticationError")

async def app_exception_handler(request: Request, exc: BaseAppException):
    logger.error("App exception occurred", error=exc.name, message=exc.message, path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.name, "message": exc.message}}
    )
