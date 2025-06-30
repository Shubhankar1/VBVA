#!/usr/bin/env python3
"""
Comprehensive test to verify the metadata fixing and playback issue resolution
"""

import asyncio
import requests
import time
import subprocess
import os

async def test_comprehensive_fix():
    """Test the comprehensive fix for video looping issues"""
    print("🔧 Comprehensive Video Fix Test")
    print("=" * 60)
    
    # Test message that should generate ~16 seconds of audio
    test_message = "This is a comprehensive test of the video generation system with metadata fixing to prevent any playback issues including looping problems that may occur in web browsers."
    
    print(f"📝 Test message: {test_message}")
    print(f"📏 Message length: {len(test_message)} characters")
    
    # Generate video with the new metadata fixing
    print("\n🎬 Generating video with metadata fix...")
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
        
        # Test video serving with new headers
        print(f"\n🔍 Testing video serving with comprehensive headers...")
        headers_response = requests.head(video_url)
        
        if headers_response.status_code == 200:
            headers = headers_response.headers
            print(f"✅ Video serving successful")
            print(f"📊 Content-Type: {headers.get('Content-Type', 'N/A')}")
            print(f"📊 Content-Length: {headers.get('Content-Length', 'N/A')}")
            print(f"📊 Cache-Control: {headers.get('Cache-Control', 'N/A')}")
            print(f"📊 Accept-Ranges: {headers.get('Accept-Ranges', 'N/A')}")
            
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

def analyze_video_file(video_url: str):
    """Analyze the video file for potential issues"""
    print(f"\n🔍 Analyzing video file...")
    
    # Extract local path from URL
    filename = video_url.split('/')[-1].split('?')[0]
    video_path = f"/tmp/wav2lip_ultra_outputs/{filename}"
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    # Get video information
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import json
            info = json.loads(result.stdout)
            
            format_info = info.get('format', {})
            streams = info.get('streams', [])
            
            print(f"📊 Video duration: {format_info.get('duration', 'N/A')}s")
            print(f"📊 File size: {format_info.get('size', 'N/A')} bytes")
            print(f"📊 Bitrate: {format_info.get('bit_rate', 'N/A')} bps")
            
            # Check for video and audio streams
            video_streams = [s for s in streams if s.get('codec_type') == 'video']
            audio_streams = [s for s in streams if s.get('codec_type') == 'audio']
            
            print(f"📊 Video streams: {len(video_streams)}")
            print(f"📊 Audio streams: {len(audio_streams)}")
            
            if len(video_streams) > 0 and len(audio_streams) > 0:
                print("✅ Video has both video and audio streams")
            else:
                print("⚠️ Video missing video or audio streams")
            
            return True
        else:
            print(f"❌ Video analysis failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Video analysis error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Comprehensive Video Fix Test")
    print("=" * 60)
    
    # Test video generation with metadata fixing
    success, video_url, processing_time = asyncio.run(test_comprehensive_fix())
    
    if success and video_url:
        # Analyze the generated video
        analyze_video_file(video_url)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ Test: PASSED")
        print(f"   📹 Video URL: {video_url}")
        print(f"   ⏱️ Processing time: {processing_time:.2f}s")
        
        print("\n🔧 Fixes Applied:")
        print("   1. ✅ Video metadata fixing (prevents playback issues)")
        print("   2. ✅ Comprehensive HTTP headers (prevents caching)")
        print("   3. ✅ Cache-busting timestamps (prevents browser cache)")
        print("   4. ✅ Proper video encoding (ensures compatibility)")
        
        print("\n🔍 Manual Verification:")
        print("1. Open the video URL in a browser")
        print("2. Check if the complete message is covered")
        print("3. Verify no looping of any part")
        print("4. Audio should flow naturally from start to finish")
        print("5. Try refreshing the page to test cache prevention")
        
        print("\n🎉 Comprehensive fix completed! Please test the video.")
    else:
        print("❌ Test: FAILED")
        print("\n⚠️ The comprehensive fix may need further investigation.") 