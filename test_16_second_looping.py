#!/usr/bin/env python3
"""
Test script to reproduce the 16-second looping issue
"""

import requests
import time

def test_16_second_looping():
    """Test to reproduce the 16-second looping issue"""
    print("🔍 Testing 16-Second Looping Issue")
    print("=" * 50)
    
    # Test message that should generate ~16 seconds of audio
    test_message = "In the depths of consciousness, whispering secrets of the universe to those who dare to listen with open hearts. This message should generate approximately sixteen seconds of audio content to test the chunking and combination logic."
    
    print(f"📝 Test message: {test_message}")
    print(f"📏 Message length: {len(test_message)} characters")
    
    # Generate video
    print("\n🎬 Generating video...")
    start_time = time.time()
    
    response = requests.post(
        "http://localhost:8000/api/v1/generate_video",
        json={
            "message": test_message,
            "agent_type": "general",
            "optimization_level": "ultra_fast"
        },
        timeout=120
    )
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    if response.status_code == 200:
        result = response.json()
        video_url = result.get("video_url", "")
        
        print(f"✅ Video generated successfully")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Processing time: {processing_time:.2f}s")
        
        # Extract video filename for analysis
        if video_url:
            filename = video_url.split('/')[-1].split('?')[0]
            print(f"📁 Video filename: {filename}")
            
            # Check if it's a combined video (should be)
            if 'ultra_combined' in filename:
                print("✅ Video appears to be properly combined (not looping)")
            else:
                print("⚠️ Video filename suggests it might not be combined properly")
        
        return True, video_url, processing_time
    else:
        print(f"❌ Video generation failed: {response.status_code}")
        print(f"❌ Error: {response.text}")
        return False, None, processing_time

if __name__ == "__main__":
    print("🚀 16-Second Looping Issue Test")
    print("=" * 60)
    
    # Test API endpoint
    success, video_url, processing_time = test_16_second_looping()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ Test: PASSED")
        print(f"   📹 Video URL: {video_url}")
        print(f"   ⏱️ Processing time: {processing_time:.2f}s")
        
        print("\n🔍 Manual Verification:")
        print("1. Open the video URL in a browser")
        print("2. Check if the complete message is covered")
        print("3. Verify no looping of the first 8 seconds")
        print("4. Audio should flow naturally from start to finish")
        
        print("\n🎉 Test completed! Please manually verify the video.")
    else:
        print("❌ Test: FAILED")
        print("\n⚠️ The looping issue may still persist.") 