from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
from app.routers import auth, scheduler, videos, stream, settings

# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI(
    title="reTwitch API",
    description="API for managing scheduled streams and live streaming.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(videos.router, prefix="/videos", tags=["Video Management"])
app.include_router(scheduler.router, prefix="/schedule", tags=["Schedule Management"])
app.include_router(stream.router, prefix="/stream", tags=["Streaming Control"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])
