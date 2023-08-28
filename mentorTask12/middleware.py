from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time
from fastapi import Request

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        st=time.time()
        response = await call_next(request)
        response.headers['time'] = str(time.time()-st)
        print(response.headers)
        return response





