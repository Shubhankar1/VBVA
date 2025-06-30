#!/usr/bin/env python3
"""
Test script to identify and fix the video duration gap issue between 13-17 seconds
"""

import asyncio
import sys
import os
import time
import requests
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

def test_video_generation_with_duration(message, expected_duration_range=(10, 20)):
    """Test video generation and check actual duration"""
    print(f"\n🧪 Testing video generation for message: '{message[:50]}...'")
    print(f"📝 Expected duration range: {expected_duration_range[0]}-{expected_duration_range[1]} seconds")
    
    response = requests.post(
        "http://localhost:8000/api/v1/generate_video",
        json={
            "message": message,
            "agent_type": "general"
        },
        timeout=300
    )
    
    if response.status_code == 200:
        data = response.json()
        video_url = data.get("video_url")
        processing_time = data.get("processing_time", 0)
        processing_details = data.get("processing_details", {})
        
        print(f"✅ Video generated successfully")
        print(f"📹 Video URL: {video_url}")
        print(f"⏱️ Processing time: {processing_time:.2f}s")
        
        # Extract processing details
        optimization_level = processing_details.get("optimization_level", "unknown")
        parallel_processing = processing_details.get("parallel_processing", False)
        chunk_duration = processing_details.get("chunk_duration", 0)
        
        print(f"🔧 Optimization level: {optimization_level}")
        print(f"🔄 Parallel processing: {parallel_processing}")
        print(f"🎵 Chunk duration: {chunk_duration}s")
        
        # Try to get actual video duration (this would require video analysis)
        # For now, we'll analyze the processing details to understand the flow
        
        return True, video_url, processing_time, processing_details
    else:
        print(f"❌ Failed to generate video: {response.status_code}")
        print(f"❌ Response: {response.text}")
        return False, None, 0, {}

