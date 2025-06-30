#!/usr/bin/env python3
"""
Test to verify the robust looping fix with improved video combination
"""

import asyncio
import requests
import time
import subprocess
import os

async def test_robust_looping_fix():
    """Test the robust fix for video looping issues"""
    print("🔧 Robust Video Looping Fix Test")
    print("=" * 60)
    
    # Test message that should generate ~16 seconds of audio
    test_message = "This is a comprehensive test of the robust video generation system with improved synchronization to prevent any looping issues that may occur in video playback."
    
    print(f"📝 Test message: {test_message}")
    print(f"📏 Message length: {len(test_message)} characters")
    
    # Generate video with the new robust combination method
    print("\n🎬 Generating video with robust combination...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/generate_video",
            json={
                "message": test_message,
                "agent_type": "general"
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video_url", "")
            processing_time = time.time() - start_time
            
            print(f"✅ Video generated successfully!")
            print(f"🎬 Video URL: {video_url}")
            print(f"⏱️ Processing time: {processing_time:.2f}s")
            
            # Extract filename from URL
            filename = video_url.split('/')[-1].split('?')[0]
            local_path = f"/tmp/wav2lip_ultra_outputs/{filename}"
            
            print(f"\n📁 Local video path: {local_path}")
            
            # Verify the video file exists
            if os.path.exists(local_path):
                file_size = os.path.getsize(local_path)
                print(f"📊 File size: {file_size:,} bytes")
                
                # Analyze video properties
                print(f"\n🔍 Analyzing video properties...")
                cmd = [
                    "ffprobe", 
                    "-v", "quiet", 
                    "-print_format", "json", 
                    "-show_format", 
                    "-show_streams", 
                    local_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    import json
                    data = json.loads(result.stdout)
                    
                    format_info = data.get("format", {})
                    streams = data.get("streams", [])
                    
                    print(f"📹 Video duration: {format_info.get('duration', 'N/A')}s")
                    print(f"🎵 Audio duration: {format_info.get('duration', 'N/A')}s")
                    
                    # Check for timing issues
                    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
                    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
                    
                    if video_stream and audio_stream:
                        video_start = float(video_stream.get("start_time", 0))
                        audio_start = float(audio_stream.get("start_time", 0))
                        
                        print(f"🎬 Video start time: {video_start}s")
                        print(f"🎵 Audio start time: {audio_start}s")
                        
                        if abs(video_start - audio_start) > 0.1:
                            print(f"⚠️ Timing mismatch detected: {abs(video_start - audio_start):.3f}s")
                        else:
                            print(f"✅ Audio-video timing is synchronized")
                    
                    print(f"\n🎯 Video analysis complete!")
                    print(f"📥 Download URL: {video_url}")
                    print(f"💾 Local file: {local_path}")
                    
                else:
                    print(f"❌ Failed to analyze video: {result.stderr}")
            else:
                print(f"❌ Video file not found: {local_path}")
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_robust_looping_fix()) 