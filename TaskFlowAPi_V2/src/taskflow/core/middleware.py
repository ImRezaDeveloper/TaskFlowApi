import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.taskflow.core.loggin import logger

# logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start = time.perf_counter()

        logger.info(
            "http_request_started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "http_request_finished",
            method= request.method,
            path= request.url.path,
            status_code= response.status_code,
            duration_ms= round(duration_ms, 2),
        )

        return response