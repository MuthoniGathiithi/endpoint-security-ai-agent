from typing import Dict, List
from fastapi import WebSocket
import json
from loguru import logger

class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"New WebSocket connection: {client_id}")
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            # Remove from all subscriptions
            for channel in self.subscriptions:
                if client_id in self.subscriptions[channel]:
                    self.subscriptions[channel].remove(client_id)
            logger.info(f"Disconnected WebSocket: {client_id}")
    
    async def send_personal_message(self, message: dict, client_id: str):
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)
    
    async def broadcast(self, message: dict, channel: str = "alerts"):
        """Send a message to all clients subscribed to a channel."""
        if channel not in self.subscriptions:
            return
            
        for client_id in list(self.subscriptions[channel]):
            await self.send_personal_message(message, client_id)
    
    async def subscribe(self, client_id: str, channel: str):
        """Subscribe a client to a channel."""
        if channel not in self.subscriptions:
            self.subscriptions[channel] = []
        if client_id not in self.subscriptions[channel]:
            self.subscriptions[channel].append(client_id)
            logger.info(f"Client {client_id} subscribed to {channel}")
    
    async def unsubscribe(self, client_id: str, channel: str):
        """Unsubscribe a client from a channel."""
        if channel in self.subscriptions and client_id in self.subscriptions[channel]:
            self.subscriptions[channel].remove(client_id)
            logger.info(f"Client {client_id} unsubscribed from {channel}")
    
    async def publish_alert(self, alert: dict):
        """Publish an alert to all subscribed clients."""
        await self.broadcast({
            "type": "alert",
            "data": alert
        }, channel="alerts")
