from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class DetectionStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class DetectionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DetectionBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    status: DetectionStatus = DetectionStatus.NEW
    severity: DetectionSeverity = DetectionSeverity.MEDIUM
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    source: str = Field(..., max_length=100)
    endpoint_id: Optional[str] = Field(None, max_length=100)
    tags: List[str] = Field(default_factory=list)

class DetectionCreate(DetectionBase):
    raw_data: Dict[str, Any]

class DetectionUpdate(BaseModel):
    status: Optional[DetectionStatus] = None
    severity: Optional[DetectionSeverity] = None
    tags: Optional[List[str]] = None

class DetectionInDBBase(DetectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    raw_data: Dict[str, Any]

    class Config:
        orm_mode = True

class Detection(DetectionInDBBase):
    pass

class DetectionEventType(str, Enum):
    STATUS_CHANGE = "status_change"
    COMMENT = "comment"
    INVESTIGATION = "investigation"
    REMEDIATION = "remediation"

class DetectionEventBase(BaseModel):
    event_type: DetectionEventType
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DetectionEventCreate(DetectionEventBase):
    pass

class DetectionEventInDB(DetectionEventBase):
    id: int
    detection_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DetectionWithEvents(DetectionInDBBase):
    events: List[DetectionEventInDB] = []

class DetectionStats(BaseModel):
    total: int = 0
    by_status: Dict[str, int] = Field(default_factory=dict)
    by_severity: Dict[str, int] = Field(default_factory=dict)
    by_source: Dict[str, int] = Field(default_factory=dict)
    recent: List[Detection] = Field(default_factory=list)

class DetectionSearchResults(BaseModel):
    results: List[Detection]
    total: int
    page: int
    page_size: int
