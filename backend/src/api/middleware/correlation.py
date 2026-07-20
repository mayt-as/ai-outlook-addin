import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from core.logging import correlation_id

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        token = correlation_id.set(req_id)
        
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = req_id
        
        correlation_id.reset(token)
        return response
