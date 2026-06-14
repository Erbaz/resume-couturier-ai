from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from utils.global_request_manager import global_request_manager

async def global_rate_limit_middleware(request: Request, call_next):
    """
    ASGI middleware that increments global request counters and blocks
    all requests if any limit (minute, daily requests, daily budget) is exceeded.
    """
    try:
        print("[GLOBAL_LIMIT] Starting to check global limits...", flush=True)
        should_block = global_request_manager.increment_global_request()
        
        if should_block:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too Many Requests. Service limit constraints exceeded."},
                headers={"Retry-After": "3600"}
            )
        print("[GLOBAL_LIMIT] Limits not exceeded, continuing...", flush=True)

        response = await call_next(request)
        return response
    except Exception as e:
        print(f"[GLOBAL_LIMIT] Error while checking limits: {e}", flush=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."}
        )
