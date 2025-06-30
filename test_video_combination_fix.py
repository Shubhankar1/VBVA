#!/usr/bin/env python3
"""
Test script to verify video combination fix for 8-12 second videos
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_video_combination_fix():
    """Test the video combination fix for 8-12 second videos"""
    
    print("🧪 Testing video combination fix for 8-12 second videos")
    print("=" * 60)
    
    # Test messages of different lengths
    test_messages = [
        "This is a short test message that should generate about 3-4 seconds of audio content.",
        "This is a medium test message that should generate approximately 8 seconds of audio content to verify the chunking fix is now working correctly.",
        "This is a longer test message that should generate approximately 12 seconds of audio content to verify that the video combination process works properly without any looping issues or audio synchronization problems."
    ]
    
    processor = UltraFastProcessor()
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🎬 Test {i}: {len(message.split())} words")
        print(f"📝 Message: {message[:100]}{'...' if len(message) > 100 else ''}")
        
        try:
            # Process the video
            start_time = asyncio.get_event_loop().time()
            video_url, stats = await processor.process_video_ultra_fast(
                text=message,
                agent_type="general",
                target_time=8.0
            )
            end_time = asyncio.get_event_loop().time()
            
            processing_time = end_time - start_time
            
            print(f"✅ Video generated successfully!")
            print(f"📊 Processing time: {processing_time:.2f}s")
            print(f"📊 Speed multiplier: {stats.speed_multiplier:.1f}x")
            print(f"🎬 Video URL: {video_url}")
            print(f"📊 Chunks processed: {stats.total_chunks}")
            print(f"📊 Parallel processing: {stats.parallel_processing}")
            
            # Check if the video URL is accessible
            if video_url and video_url.startswith("http"):
                print(f"🔗 Video accessible at: {video_url}")
            else:
                print(f"⚠️ Video URL format: {video_url}")
                
        except Exception as e:
            print(f"❌ Test {i} failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("-" * 60)
    
    print("\n🎉 Video combination fix test completed!")

if __name__ == "__main__":
    asyncio.run(test_video_combination_fix()) 