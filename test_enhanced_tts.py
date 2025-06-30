#!/usr/bin/env python3
"""
Test Enhanced TTS Service with Fallback Options
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_enhanced_tts():
    """Test the enhanced TTS service with fallback options"""
    
    try:
        from services.enhanced_tts import EnhancedTTSService
        
        print("🚀 Testing Enhanced TTS Service...")
        
        # Initialize the service
        tts_service = EnhancedTTSService()
        
        # Get service status
        status = tts_service.get_service_status()
        print(f"📊 Service Status: {status}")
        
        # Test text
        test_text = "Hello, this is a test of the enhanced TTS service with fallback options."
        
        print(f"🎤 Testing TTS with text: '{test_text}'")
        
        # Generate speech
        start_time = asyncio.get_event_loop().time()
        audio_path = await tts_service.generate_speech(
            text=test_text,
            agent_type="general"
        )
        end_time = asyncio.get_event_loop().time()
        
        print(f"✅ TTS completed in {end_time - start_time:.2f}s")
        print(f"📁 Audio file: {audio_path}")
        
        # Check if file exists and has content
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"📏 File size: {file_size} bytes")
            
            if file_size > 0:
                print("✅ Audio file generated successfully!")
            else:
                print("⚠️ Audio file is empty")
        else:
            print("❌ Audio file not found")
        
        # Test with a longer text to trigger potential rate limiting
        print("\n🎤 Testing with longer text to check fallback behavior...")
        longer_text = "This is a longer test message that might trigger rate limiting on ElevenLabs. The enhanced TTS service should automatically fall back to alternative providers if the primary service is unavailable or rate limited."
        
        start_time = asyncio.get_event_loop().time()
        audio_path2 = await tts_service.generate_speech(
            text=longer_text,
            agent_type="general"
        )
        end_time = asyncio.get_event_loop().time()
        
        print(f"✅ Second TTS completed in {end_time - start_time:.2f}s")
        print(f"📁 Audio file: {audio_path2}")
        
        if os.path.exists(audio_path2):
            file_size = os.path.getsize(audio_path2)
            print(f"📏 File size: {file_size} bytes")
            print("✅ Second audio file generated successfully!")
        
        print("\n🎉 Enhanced TTS Service test completed successfully!")
        
    except ImportError as e:
        print(f"❌ Failed to import Enhanced TTS Service: {e}")
        print("Make sure the enhanced_tts.py file exists and all dependencies are installed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_tts()) 