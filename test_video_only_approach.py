#!/usr/bin/env python3
"""
Test script for video-only avatar approach
"""

import asyncio
import os
import sys
import time
import json
from pathlib import Path

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.video_avatar_processor import VideoAvatarProcessor

async def test_video_only_approach():
    """Test the video-only avatar approach"""
    print("🎬 Testing Video-Only Avatar Approach")
    print("=" * 50)
    
    # Initialize the video avatar processor
    processor = VideoAvatarProcessor()
    
    # Test 1: Check current video availability
    print("\n📊 Current Video Avatar Status:")
    available_videos = processor.get_available_videos()
    
    for agent_type, info in available_videos.items():
        print(f"\n{agent_type.upper()}:")
        print(f"  AI Generated: {'✅' if info['ai_generated'] else '❌'}")
        print(f"  Enhanced: {'✅' if info['enhanced'] else '❌'}")
        print(f"  Legacy: {'✅' if info['legacy'] else '❌'}")
        print(f"  Static Fallback: {'✅' if info['static_fallback'] else '❌'}")
        if info['file_sizes']:
            print(f"  File sizes: {info['file_sizes']}")
            print(f"  Total size: {info['total_size']:.2f} MB")
    
    # Test 2: Test avatar selection for each agent type
    print("\n🎯 Testing Avatar Selection:")
    
    for agent_type in ["general", "hotel", "airport", "sales"]:
        print(f"\nTesting {agent_type}:")
        
        start_time = time.time()
        avatar_path = await processor.get_video_avatar(agent_type)
        selection_time = time.time() - start_time
        
        if avatar_path:
            file_size = os.path.getsize(avatar_path) / (1024 * 1024)  # MB
            print(f"  Selected: {os.path.basename(avatar_path)} ({file_size:.2f} MB)")
            print(f"  Selection time: {selection_time:.4f}s")
            
            # Check if it's a video or image
            if avatar_path.endswith('.mp4'):
                print(f"  Type: Video")
            else:
                print(f"  Type: Image (will be converted to video)")
        else:
            print(f"  ❌ No avatar found")
    
    # Test 3: Create placeholder videos for testing (only if missing)
    print("\n🎬 Creating Placeholder Videos for Testing:")
    for agent_type in ["general", "hotel", "airport", "sales"]:
        ai_video_path = processor.ai_generated_dir / processor.video_configs[agent_type]["ai_video"]
        if ai_video_path.exists():
            print(f"  ⏩ Skipping placeholder for {agent_type} (already exists: {ai_video_path.name})")
            continue
        print(f"\nCreating placeholder for {agent_type}...")
        placeholder = await processor.create_video_placeholder(agent_type)
        if placeholder:
            size = os.path.getsize(placeholder) / (1024 * 1024)
            print(f"  ✅ Created: {os.path.basename(placeholder)} ({size:.2f} MB)")
            print(f"  ⏱️ Creation time: {time.time() - start_time:.2f}s")
        else:
            print(f"  ❌ Failed to create placeholder for {agent_type}")
    
    # Test 4: Test video validation
    print("\n🔍 Testing Video Validation:")
    
    # Test with a placeholder video
    test_video = await processor.create_video_placeholder("general", duration=3.0)
    if test_video:
        print(f"\nValidating test video: {os.path.basename(test_video)}")
        
        is_valid = await processor._validate_video(test_video)
        print(f"  Validation result: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        # Get metadata
        metadata = await processor.get_video_metadata(test_video)
        if metadata:
            print(f"  Metadata: {json.dumps(metadata, indent=2)}")
    
    # Test 5: Test video optimization
    print("\n⚡ Testing Video Optimization:")
    
    if test_video:
        print(f"\nOptimizing test video: {os.path.basename(test_video)}")
        
        start_time = time.time()
        optimized_path = await processor.optimize_video_for_wav2lip(test_video)
        optimization_time = time.time() - start_time
        
        if optimized_path:
            original_size = os.path.getsize(test_video) / (1024 * 1024)
            optimized_size = os.path.getsize(optimized_path) / (1024 * 1024)
            print(f"  ✅ Optimized: {os.path.basename(optimized_path)}")
            print(f"  📊 Size: {original_size:.2f} MB → {optimized_size:.2f} MB")
            print(f"  ⏱️ Optimization time: {optimization_time:.2f}s")
        else:
            print(f"  ❌ Optimization failed")
    
    # Test 6: Final status check
    print("\n📊 Final Video Avatar Status:")
    final_videos = processor.get_available_videos()
    
    total_ai_videos = sum(1 for info in final_videos.values() if info['ai_generated'])
    total_size = sum(info['total_size'] for info in final_videos.values())
    
    print(f"\nSummary:")
    print(f"  AI-generated videos: {total_ai_videos}/4")
    print(f"  Total storage used: {total_size:.2f} MB")
    
    for agent_type, info in final_videos.items():
        if info['ai_generated']:
            print(f"  ✅ {agent_type}: AI video available")
        else:
            print(f"  ⚠️ {agent_type}: Using fallback")
    
    print("\n🎉 Video-Only Avatar Approach Test Complete!")
    
    # Instructions for adding AI-generated videos
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS FOR ADDING AI-GENERATED VIDEOS")
    print("=" * 60)
    
    print("\n🎬 To add your AI-generated 5-second videos:")
    print("1. Place your videos in: avatars/videos/ai_generated/")
    print("2. Use these exact filenames:")
    print("   - general_ai.mp4")
    print("   - hotel_ai.mp4")
    print("   - airport_ai.mp4")
    print("   - sales_ai.mp4")
    
    print("\n📋 Video Requirements:")
    print("- Duration: 5 seconds (loopable)")
    print("- Format: MP4 (H.264)")
    print("- Resolution: 512x512 or 720x720")
    print("- Frame Rate: 25 FPS")
    print("- File Size: 2-8 MB per video")
    print("- Content: Natural talking movements")
    
    print("\n🔧 Adding Videos Programmatically:")
    print("```python")
    print("processor = VideoAvatarProcessor()")
    print("await processor.add_ai_generated_video('general', '/path/to/your/video.mp4')")
    print("```")
    
    print("\n🚀 Integration:")
    print("The system will automatically use AI-generated videos when available.")
    print("No code changes needed - just add the videos to the correct directory!")

if __name__ == "__main__":
    asyncio.run(test_video_only_approach()) 