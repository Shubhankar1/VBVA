import os
from dotenv import load_dotenv
from elevenlabs import set_api_key, generate, save, voices

# Load environment variables from .env file
load_dotenv()

# Load from .env or set directly here
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_monolingual_v1")

print(f"API Key loaded: {ELEVENLABS_API_KEY[:10]}...")
print(f"Voice ID: {VOICE_ID}")
print(f"Model: {MODEL}")

set_api_key(ELEVENLABS_API_KEY)

print("\nAvailable voices:")
for v in voices():
    print(f"- {v.voice_id}: {v.name}")

try:
    print("\nGenerating speech...")
    audio = generate(
        text="Hello! This is a test of the ElevenLabs TTS API.",
        voice=VOICE_ID,
        model=MODEL
    )
    save(audio, "test_output.mp3")
    print("Audio saved to test_output.mp3")
except Exception as e:
    print(f"TTS generation failed: {e}") 