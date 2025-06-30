#!/usr/bin/env python3
"""
Debug Ultra-Fast Processor
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def debug_ultra_fast():
    """Debug the ultra-fast processor"""
    
    try:
        from services.ultra_fast_processor import UltraFastProcessor
        
        print("🔍 Debugging Ultra-Fast Processor...")
        
        # Initialize the processor
        processor = UltraFastProcessor()
        
        # Test text
        test_text = "Debug test for ultra-fast processor."
        
        print(f"📝 Test text: '{test_text}'")
        
        # Check directories before processing
        print(f"\n📁 Before processing:")
        print(f"   Regular outputs: {len(os.listdir('/tmp/wav2lip_outputs/')) if os.path.exists('/tmp/wav2lip_outputs/') else 'N/A'}")
        print(f"   Ultra outputs: {len(os.listdir('/tmp/wav2lip_ultra_outputs/')) if os.path.exists('/tmp/wav2lip_ultra_outputs/') else 'N/A'}")
        
        # Generate video
        start_time = asyncio.get_event_loop().time()
        
        video_url, stats = await processor.process_video_ultra_fast(
            text=test_text,
            agent_type="general",
            target_time=8.0
        )
        
        end_time = asyncio.get_event_loop().time()
        processing_time = end_time - start_time
        
        print(f"\n📊 Results:")
        print(f"   ⏱️  Processing time: {processing_time:.2f}s")
        print(f"   🎬 Video URL: {video_url}")
        print(f"   📈 Stats: {stats}")
        
        # Check directories after processing
        print(f"\n📁 After processing:")
        print(f"   Regular outputs: {len(os.listdir('/tmp/wav2lip_outputs/')) if os.path.exists('/tmp/wav2lip_outputs/') else 'N/A'}")
        print(f"   Ultra outputs: {len(os.listdir('/tmp/wav2lip_ultra_outputs/')) if os.path.exists('/tmp/wav2lip_ultra_outputs/') else 'N/A'}")
        
        # List recent files in both directories
        if os.path.exists('/tmp/wav2lip_ultra_outputs/'):
            ultra_files = os.listdir('/tmp/wav2lip_ultra_outputs/')
            if ultra_files:
                print(f"   Ultra files: {ultra_files}")
            else:
                print(f"   Ultra files: (empty)")
        
        if os.path.exists('/tmp/wav2lip_outputs/'):
            regular_files = os.listdir('/tmp/wav2lip_outputs/')
            recent_files = [f for f in regular_files if f.endswith('.mp4')][-5:]
            print(f"   Recent regular files: {recent_files}")
        
        # Test if the video URL is accessible
        if video_url and video_url.startswith('http'):
            print(f"\n🔗 Testing video URL accessibility...")
            import httpx
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.head(video_url)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print(f"   ✅ Video accessible!")
                    else:
                        print(f"   ❌ Video not accessible")
            except Exception as e:
                print(f"   ❌ Error accessing video: {e}")
        
        print("\n🎉 Debug completed!")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ultra_fast()) 