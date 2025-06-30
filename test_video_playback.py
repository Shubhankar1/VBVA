#!/usr/bin/env python3
"""
Test script to verify video playback behavior
Tests if the video is playing from the beginning or from the end
"""

import requests
import subprocess
import tempfile
import os
import time

def test_video_playback():
    """Test video playback to see if it starts from beginning or end"""
    
    print("🧪 Testing video playback behavior...")
    
    # Get the most recent video file
    video_dir = "/tmp/wav2lip_ultra_outputs"
    video_files = [f for f in os.listdir(video_dir) if f.startswith("ultra_combined_") and f.endswith("_fixed.mp4")]
    
    if not video_files:
        print("❌ No combined video files found")
        return
    
    # Get the most recent file
    latest_video = sorted(video_files)[-1]
    video_path = os.path.join(video_dir, latest_video)
    
    print(f"📹 Testing video: {latest_video}")
    
    # Check video duration
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", 
            "-show_entries", "format=duration", 
            "-of", "csv=p=0", 
            video_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            print(f"⏱️ Video duration: {duration:.2f} seconds")
        else:
            print(f"❌ Could not get video duration: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error getting video duration: {e}")
        return
    
    # Check video stream info
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", 
            "-show_entries", "stream=duration,start_time", 
            "-of", "csv=p=0", 
            video_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"📊 Stream info: {result.stdout.strip()}")
        else:
            print(f"⚠️ Could not get stream info: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Error getting stream info: {e}")
    
    # Check if video has proper start time
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", 
            "-show_entries", "format=start_time", 
            "-of", "csv=p=0", 
            video_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            start_time = result.stdout.strip()
            print(f"🕐 Video start time: {start_time}")
        else:
            print(f"⚠️ Could not get start time: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Error getting start time: {e}")
    
    # Test video URL accessibility
    video_url = f"http://localhost:8000/api/v1/videos/{latest_video}"
    print(f"🌐 Testing video URL: {video_url}")
    
    try:
        response = requests.head(video_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Video URL accessible (Status: {response.status_code})")
            print(f"📊 Content-Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"📊 Content-Length: {response.headers.get('content-length', 'Unknown')} bytes")
        else:
            print(f"❌ Video URL not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing video URL: {e}")
    
    # Test video seeking behavior
    print("\n🔍 Testing video seeking behavior...")
    
    # Check if video has proper seeking information
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", 
            "-show_entries", "format=duration,start_time,bit_rate", 
            "-show_entries", "stream=duration,start_time,time_base", 
            "-of", "json", 
            video_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("📋 Video metadata:")
            print(result.stdout)
        else:
            print(f"⚠️ Could not get video metadata: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Error getting video metadata: {e}")
    
    # Test if video can be played from beginning
    print("\n🎬 Testing video playback from beginning...")
    
    try:
        # Use ffplay to test playback (this will show if video plays correctly)
        print("🎥 Starting video playback test (this will open a video player)...")
        print("💡 If the video plays from the beginning, the issue is in the frontend.")
        print("💡 If the video plays from the end, there's a video file issue.")
        print("⏹️ Press 'q' in the video player to stop the test.")
        
        # Start ffplay in background
        process = subprocess.Popen([
            "ffplay", "-v", "quiet", "-autoexit", video_path
        ])
        
        print("✅ Video player started. Check if it plays from the beginning or end.")
        print("⏹️ The video player will close automatically after playback.")
        
        # Wait a bit for the player to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Video player is running")
        else:
            print("❌ Video player closed unexpectedly")
            
    except Exception as e:
        print(f"❌ Error testing video playback: {e}")
        print("💡 Try running: ffplay /tmp/wav2lip_ultra_outputs/ultra_combined_*_fixed.mp4")

if __name__ == "__main__":
    test_video_playback() 