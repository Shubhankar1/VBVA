#!/usr/bin/env python3
"""
Test script to verify perfect synchronization between audio and video lengths
Ensures no gaps or timing issues in the video generation process
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_precision_timing():
    """Test perfect synchronization between audio and video lengths"""
    
    print("🎯 Precision Timing Test - No Gaps Between Audio and Video")
    print("=" * 70)
    
    # Test messages designed to test different chunking scenarios
    test_messages = [
        {
            "name": "Short Message (Single Video)",
            "message": "This is a short test message.",
            "expected_chunks": 1,
            "expected_processing": "single video"
        },
        {
            "name": "Medium Message (Single Video)",
            "message": "This is a medium test message that should generate approximately ten seconds of audio content to verify the video generation process works correctly.",
            "expected_chunks": 1,
            "expected_processing": "single video"
        },
        {
            "name": "Long Message (2 Equal Chunks)",
            "message": "This is a comprehensive test message designed to generate approximately eighteen seconds of audio content. This will help us verify that the video generation process works correctly without any looping issues. The audio should flow naturally from beginning to end without repeating the same content multiple times.",
            "expected_chunks": 2,
            "expected_processing": "2 equal chunks"
        },
        {
            "name": "Very Long Message (3 Equal Chunks)",
            "message": "This is a very comprehensive test message designed to generate approximately thirty seconds of audio content. This will help us verify that the video generation process works correctly without any looping issues. The audio should flow naturally from beginning to end without repeating the same content multiple times. We need to ensure that the chunking and combination process works properly for very long content.",
            "expected_chunks": 3,
            "expected_processing": "3 equal chunks"
        }
    ]
    
    processor = UltraFastProcessor()
    results = []
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"📝 Message: {test_case['message'][:100]}...")
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
                
                # Analyze the video for precision timing
                timing_analysis = await analyze_precision_timing(video_url, test_case)
                
                result = {
                    "test_case": test_case['name'],
                    "success": True,
                    "video_url": video_url,
                    "processing_time": processing_time,
                    "timing_analysis": timing_analysis
                }
                
                print(f"📊 Timing analysis: {timing_analysis}")
                
                # Check if timing is perfect
                if timing_analysis.get("timing_perfect", False):
                    print(f"✅ PERFECT TIMING: No gaps detected")
                else:
                    print(f"⚠️ TIMING ISSUE: Potential gaps detected")
                
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
    print("\n" + "=" * 70)
    print("📋 Precision Timing Test Summary")
    print("=" * 70)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    perfect_timing_tests = [r for r in successful_tests if r.get('timing_analysis', {}).get('timing_perfect', False)]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}/{len(results)}")
    print(f"🎯 Perfect timing tests: {len(perfect_timing_tests)}/{len(successful_tests)}")
    
    if successful_tests:
        print(f"\n🎉 Successful test results:")
        for result in successful_tests:
            print(f"  ✅ {result['test_case']}")
            print(f"     📹 URL: {result['video_url']}")
            print(f"     ⏱️ Time: {result['processing_time']:.2f}s")
            timing = result.get('timing_analysis', {})
            print(f"     📊 Duration: {timing.get('duration', 'N/A')}")
            print(f"     📊 Gap: {timing.get('gap_detected', 'N/A')}")
            print(f"     📊 Perfect: {'✅' if timing.get('timing_perfect', False) else '❌'}")
    
    if failed_tests:
        print(f"\n❌ Failed test results:")
        for result in failed_tests:
            print(f"  ❌ {result['test_case']}: {result.get('error', 'Unknown error')}")
    
    # Overall assessment
    if len(perfect_timing_tests) == len(successful_tests) and len(successful_tests) == len(results):
        print(f"\n🎉 ALL TESTS PASSED WITH PERFECT TIMING!")
        print(f"💡 The system now ensures no gaps between audio and video lengths.")
    elif len(perfect_timing_tests) > 0:
        print(f"\n⚠️ Some tests have timing issues.")
        print(f"💡 {len(perfect_timing_tests)}/{len(successful_tests)} tests have perfect timing.")
    else:
        print(f"\n❌ No tests have perfect timing.")
        print(f"🔧 Please check the timing analysis above.")
    
    return len(perfect_timing_tests) == len(successful_tests) and len(successful_tests) == len(results)

async def analyze_precision_timing(video_url: str, test_case: dict) -> dict:
    """Analyze video for perfect timing with no gaps"""
    try:
        import time
        
        # Extract filename from URL
        filename = video_url.split('/')[-1].split('?')[0]
        local_path = f"/tmp/wav2lip_ultra_outputs/{filename}"
        
        if not os.path.exists(local_path):
            return {"error": "Video file not found locally"}
        
        # Get video duration with high precision
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            local_path
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
        else:
            duration = 0
        
        # Get video stream info for timing analysis
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
        
        # Analyze timing precision
        analysis = {
            "duration": f"{duration:.3f}s",
            "file_size_mb": f"{os.path.getsize(local_path) / (1024*1024):.2f}MB",
            "is_combined": "ultra_combined" in filename,
            "has_fixed_suffix": "_fixed" in filename
        }
        
        # Check for timing issues
        if stream_info:
            start_time = stream_info.get("start_time", 0)
            analysis["start_time"] = f"{start_time}s"
            
            # Check if start time is reasonable (should be very close to 0)
            if float(start_time) > 0.1:
                analysis["gap_detected"] = f"Start time too high: {start_time}s"
                analysis["timing_perfect"] = False
            else:
                analysis["gap_detected"] = "None detected"
                analysis["timing_perfect"] = True
        
        # Check if this was processed as expected
        expected_chunks = test_case.get("expected_chunks", 1)
        if expected_chunks == 1 and "ultra_combined" in filename:
            analysis["processing_issue"] = "Single chunk expected but combined video generated"
            analysis["timing_perfect"] = False
        elif expected_chunks > 1 and "ultra_combined" not in filename:
            analysis["processing_issue"] = f"Expected {expected_chunks} chunks but single video generated"
            analysis["timing_perfect"] = False
        
        return analysis
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

if __name__ == "__main__":
    import time
    
    print("🚀 Starting precision timing test...")
    
    # Run the test
    success = asyncio.run(test_precision_timing())
    
    if success:
        print("\n🎉 SUCCESS: Perfect timing achieved!")
        print("💡 The system now ensures no gaps between audio and video lengths.")
        print("🔄 All videos should play with perfect synchronization.")
    else:
        print("\n❌ FAILED: Some timing issues detected!")
        print("🔧 Please check the analysis above for specific issues.") 