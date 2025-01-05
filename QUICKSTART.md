# Quick Start Guide

## 🚀 One-Command Setup

```bash
git clone https://github.com/yourusername/endpoint-security-ai-agent.git
cd endpoint-security-ai-agent
docker compose up --build
```

Then open **http://localhost:3000** in your browser.

## 📋 Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.10+, Node.js 18+

## 🐳 Docker Setup (Recommended)

```bash
# Start all services
docker compose up --build

# In another terminal, run attack simulator
python scripts/simulate_attacks.py
```

Services will be available at:
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## 🛠️ Manual Setup

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run backend
python -m app.main
```

Backend will be available at http://localhost:8000

### Frontend (in another terminal)

```bash
cd dashboard

# Install dependencies
npm install

# Run development server
npm run dev
```

Dashboard will be available at http://localhost:3000

### Run Attack Simulator

```bash
python scripts/simulate_attacks.py
```

## 🎯 First Steps

1. **Open Dashboard**: http://localhost:3000
2. **View Live Alerts**: Check the Live Dashboard page for real-time detections
3. **Chat with AI**: Go to "AI Analyst Chat" and ask questions about threats
4. **Explore Timeline**: View the Incident Timeline for all detected events
5. **Manage Endpoints**: See connected endpoints and their threat status

## 🔧 Configuration

Edit `.env` to customize:

```env
# Backend
DEBUG=True
PORT=8000

# Database
DATABASE_URL=sqlite:///./data/edr.db

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## 📚 API Examples

### Create a Detection

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
    "tags": ["ransomware"],
    "raw_data": {}
  }'
```

### Chat with AI

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What threats were detected today?",
    "conversation_id": "default"
  }'
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change ports in docker-compose.yml or .env
# Or kill existing processes:
lsof -i :8000  # Find process on port 8000
kill -9 <PID>
```

### Database Errors

```bash
# Reset database
rm -rf data/
docker compose up --build
```

### Frontend Won't Connect

- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env`
- Clear browser cache and refresh

## 📖 Documentation

- [README.md](README.md) - Full project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [API Docs](http://localhost:8000/api/docs) - Interactive API documentation

## 🆘 Need Help?

- Check logs: `docker compose logs -f`
- Open an issue on GitHub
- Review the [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
