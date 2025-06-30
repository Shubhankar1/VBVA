#!/usr/bin/env python3
"""
Test script for Wav2Lip integration with VBVA backend
"""

import asyncio
import os
import sys
from services.lip_sync import LipSyncService

async def test_wav2lip_integration():
    """Test the Wav2Lip integration"""
    print("Testing Wav2Lip integration with VBVA backend...")
    
    # Initialize the lip-sync service
    service = LipSyncService()
    
    # Check if Wav2Lip is available
    is_available = service._check_wav2lip_available()
    print(f"Wav2Lip available: {is_available}")
    
    if not is_available:
        print("❌ Wav2Lip not available. Please ensure it's properly installed.")
        return False
    
    # Test with a sample audio file
    # Use the test audio we created earlier
    test_audio_path = "Wav2Lip/test_samples/realistic_speech.wav"
    
    if not os.path.exists(test_audio_path):
        print(f"❌ Test audio file not found: {test_audio_path}")
        return False
    
    print(f"✅ Test audio found: {test_audio_path}")
    
    # Test avatar path
    avatar_path = "avatars/general.jpg"
    if not os.path.exists(avatar_path):
        print(f"❌ Avatar file not found: {avatar_path}")
        return False
    
    print(f"✅ Avatar found: {avatar_path}")
    
    try:
        # Test the local Wav2Lip generation
        print("🔄 Generating lip-sync video...")
        output_path = await service._generate_local_wav2lip(
            audio_url=test_audio_path,
            avatar_image=avatar_path,
            avatar_type="general"
        )
        
        print(f"✅ Video generated successfully: {output_path}")
        
        # Check if output file exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Output file exists, size: {file_size} bytes")
            return True
        else:
            print(f"❌ Output file not found: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during video generation: {str(e)}")
        return False

async def test_full_pipeline():
    """Test the full pipeline including the main generate_video method"""
    print("\n" + "="*50)
    print("Testing full pipeline...")
    
    service = LipSyncService()
    
    # Test with the main method
    test_audio_path = "Wav2Lip/test_samples/realistic_speech.wav"
    
    try:
        print("🔄 Testing full generate_video pipeline...")
        video_url = await service.generate_video(
            audio_url=test_audio_path,
            avatar_type="general"
        )
        
        print(f"✅ Full pipeline successful: {video_url}")
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline failed: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Wav2Lip integration tests...")
    
    # Test 1: Basic integration
    test1_result = await test_wav2lip_integration()
    
    # Test 2: Full pipeline
    test2_result = await test_full_pipeline()
    
    print("\n" + "="*50)
    print("Test Results:")
    print(f"Basic Integration: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Full Pipeline: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Wav2Lip integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main()) 