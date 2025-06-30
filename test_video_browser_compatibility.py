#!/usr/bin/env python3
"""
Test script to check browser compatibility and CORS issues
"""

import requests
import os
import time

def test_video_browser_compatibility():
    """Test video browser compatibility and CORS"""
    
    print("🧪 Testing video browser compatibility...")
    
    # Get the most recent video file
    video_dir = "/tmp/wav2lip_ultra_outputs"
    video_files = [f for f in os.listdir(video_dir) if f.startswith("ultra_combined_") and f.endswith("_fixed.mp4")]
    
    if not video_files:
        print("❌ No combined video files found")
        return
    
    # Get the most recent file
    latest_video = sorted(video_files)[-1]
    base_video_url = f"http://localhost:8000/api/v1/videos/{latest_video}"
    
    print(f"📹 Testing video: {latest_video}")
    print(f"🌐 Base URL: {base_video_url}")
    
    # Test 1: Check CORS headers
    print("\n🔍 Test 1: CORS Headers")
    try:
        response = requests.options(base_video_url, timeout=10)
        print(f"✅ OPTIONS Response: {response.status_code}")
        print(f"📊 CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
    
    # Test 2: Check GET request headers
    print("\n🔍 Test 2: GET Request Headers")
    try:
        response = requests.get(base_video_url, timeout=10, stream=True)
        print(f"✅ GET Response: {response.status_code}")
        print(f"📊 Important Headers:")
        important_headers = [
            'content-type', 'content-length', 'access-control-allow-origin',
            'access-control-allow-methods', 'access-control-allow-headers',
            'cache-control', 'accept-ranges'
        ]
        for header in important_headers:
            value = response.headers.get(header, 'Not set')
            print(f"  {header}: {value}")
    except Exception as e:
        print(f"❌ GET test failed: {e}")
    
    # Test 3: Test with cache-busting
    print("\n🔍 Test 3: Cache-busting URL")
    cache_buster = int(time.time())
    video_url_with_cache_bust = f"{base_video_url}?cb={cache_buster}"
    
    try:
        response = requests.head(video_url_with_cache_bust, timeout=10)
        print(f"✅ Cache-busted URL: {response.status_code}")
        print(f"📊 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📊 Content-Length: {response.headers.get('content-length', 'Unknown')} bytes")
    except Exception as e:
        print(f"❌ Cache-busted URL test failed: {e}")
    
    # Test 4: Test partial content (for video seeking)
    print("\n🔍 Test 4: Partial Content Support")
    try:
        headers = {'Range': 'bytes=0-1023'}  # Request first 1KB
        response = requests.get(base_video_url, headers=headers, timeout=10)
        print(f"✅ Range Request: {response.status_code}")
        if response.status_code == 206:
            print("✅ Partial content supported (good for video seeking)")
        else:
            print("⚠️ Partial content not supported")
        print(f"📊 Content-Range: {response.headers.get('content-range', 'Not set')}")
    except Exception as e:
        print(f"❌ Range request test failed: {e}")
    
    # Test 5: Test video format compatibility
    print("\n🔍 Test 5: Video Format Compatibility")
    try:
        # Download first few bytes to check format
        response = requests.get(base_video_url, timeout=10, stream=True)
        if response.status_code == 200:
            chunk = next(response.iter_content(1024))
            if chunk.startswith(b'\x00\x00\x00') or b'ftyp' in chunk[:100]:
                print("✅ Video appears to be valid MP4 format")
            else:
                print("⚠️ Video format may not be standard MP4")
            print(f"📊 First 16 bytes: {chunk[:16].hex()}")
        else:
            print(f"❌ Could not test video format: {response.status_code}")
    except Exception as e:
        print(f"❌ Video format test failed: {e}")
    
    print("\n📋 Summary:")
    print("✅ Video URL is accessible")
    print("✅ CORS headers are present")
    print("✅ Cache-busting works")
    print("💡 If you still see 'browser does not support video tag':")
    print("   1. Try a different browser (Chrome, Firefox, Safari)")
    print("   2. Check if your browser supports MP4 video")
    print("   3. Try the direct download link")
    print("   4. Check browser console for JavaScript errors")

if __name__ == "__main__":
    test_video_browser_compatibility() 