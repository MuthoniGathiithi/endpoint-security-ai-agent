from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from typing import List, Optional
from datetime import datetime, timedelta
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ....db.session import get_db
from ....models.detection import Detection, DetectionEvent, DetectionStatus, DetectionSeverity
from ....schemas.detection import (
    DetectionCreate, DetectionUpdate, DetectionWithEvents,
    DetectionStats, DetectionSearchResults, DetectionEvent as DetectionEventSchema
)
from ....schemas.detection import Detection as DetectionSchema
from ....services.detection import DetectionService
from ....websocket.manager import ConnectionManager

router = APIRouter()
ws_manager = ConnectionManager()

@router.post("/", response_model=DetectionSchema)
async def create_detection(
    detection: DetectionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new detection"""
    service = DetectionService(db)
    return await service.create_detection(
        title=detection.title,
        description=detection.description,
        severity=detection.severity,
        source=detection.source,
        raw_data=detection.raw_data,
        endpoint_id=detection.endpoint_id,
        confidence=detection.confidence,
        tags=detection.tags
    )

@router.get("/{detection_id}", response_model=DetectionWithEvents)
async def get_detection(
    detection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific detection by ID"""
    service = DetectionService(db)
    detection = await service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection

@router.get("/", response_model=List[DetectionSchema])
async def list_detections(
    skip: int = 0,
    limit: int = 100,
    status: Optional[DetectionStatus] = None,
    severity: Optional[DetectionSeverity] = None,
    source: Optional[str] = None,
    days: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List detections with optional filtering"""
    service = DetectionService(db)
    return await service.list_detections(
        skip=skip,
        limit=limit,
        status=status,
        severity=severity,
        source=source,
        days=days
    )

@router.patch("/{detection_id}", response_model=DetectionSchema)
async def update_detection(
    detection_id: int,
    detection_update: DetectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a detection"""
    service = DetectionService(db)
    detection = await service.get_detection(detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    update_data = detection_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(detection, field, value)
    
    await db.commit()
    await db.refresh(detection)
    
    # Notify WebSocket subscribers
    await ws_manager.publish_alert({
        "type": "detection_updated",
        "detection_id": detection.id,
        "status": detection.status,
        "updated_at": datetime.utcnow().isoformat()
    })
    
    return detection

@router.post("/{detection_id}/events", response_model=DetectionEventSchema)
async def add_detection_event(
    detection_id: int,
    event: DetectionEventSchema,
    db: AsyncSession = Depends(get_db)
):
    """Add an event to a detection"""
    detection = await db.get(Detection, detection_id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    db_event = DetectionEvent(
        detection_id=detection_id,
        event_type=event.event_type,
        description=event.description,
        metadata=event.metadata or {}
    )
    
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    # Notify WebSocket subscribers
    await ws_manager.publish_alert({
        "type": "detection_event_added",
        "detection_id": detection_id,
        "event_id": db_event.id,
        "event_type": db_event.event_type,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return db_event

@router.get("/stats/summary", response_model=DetectionStats)
async def get_detection_stats(
    days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    """Get detection statistics"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Get total count
    result = await db.execute(select(Detection))
    total = len(result.scalars().all())
    
    # Get counts by status
    status_result = await db.execute(
        select(Detection.status, func.count(Detection.id))
        .where(Detection.created_at >= cutoff_date)
        .group_by(Detection.status)
    )
    by_status = {status: count for status, count in status_result.all()}
    
    # Get counts by severity
    severity_result = await db.execute(
        select(Detection.severity, func.count(Detection.id))
        .where(Detection.created_at >= cutoff_date)
        .group_by(Detection.severity)
    )
    by_severity = {severity: count for severity, count in severity_result.all()}
    
    # Get counts by source
    source_result = await db.execute(
        select(Detection.source, func.count(Detection.id))
        .where(Detection.created_at >= cutoff_date)
        .group_by(Detection.source)
        .order_by(func.count(Detection.id).desc())
        .limit(10)
    )
    by_source = {source: count for source, count in source_result.all()}
    
    # Get recent detections
    recent_result = await db.execute(
        select(Detection)
        .order_by(Detection.created_at.desc())
        .limit(5)
    )
    recent = recent_result.scalars().all()
    
    return DetectionStats(
        total=total,
        by_status=by_status,
        by_severity=by_severity,
        by_source=by_source,
        recent=recent
    )

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: AsyncSession = Depends(get_db)):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message.get("action") == "subscribe":
                    channel = message.get("channel", "alerts")
                    await ws_manager.subscribe(client_id, channel)
                    
                    # Send initial data if needed
                    if channel == "detections":
                        service = DetectionService(db)
                        detections = await service.list_detections(limit=10)
                        await ws_manager.send_personal_message({
                            "type": "initial_detections",
                            "data": [
                                {"id": d.id, "title": d.title, "status": d.status, "severity": d.severity}
                                for d in detections
                            ]
                        }, client_id)
                
            except json.JSONDecodeError:
                await ws_manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON"
                }, client_id)
                
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
    except Exception as e:
        await ws_manager.send_personal_message({
            "type": "error",
            "message": str(e)
        }, client_id)
        ws_manager.disconnect(client_id)
