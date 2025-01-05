#!/usr/bin/env python3
"""
Simulate security events for demo purposes.

This script generates realistic-looking security detections to demonstrate
the EDR system's detection and response capabilities.
"""

import asyncio
import random
from datetime import datetime
import httpx

API_URL = "http://localhost:8000/api/v1"

THREAT_SCENARIOS = [
    {
        "title": "Ransomware Encryption Detected",
        "description": "Multiple files encrypted with .locked extension in C:\\Users\\Documents",
        "severity": "critical",
        "tags": ["ransomware", "encryption", "impact"],
        "source": "ransomware_model",
    },
    {
        "title": "C2 Beaconing Activity",
        "description": "Suspicious outbound connections to 203.0.113.42:443 with 60s interval",
        "severity": "high",
        "tags": ["c2", "beaconing", "command-and-control"],
        "source": "beaconing_model",
    },
    {
        "title": "Suspicious PowerShell Execution",
        "description": "PowerShell with encoded command line and network operations detected",
        "severity": "high",
        "tags": ["lolbas", "powershell", "execution"],
        "source": "lolbas_model",
    },
    {
        "title": "Process Injection Attempt",
        "description": "svchost.exe attempted to inject code into explorer.exe",
        "severity": "high",
        "tags": ["injection", "defense_evasion"],
        "source": "behavioral_model",
    },
    {
        "title": "Unusual Scheduled Task",
        "description": "New scheduled task created by non-admin user: WindowsUpdate",
        "severity": "medium",
        "tags": ["persistence", "scheduled_task"],
        "source": "behavioral_model",
    },
]

ENDPOINTS = [
    "workstation-01",
    "workstation-02",
    "server-03",
    "laptop-07",
    "desktop-05",
]


async def simulate_attack():
    """Simulate a single attack event."""
    async with httpx.AsyncClient() as client:
        threat = random.choice(THREAT_SCENARIOS)
        endpoint = random.choice(ENDPOINTS)

        payload = {
            "title": threat["title"],
            "description": threat["description"],
            "severity": threat["severity"],
            "source": threat["source"],
            "endpoint_id": endpoint,
            "confidence": random.uniform(0.7, 0.99),
            "tags": threat["tags"],
            "raw_data": {
                "timestamp": datetime.utcnow().isoformat(),
                "endpoint": endpoint,
                "scenario": threat["title"],
            },
        }

        try:
            response = await client.post(f"{API_URL}/detections", json=payload)
            if response.status_code == 200:
                print(f"✓ Created detection: {threat['title']} on {endpoint}")
            else:
                print(f"✗ Failed to create detection: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {e}")


async def main():
    """Run continuous attack simulation."""
    print("🎯 Starting attack simulation...")
    print(f"📍 API URL: {API_URL}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            await simulate_attack()
            # Simulate attacks every 5-15 seconds
            await asyncio.sleep(random.uniform(5, 15))
    except KeyboardInterrupt:
        print("\n\n🛑 Simulation stopped")


if __name__ == "__main__":
    asyncio.run(main())
