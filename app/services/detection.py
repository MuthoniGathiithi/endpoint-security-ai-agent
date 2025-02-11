from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, String
from sqlalchemy.orm import selectinload

from ..models.detection import Detection, DetectionStatus, DetectionEvent

class DetectionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_detection(
        self,
        title: str,
        description: str,
        severity: str,
        source: str,
        raw_data: Dict[str, Any],
        endpoint_id: Optional[str] = None,
        confidence: float = 0.8,
        tags: Optional[List[str]] = None
    ) -> Detection:
        """Create a new detection with an initial status event"""
        detection = Detection(
            title=title,
            description=description,
            severity=severity,
            source=source,
            raw_data=raw_data,
            endpoint_id=endpoint_id,
            confidence=confidence,
            tags=tags or []
        )
        
        # Create initial status event
        event = DetectionEvent(
            event_type="status_change",
            description=f"Detection created with status: {DetectionStatus.NEW}",
            metadata={"status": DetectionStatus.NEW}
        )
        detection.events.append(event)
        
        self.db.add(detection)
        await self.db.commit()
        await self.db.refresh(detection)
        return detection

    async def get_detection(self, detection_id: int) -> Optional[Detection]:
        """Get a single detection by ID with its events"""
        result = await self.db.execute(
            select(Detection)
            .where(Detection.id == detection_id)
            .options(selectinload(Detection.events))
        )
        return result.scalars().first()

    async def list_detections(
        self,
        limit: int = 100,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        source: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[Detection]:
        """List detections with optional filtering"""
        query = select(Detection).order_by(Detection.created_at.desc())
        
        if status:
            query = query.where(Detection.status == status)
        if severity:
            query = query.where(Detection.severity == severity)
        if source:
            query = query.where(Detection.source == source)
        if days:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.where(Detection.created_at >= cutoff_date)
            
        query = query.limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_status(
        self,
        detection_id: int,
        status: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Detection]:
        """Update detection status and create an event"""
        detection = await self.get_detection(detection_id)
        if not detection:
            return None
            
        old_status = detection.status
        detection.status = status
        
        event = DetectionEvent(
            event_type="status_change",
            description=description,
            metadata={
                "old_status": old_status,
                "new_status": status,
                **(metadata or {})
            }
        )
        detection.events.append(event)
        
        await self.db.commit()
        await self.db.refresh(detection)
        return detection

    async def add_comment(
        self,
        detection_id: int,
        comment: str,
        user: str = "system"
    ) -> Optional[Detection]:
        """Add a comment to a detection"""
        detection = await self.get_detection(detection_id)
        if not detection:
            return None
            
        event = DetectionEvent(
            event_type="comment",
            description=comment,
            metadata={"user": user}
        )
        detection.events.append(event)
        
        await self.db.commit()
        await self.db.refresh(detection)
        return detection

    async def search_detections(
        self,
        query: str,
        limit: int = 50
    ) -> List[Detection]:
        """Search detections by title, description, or tags"""
        search = f"%{query}%"
        result = await self.db.execute(
            select(Detection)
            .where(
                or_(
                    Detection.title.ilike(search),
                    Detection.description.ilike(search),
                    Detection.tags.cast(String).ilike(search)
                )
            )
            .order_by(Detection.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
