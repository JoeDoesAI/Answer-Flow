from fastapi import Request
from core.logging_config import logger
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        client_ip = request.client.host
        method = request.method
        url = request.url.path

        logger.info(f"Request: {method} {url} from {client_ip}")

        # Process the request
        response = await call_next(request)

        # Log response details
        status_code = response.status_code
        logger.info(f"Response: {method} {url} returned {status_code} to {client_ip}")

        return response