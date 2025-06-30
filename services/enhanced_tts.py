"""
VBVA Enhanced Text-to-Speech Service
Multiple TTS providers with fallback options for reliability
"""

import asyncio
import tempfile
import os
import time
import hashlib
from typing import Optional, Dict, List
import traceback

# Try to import ElevenLabs
try:
    from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings, Model
    from elevenlabs.api import History
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs not available - will use fallback TTS")

# Try to import gTTS (Google Text-to-Speech)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available - will use basic fallback")

# Try to import pyttsx3 (offline TTS)
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 not available - will use basic fallback")

from config.settings import get_settings

class EnhancedTTSService:
    """Enhanced TTS service with multiple fallback options"""
    
    def __init__(self):
        """Initialize enhanced TTS service with multiple providers"""
        self.cache_dir = "/tmp/tts_enhanced_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Provider availability
        self.elevenlabs_enabled = False  # Force disable ElevenLabs
        self.gtts_enabled = True         # Force enable gTTS
        self.offline_enabled = False     # Force disable offline TTS
        
        # Rate limiting configuration
        self.last_elevenlabs_call = 0
        self.min_call_interval = 1.0  # Minimum 1 second between calls
        
        # Default voice and model
        self.voice_id = 'pNInz6obpgDQGcFmaJgB'  # Default voice
        self.model = 'eleven_monolingual_v1'
        
        # Initialize offline engine if available
        if PYTTSX3_AVAILABLE:
            try:
                self.offline_engine = pyttsx3.init()
                self.offline_engine.setProperty('rate', 150)
                self.offline_engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"⚠️ Offline TTS initialization failed: {e}")
                self.offline_engine = None
        
        print("🚀 Enhanced TTS Service initialized with providers:")
        print(f"   ElevenLabs: {'✅' if self.elevenlabs_enabled else '❌'}")
        print(f"   gTTS: {'✅' if self.gtts_enabled else '❌'}")
        print(f"   Offline: {'✅' if self.offline_enabled else '❌'}")
        
        # Set up ElevenLabs API key if available
        if ELEVENLABS_AVAILABLE:
            api_key = os.getenv("ELEVENLABS_API_KEY")
            if api_key:
                set_api_key(api_key)
                print("✅ ElevenLabs TTS enabled")
            else:
                print("⚠️ ElevenLabs API key not found")
                self.elevenlabs_enabled = False
        
        if GTTS_AVAILABLE:
            print("✅ Offline TTS enabled")
        
        if self.offline_enabled:
            print("✅ Offline TTS enabled")
    
    async def generate_speech(
        self, 
        text: str, 
        voice_id: Optional[str] = None,
        agent_type: str = "general",
        use_fallback: bool = True,
        target_duration: Optional[float] = None
    ) -> str:
        """Generate speech with multiple fallback options"""
        
        # Estimate expected duration and adjust text if needed
        if target_duration:
            estimated_duration = self._estimate_speech_duration(text)
            print(f"🎵 Estimated speech duration: {estimated_duration:.2f}s (target: {target_duration:.2f}s)")
            
            # If estimated duration is significantly longer than target, truncate text
            if estimated_duration > target_duration * 1.5:  # Allow 50% tolerance
                max_words = int(len(text.split()) * (target_duration / estimated_duration))
                truncated_text = ' '.join(text.split()[:max_words])
                print(f"🎵 Truncating text from {len(text.split())} to {max_words} words to match target duration")
                text = truncated_text
        
        # Create unique cache path with timestamp to prevent conflicts
        timestamp = str(int(time.time() * 1000))
        cache_path = os.path.join(self.cache_dir, f"{timestamp}.mp3")
        
        # Try ElevenLabs first
        if ELEVENLABS_AVAILABLE and self.elevenlabs_enabled:
            try:
                print("🎤 Trying elevenlabs TTS...")
                audio_path = await self._generate_elevenlabs(text, voice_id, agent_type, cache_path, target_duration)
                if audio_path:
                    print(f"✅ elevenlabs TTS successful: {audio_path}")
                    return audio_path
            except Exception as e:
                print(f"❌ ElevenLabs TTS failed: {e}")
                if "429" in str(e):
                    print("🔄 Rate limited, trying fallback...")
        
        # Try gTTS fallback
        if GTTS_AVAILABLE and self.gtts_enabled:
            try:
                print("🎤 Trying gTTS fallback...")
                audio_path = await self._generate_gtts(text, agent_type, cache_path, target_duration)
                if audio_path:
                    print(f"✅ gTTS fallback successful: {audio_path}")
                    return audio_path
            except Exception as e:
                print(f"❌ gTTS fallback failed: {e}")
        
        # Try offline TTS as last resort
        if self.offline_enabled:
            try:
                print("🎤 Trying offline TTS...")
                audio_path = await self._generate_offline(text, agent_type, cache_path, target_duration)
                if audio_path:
                    print(f"✅ Offline TTS successful: {audio_path}")
                    return audio_path
            except Exception as e:
                print(f"❌ Offline TTS failed: {e}")
        
        raise Exception("All TTS providers failed")
    
    def _estimate_speech_duration(self, text: str) -> float:
        """Estimate speech duration based on text length"""
        # Average speaking rate: ~150 words per minute = 2.5 words per second
        words = len(text.split())
        estimated_seconds = words / 2.5
        return estimated_seconds
    
    async def _generate_elevenlabs(self, text: str, voice_id: Optional[str], agent_type: str, cache_path: str, target_duration: Optional[float] = None) -> str:
        """Generate speech using ElevenLabs"""
        # Rate limiting
        current_time = time.time()
        if hasattr(self, 'last_elevenlabs_call'):
            if current_time - self.last_elevenlabs_call < getattr(self, 'min_call_interval', 1.0):
                await asyncio.sleep(getattr(self, 'min_call_interval', 1.0))
        self.last_elevenlabs_call = current_time
        
        # Use default voice if not specified
        if not voice_id:
            voice_id = getattr(self, 'voice_id', 'pNInz6obpgDQGcFmaJgB')  # Default voice
        
        # Use default model if not specified
        model = getattr(self, 'model', 'eleven_monolingual_v1')
        
        # Generate audio with voice settings for speed control
        voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
        
        audio = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: generate(
                text=text,
                voice=voice_id,
                model=model,
                voice_settings=voice_settings
            )
        )
        
        # Save to cache
        save(audio, cache_path)
        return cache_path
    
    async def _generate_gtts(self, text: str, agent_type: str, cache_path: str, target_duration: Optional[float] = None) -> str:
        """Generate speech using Google TTS (gTTS)"""
        if not GTTS_AVAILABLE:
            raise Exception("gTTS not available")
        
        try:
            # Create gTTS object with fast speech rate
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to cache file
            tts.save(cache_path)
            
            return cache_path
            
        except Exception as e:
            raise Exception(f"gTTS error: {str(e)}")
    
    async def _generate_offline(self, text: str, agent_type: str, cache_path: str, target_duration: Optional[float] = None) -> str:
        """Generate speech using offline TTS (pyttsx3)"""
        if not self.offline_enabled or self.offline_engine is None:
            raise Exception("Offline TTS not available")
        
        try:
            # Adjust speech rate based on target duration
            if target_duration:
                estimated_duration = self._estimate_speech_duration(text)
                if estimated_duration > target_duration:
                    # Increase speech rate to match target duration
                    rate_adjustment = estimated_duration / target_duration
                    new_rate = int(150 * rate_adjustment)  # Base rate is 150
                    self.offline_engine.setProperty('rate', new_rate)
                    print(f"🎵 Adjusted offline TTS rate to {new_rate} for target duration")
            
            # Generate audio using offline engine
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.offline_engine.save_to_file(text, cache_path)
            )
            
            # Wait for file to be created
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.offline_engine.runAndWait()
            )
            
            # Check if file was created
            if os.path.exists(cache_path):
                return cache_path
            else:
                raise Exception("Offline TTS file not created")
                
        except Exception as e:
            raise Exception(f"Offline TTS error: {str(e)}")
    
    async def _generate_fallback(self, text: str, agent_type: str, cache_path: str) -> str:
        """Generate fallback audio (silent with beep)"""
        try:
            # Create a simple audio file with a beep
            import wave
            import struct
            
            # Create a simple beep sound
            sample_rate = 44100
            duration = 0.5  # 0.5 seconds
            frequency = 440  # A4 note
            
            # Generate beep samples
            samples = []
            for i in range(int(sample_rate * duration)):
                sample = int(32767 * 0.3 * (i % 2))  # Simple square wave
                samples.append(struct.pack('<h', sample))
            
            # Write WAV file
            with wave.open(cache_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b''.join(samples))
            
            print(f"⚠️ Created fallback audio: {cache_path}")
            return cache_path
            
        except Exception as e:
            # If even fallback fails, create an empty file
            with open(cache_path, 'wb') as f:
                f.write(b'')
            print(f"⚠️ Created empty fallback audio: {cache_path}")
            return cache_path
    
    async def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        voices = []
        
        if self.elevenlabs_enabled:
            voices.append({
                "provider": "elevenlabs",
                "voice_id": self.voice_id,
                "name": "ElevenLabs Voice",
                "category": "premium"
            })
        
        if GTTS_AVAILABLE:
            voices.append({
                "provider": "gtts",
                "voice_id": "en",
                "name": "Google TTS",
                "category": "free"
            })
        
        if self.offline_enabled:
            voices.append({
                "provider": "offline",
                "voice_id": "system",
                "name": "System Voice",
                "category": "offline"
            })
        
        return voices
    
    def get_service_status(self) -> Dict:
        """Get TTS service status"""
        return {
            "elevenlabs_enabled": self.elevenlabs_enabled,
            "gtts_available": GTTS_AVAILABLE,
            "offline_enabled": self.offline_enabled,
            "cache_directory": self.cache_dir,
            "providers": [
                "elevenlabs" if self.elevenlabs_enabled else None,
                "gtts" if GTTS_AVAILABLE else None,
                "offline" if self.offline_enabled else None
            ]
        }
    
    async def cleanup_audio_file(self, file_path: str) -> None:
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to cleanup audio file {file_path}: {e}") 