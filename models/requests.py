"""
VBVA Request Models
Pydantic models for API request validation
"""

from typing import Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Chat request model with enhanced processing options"""
    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: str = Field(default="general", description="Type of agent to use")
    enable_parallel: bool = Field(default=True, description="Enable parallel processing for video generation")
    chunk_duration: int = Field(default=8, ge=3, le=30, description="Optimal chunk duration in seconds for parallel processing")
    use_ultra_fast: bool = Field(default=True, description="Enable ultra-fast processing mode for maximum speed")

class VoiceRequest(BaseModel):
    """Voice request model"""
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: str = Field(default="general", description="Type of agent to use")
    voice_settings: Optional[dict] = Field(default=None, description="Voice generation settings")

class AgentConfigRequest(BaseModel):
    """Agent configuration request"""
    agent_type: str = Field(..., description="Type of agent")
    config: dict = Field(..., description="Agent configuration")

class VideoGenerationRequest(BaseModel):
    """Video generation request model"""
    message: str = Field(..., min_length=1, max_length=2000, description="Text to convert to video")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: str = Field(default="general", description="Type of agent to use")
    avatar_image: Optional[str] = Field(None, description="Custom avatar image path or URL") 