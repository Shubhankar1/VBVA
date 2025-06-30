"""
VBVA Configuration Settings
Environment-based configuration using Pydantic
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    
    # ElevenLabs Configuration
    elevenlabs_api_key: str = Field(..., env="ELEVENLABS_API_KEY")
    elevenlabs_voice_id: str = Field(default="21m00Tcm4TlvDq8ikWAM", env="ELEVENLABS_VOICE_ID")
    elevenlabs_model: str = Field(default="eleven_monolingual_v1", env="ELEVENLABS_MODEL")
    
    # Speech-to-Text Configuration
    stt_provider: str = Field(default="whisper_api", env="STT_PROVIDER")
    deepgram_api_key: Optional[str] = Field(default=None, env="DEEPGRAM_API_KEY")
    
    # Lip-Sync Configuration
    lip_sync_provider: str = Field(default="local_wav2lip", env="LIP_SYNC_PROVIDER")
    d_id_api_key: Optional[str] = Field(default=None, env="D_ID_API_KEY")
    replicate_api_token: Optional[str] = Field(default=None, env="REPLICATE_API_TOKEN")
    heygen_api_key: Optional[str] = Field(default=None, env="HEYGEN_API_KEY")
    
    # Security Configuration
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./vbva.db", env="DATABASE_URL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # CORS Configuration
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8501"],
        env="ALLOWED_ORIGINS"
    )
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # File Storage
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # Cache Configuration
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Avatar Configuration
    avatar_dir: str = Field(default="./avatars", env="AVATAR_DIR")
    default_avatar: str = Field(default="./avatars/general.jpg", env="DEFAULT_AVATAR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 