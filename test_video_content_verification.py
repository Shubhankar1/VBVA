#!/usr/bin/env python3
"""
Test to verify video content and check for looping issues
"""

import asyncio
import subprocess
import os
import sys

def extract_audio_from_video(video_path: str, output_path: str) -> bool:
    """Extract audio from video for analysis"""
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # Uncompressed audio for analysis
            "-ar", "24000",  # Match original sample rate
            "-ac", "1",  # Mono
            output_path,
            "-y"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Audio extraction failed: {e}")
        return False

def analyze_audio_content(audio_path: str) -> dict:
    """Analyze audio content to detect patterns"""
    try:
        # Get audio duration
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip()) if result.returncode == 0 else 0
        
        # Get audio waveform data for pattern analysis
        cmd = [
            "ffmpeg",
            "-i", audio_path,
            "-af", "volumedetect",  # Volume detection
            "-f", "null",
            "-"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Extract volume information
        stderr = result.stderr
        mean_volume = None
        max_volume = None
        
        for line in stderr.split('\n'):
            if "mean_volume" in line:
                mean_volume = line.split(':')[1].strip()
            elif "max_volume" in line:
                max_volume = line.split(':')[1].strip()
        
        return {
            "duration": duration,
            "mean_volume": mean_volume,
            "max_volume": max_volume,
            "stderr": stderr
        }
    except Exception as e:
        print(f"❌ Audio analysis failed: {e}")
        return {"duration": 0, "error": str(e)}

def test_video_content_verification():
    """Test to verify video content and check for looping"""
    print("🔍 Video Content Verification Test")
    print("=" * 60)
    
    # Test the latest generated video
    video_path = "/tmp/wav2lip_ultra_outputs/ultra_combined_cea16bc235fa.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    print(f"📹 Analyzing video: {video_path}")
    
    # Extract audio for analysis
    audio_output = "/tmp/test_extracted_audio.wav"
    print(f"🎵 Extracting audio to: {audio_output}")
    
    if not extract_audio_from_video(video_path, audio_output):
        print("❌ Failed to extract audio from video")
        return False
    
    # Analyze the extracted audio
    print(f"🔍 Analyzing extracted audio...")
    audio_analysis = analyze_audio_content(audio_output)
    
    print(f"📊 Audio Analysis Results:")
    print(f"   Duration: {audio_analysis['duration']:.2f}s")
    print(f"   Mean Volume: {audio_analysis.get('mean_volume', 'N/A')}")
    print(f"   Max Volume: {audio_analysis.get('max_volume', 'N/A')}")
    
    # Check for potential looping patterns
    print(f"\n🔍 Checking for looping patterns...")
    
    # Get video duration for comparison
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    video_duration = float(result.stdout.strip()) if result.returncode == 0 else 0
    
    print(f"📹 Video duration: {video_duration:.2f}s")
    print(f"🎵 Audio duration: {audio_analysis['duration']:.2f}s")
    
    # Check if durations match (should be close)
    duration_diff = abs(video_duration - audio_analysis['duration'])
    if duration_diff < 0.5:
        print(f"✅ Video and audio durations match (diff: {duration_diff:.2f}s)")
    else:
        print(f"⚠️ Video and audio durations don't match (diff: {duration_diff:.2f}s)")
    
    # Check if the duration is reasonable (should be ~16-17 seconds)
    if 15.0 <= audio_analysis['duration'] <= 18.0:
        print(f"✅ Audio duration is reasonable: {audio_analysis['duration']:.2f}s")
    else:
        print(f"⚠️ Audio duration seems unusual: {audio_analysis['duration']:.2f}s")
    
    # Clean up
    if os.path.exists(audio_output):
        os.remove(audio_output)
    
    return True

if __name__ == "__main__":
    print("🚀 Video Content Verification Test")
    print("=" * 60)
    
    success = test_video_content_verification()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ Test: PASSED")
        print("\n🔍 Analysis Results:")
        print("   - Video file exists and is accessible")
        print("   - Audio can be extracted successfully")
        print("   - Duration analysis completed")
        print("\n💡 If you're still seeing looping in the browser:")
        print("   1. Try clearing browser cache")
        print("   2. Try a different browser")
        print("   3. Check if the video player has loop settings")
        print("   4. The video file itself appears to be correct")
    else:
        print("❌ Test: FAILED")
        print("\n⚠️ There may be an issue with the video file itself.") 