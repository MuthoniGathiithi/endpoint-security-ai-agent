from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy.future import select

from .session import async_session
from app.models.detection import Detection, DetectionSeverity
from app.services.detection import DetectionService
from app.ml.models import ModelManager


async def init_db() -> None:
    """Seed the database with a small set of demo detections if empty.

    This is called once on startup from main.lifespan().
    """
    async with async_session() as db:
        result = await db.execute(select(Detection))
        if result.scalars().first():
            # Already seeded
            return

        service = DetectionService(db)
        models = ModelManager()

        # --- Ransomware-style detection ---
        rw_features = {
            "extension": ".locked",
            "suspicious_process": True,
            "high_entropy": True,
            "rapid_file_changes": True,
        }
        rw_res = models.predict_ransomware(rw_features)
        await service.create_detection(
            title="Ransomware encryption burst on workstation-01",
            description="Multiple user documents were renamed with .locked extension and modified in a short time window.",
            severity=DetectionSeverity.CRITICAL.value,
            source="ransomware_model",
            raw_data={"features": rw_features, "model_result": rw_res.__dict__},
            endpoint_id="workstation-01",
            confidence=rw_res.score,
            tags=["ransomware", "encryption", "impact"],
        )

        # --- Beaconing-style detection ---
        bc_features = {
            "interval_seconds": 60.0,
            "jitter": 0.05,
            "dest_reputation": 0.1,
            "suspicious_user_agent": True,
        }
        bc_res = models.predict_beaconing(bc_features)
        await service.create_detection(
            title="Possible C2 beaconing from server-03",
            description="Regular outbound connections to low-reputation host with minimal jitter; pattern resembles C2 beaconing.",
            severity=DetectionSeverity.HIGH.value,
            source="beaconing_model",
            raw_data={"features": bc_features, "model_result": bc_res.__dict__},
            endpoint_id="server-03",
            confidence=bc_res.score,
            tags=["c2", "beaconing", "command-and-control"],
        )

        # --- LOLBAS-style detection ---
        lb_features = {
            "binary_name": "powershell.exe",
            "uses_encoded_command": True,
            "network_ops": 3,
        }
        lb_res = models.predict_lolbas(lb_features)
        await service.create_detection(
            title="Suspicious PowerShell LOLBAS activity",
            description="PowerShell executed with encoded command line and outbound network activity, consistent with LOLBAS tradecraft.",
            severity=DetectionSeverity.HIGH.value,
            source="lolbas_model",
            raw_data={"features": lb_features, "model_result": lb_res.__dict__},
            endpoint_id="laptop-07",
            confidence=lb_res.score,
            tags=["lolbas", "powershell", "execution"],
        )

        # --- Benign baseline detection for contrast ---
        base_features = {
            "extension": ".docx",
            "suspicious_process": False,
            "high_entropy": False,
            "rapid_file_changes": False,
        }
        base_res = models.predict_ransomware(base_features)
        await service.create_detection(
            title="Unusual but benign activity",
            description="User performed a large document reorganisation; no strong ransomware or beaconing indicators detected.",
            severity=DetectionSeverity.LOW.value,
            source="heuristic_baseline",
            raw_data={"features": base_features, "model_result": base_res.__dict__},
            endpoint_id="workstation-02",
            confidence=base_res.score,
            tags=["benign", "baseline"],
        )

        await db.commit()
