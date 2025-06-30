"""
VBVA Text-to-Speech Service
ElevenLabs TTS service with voice cloning support
"""

import asyncio
import tempfile
import os
from typing import Optional, Dict
from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings, Model
from elevenlabs.api import History

from config.settings import get_settings

class TTSService:
    """Text-to-Speech service using ElevenLabs"""
    
    def __init__(self):
        self.settings = get_settings()
        set_api_key(self.settings.elevenlabs_api_key)
        
        self.voice_id = self.settings.elevenlabs_voice_id
        self.model = self.settings.elevenlabs_model
        
        # Voice settings for different agent types
        self.voice_settings = {
            "general": VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            ),
            "hotel": VoiceSettings(
                stability=0.7,
                similarity_boost=0.8,
                style=0.1,
                use_speaker_boost=True
            ),
            "airport": VoiceSettings(
                stability=0.6,
                similarity_boost=0.7,
                style=0.2,
                use_speaker_boost=True
            ),
            "sales": VoiceSettings(
                stability=0.8,
                similarity_boost=0.9,
                style=0.3,
                use_speaker_boost=True
            )
        }
    
    async def generate_speech(
        self, 
        text: str, 
        voice_id: Optional[str] = None,
        agent_type: str = "general"
    ) -> str:
        """Generate speech from text with smart splitting for long content"""
        """Generate speech from text and return audio file path"""
        import traceback
        import hashlib
        try:
            voice_id = voice_id or self.voice_id
            
            # Create cache key
            cache_key = hashlib.md5(f"{text}_{voice_id}_{agent_type}".encode()).hexdigest()[:8]
            cache_dir = "/tmp/tts_cache"
            os.makedirs(cache_dir, exist_ok=True)
            cache_path = os.path.join(cache_dir, f"{cache_key}.mp3")
            
            # Check cache first
            if os.path.exists(cache_path):
                print(f"Using cached audio: {cache_path}")
                return cache_path
            
            # Generate audio using ElevenLabs API
            # Use keyword arguments like the working test script
            audio = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: generate(
                    text=text,
                    voice=voice_id,
                    model=self.model
                )
            )
            
            # Save to cache file
            save(audio, cache_path)
            
            return cache_path
            
        except Exception as e:
            print(f"TTS Error details: {str(e)}")
            print(traceback.format_exc())
            raise Exception(f"TTS generation failed: {str(e)}")
    
    async def clone_voice(self, audio_file_path: str, name: str) -> str:
        """Clone voice from audio file"""
        try:
            # This would require ElevenLabs voice cloning API
            # Implementation depends on specific API version
            raise NotImplementedError("Voice cloning not implemented yet")
        except Exception as e:
            raise Exception(f"Voice cloning failed: {str(e)}")
    
    async def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            # This would require ElevenLabs API call to list voices
            # For now, return default voice
            return [
                {
                    "voice_id": self.voice_id,
                    "name": "Default Voice",
                    "category": "general"
                }
            ]
        except Exception as e:
            raise Exception(f"Failed to get voices: {str(e)}")
    
    def get_voice_settings(self, agent_type: str) -> VoiceSettings:
        """Get voice settings for agent type"""
        return self.voice_settings.get(agent_type, self.voice_settings["general"])
    
    async def cleanup_audio_file(self, file_path: str) -> None:
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to cleanup audio file {file_path}: {e}") 