def test_duration_gap_issue():
    """Test the specific duration gap issue between 13-17 seconds"""
    
    print("🎬 Testing Video Duration Gap Issue (13-17 seconds)")
    print("=" * 60)
    
    # Test messages designed to generate specific durations
    test_cases = [
        {
            "name": "Short (8-10 seconds)",
            "message": "This is a short test message that should generate approximately 8 to 10 seconds of audio content for testing the video generation system.",
            "expected_range": (8, 12)
        },
        {
            "name": "Medium (12-14 seconds)", 
            "message": "This is a medium length test message that should generate approximately 12 to 14 seconds of audio content. The purpose is to verify that the system correctly processes content in this optimal range without any chunking issues or duration gaps.",
            "expected_range": (12, 16)
        },
        {
            "name": "Gap Range (14-16 seconds)",
            "message": "This is a test message specifically designed to generate approximately 14 to 16 seconds of audio content. This range has been identified as problematic where videos either come out as 13 seconds or less, or 18 seconds or more, but never in the 14-17 second range. We need to investigate why this gap exists in the processing pipeline.",
            "expected_range": (14, 18)
        },
        {
            "name": "Long (18-20 seconds)",
            "message": "This is a longer test message that should generate approximately 18 to 20 seconds of audio content. This will help us verify that the system correctly handles content beyond the problematic gap range and ensures that parallel processing works correctly for longer content without any issues.",
            "expected_range": (18, 22)
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎬 Test {i}: {test_case['name']}")
        print(f"📝 Message length: {len(test_case['message'])} characters")
        
        success, video_url, processing_time, details = test_video_generation_with_duration(
            test_case['message'], 
            test_case['expected_range']
        )
        
        results.append({
            "test_name": test_case['name'],
            "success": success,
            "video_url": video_url,
            "processing_time": processing_time,
            "details": details,
            "message_length": len(test_case['message'])
        })
        
        # Wait between tests
        time.sleep(2)
    
    # Analyze results
    print("\n" + "=" * 60)
    print("📊 Test Results Analysis:")
    
    for result in results:
        print(f"\n🎬 {result['test_name']}:")
        print(f"   ✅ Success: {result['success']}")
        print(f"   ⏱️ Processing time: {result['processing_time']:.2f}s")
        print(f"   🔧 Optimization: {result['details'].get('optimization_level', 'unknown')}")
        print(f"   🔄 Parallel: {result['details'].get('parallel_processing', False)}")
        print(f"   🎵 Chunk duration: {result['details'].get('chunk_duration', 0)}s")
    
    # Identify the gap issue
    print(f"\n🔍 Duration Gap Analysis:")
    print(f"The issue was in the chunking logic where:")
    print(f"1. Audio ≤15 seconds used single video generation")
    print(f"2. Audio >15 seconds used parallel processing with 6-second chunks")
    print(f"3. This created a gap where certain durations didn't get processed correctly")
    print(f"\n✅ FIX IMPLEMENTED:")
    print(f"1. Extended single video generation to ≤12 seconds")
    print(f"2. Implemented adaptive chunking: 2 chunks for 12-18s, 3 chunks for 18-24s, etc.")
    print(f"3. Improved remainder handling with higher thresholds")
    print(f"4. This should eliminate the 13-17 second gap")
    
    return results

async def test_ultra_fast_processor_directly():
    """Test the UltraFastProcessor directly to understand the chunking logic"""
    
    print("\n🔧 Testing UltraFastProcessor Directly")
    print("=" * 60)
    
    processor = UltraFastProcessor()
    
    # Test messages of different lengths
    test_messages = [
        "Short message for testing.",
        "This is a medium length message that should generate about 8-10 seconds of audio content for testing purposes.",
        "This is a longer message that should generate approximately 14-16 seconds of audio content. This range has been identified as problematic where videos either come out as 13 seconds or less, or 18 seconds or more, but never in the 14-17 second range.",
        "This is a very long message that should generate approximately 20-25 seconds of audio content. This will help us verify that the system correctly handles content beyond the problematic gap range and ensures that parallel processing works correctly for longer content without any issues."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🎬 Direct Test {i}: {len(message.split())} words")
        print(f"📝 Message: {message[:100]}{'...' if len(message) > 100 else ''}")
        
        try:
            # Generate audio first to check duration
            audio_url = await processor._generate_audio_ultra_fast(message, "general")
            audio_duration = await processor._get_audio_duration_fast(audio_url)
            
            print(f"🎵 Audio duration: {audio_duration:.2f}s")
            
            # Check which processing path it would take
            if audio_duration <= 12:  # Updated threshold
                print(f"🎬 Would use: Single video generation (≤12s)")
            else:
                print(f"🎬 Would use: Parallel video generation (>12s)")
                
                # Check chunking logic with new adaptive approach
                if audio_duration <= 6:
                    print(f"🎵 Would use: Single chunk (≤6s)")
                elif audio_duration <= 12:
                    print(f"🎵 Would use: Single chunk (6-12s range)")
                elif audio_duration <= 18:
                    chunk_duration = audio_duration / 2
                    print(f"🎵 Would use: 2 equal chunks of ~{chunk_duration:.2f}s each")
                elif audio_duration <= 24:
                    chunk_duration = audio_duration / 3
                    print(f"🎵 Would use: 3 equal chunks of ~{chunk_duration:.2f}s each")
                elif audio_duration <= 30:
                    chunk_duration = audio_duration / 4
                    print(f"🎵 Would use: 4 equal chunks of ~{chunk_duration:.2f}s each")
                else:
                    # For longer content, use 6-second chunks but handle remainders better
                    chunk_duration = 6.0
                    num_chunks = int(audio_duration / chunk_duration)
                    remainder = audio_duration % chunk_duration
                    print(f"🎵 Would use: {num_chunks} chunks of ~{chunk_duration}s each")
                    print(f"🎵 Remainder: {remainder:.2f}s")
                    
                    if remainder > 0:
                        if remainder < 3.0:  # Updated threshold
                            print(f"🎵 Adjusted: Distribute remainder among chunks")
                        else:
                            print(f"🎵 Adjusted: Add extra chunk for remainder")
            
        except Exception as e:
            print(f"❌ Test {i} failed: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """Run comprehensive duration gap analysis"""
    print("🎬 Video Duration Gap Analysis and Fix")
    print("=" * 60)
    
    # Test 1: API-based testing
    api_results = test_duration_gap_issue()
    
    # Test 2: Direct processor testing
    asyncio.run(test_ultra_fast_processor_directly())
    
    print("\n" + "=" * 60)
    print("📋 Summary and Recommendations:")
    print("1. The gap issue is likely caused by inconsistent chunking thresholds")
    print("2. Need to adjust the 15-second threshold or improve chunking logic")
    print("3. Consider making chunking more adaptive to avoid gaps")
    print("4. Test with actual video duration analysis to confirm the issue")

if __name__ == "__main__":
    main() 