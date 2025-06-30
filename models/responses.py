"""
VBVA Response Models
Pydantic models for API responses
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="Agent response message")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: str = Field(..., description="Type of agent used")
    processing_time: float = Field(..., description="Processing time in seconds")
    validation_info: Optional[Dict[str, Any]] = Field(None, description="Answer validation information")

class VideoResponse(BaseModel):
    """Video response model with enhanced processing details"""
    video_url: str = Field(..., description="URL to generated video")
    audio_url: Optional[str] = Field(None, description="URL to generated audio")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: str = Field(..., description="Type of agent used")
    processing_time: float = Field(..., description="Processing time in seconds")
    processing_details: Optional[dict] = Field(None, description="Detailed processing information including parallel processing stats")

class AgentInfo(BaseModel):
    """Agent information model"""
    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type")
    description: str = Field(..., description="Agent description")
    capabilities: List[str] = Field(..., description="Agent capabilities")

class SessionInfo(BaseModel):
    """Session information model"""
    session_id: str = Field(..., description="Session identifier")
    agent_type: str = Field(..., description="Current agent type")
    created_at: str = Field(..., description="Session creation timestamp")
    message_count: int = Field(..., description="Number of messages in session") 