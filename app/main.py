from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import asyncio
import uvicorn
import os
from pathlib import Path

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import get_db, engine
from app.db.init_db import init_db
from app.websocket.manager import ConnectionManager
from app.services.ai_analyst import AIAnalyst

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    logger.info("🚀 Starting Endpoint Security AI Agent")
    
    # Create database tables
    logger.info("🛢️  Initializing database...")
    async with engine.begin() as conn:
        # Import models package so all tables are registered
        from app.models import Base  # noqa: WPS433
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize database with sample data
    await init_db()
    
    # Initialize ML models and other resources
    await initialize_services()
    
    yield
    
    # Cleanup resources
    logger.info("🛑 Shutting down Endpoint Security AI Agent")

async def initialize_services():
    """Initialize all required services"""
    # Initialize ML models, threat intel, etc.
    logger.info("🤖 Initializing AI/ML models and services...")
    
    # Initialize AI Analyst
    try:
        ai_analyst = AIAnalyst()
        logger.info("✅ AI Analyst initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI Analyst: {str(e)}")
        raise
    
    # Initialize other services here
    logger.info("✅ All services initialized")

app = FastAPI(
    title="Endpoint Security AI Agent",
    description="Open-source AI EDR with real-time threat detection and response",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Mount static files (for the dashboard)
frontend_path = Path(__file__).parent.parent / "dashboard" / "out"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="dashboard")
else:
    logger.warning(f"Dashboard not found at {frontend_path}. Frontend will not be served.")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {"status": "ok", "version": "1.0.0"}

# API info endpoint
@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Endpoint Security AI Agent API",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "endpoints": [
            {"path": "/api/v1/detections", "methods": ["GET", "POST"], "description": "Manage security detections"},
            {"path": "/api/v1/ai/chat", "methods": ["POST"], "description": "Chat with AI analyst"},
            {"path": "/ws", "methods": ["WEBSOCKET"], "description": "WebSocket for real-time updates"}
        ]
    }

# WebSocket manager
websocket_manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for real-time communication with the dashboard"""
    await websocket_manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message.get("type") == "subscribe":
                    channel = message.get("channel", "alerts")
                    await websocket_manager.subscribe(client_id, channel)
                    
                    # Send initial data if needed
                    if channel == "detections":
                        from app.services.detection import DetectionService
                        service = DetectionService(db)
                        detections = await service.list_detections(limit=10)
                        await websocket_manager.send_personal_message({
                            "type": "initial_detections",
                            "data": [
                                {"id": d.id, "title": d.title, "status": d.status, "severity": d.severity}
                                for d in detections
                            ]
                        }, client_id)
                
            except json.JSONDecodeError:
                await websocket_manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON"
                }, client_id)
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": str(e)
        }, client_id)
        websocket_manager.disconnect(client_id)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Endpoint Security AI Agent",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
        workers=settings.WORKERS
    )
