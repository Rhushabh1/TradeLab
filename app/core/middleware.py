import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger


class RequestMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		# log each request in this middleware & track latency too
		request_id = str(uuid.uuid4())[:8]
		start = time.perf_counter()
		response = await call_next(request)
		elapsed = round((time.perf_counter() - start)*1000,
						2)
		logger.info("request",
					request_id = request_id,
					method = request.method,
					path = request.url.path,
					status = response.status_code,
					latency_ms = elapsed)
		response.headers["X-Request-ID"] = request_id
		return response
