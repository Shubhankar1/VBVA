#!/usr/bin/env python3
"""
Test script for hybrid avatar approach (static images vs video avatars)
"""

import asyncio
import os
import sys
import time
import json
from pathlib import Path

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.enhanced_avatar_processor import EnhancedAvatarProcessor

async def test_hybrid_avatar_approach():
    """Test the hybrid avatar approach"""
    print("🧪 Testing Hybrid Avatar Approach")
    print("=" * 50)
    
    # Initialize the enhanced avatar processor
    processor = EnhancedAvatarProcessor()
    
    # Test 1: Get current avatar statistics
    print("\n📊 Current Avatar Statistics:")
    stats = processor.get_avatar_stats()
    for agent_type, agent_stats in stats.items():
        print(f"\n{agent_type.upper()}:")
        print(f"  Original: {'✅' if agent_stats['has_original'] else '❌'}")
        print(f"  Enhanced: {'✅' if agent_stats['has_enhanced'] else '❌'}")
        print(f"  Video: {'✅' if agent_stats['has_video'] else '❌'}")
        if agent_stats['file_sizes']:
            print(f"  File sizes: {agent_stats['file_sizes']}")
    
    # Test 2: Test optimal avatar selection
    print("\n🎯 Testing Optimal Avatar Selection:")
    
    test_cases = [
        {"agent_type": "general", "content_length": 50, "use_video": False},
        {"agent_type": "general", "content_length": 200, "use_video": True},
        {"agent_type": "hotel", "content_length": 150, "use_video": True},
        {"agent_type": "airport", "content_length": 300, "use_video": True},
        {"agent_type": "sales", "content_length": 100, "use_video": False},
    ]
    
    for test_case in test_cases:
        print(f"\nTesting {test_case['agent_type']} (length: {test_case['content_length']}, video: {test_case['use_video']}):")
        
        avatar_path = await processor.get_optimal_avatar(
            agent_type=test_case['agent_type'],
            content_length=test_case['content_length'],
            use_video=test_case['use_video']
        )
        
        if avatar_path:
            file_size = os.path.getsize(avatar_path) / (1024 * 1024)  # MB
            print(f"  Selected: {os.path.basename(avatar_path)} ({file_size:.2f} MB)")
        else:
            print(f"  ❌ No avatar found")
    
    # Test 3: Create enhanced video avatars (if they don't exist)
    print("\n🎬 Creating Enhanced Video Avatars:")
    
    for agent_type in ["general", "hotel", "airport", "sales"]:
        print(f"\nCreating video avatar for {agent_type}...")
        
        start_time = time.time()
        video_path = await processor.create_enhanced_avatar_video(
            agent_type=agent_type,
            duration=10.0,  # 10 seconds
            fps=25
        )
        creation_time = time.time() - start_time
        
        if video_path:
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            print(f"  ✅ Created: {os.path.basename(video_path)} ({file_size:.2f} MB)")
            print(f"  ⏱️ Creation time: {creation_time:.2f}s")
        else:
            print(f"  ❌ Failed to create video avatar")
    
    # Test 4: Performance comparison
    print("\n⚡ Performance Comparison:")
    
    # Test with short content (should use static image)
    print("\nShort content (50 chars) - should use static image:")
    start_time = time.time()
    short_avatar = await processor.get_optimal_avatar("general", 50, False)
    short_time = time.time() - start_time
    short_size = os.path.getsize(short_avatar) / (1024 * 1024) if short_avatar else 0
    print(f"  Avatar: {os.path.basename(short_avatar)}")
    print(f"  Size: {short_size:.2f} MB")
    print(f"  Selection time: {short_time:.4f}s")
    
    # Test with long content (should use video if available)
    print("\nLong content (300 chars) - should use video if available:")
    start_time = time.time()
    long_avatar = await processor.get_optimal_avatar("general", 300, True)
    long_time = time.time() - start_time
    long_size = os.path.getsize(long_avatar) / (1024 * 1024) if long_avatar else 0
    print(f"  Avatar: {os.path.basename(long_avatar)}")
    print(f"  Size: {long_size:.2f} MB")
    print(f"  Selection time: {long_time:.4f}s")
    
    # Test 5: Final statistics
    print("\n📊 Final Avatar Statistics:")
    final_stats = processor.get_avatar_stats()
    for agent_type, agent_stats in final_stats.items():
        print(f"\n{agent_type.upper()}:")
        print(f"  Original: {'✅' if agent_stats['has_original'] else '❌'}")
        print(f"  Enhanced: {'✅' if agent_stats['has_enhanced'] else '❌'}")
        print(f"  Video: {'✅' if agent_stats['has_video'] else '❌'}")
        if agent_stats['file_sizes']:
            print(f"  File sizes: {agent_stats['file_sizes']}")
    
    print("\n🎉 Hybrid Avatar Approach Test Complete!")
    
    # Summary and recommendations
    print("\n" + "=" * 60)
    print("📋 RECOMMENDATIONS")
    print("=" * 60)
    
    print("\n🎯 For Your VBVA Project:")
    print("1. ✅ Use enhanced static images for short responses (< 100 chars)")
    print("2. 🎬 Use video avatars for longer responses (> 100 chars)")
    print("3. 🔄 Implement intelligent switching based on content length")
    print("4. 💾 Cache both image and video avatars for performance")
    print("5. 🎨 Create subtle video movements for natural appearance")
    
    print("\n📈 Expected Benefits:")
    print("- Better lip-sync quality with video avatars")
    print("- Faster processing for short content with static images")
    print("- More engaging user experience")
    print("- Optimal resource usage")
    
    print("\n🚀 Next Steps:")
    print("1. Integrate EnhancedAvatarProcessor into your lip-sync service")
    print("2. Update avatar selection logic in your video generation pipeline")
    print("3. Test with real content to validate improvements")
    print("4. Monitor performance and user feedback")

if __name__ == "__main__":
    asyncio.run(test_hybrid_avatar_approach()) 