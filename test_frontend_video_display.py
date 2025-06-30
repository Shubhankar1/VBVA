#!/usr/bin/env python3
"""
Test script to verify frontend video display functionality
and identify the specific issue with video URL handling.
"""

import requests
import time

def test_video_url_accessibility():
    """Test if video URLs are accessible from the frontend perspective"""
    
    print("🧪 Testing video URL accessibility...")
    
    # Test the specific URL that's failing
    test_url = "http://localhost:8000/api/v1/videos/ultra_wav2lip_04f69837_cfc03ca9_068242_fixed.mp4?t=1751244077"
    
    try:
        print(f"🔍 Testing URL: {test_url}")
        
        # Test 1: HEAD request (like the frontend does)
        print("📡 Testing HEAD request...")
        head_response = requests.head(test_url, timeout=10)
        print(f"✅ HEAD response: {head_response.status_code}")
        print(f"📊 Content-Type: {head_response.headers.get('content-type')}")
        print(f"📊 Content-Length: {head_response.headers.get('content-length')}")
        
        # Test 2: GET request with streaming (like video player)
        print("\n📡 Testing GET request with streaming...")
        get_response = requests.get(test_url, timeout=10, stream=True)
        print(f"✅ GET response: {get_response.status_code}")
        
        if get_response.status_code == 200:
            # Read first few bytes to verify content
            first_chunk = next(get_response.iter_content(chunk_size=1024))
            print(f"📊 First chunk size: {len(first_chunk)} bytes")
            print(f"📊 First few bytes: {first_chunk[:20].hex()}")
            
            # Check if it looks like an MP4 file
            if first_chunk.startswith(b'\x00\x00\x00') or b'ftyp' in first_chunk:
                print("✅ Content appears to be valid MP4")
            else:
                print("⚠️ Content doesn't appear to be valid MP4")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing video URL: {str(e)}")
        return False

def test_backend_video_generation():
    """Test backend video generation to get a fresh URL"""
    
    print("\n🧪 Testing backend video generation...")
    
    try:
        # Generate a new video
        response = requests.post(
            "http://localhost:8000/api/v1/generate_video",
            json={
                "message": "Test video generation for frontend display.",
                "agent_type": "general",
                "session_id": None
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video_url")
            print(f"✅ Video generated successfully")
            print(f"🎬 Video URL: {video_url}")
            
            # Test the new URL
            print(f"\n🔍 Testing newly generated URL...")
            test_response = requests.head(video_url, timeout=10)
            print(f"✅ New URL HEAD response: {test_response.status_code}")
            
            return video_url
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error in video generation test: {str(e)}")
        return None

def test_video_serving_endpoint():
    """Test the video serving endpoint directly"""
    
    print("\n🧪 Testing video serving endpoint...")
    
    try:
        # Test the debug endpoint to see available videos
        debug_response = requests.get("http://localhost:8000/api/v1/debug/videos")
        
        if debug_response.status_code == 200:
            debug_data = debug_response.json()
            print(f"✅ Debug endpoint accessible")
            print(f"📊 Total videos: {debug_data.get('video_count', 0)}")
            
            # Show recent videos
            videos = debug_data.get('videos', [])
            if videos:
                print(f"\n📋 Recent videos:")
                for i, video in enumerate(videos[-5:], 1):  # Last 5 videos
                    print(f"  {i}. {video['filename']} ({video['size_mb']}MB)")
                    print(f"     URL: {video['url']}")
            else:
                print("⚠️ No videos found")
        else:
            print(f"❌ Debug endpoint failed: {debug_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing debug endpoint: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting frontend video display tests...")
    print("=" * 60)
    
    # Test 1: Check if the failing URL is accessible
    test1_result = test_video_url_accessibility()
    
    # Test 2: Check video serving endpoint
    test_video_serving_endpoint()
    
    # Test 3: Generate a new video and test its URL
    new_video_url = test_backend_video_generation()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"✅ URL accessibility test: {'PASSED' if test1_result else 'FAILED'}")
    print(f"✅ New video generation: {'PASSED' if new_video_url else 'FAILED'}")
    
    if test1_result and new_video_url:
        print("🎉 All tests passed!")
        print("\n💡 The issue appears to be in the frontend video display logic,")
        print("   not with the backend or URL accessibility.")
        print("   The problem might be with Streamlit's st.video() function")
        print("   or browser compatibility issues.")
    else:
        print("❌ Some tests failed - backend issue detected")

if __name__ == "__main__":
    main() 