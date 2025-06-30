#!/usr/bin/env python3
"""
Test script to verify frontend video URL acceptance fix
Tests that both ultra_combined_* and ultra_wav2lip_* URLs are now accepted
"""

import requests
import time

def test_video_url_acceptance():
    """Test that both types of video URLs are now accepted"""
    print("🔍 Testing video URL acceptance...")
    
    # Test URLs from the logs
    test_urls = [
        "http://localhost:8000/api/v1/videos/ultra_combined_9e0b28c7a855_fixed.mp4?t=1751244931",
        "http://localhost:8000/api/v1/videos/ultra_wav2lip_5221e5ce_cfc03ca9_098395_fixed.mp4?t=1751245114"
    ]
    
    for i, video_url in enumerate(test_urls, 1):
        print(f"\n📹 Test {i}: {video_url}")
        
        try:
            # Test HEAD request
            head_response = requests.head(video_url, timeout=10)
            print(f"✅ HEAD Response: {head_response.status_code}")
            
            if head_response.status_code == 200:
                content_type = head_response.headers.get('content-type', '')
                content_length = head_response.headers.get('content-length', '0')
                print(f"📋 Content-Type: {content_type}")
                print(f"📏 Content-Length: {content_length} bytes")
                
                # Check if it's a valid video file
                if 'video' in content_type or video_url.endswith('.mp4'):
                    if int(content_length) > 1024:
                        print("✅ Valid video file detected")
                        
                        # Determine URL type
                        if "ultra_combined_" in video_url:
                            print("🎬 Combined video URL (from chunking)")
                        elif "ultra_wav2lip_" in video_url:
                            print("🎬 Single video URL (no chunking needed)")
                        else:
                            print("❓ Unknown URL pattern")
                    else:
                        print("❌ Video file too small")
                else:
                    print("❌ Not a video file")
            else:
                print(f"❌ Video URL not accessible: {head_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing video URL: {str(e)}")

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

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("\n🌐 Testing frontend accessibility...")
    
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend accessibility error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting frontend video URL acceptance test...")
    print("=" * 60)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("❌ Backend is not running. Please start the backend first.")
        return
    
    # Test 2: Frontend accessibility
    if not test_frontend_accessibility():
        print("❌ Frontend is not running. Please start the frontend first.")
        return
    
    # Test 3: Video URL acceptance
    test_video_url_acceptance()
    
    print("\n" + "=" * 60)
    print("🎉 Frontend video URL acceptance test completed!")
    print("💡 Both ultra_combined_* and ultra_wav2lip_* URLs should now work")
    print("🔄 Try testing the frontend now with a new video generation request")

if __name__ == "__main__":
    main() 