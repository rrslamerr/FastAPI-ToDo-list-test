import logging
from time import perf_counter

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger("app.middleware")


async def log_requests(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


request_count = 0


async def request_number(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    response = await call_next(request)
    global request_count
    request_count += 1
    response.headers["x-request-number"] = str(request_count)
    return response
