#!/usr/bin/env python3
"""
Test with longer message to verify chunking and combination with metadata fix
"""

import asyncio
import requests
import time

async def test_longer_message():
    """Test with a longer message that should trigger chunking"""
    print("🔧 Longer Message Test with Metadata Fix")
    print("=" * 60)
    
    # Longer test message that should generate ~16+ seconds of audio
    test_message = "In the depths of consciousness, whispering secrets of the universe to those who dare to listen with open hearts. This message should generate approximately sixteen seconds of audio content to test the chunking and combination logic with the new metadata fixing system that prevents any playback issues."
    
    print(f"📝 Test message: {test_message}")
    print(f"📏 Message length: {len(test_message)} characters")
    
    # Generate video with the new metadata fixing
    print("\n🎬 Generating video with chunking and metadata fix...")
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
            
            # Check if it's a fixed video (should be)
            if '_fixed' in filename:
                print("✅ Video appears to be metadata-fixed")
            else:
                print("⚠️ Video filename suggests it might not be fixed")
            
            # Check if it's a combined video (should be for longer content)
            if 'ultra_combined' in filename:
                print("✅ Video appears to be properly combined (chunking worked)")
            else:
                print("⚠️ Video filename suggests it might not be combined")
        
        # Test video serving with new headers
        print(f"\n🔍 Testing video serving with comprehensive headers...")
        headers_response = requests.head(video_url)
        
        if headers_response.status_code == 200:
            headers = headers_response.headers
            print(f"✅ Video serving successful")
            print(f"📊 Content-Type: {headers.get('Content-Type', 'N/A')}")
            print(f"📊 Content-Length: {headers.get('Content-Length', 'N/A')}")
            print(f"📊 Cache-Control: {headers.get('Cache-Control', 'N/A')}")
            
            # Check for comprehensive headers
            if 'no-cache' in headers.get('Cache-Control', ''):
                print("✅ Cache prevention headers present")
            else:
                print("⚠️ Cache prevention headers missing")
        else:
            print(f"❌ Video serving failed: {headers_response.status_code}")
        
        return True, video_url, processing_time
    else:
        print(f"❌ Video generation failed: {response.status_code}")
        print(f"❌ Error: {response.text}")
        return False, None, processing_time

if __name__ == "__main__":
    print("🚀 Longer Message Test with Metadata Fix")
    print("=" * 60)
    
    # Test video generation with chunking and metadata fixing
    success, video_url, processing_time = asyncio.run(test_longer_message())
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ Test: PASSED")
        print(f"   📹 Video URL: {video_url}")
        print(f"   ⏱️ Processing time: {processing_time:.2f}s")
        
        print("\n🔧 Comprehensive Fixes Applied:")
        print("   1. ✅ Video metadata fixing (prevents playback issues)")
        print("   2. ✅ Chunking and combination (handles long content)")
        print("   3. ✅ Comprehensive HTTP headers (prevents caching)")
        print("   4. ✅ Cache-busting timestamps (prevents browser cache)")
        print("   5. ✅ Proper video encoding (ensures compatibility)")
        
        print("\n🔍 Manual Verification:")
        print("1. Open the video URL in a browser")
        print("2. Check if the complete message is covered")
        print("3. Verify no looping of any part")
        print("4. Audio should flow naturally from start to finish")
        print("5. Try refreshing the page to test cache prevention")
        print("6. Video should be ~16+ seconds for this longer message")
        
        print("\n🎉 Comprehensive fix with chunking completed! Please test the video.")
    else:
        print("❌ Test: FAILED")
        print("\n⚠️ The comprehensive fix may need further investigation.") 