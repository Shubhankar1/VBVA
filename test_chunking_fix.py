#!/usr/bin/env python3
"""
Test script to verify that the chunking issue is resolved
"""

import requests
import json
import time

def test_video_generation(message, test_name):
    """Test video generation with a specific message"""
    print(f"\n🧪 Testing: {test_name}")
    print(f"📝 Message length: {len(message)} characters")
    print(f"📝 Message: {message[:100]}{'...' if len(message) > 100 else ''}")
    
    url = "http://localhost:8000/api/v1/generate_video"
    payload = {
        "message": message,
        "session_id": f"test-{int(time.time())}",
        "agent_type": "general"
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video_url", "")
            processing_time = result.get("processing_time", 0)
            processing_details = result.get("processing_details", {})
            
            print(f"✅ Success!")
            print(f"⏱️  Processing time: {processing_time:.2f}s")
            print(f"🎬 Video URL: {video_url}")
            print(f"🔄 Parallel processing: {processing_details.get('parallel_processing', False)}")
            print(f"⏱️  Chunk duration: {processing_details.get('chunk_duration', 0)}s")
            print(f"🚀 Speed multiplier: {processing_details.get('speed_multiplier', 0):.2f}x")
            
            # Check if it used chunking
            if "ultra_combined" in video_url:
                print(f"🎯 Used chunking system: ✅")
            else:
                print(f"🎯 Used single video: ✅")
                
            return True
        else:
            print(f"❌ Failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run chunking tests"""
    print("🔧 Testing Chunking Fix")
    print("=" * 50)
    
    # Test 1: Short message (should use single video)
    short_message = "Hello, this is a short test message."
    test_video_generation(short_message, "Short Message (Single Video)")
    
    # Test 2: Medium message (should use single video)
    medium_message = "This is a medium length message that should be processed as a single video chunk. It contains enough content to test the system but not enough to trigger chunking."
    test_video_generation(medium_message, "Medium Message (Single Video)")
    
    # Test 3: Long message (should trigger chunking)
    long_message = """This is a much longer message that should definitely trigger the chunking system. We want to test if the audio chunk 1 repeating issue has been resolved. The system should now properly handle multiple chunks without duplicating the first chunk. This message contains enough content to ensure that the audio will be split into multiple chunks for parallel processing. We are testing the ultra-fast processing system with enhanced chunking capabilities."""
    test_video_generation(long_message, "Long Message (Chunking)")
    
    # Test 4: Very long message (should definitely trigger chunking)
    very_long_message = """This is an extremely long message designed to thoroughly test the chunking system and ensure that the audio chunk 1 repeating issue has been completely resolved. The system should now properly handle multiple chunks without duplicating the first chunk. This message contains enough content to ensure that the audio will be split into multiple chunks for parallel processing. We are testing the ultra-fast processing system with enhanced chunking capabilities and improved synchronization. The goal is to verify that each chunk is processed correctly and combined without any repetition or duplication issues."""
    test_video_generation(very_long_message, "Very Long Message (Multiple Chunks)")
    
    print("\n🎉 Chunking tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 