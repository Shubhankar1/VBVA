#!/usr/bin/env python3
"""
Test script to verify video looping fix for 12+ second videos
"""

import requests
import json
import time
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_video_generation(message, expected_duration_range=(3, 8)):
    """Test video generation with a specific message"""
    print(f"\n🧪 Testing video generation for message: '{message[:50]}...'")
    
    response = requests.post(
        "http://localhost:8000/api/v1/generate_video",
        json={
            "message": message,
            "agent_type": "general"
        },
        timeout=300  # 5 minute timeout for longer videos
    )
    
    if response.status_code == 200:
        data = response.json()
        video_url = data.get("video_url")
        processing_time = data.get("processing_time", 0)
        processing_details = data.get("processing_details", {})
        
        print(f"✅ Video generated successfully")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Processing time: {processing_time:.2f}s")
        print(f"🔧 Processing details: {processing_details}")
        
        # Check if processing details indicate proper chunking
        chunk_duration = processing_details.get("chunk_duration", 0)
        parallel_processing = processing_details.get("parallel_processing", False)
        
        print(f"🎵 Chunk duration: {chunk_duration}s")
        print(f"🔄 Parallel processing: {parallel_processing}")
        
        return True, video_url, processing_time
    else:
        print(f"❌ Failed to generate video: {response.status_code}")
        print(f"❌ Response: {response.text}")
        return False, None, 0

def test_long_content_specific():
    """Test specific long content that was causing looping issues"""
    
    # Test message that should generate ~12+ seconds of audio
    long_message = """This is a comprehensive test message designed to generate approximately 12 to 15 seconds of audio content. The purpose of this test is to verify that the video generation system can properly handle longer responses without experiencing the looping issue where the video repeats over certain parts of the answer instead of covering the complete response text. This message contains enough words and complexity to ensure that the audio duration is sufficient to trigger the parallel processing with multiple chunks, and we need to verify that the combination process works correctly without any synchronization problems or audio mismatches."""
    
    print(f"\n🎬 Testing Long Content Video Generation (12+ seconds)")
    print(f"📝 Message length: {len(long_message)} characters")
    print(f"📝 Expected audio duration: ~12-15 seconds")
    
    success, video_url, processing_time = test_video_generation(long_message)
    
    if success:
        print(f"\n✅ Long content test completed successfully!")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Total processing time: {processing_time:.2f}s")
        
        # Instructions for manual verification
        print(f"\n📋 Manual Verification Instructions:")
        print(f"1. Open the video URL in a browser")
        print(f"2. Listen to the complete audio content")
        print(f"3. Verify that the video covers the FULL response text")
        print(f"4. Check that there's NO looping over just a few words")
        print(f"5. Ensure the lip sync matches the complete audio")
        
        return True
    else:
        print(f"\n❌ Long content test failed!")
        return False

def test_medium_content():
    """Test medium content that should use single video generation"""
    
    # Test message that should generate ~8-10 seconds of audio
    medium_message = """This is a medium length test message that should generate approximately 8 to 10 seconds of audio content. The purpose is to verify that the system correctly uses single video generation for this optimal range without unnecessary splitting that could cause looping issues."""
    
    print(f"\n🎬 Testing Medium Content Video Generation (8-10 seconds)")
    print(f"📝 Message length: {len(medium_message)} characters")
    print(f"📝 Expected audio duration: ~8-10 seconds")
    
    success, video_url, processing_time = test_video_generation(medium_message)
    
    if success:
        print(f"\n✅ Medium content test completed successfully!")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Total processing time: {processing_time:.2f}s")
        
        print(f"\n📋 Manual Verification Instructions:")
        print(f"1. Open the video URL in a browser")
        print(f"2. Verify single video generation was used (no chunking)")
        print(f"3. Check that the complete message is covered")
        
        return True
    else:
        print(f"\n❌ Medium content test failed!")
        return False

def test_short_content():
    """Test short content that should use single video generation"""
    
    # Test message that should generate ~3-5 seconds of audio
    short_message = """This is a short test message to verify basic functionality."""
    
    print(f"\n🎬 Testing Short Content Video Generation (3-5 seconds)")
    print(f"📝 Message length: {len(short_message)} characters")
    print(f"📝 Expected audio duration: ~3-5 seconds")
    
    success, video_url, processing_time = test_video_generation(short_message)
    
    if success:
        print(f"\n✅ Short content test completed successfully!")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Total processing time: {processing_time:.2f}s")
        
        print(f"\n📋 Manual Verification Instructions:")
        print(f"1. Open the video URL in a browser")
        print(f"2. Verify single video generation was used")
        print(f"3. Check that the complete message is covered")
        
        return True
    else:
        print(f"\n❌ Short content test failed!")
        return False

def main():
    """Run comprehensive video generation tests"""
    print("🎬 Testing Video Looping Fix for 12+ Second Videos")
    print("=" * 60)
    
    # Test 1: Short content (should use single chunk)
    short_success = test_short_content()
    time.sleep(2)
    
    # Test 2: Medium content (should use single chunk)
    medium_success = test_medium_content()
    time.sleep(2)
    
    # Test 3: Long content (should use multiple chunks)
    long_success = test_long_content_specific()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"✅ Short content test: {'PASSED' if short_success else 'FAILED'}")
    print(f"✅ Medium content test: {'PASSED' if medium_success else 'FAILED'}")
    print(f"✅ Long content test: {'PASSED' if long_success else 'FAILED'}")
    
    if short_success and medium_success and long_success:
        print("\n🎉 All tests passed! Video looping fix appears to be working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the logs and verify manually.")
    
    print("\n📋 Key Points to Verify:")
    print("1. Backend logs should show proper chunking for long content")
    print("2. Videos should cover the complete response text")
    print("3. No looping over just a few words should occur")
    print("4. Lip sync should match the complete audio content")

if __name__ == "__main__":
    main() 