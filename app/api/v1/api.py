from fastapi import APIRouter

from .endpoints import detections, chat

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(detections.router, prefix="/detections", tags=["detections"])
api_router.include_router(chat.router, prefix="/ai", tags=["ai"])

# Health check endpoint
@api_router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "services": ["api", "database", "ai"]
    }
