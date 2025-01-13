#!/bin/bash
set -e

echo "🔨 Building Endpoint Security AI Agent for Render..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Build frontend
echo "🎨 Building Next.js dashboard..."
cd dashboard
npm install
npm run build
cd ..

echo "✅ Build complete!"
