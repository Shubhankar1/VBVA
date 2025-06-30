"""
VBVA Speech-to-Text Service
Multi-provider STT service (Whisper API, Deepgram, local Whisper)
"""

import asyncio
import tempfile
import os
from typing import Optional
import openai
import whisper
# from deepgram import Deepgram  # Uncomment if Deepgram is used

from config.settings import get_settings

class STTService:
    """Speech-to-Text service with multiple provider support"""
    
    def __init__(self):
        self.settings = get_settings()
        self.provider = self.settings.stt_provider
        
        # Initialize providers
        if self.provider == "whisper_api":
            openai.api_key = self.settings.openai_api_key
        # elif self.provider == "deepgram":
        #     self.deepgram = Deepgram(self.settings.deepgram_api_key)
        elif self.provider == "whisper_local":
            self.whisper_model = whisper.load_model("base")
    
    async def transcribe(self, audio_file) -> str:
        """Transcribe audio file to text"""
        try:
            if self.provider == "whisper_api":
                return await self._transcribe_whisper_api(audio_file)
            # elif self.provider == "deepgram":
            #     return await self._transcribe_deepgram(audio_file)
            elif self.provider == "whisper_local":
                return await self._transcribe_whisper_local(audio_file)
            else:
                raise ValueError(f"Unsupported STT provider: {self.provider}")
        except Exception as e:
            raise Exception(f"STT transcription failed: {str(e)}")
    
    async def _transcribe_whisper_api(self, audio_file) -> str:
        """Transcribe using OpenAI Whisper API"""
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, "rb") as audio:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    audio,
                    language="en"
                )
            return transcript["text"]
        finally:
            os.unlink(temp_file_path)
    
    # async def _transcribe_deepgram(self, audio_file) -> str:
    #     """Transcribe using Deepgram API"""
    #     content = await audio_file.read()
    #     response = await self.deepgram.transcription.prerecorded(
    #         {"buffer": content, "mimetype": audio_file.content_type},
    #         {"smart_format": True, "punctuate": True, "diarize": False}
    #     )
    #     return response["results"]["channels"][0]["alternatives"][0]["transcript"]
    
    async def _transcribe_whisper_local(self, audio_file) -> str:
        """Transcribe using local Whisper model"""
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Run Whisper in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self.whisper_model.transcribe, 
                temp_file_path
            )
            return result["text"]
        finally:
            os.unlink(temp_file_path)
    
    def get_supported_providers(self) -> list:
        """Get list of supported STT providers"""
        return ["whisper_api", "deepgram", "whisper_local"]
    
    def get_provider_info(self) -> dict:
        """Get information about current provider"""
        return {
            "provider": self.provider,
            "supported_providers": self.get_supported_providers()
        } 