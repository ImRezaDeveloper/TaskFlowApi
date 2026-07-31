import time
import logging
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.taskflow.core.loggin import logger

# logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start = time.perf_counter()

        request_id = str(uuid.uuid4())

        request_logger = logger.bind(
            request_id = request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

        user = getattr(request.state, "user", None)
        if user and getattr(user, "is_authenticated", False):
            request_logger = request_logger.bind(user_id=str(user.id))
        
        request.state.logger = request_logger
        request.state.request_id = request_id

        request_logger.info("http_request_started")

        response = await call_next(request)
        
        duration_ms = (time.perf_counter() - start) * 1000

        request_logger.info(
            "http_request_finished",
            method= request.method,
            path= request.url.path,
            status_code= response.status_code,
            duration_ms= round(duration_ms, 2),
        )

        return response