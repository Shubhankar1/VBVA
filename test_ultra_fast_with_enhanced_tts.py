#!/usr/bin/env python3
"""
Test Ultra-Fast Video Generation with Enhanced TTS Service
"""

import asyncio
import sys
import os
import json

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_ultra_fast_video():
    """Test ultra-fast video generation with enhanced TTS"""
    
    try:
        from services.ultra_fast_processor import UltraFastProcessor
        
        print("🚀 Testing Ultra-Fast Video Generation with Enhanced TTS...")
        
        # Initialize the processor
        processor = UltraFastProcessor()
        
        # Test text
        test_text = "Hello, this is a test of the ultra-fast video generation with enhanced TTS service and fallback options."
        
        print(f"📝 Test text: '{test_text}'")
        print(f"🎯 Target: Generate video in under 8 seconds")
        
        # Generate video
        start_time = asyncio.get_event_loop().time()
        
        video_url, stats = await processor.process_video_ultra_fast(
            text=test_text,
            agent_type="general",
            target_time=8.0  # Target 8 seconds
        )
        
        end_time = asyncio.get_event_loop().time()
        processing_time = end_time - start_time
        
        print(f"\n📊 Results:")
        print(f"   ⏱️  Total processing time: {processing_time:.2f}s")
        print(f"   🎬 Video URL: {video_url}")
        print(f"   📈 Performance stats: {stats}")
        
        # Check if video was generated successfully
        if video_url and video_url.startswith('/'):
            # Convert local path to check if file exists
            video_path = video_url
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                print(f"   📏 Video file size: {file_size} bytes")
                print(f"   ✅ Video generated successfully!")
                
                if processing_time < 8.0:
                    print(f"   🚀 Ultra-fast target achieved! ({processing_time:.2f}s < 8.0s)")
                else:
                    print(f"   ⚠️  Processing time exceeded target ({processing_time:.2f}s > 8.0s)")
            else:
                print(f"   ❌ Video file not found at {video_path}")
        else:
            print(f"   ✅ Video URL generated: {video_url}")
        
        # Test with rate limiting simulation
        print(f"\n🎤 Testing fallback behavior with multiple requests...")
        
        # Make multiple requests quickly to test fallback
        tasks = []
        for i in range(3):
            task = processor.process_video_ultra_fast(
                text=f"Test message {i+1} for fallback testing.",
                agent_type="general",
                target_time=8.0
            )
            tasks.append(task)
        
        start_time = asyncio.get_event_loop().time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = asyncio.get_event_loop().time()
        
        print(f"📊 Batch processing results:")
        print(f"   ⏱️  Batch processing time: {end_time - start_time:.2f}s")
        
        success_count = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   ❌ Request {i+1} failed: {result}")
            else:
                success_count += 1
                if isinstance(result, tuple) and len(result) >= 2:
                    video_url, stats = result
                    print(f"   ✅ Request {i+1} successful: {video_url}")
                else:
                    print(f"   ⚠️  Request {i+1} completed with unexpected result format")
        
        print(f"   📈 Success rate: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
        
        print("\n🎉 Ultra-fast video generation test completed!")
        
    except ImportError as e:
        print(f"❌ Failed to import UltraFastProcessor: {e}")
        print("Make sure the ultra_fast_processor.py file exists and all dependencies are installed.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ultra_fast_video()) 