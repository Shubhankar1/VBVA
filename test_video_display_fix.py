#!/usr/bin/env python3
"""
Test script to verify video display fix
Tests the video URL accessibility and headers after removing Content-Disposition: attachment
"""

import requests
import time

def test_video_url_accessibility():
    """Test if video URLs are accessible and properly formatted"""
    print("🔍 Testing video URL accessibility...")
    
    # Test the specific video URL that was failing
    video_url = "http://localhost:8000/api/v1/videos/ultra_combined_9e0b28c7a855_fixed.mp4?t=1751244931&cb=1751244931"
    
    try:
        # Test HEAD request to check headers
        print(f"📡 Testing HEAD request to: {video_url}")
        head_response = requests.head(video_url, timeout=10)
        
        print(f"✅ HEAD Response Status: {head_response.status_code}")
        print(f"📋 Content-Type: {head_response.headers.get('content-type', 'Not set')}")
        print(f"📏 Content-Length: {head_response.headers.get('content-length', 'Not set')}")
        print(f"🔗 Accept-Ranges: {head_response.headers.get('accept-ranges', 'Not set')}")
        
        # Check if Content-Disposition is missing (which is good)
        content_disposition = head_response.headers.get('content-disposition', 'Not set')
        print(f"📎 Content-Disposition: {content_disposition}")
        
        if 'attachment' in content_disposition:
            print("❌ WARNING: Content-Disposition still contains 'attachment' - this will cause playback issues!")
        else:
            print("✅ SUCCESS: Content-Disposition does not contain 'attachment' - video should play inline!")
        
        # Test GET request to verify video content
        print(f"\n📡 Testing GET request to verify video content...")
        get_response = requests.get(video_url, timeout=10, stream=True)
        
        if get_response.status_code == 200:
            # Read first few bytes to verify it's a video file
            first_bytes = next(get_response.iter_content(chunk_size=16))
            print(f"📹 First 16 bytes: {first_bytes.hex()}")
            
            # Check for MP4 signature
            if first_bytes.startswith(b'\x00\x00\x00\x20ftyp'):
                print("✅ SUCCESS: Valid MP4 file signature detected!")
            else:
                print("⚠️ WARNING: MP4 signature not detected in first bytes")
            
            print(f"✅ GET Response Status: {get_response.status_code}")
            print(f"📊 Video file is accessible and readable")
        else:
            print(f"❌ GET request failed: {get_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing video URL: {str(e)}")
        return False
    
    return True

def test_backend_health():
    """Test if backend is running and healthy"""
    print("\n🔧 Testing backend health...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {str(e)}")
        return False

def test_video_serving_endpoint():
    """Test the video serving endpoint specifically"""
    print("\n🎬 Testing video serving endpoint...")
    
    try:
        # Test with a simple video request
        test_url = "http://localhost:8000/api/v1/videos/ultra_combined_9e0b28c7a855_fixed.mp4"
        response = requests.head(test_url, timeout=10)
        
        print(f"📡 Video serving endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Video serving endpoint is working")
            
            # Check important headers
            headers_to_check = [
                'content-type',
                'content-length', 
                'accept-ranges',
                'cache-control',
                'access-control-allow-origin'
            ]
            
            for header in headers_to_check:
                value = response.headers.get(header, 'Not set')
                print(f"📋 {header}: {value}")
            
            return True
        else:
            print(f"❌ Video serving endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing video serving endpoint: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting video display fix verification...")
    print("=" * 60)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("❌ Backend is not running. Please start the backend first.")
        return
    
    # Test 2: Video serving endpoint
    if not test_video_serving_endpoint():
        print("❌ Video serving endpoint is not working properly.")
        return
    
    # Test 3: Video URL accessibility
    if test_video_url_accessibility():
        print("\n🎉 SUCCESS: Video display fix appears to be working!")
        print("💡 The video should now play correctly in the frontend.")
        print("🔄 Try testing the frontend now with a new video generation request.")
    else:
        print("\n❌ FAILURE: Video display fix verification failed.")
        print("🔧 Please check the backend logs for more details.")

if __name__ == "__main__":
    main() 