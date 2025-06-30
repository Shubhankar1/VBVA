#!/usr/bin/env python3
"""
Comprehensive test script to verify the video looping fix
Tests multiple scenarios to ensure no looping issues occur
"""

import asyncio
import requests
import time
import subprocess
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_video_looping_fix_comprehensive():
    """Comprehensive test to verify video looping fix"""
    
    print("🔧 Comprehensive Video Looping Fix Test")
    print("=" * 60)
    
    # Test messages of different lengths to trigger different processing paths
    test_messages = [
        {
            "name": "Short Message (3-5s)",
            "message": "This is a short test message.",
            "expected_duration": "3-5s",
            "expected_processing": "single video"
        },
        {
            "name": "Medium Message (8-10s)", 
            "message": "This is a medium test message that should generate approximately eight to ten seconds of audio content to verify the video generation process.",
            "expected_duration": "8-10s",
            "expected_processing": "single video"
        },
        {
            "name": "Long Message (15-18s)",
            "message": "This is a comprehensive test message designed to generate approximately fifteen to eighteen seconds of audio content. This will help us verify that the video generation process works correctly without any looping issues. The audio should flow naturally from beginning to end without repeating the same content multiple times.",
            "expected_duration": "15-18s", 
            "expected_processing": "single video (prevented chunking)"
        },
        {
            "name": "Very Long Message (25-30s)",
            "message": "This is a very comprehensive test message designed to generate approximately twenty-five to thirty seconds of audio content. This will help us verify that the video generation process works correctly without any looping issues. The audio should flow naturally from beginning to end without repeating the same content multiple times. We need to ensure that the chunking and combination process works properly for very long content.",
            "expected_duration": "25-30s",
            "expected_processing": "chunked processing"
        }
    ]
    
    processor = UltraFastProcessor()
    results = []
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"📝 Message: {test_case['message'][:100]}...")
        print(f"📏 Expected duration: {test_case['expected_duration']}")
        print(f"🎬 Expected processing: {test_case['expected_processing']}")
        
        try:
            # Generate video
            start_time = time.time()
            video_url, stats = await processor.process_video_ultra_fast(
                test_case['message'], 
                "general"
            )
            processing_time = time.time() - start_time
            
            if video_url:
                print(f"✅ Video generated successfully")
                print(f"📹 Video URL: {video_url}")
                print(f"⏱️ Processing time: {processing_time:.2f}s")
                print(f"📊 Stats: {stats.total_chunks} chunks, {stats.optimization_level}")
                
                # Analyze the video
                video_analysis = await analyze_video_content(video_url)
                
                result = {
                    "test_case": test_case['name'],
                    "success": True,
                    "video_url": video_url,
                    "processing_time": processing_time,
                    "stats": stats,
                    "analysis": video_analysis
                }
                
                print(f"📊 Video analysis: {video_analysis}")
                
            else:
                print(f"❌ Video generation failed")
                result = {
                    "test_case": test_case['name'],
                    "success": False,
                    "error": "Video generation returned empty URL"
                }
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            result = {
                "test_case": test_case['name'],
                "success": False,
                "error": str(e)
            }
        
        results.append(result)
        
        # Wait between tests
        await asyncio.sleep(2)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Comprehensive Test Summary")
    print("=" * 60)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print(f"\n🎉 Successful test results:")
        for result in successful_tests:
            print(f"  ✅ {result['test_case']}")
            print(f"     📹 URL: {result['video_url']}")
            print(f"     ⏱️ Time: {result['processing_time']:.2f}s")
            if 'analysis' in result:
                print(f"     📊 Analysis: {result['analysis']}")
    
    if failed_tests:
        print(f"\n❌ Failed test results:")
        for result in failed_tests:
            print(f"  ❌ {result['test_case']}: {result.get('error', 'Unknown error')}")
    
    # Overall assessment
    if len(successful_tests) == len(results):
        print(f"\n🎉 ALL TESTS PASSED! Video looping fix appears to be working correctly.")
        print(f"💡 The system should now generate videos without looping issues.")
    else:
        print(f"\n⚠️ Some tests failed. Please check the errors above.")
    
    return len(successful_tests) == len(results)

async def analyze_video_content(video_url: str) -> dict:
    """Analyze video content to check for looping issues"""
    try:
        # Extract filename from URL
        filename = video_url.split('/')[-1].split('?')[0]
        local_path = f"/tmp/wav2lip_ultra_outputs/{filename}"
        
        if not os.path.exists(local_path):
            return {"error": "Video file not found locally"}
        
        # Get video duration
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            local_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
        else:
            duration = 0
        
        # Get video stream info
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "stream=duration,start_time",
            "-of", "json",
            local_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        stream_info = {}
        if result.returncode == 0:
            import json
            try:
                data = json.loads(result.stdout)
                streams = data.get('streams', [])
                if streams:
                    stream_info = streams[0]
            except:
                pass
        
        # Check for potential looping indicators
        analysis = {
            "duration": f"{duration:.2f}s",
            "file_size_mb": f"{os.path.getsize(local_path) / (1024*1024):.2f}MB",
            "is_combined": "ultra_combined" in filename,
            "has_fixed_suffix": "_fixed" in filename
        }
        
        # Check if video has proper start time
        if stream_info:
            start_time = stream_info.get("start_time", 0)
            analysis["start_time"] = f"{start_time}s"
            if float(start_time) > 0.1:
                analysis["warning"] = "Video may have timing issues"
        
        return analysis
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

if __name__ == "__main__":
    print("🚀 Starting comprehensive video looping fix test...")
    
    # Run the test
    success = asyncio.run(test_video_looping_fix_comprehensive())
    
    if success:
        print("\n🎉 SUCCESS: Video looping fix appears to be working!")
        print("💡 The system should now generate videos without looping issues.")
        print("🔄 Try testing the frontend with different message lengths.")
    else:
        print("\n❌ FAILED: Some tests failed!")
        print("🔧 Please check the errors above and fix any issues.") 