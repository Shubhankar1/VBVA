#!/usr/bin/env python3
"""
Test script for enhanced Wav2Lip quality settings
"""

import asyncio
import os
import sys
import tempfile
import uuid

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.lip_sync import LipSyncService

async def test_enhanced_wav2lip():
    """Test the enhanced Wav2Lip quality settings"""
    print("🧪 Testing Enhanced Wav2Lip Quality Settings")
    print("=" * 50)
    
    # Initialize the lip-sync service
    lip_sync_service = LipSyncService()
    
    # Check if Wav2Lip is available
    if not lip_sync_service._check_wav2lip_available():
        print("❌ Wav2Lip not available. Please ensure it's properly installed.")
        return
    
    print("✅ Wav2Lip is available")
    
    # Test with a sample audio file
    test_audio = "/var/folders/ng/n5yqsq_15gqbr7z_6ssx_tvh0000gn/T/tmpqbgyeonb.mp3"  # Use existing audio
    test_avatar = "./avatars/general.jpg"
    
    if not os.path.exists(test_audio):
        print(f"❌ Test audio file not found: {test_audio}")
        return
    
    if not os.path.exists(test_avatar):
        print(f"❌ Test avatar file not found: {test_avatar}")
        return
    
    print(f"📁 Using audio: {test_audio}")
    print(f"🖼️  Using avatar: {test_avatar}")
    
    try:
        print("\n🎬 Generating enhanced video...")
        
        # Generate video with enhanced settings
        video_url = await lip_sync_service.generate_video(
            audio_url=test_audio,
            avatar_type="general",
            avatar_image=test_avatar
        )
        
        print(f"✅ Video generated successfully!")
        print(f"📹 Video URL: {video_url}")
        
        # Check if the video file exists
        if "wav2lip_output" in video_url:
            filename = video_url.split("/")[-1]
            video_path = f"/tmp/wav2lip_outputs/{filename}"
            
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                print(f"📊 Video file size: {file_size / (1024*1024):.2f} MB")
                
                # Check if it's the enhanced version
                if "_enhanced" in filename:
                    print("✨ Enhanced video generated!")
                else:
                    print("⚠️  Standard video generated (enhancement may have failed)")
            else:
                print("❌ Video file not found")
        
    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_wav2lip()) 