#!/usr/bin/env python3
"""
Test script to reproduce and fix the video URL issue
where individual chunk URLs are being returned instead of combined video URLs.
"""

import asyncio
import time
import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_video_url_generation():
    """Test video URL generation to ensure combined videos are returned"""
    
    print("🧪 Testing video URL generation...")
    
    # Test text that will trigger chunking
    test_text = "This is a longer test message that should trigger parallel processing with multiple chunks to ensure we get the combined video URL instead of individual chunk URLs. The system should process this in chunks and then combine them into a single video file."
    
    processor = UltraFastProcessor()
    
    try:
        print(f"📝 Test text length: {len(test_text)} characters")
        
        # Generate video with ultra-fast processing
        start_time = time.time()
        video_url, stats = await processor.process_video_ultra_fast(
            text=test_text,
            agent_type="general",
            target_time=8.0
        )
        total_time = time.time() - start_time
        
        print(f"✅ Video generation completed in {total_time:.2f}s")
        print(f"🎬 Video URL: {video_url}")
        
        # Check if the URL is for a combined video (not individual chunk)
        if "ultra_combined_" in video_url:
            print("✅ SUCCESS: Combined video URL returned")
            return True
        elif "ultra_wav2lip_" in video_url:
            print("❌ ERROR: Individual chunk URL returned instead of combined video")
            print("🔧 This is the bug we need to fix!")
            return False
        else:
            print("⚠️ UNKNOWN: URL pattern not recognized")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

async def test_single_video_generation():
    """Test single video generation to ensure it works correctly"""
    
    print("\n🧪 Testing single video generation...")
    
    # Test text that should not trigger chunking
    test_text = "This is a short test message."
    
    processor = UltraFastProcessor()
    
    try:
        print(f"📝 Test text length: {len(test_text)} characters")
        
        # Generate video with ultra-fast processing
        start_time = time.time()
        video_url, stats = await processor.process_video_ultra_fast(
            text=test_text,
            agent_type="general",
            target_time=8.0
        )
        total_time = time.time() - start_time
        
        print(f"✅ Video generation completed in {total_time:.2f}s")
        print(f"🎬 Video URL: {video_url}")
        
        # Check if the URL is for a single video
        if "ultra_wav2lip_" in video_url:
            print("✅ SUCCESS: Single video URL returned (expected for short content)")
            return True
        elif "ultra_combined_" in video_url:
            print("⚠️ WARNING: Combined video URL returned for short content (unexpected)")
            return False
        else:
            print("⚠️ UNKNOWN: URL pattern not recognized")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting video URL generation tests...")
    print("=" * 60)
    
    # Test 1: Long content that should trigger chunking
    test1_result = await test_video_url_generation()
    
    # Test 2: Short content that should not trigger chunking
    test2_result = await test_single_video_generation()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"✅ Long content test: {'PASSED' if test1_result else 'FAILED'}")
    print(f"✅ Short content test: {'PASSED' if test2_result else 'FAILED'}")
    
    if test1_result and test2_result:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed - investigation needed")
        
        if not test1_result:
            print("\n🔍 Investigating long content test failure...")
            print("The issue is that individual chunk URLs are being returned")
            print("instead of combined video URLs for long content.")
            print("This needs to be fixed in the ultra-fast processor.")

if __name__ == "__main__":
    asyncio.run(main()) 