from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DetectionResult(BaseModel):
    """Represents the result of a detection operation."""
    detection_id: str
    timestamp: datetime
    threat_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    confidence: float  # 0.0 to 1.0
    description: str
    source: str
    raw_data: Dict[str, Any]
    metadata: Dict[str, Any] = {}
    is_false_positive: bool = False

class ResponseAction(BaseModel):
    """Represents an action to be taken in response to a detection."""
    action_type: str  # 'kill_process', 'quarantine_file', 'isolate_host', 'alert'
    target: str
    parameters: Dict[str, Any] = {}
    requires_confirmation: bool = True

class BaseAgent(ABC):
    """Base class for all security agents in the system."""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.is_running = False
        self.last_activity = None
        self._initialize_agent()
    
    def _initialize_agent(self) -> None:
        """Initialize the agent's resources."""
        logger.info(f"Initializing agent: {self.name} ({self.agent_id})")
        self.on_initialize()
    
    @abstractmethod
    def on_initialize(self) -> None:
        """Called when the agent is being initialized."""
        pass
    
    @abstractmethod
    async def start(self) -> None:
        """Start the agent's main processing loop."""
        self.is_running = True
        self.last_activity = datetime.utcnow()
        logger.info(f"Started agent: {self.name}")
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the agent's processing."""
        self.is_running = False
        logger.info(f"Stopped agent: {self.name}")
    
    @abstractmethod
    async def detect(self, data: Any) -> List[DetectionResult]:
        """
        Perform detection on the provided data.
        
        Args:
            data: The data to analyze for potential threats.
            
        Returns:
            A list of detection results.
        """
        pass
    
    async def respond(self, detection: DetectionResult) -> List[ResponseAction]:
        """
        Generate response actions for a given detection.
        
        Args:
            detection: The detection to respond to.
            
        Returns:
            A list of response actions.
        """
        self.last_activity = datetime.utcnow()
        return await self.generate_response_actions(detection)
    
    @abstractmethod
    async def generate_response_actions(self, detection: DetectionResult) -> List[ResponseAction]:
        """
        Generate appropriate response actions for a detection.
        
        Args:
            detection: The detection to generate responses for.
            
        Returns:
            A list of response actions.
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the agent's state to a dictionary."""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'description': self.description,
            'is_running': self.is_running,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }
    
    def __str__(self) -> str:
        return f"{self.name} ({self.agent_id})"

class AgentRegistry:
    """Manages the registration and retrieval of agent instances."""
    
    _instance = None
    _agents: Dict[str, BaseAgent] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, agent: BaseAgent) -> None:
        """Register a new agent."""
        if agent.agent_id in cls._agents:
            raise ValueError(f"Agent with ID {agent.agent_id} is already registered.")
        cls._agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent}")
    
    @classmethod
    def get_agent(cls, agent_id: str) -> Optional[BaseAgent]:
        """Retrieve an agent by its ID."""
        return cls._agents.get(agent_id)
    
    @classmethod
    def list_agents(cls) -> List[Dict[str, Any]]:
        """List all registered agents."""
        return [agent.to_dict() for agent in cls._agents.values()]
    
    @classmethod
    async def start_all(cls) -> None:
        """Start all registered agents."""
        for agent in cls._agents.values():
            if not agent.is_running:
                await agent.start()
    
    @classmethod
    async def stop_all(cls) -> None:
        """Stop all registered agents."""
        for agent in cls._agents.values():
            if agent.is_running:
                await agent.stop()
