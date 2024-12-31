# 🛡️ CrowdStrike but free → AI EDR with a web dashboard you can chat with

[![GitHub stars](https://img.shields.io/github/stars/yourusername/endpoint-security-ai-agent?style=flat-square)](https://github.com/yourusername/endpoint-security-ai-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)

> **Open-source AI EDR that detects and stops ransomware, Cobalt Strike, and living-off-the-land attacks in real time — with a beautiful web dashboard and ChatGPT-style AI analyst you can talk to.**

![Demo](assets/demo.gif)

## 🚀 Features

- **🎯 Real-time Threat Detection**
  - ML-powered ransomware, C2 beaconing, and LOLBAS detection
  - Lightweight heuristic models (no heavy dependencies)
  - Sub-second detection latency

- **⚡ Autonomous Response**
  - Auto-kill malicious processes
  - Quarantine infected files
  - Isolate compromised hosts
  - Customizable playbooks

- **🎨 Stunning Web Dashboard**
  - Next.js 15 + TypeScript + Tailwind CSS
  - Dark hacker theme, fully responsive
  - Real-time WebSocket updates
  - 6 killer pages (Live Dashboard, AI Chat, Timeline, Endpoints, Hunting, Settings)

- **🤖 ChatGPT-style AI Analyst**
  - Ask natural language questions about security events
  - Get AI-powered incident analysis
  - Threat intelligence integration
  - MITRE ATT&CK mapping

- **🔧 Cross-platform**
  - Windows, macOS, Linux support
  - Docker + Docker Compose for easy deployment
  - Zero external dependencies (SQLite/DuckDB)

- **📊 Enterprise-ready**
  - FastAPI backend with async/await
  - Multi-agent CrewAI system
  - Real-time telemetry via osquery
  - Production-grade logging

## ⚡ Quick Start

### One-liner install & run:

```bash
git clone https://github.com/yourusername/endpoint-security-ai-agent.git && \
cd endpoint-security-ai-agent && \
docker compose up --build
```

Then open **http://localhost:3000** and watch live attacks being detected and stopped.

### Manual setup:

```bash
# Backend
pip install -r requirements.txt
python -m app.main

# Frontend (in another terminal)
cd dashboard
npm install
npm run dev
```

## 📖 Documentation

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Dashboard (Next.js)                  │
│  Live Dashboard │ AI Chat │ Timeline │ Endpoints │ Hunting  │
└────────────────────────┬────────────────────────────────────┘
                         │ WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CrewAI Multi-Agent System                           │   │
│  │  ├─ Detection Agent (ML models)                      │   │
│  │  ├─ Investigation Agent (Threat analysis)            │   │
│  │  └─ Response Agent (Auto-remediation)                │   │
│  └──────────────────────────────────────────────────────┘   │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Telemetry Collection (osquery)                      │   │
│  │  ├─ Process monitoring                               │   │
│  │  ├─ File operations                                  │   │
│  │  ├─ Network connections                              │   │
│  │  └─ Registry changes (Windows)                       │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  SQLite/DuckDB Storage         │
        │  ├─ Detections                 │
        │  ├─ Events                     │
        │  └─ Endpoints                  │
        └────────────────────────────────┘
```

### Dashboard Pages

| Page | Purpose |
|------|---------|
| **Live Dashboard** | Real-time alerts, threat stats, system health |
| **AI Analyst Chat** | Ask questions about security events |
| **Incident Timeline** | Visual timeline of all detections |
| **Endpoints** | Manage & monitor connected endpoints |
| **Threat Hunting** | Search & investigate security events |
| **Settings** | Configure thresholds & playbooks |

### AI Detection Models

- **Ransomware Detector**: Flags encrypted extensions, high entropy, rapid file changes
- **Beaconing Detector**: Identifies C2 patterns (interval, jitter, reputation)
- **LOLBAS Detector**: Detects abuse of PowerShell, cmd, wmic, rundll32, etc.

## 🎮 Demo

### Run the attack simulator:

```bash
python scripts/simulate_attacks.py
```

This will generate realistic security events every 5-15 seconds. Watch the dashboard update in real-time!

### Atomic Red Team integration (coming soon):

```bash
# Simulate ransomware attack
docker exec edr-agent python -m app.demo.atomic_red_team ransomware

# Simulate C2 beaconing
docker exec edr-agent python -m app.demo.atomic_red_team c2
```

## 🔌 API

### Create a detection:

```bash
curl -X POST http://localhost:8000/api/v1/detections \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ransomware detected",
    "description": "Files encrypted with .locked extension",
    "severity": "critical",
    "source": "ransomware_model",
    "endpoint_id": "workstation-01",
    "confidence": 0.95,
    "tags": ["ransomware", "encryption"],
    "raw_data": {}
  }'
```

### Chat with AI analyst:

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What ransomware attacks happened today?",
    "conversation_id": "default"
  }'
```

Full API docs: **http://localhost:8000/api/docs**

## 🛠️ Configuration

Create a `.env` file (copy from `.env.example`):

```env
# Backend
DEBUG=True
PORT=8000

# Database
DATABASE_URL=sqlite:///./data/edr.db

# AI (optional)
OPENAI_API_KEY=your-key-here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## 📦 Requirements

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, osquery
- **Frontend**: Node.js 18+, Next.js 15, React 18, Tailwind CSS
- **Docker**: Docker 20.10+, Docker Compose 2.0+

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development setup:

```bash
# Clone & install
git clone https://github.com/yourusername/endpoint-security-ai-agent.git
cd endpoint-security-ai-agent

# Backend
pip install -r requirements.txt
python -m pytest

# Frontend
cd dashboard
npm install
npm run lint
```

## 📄 License

MIT License 2025 Endpoint Security AI Agent Contributors

See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework for production
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful React components
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [osquery](https://osquery.io/) - SQL-powered endpoint visibility
- [CrewAI](https://crewai.com/) - Multi-agent AI framework

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/endpoint-security-ai-agent&type=Date)](https://star-history.com/#yourusername/endpoint-security-ai-agent&Date)

---

**Made with ❤️ for the security community. If you find this useful, please star ⭐ and share!**
