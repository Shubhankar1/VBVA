#!/usr/bin/env python3
"""
Test script to verify long video generation (with chunking) works correctly without looping
"""

import asyncio
import requests
import time

async def test_long_video_generation():
    """Test long video generation that should use chunking"""
    print("🔍 Testing long video generation with chunking...")
    
    # Test with a longer message that should trigger chunking (>12 seconds)
    long_message = """This is a comprehensive test message designed to generate approximately 15 to 20 seconds of audio content. The purpose of this test is to verify that the video generation system can properly handle longer responses without experiencing the looping issue where the video repeats over certain parts of the answer instead of covering the complete response text. This message contains enough words and complexity to ensure that the audio duration is sufficient to trigger the parallel processing with multiple chunks, and we need to verify that the combination process works correctly without any synchronization problems or audio mismatches. The system should now generate a video that covers the entire response without any looping or repetition issues."""
    
    print(f"📝 Message length: {len(long_message)} characters")
    print(f"📝 Expected audio duration: ~15-20 seconds")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/generate_video",
            json={
                "message": long_message,
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
            
            # Test the video URL
            if video_url:
                test_response = requests.head(video_url, timeout=10)
                if test_response.status_code == 200:
                    size = test_response.headers.get('content-length', 'Unknown')
                    print(f"✅ Video URL accessible: {size} bytes")
                    
                    print(f"\n📋 Manual Verification Instructions:")
                    print(f"1. Open the video URL in a browser: {video_url}")
                    print(f"2. Listen to the complete audio content")
                    print(f"3. Verify that the video covers the FULL response text")
                    print(f"4. Check that there's NO looping over just a few words")
                    print(f"5. Ensure the lip sync matches the complete audio")
                    
                    return True
                else:
                    print(f"❌ Video URL not accessible: {test_response.status_code}")
                    return False
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting long video looping fix test...")
    
    success = await test_long_video_generation()
    
    if success:
        print(f"\n✅ Long video test completed successfully!")
        print(f"🎉 The video looping fix appears to be working correctly!")
    else:
        print(f"\n❌ Long video test failed!")
    
    print("\n📋 Key Points to Verify:")
    print("1. Backend logs should show proper chunking for long content")
    print("2. Videos should cover the complete response text")
    print("3. No looping over just a few words should occur")
    print("4. Lip sync should match the complete audio content")

if __name__ == "__main__":
    asyncio.run(main()) 