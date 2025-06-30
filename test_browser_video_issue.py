#!/usr/bin/env python3
"""
Test script to isolate browser/Streamlit video looping issues
"""

import os
import subprocess
import tempfile
import time
import requests
from pathlib import Path

def test_video_generation():
    """Test video generation and analyze the output"""
    print("🔍 Testing video generation to isolate looping issue...")
    
    # Test text
    test_text = "Hello, this is a test message to check if video looping is happening. The video should play this content once without any repetition or looping."
    
    # Backend URL
    backend_url = "http://localhost:8000"
    
    try:
        # Step 1: Generate video
        print(f"📝 Sending text to backend: {test_text[:50]}...")
        
        response = requests.post(
            f"{backend_url}/api/v1/generate_video",
            json={
                "message": test_text,
                "agent_type": "general"
            },
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"❌ Backend error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        video_url = result.get("video_url")
        
        if not video_url:
            print("❌ No video URL returned")
            return False
        
        print(f"✅ Video generated: {video_url}")
        
        # Step 2: Download and analyze video
        print("📥 Downloading video for analysis...")
        
        video_response = requests.get(video_url, timeout=30)
        if video_response.status_code != 200:
            print(f"❌ Failed to download video: {video_response.status_code}")
            return False
        
        # Save video to temp file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            f.write(video_response.content)
            temp_video_path = f.name
        
        print(f"💾 Video saved to: {temp_video_path}")
        
        # Step 3: Analyze video properties
        print("🔍 Analyzing video properties...")
        
        # Get video duration
        duration_cmd = [
            "ffprobe", "-v", "quiet", 
            "-show_entries", "format=duration", 
            "-of", "csv=p=0", 
            temp_video_path
        ]
        
        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
        if duration_result.returncode == 0:
            duration = float(duration_result.stdout.strip())
            print(f"⏱️ Video duration: {duration:.3f} seconds")
        else:
            print("❌ Could not get video duration")
            duration = None
        
        # Get video info
        info_cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "stream=codec_name,duration,start_time",
            "-of", "csv=p=0",
            temp_video_path
        ]
        
        info_result = subprocess.run(info_cmd, capture_output=True, text=True)
        if info_result.returncode == 0:
            print("📊 Video stream info:")
            for line in info_result.stdout.strip().split('\n'):
                if line:
                    print(f"   {line}")
        
        # Step 4: Check for audio content analysis
        print("🎵 Analyzing audio content...")
        
        # Extract audio and analyze
        audio_cmd = [
            "ffmpeg", "-i", temp_video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000",
            "-f", "wav", "-"
        ]
        
        audio_result = subprocess.run(audio_cmd, capture_output=True)
        if audio_result.returncode == 0:
            audio_data = audio_result.stdout
            print(f"🎵 Audio extracted: {len(audio_data)} bytes")
            
            # Simple audio analysis - check for patterns
            if len(audio_data) > 1000:
                # Check first and last 1000 bytes for similarity
                first_1000 = audio_data[:1000]
                last_1000 = audio_data[-1000:]
                
                # Simple similarity check
                if first_1000 == last_1000:
                    print("⚠️ WARNING: First and last 1000 bytes are identical - possible looping!")
                else:
                    print("✅ Audio appears to have natural progression")
            else:
                print("⚠️ Audio data too small for analysis")
        else:
            print("❌ Could not extract audio for analysis")
        
        # Step 5: Check file size
        file_size = os.path.getsize(temp_video_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        # Step 6: Test with different video players
        print("🎬 Testing video playback methods...")
        
        # Method 1: Direct file access
        print("   Method 1: Direct file access")
        print(f"   File: {temp_video_path}")
        
        # Method 2: HTTP URL
        print("   Method 2: HTTP URL")
        print(f"   URL: {video_url}")
        
        # Method 3: HTML video tag
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video Test</title>
        </head>
        <body>
            <h1>Video Looping Test</h1>
            <p>Test video URL: {video_url}</p>
            <video width="640" height="480" controls>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <br><br>
            <p>If you see looping, it's a browser/player issue.</p>
            <p>If no looping, the issue is with Streamlit's video component.</p>
        </body>
        </html>
        """
        
        html_path = "/tmp/video_test.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        print(f"   Method 3: HTML test page saved to {html_path}")
        print(f"   Open this file in your browser to test video playback")
        
        # Cleanup
        print(f"🧹 Cleanup: {temp_video_path}")
        os.unlink(temp_video_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def main():
    print("🚀 VBVA Video Looping Issue Isolation Test")
    print("=" * 50)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running")
            return
    except:
        print("❌ Backend not accessible")
        return
    
    print("✅ Backend is running")
    
    # Run the test
    success = test_video_generation()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("\n📋 Analysis Summary:")
        print("1. Check the video duration vs expected audio duration")
        print("2. Open the HTML test page in your browser")
        print("3. Compare browser playback vs Streamlit playback")
        print("4. If browser shows looping: Backend issue")
        print("5. If browser shows no looping: Streamlit/browser issue")
    else:
        print("\n❌ Test failed")

if __name__ == "__main__":
    main() 