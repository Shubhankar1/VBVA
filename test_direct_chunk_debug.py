#!/usr/bin/env python3
"""
Direct test to see chunk processing debug output
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_direct_chunk_processing():
    """Test chunk processing directly to see debug output"""
    print("🔍 Direct Chunk Processing Debug Test")
    print("=" * 60)
    
    processor = UltraFastProcessor()
    
    # Test message that should generate ~16 seconds of audio
    test_message = "In the depths of consciousness, whispering secrets of the universe to those who dare to listen with open hearts. This message should generate approximately sixteen seconds of audio content to test the chunking and combination logic."
    
    print(f"📝 Test message: {test_message}")
    print(f"📏 Message length: {len(test_message)} characters")
    
    try:
        # Process video with ultra-fast settings
        result = await processor.process_video_ultra_fast(
            text=test_message,
            agent_type="general",
            target_time=8.0
        )
        
        video_url, stats = result
        
        print(f"\n✅ Direct processing completed")
        print(f"📹 Video URL: {video_url}")
        print(f"📊 Stats: {stats}")
        
        return True, video_url
        
    except Exception as e:
        print(f"❌ Direct processing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

if __name__ == "__main__":
    print("🚀 Direct Chunk Processing Debug Test")
    print("=" * 60)
    
    # Run the async test
    success, video_url = asyncio.run(test_direct_chunk_processing())
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ Test: PASSED")
        print(f"   📹 Video URL: {video_url}")
        
        print("\n🔍 Manual Verification:")
        print("1. Open the video URL in a browser")
        print("2. Check if the complete message is covered")
        print("3. Verify no looping of the first 8 seconds")
        print("4. Audio should flow naturally from start to finish")
        
        print("\n🎉 Test completed! Please manually verify the video.")
    else:
        print("❌ Test: FAILED")
        print("\n⚠️ The looping issue may still persist.") 