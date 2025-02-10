from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import openai
import json
import logging
from datetime import datetime
from ..core.config import settings

logger = logging.getLogger(__name__)

class AIChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str

class AIAnalyst:
    def __init__(self):
        self.model = settings.AI_MODEL or "gpt-4"
        self.system_prompt = """
        You are a cybersecurity AI analyst for an EDR (Endpoint Detection and Response) system.
        Your role is to help investigate security incidents, explain detections, and recommend responses.
        
        Guidelines:
        1. Be concise and technical in your responses
        2. Focus on actionable insights
        3. When asked about detections, analyze the provided context
        4. Provide mitigation steps when applicable
        5. Reference relevant MITRE ATT&CK techniques
        
        Current time: {current_time}
        """.format(current_time=datetime.utcnow().isoformat())
        
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.max_history = 20  # Keep last 20 messages to manage context window

    def _format_detection_context(self, detection: Dict[str, Any]) -> str:
        """Format detection data for the AI context"""
        return f"""
        Detection Details:
        - Title: {detection.get('title')}
        - Status: {detection.get('status')}
        - Severity: {detection.get('severity')}
        - Confidence: {detection.get('confidence', 0) * 100:.1f}%
        - Source: {detection.get('source')}
        - First Seen: {detection.get('created_at')}
        - Description: {detection.get('description')}
        - Tags: {', '.join(detection.get('tags', []))}
        """

    async def analyze_detection(self, detection: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a detection and provide insights"""
        context = self._format_detection_context(detection)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
            Analyze this security detection and provide:
            1. A brief summary of the potential threat
            2. Likely MITRE ATT&CK techniques
            3. Recommended investigation steps
            4. Suggested mitigation actions
            
            Detection details:
            {context}
            """}
        ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            return {
                "analysis": analysis,
                "model": self.model,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return {
                "error": f"Failed to analyze detection: {str(e)}",
                "model": self.model,
                "timestamp": datetime.utcnow().isoformat()
            }

    async def chat(
        self,
        message: str,
        detection_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a response to a user's message with optional detection context"""
        # Add detection context if provided
        if detection_context:
            context = self._format_detection_context(detection_context)
            self.conversation_history.append({
                "role": "system",
                "content": f"Current detection context:\n{context}"
            })
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Keep conversation history within limit
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = [
                self.conversation_history[0],  # Keep system prompt
                *self.conversation_history[-(self.max_history-1):]  # Keep most recent messages
            ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return {
                "response": assistant_message,
                "model": self.model,
                "detection_id": detection_context.get("id") if detection_context else None
            }
            
        except Exception as e:
            logger.error(f"Error in AI chat: {str(e)}")
            return {
                "error": f"Failed to generate response: {str(e)}",
                "model": self.model
            }

    def clear_history(self):
        """Reset the conversation history while keeping the system prompt"""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.conversation_history

    def set_system_prompt(self, prompt: str):
        """Update the system prompt and reset conversation"""
        self.system_prompt = prompt
        self.clear_history()
