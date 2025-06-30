#!/usr/bin/env python3
"""
Script to help restore AI-generated videos
"""

import os
import shutil
from pathlib import Path

def restore_ai_videos():
    """Help restore AI-generated videos"""
    print("🎬 AI Video Restoration Helper")
    print("=" * 40)
    
    ai_dir = Path("avatars/videos/ai_generated")
    
    print(f"\n📁 Current AI videos directory: {ai_dir}")
    print(f"📊 Current files in directory:")
    
    if ai_dir.exists():
        for file in ai_dir.glob("*.mp4"):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  - {file.name}: {size_mb:.2f} MB")
    
    print(f"\n🔍 Analysis:")
    
    # Check for small placeholder videos
    small_videos = []
    for file in ai_dir.glob("*.mp4"):
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb < 0.1:  # Less than 100KB
            small_videos.append(file)
    
    if small_videos:
        print(f"  ⚠️ Found {len(small_videos)} placeholder videos (small files):")
        for video in small_videos:
            size_mb = video.stat().st_size / (1024 * 1024)
            print(f"    - {video.name}: {size_mb:.2f} MB (placeholder)")
    
    # Check for actual AI videos
    large_videos = []
    for file in ai_dir.glob("*.mp4"):
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb > 1.0:  # More than 1MB
            large_videos.append(file)
    
    if large_videos:
        print(f"  ✅ Found {len(large_videos)} actual AI videos:")
        for video in large_videos:
            size_mb = video.stat().st_size / (1024 * 1024)
            print(f"    - {video.name}: {size_mb:.2f} MB (AI-generated)")
    
    print(f"\n📋 Required AI video files:")
    required_files = [
        "general_ai.mp4",
        "hotel_ai.mp4", 
        "airport_ai.mp4",
        "sales_ai.mp4"
    ]
    
    missing_files = []
    for required_file in required_files:
        file_path = ai_dir / required_file
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > 1.0:
                print(f"  ✅ {required_file}: {size_mb:.2f} MB")
            else:
                print(f"  ⚠️ {required_file}: {size_mb:.2f} MB (placeholder)")
                missing_files.append(required_file)
        else:
            print(f"  ❌ {required_file}: Missing")
            missing_files.append(required_file)
    
    if missing_files:
        print(f"\n🚨 Action Required:")
        print(f"  Your AI-generated videos appear to be missing or replaced with placeholders.")
        print(f"  Please re-upload your AI-generated videos with these exact filenames:")
        for file in missing_files:
            print(f"    - {file}")
        
        print(f"\n📁 Upload location: {ai_dir}")
        print(f"📋 Video requirements:")
        print(f"  - Duration: 5 seconds")
        print(f"  - Format: MP4 (H.264)")
        print(f"  - Resolution: 512x512 or 720x720")
        print(f"  - File size: 2-8 MB per video")
        
        print(f"\n🔧 Quick fix commands:")
        print(f"  # Remove placeholder videos")
        for video in small_videos:
            print(f"  rm '{video}'")
        
        print(f"\n  # Then upload your AI videos with correct names")
        print(f"  # Example:")
        print(f"  cp /path/to/your/general_ai.mp4 {ai_dir}/")
        print(f"  cp /path/to/your/hotel_ai.mp4 {ai_dir}/")
        print(f"  cp /path/to/your/airport_ai.mp4 {ai_dir}/")
        print(f"  cp /path/to/your/sales_ai.mp4 {ai_dir}/")
    
    else:
        print(f"\n✅ All AI videos are present and correct!")
        print(f"  Your system is ready to use AI-generated videos.")
    
    print(f"\n🧪 Test your setup:")
    print(f"  python test_video_only_approach.py")

if __name__ == "__main__":
    restore_ai_videos() 