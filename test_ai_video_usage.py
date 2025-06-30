#!/usr/bin/env python3
"""
Test script to verify AI-generated video usage
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.video_avatar_processor import VideoAvatarProcessor
from services.ultra_fast_processor import UltraFastProcessor

async def test_video_avatar_processor():
    """Test the video avatar processor directly"""
    print("🧪 Testing Video Avatar Processor...")
    
    processor = VideoAvatarProcessor()
    
    # Test each agent type
    for agent_type in ["general", "hotel", "airport", "sales"]:
        print(f"\n🎬 Testing {agent_type} agent:")
        try:
            avatar_path = await processor.get_video_avatar(agent_type)
            print(f"   ✅ Avatar path: {avatar_path}")
            
            # Check if it's an AI-generated video
            if "ai_generated" in avatar_path and avatar_path.endswith(".mp4"):
                print(f"   🎯 Using AI-generated video!")
            elif avatar_path.endswith(".mp4"):
                print(f"   📹 Using video (not AI-generated)")
            else:
                print(f"   🖼️ Using static image")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def test_ultra_fast_processor():
    """Test the ultra-fast processor avatar selection"""
    print("\n🧪 Testing Ultra-Fast Processor...")
    
    processor = UltraFastProcessor()
    
    # Test each agent type
    for agent_type in ["general", "hotel", "airport", "sales"]:
        print(f"\n🎬 Testing {agent_type} agent:")
        try:
            avatar_path = await processor._prepare_avatar_ultra_fast(agent_type)
            print(f"   ✅ Avatar path: {avatar_path}")
            
            # Check if it's an AI-generated video
            if "ai_generated" in avatar_path and avatar_path.endswith(".mp4"):
                print(f"   🎯 Using AI-generated video!")
            elif avatar_path.endswith(".mp4"):
                print(f"   📹 Using video (not AI-generated)")
            else:
                print(f"   🖼️ Using static image")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def test_available_videos():
    """Test what videos are available"""
    print("\n🧪 Testing Available Videos...")
    
    processor = VideoAvatarProcessor()
    available = processor.get_available_videos()
    
    for agent_type, info in available.items():
        print(f"\n🎬 {agent_type.upper()} agent:")
        for video_type, path in info.items():
            if path and isinstance(path, str) and os.path.exists(path):
                print(f"   ✅ {video_type}: {os.path.basename(path)}")
            else:
                print(f"   ❌ {video_type}: Not found")

async def main():
    """Run all tests"""
    print("🚀 Testing AI-Generated Video Usage")
    print("=" * 50)
    
    await test_available_videos()
    await test_video_avatar_processor()
    await test_ultra_fast_processor()
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == "__main__":
    asyncio.run(main()) 