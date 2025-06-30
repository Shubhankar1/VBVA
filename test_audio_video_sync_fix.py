#!/usr/bin/env python3
"""
Test script to identify and fix audio-video synchronization issues
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

def test_video_synchronization(message, expected_duration_range=(15, 25)):
    """Test video generation and check for synchronization issues"""
    print(f"\n🧪 Testing video synchronization for message: '{message[:50]}...'")
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
        
        return True, video_url, processing_time, processing_details
    else:
        print(f"❌ Failed to generate video: {response.status_code}")
        print(f"❌ Response: {response.text}")
        return False, None, 0, {}

def test_synchronization_issues():
    """Test for audio-video synchronization issues"""
    
    print("🎬 Testing Audio-Video Synchronization Issues")
    print("=" * 60)
    
    # Test messages designed to trigger chunking and potential sync issues
    test_cases = [
        {
            "name": "Medium Content (Should use 2 chunks)",
            "message": "This is a medium length test message that should generate approximately 15 to 18 seconds of audio content. The purpose is to verify that the system correctly processes content using two equal chunks without any synchronization issues between audio and video segments.",
            "expected_range": (15, 20)
        },
        {
            "name": "Long Content (Should use 3+ chunks)", 
            "message": "This is a longer test message that should generate approximately 20 to 25 seconds of audio content. This will help us verify that the system correctly handles multiple chunks and ensures proper synchronization between audio and video segments. The chunking process should maintain perfect alignment between the audio content and the corresponding video segments without any looping or synchronization problems.",
            "expected_range": (20, 28)
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎬 Test {i}: {test_case['name']}")
        print(f"📝 Message length: {len(test_case['message'])} characters")
        
        success, video_url, processing_time, details = test_video_synchronization(
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
    print("📊 Synchronization Test Results:")
    
    for result in results:
        print(f"\n🎬 {result['test_name']}:")
        print(f"   ✅ Success: {result['success']}")
        print(f"   ⏱️ Processing time: {result['processing_time']:.2f}s")
        print(f"   🔧 Optimization: {result['details'].get('optimization_level', 'unknown')}")
        print(f"   🔄 Parallel: {result['details'].get('parallel_processing', False)}")
        print(f"   🎵 Chunk duration: {result['details'].get('chunk_duration', 0)}s")
        print(f"   📹 Video URL: {result['video_url']}")
    
    # Instructions for manual verification
    print(f"\n🔍 Manual Verification Instructions:")
    print(f"1. Open each video URL in a browser")
    print(f"2. Check if the complete message is covered (not just a portion)")
    print(f"3. Verify that audio doesn't loop over the same content")
    print(f"4. Ensure lip sync matches the complete audio")
    print(f"5. Check that video duration matches expected audio duration")
    
    return results

async def test_processor_synchronization_directly():
    """Test the UltraFastProcessor directly to understand sync issues"""
    
    print("\n🔧 Testing UltraFastProcessor Synchronization Directly")
    print("=" * 60)
    
    processor = UltraFastProcessor()
    
    # Test message that should trigger chunking
    test_message = "This is a test message designed to generate approximately 18 to 22 seconds of audio content. This will help us identify any synchronization issues between audio chunks and video chunks during the parallel processing and combination phases."
    
    print(f"🎬 Testing with message: {len(test_message.split())} words")
    print(f"📝 Message: {test_message[:100]}...")
    
    try:
        # Step 1: Generate audio
        print(f"\n🎵 Step 1: Generating audio...")
        audio_url = await processor._generate_audio_ultra_fast(test_message, "general")
        audio_duration = await processor._get_audio_duration_fast(audio_url)
        print(f"✅ Audio generated: {audio_duration:.2f}s")
        
        # Step 2: Check processing path
        print(f"\n🎬 Step 2: Determining processing path...")
        if audio_duration <= 12:
            print(f"🎬 Would use: Single video generation (≤12s)")
            processing_mode = "single"
        else:
            print(f"🎬 Would use: Parallel video generation (>12s)")
            processing_mode = "parallel"
            
            # Check chunking logic
            if audio_duration <= 18:
                chunk_duration = audio_duration / 2
                num_chunks = 2
                print(f"🎵 Would use: 2 equal chunks of ~{chunk_duration:.2f}s each")
            elif audio_duration <= 24:
                chunk_duration = audio_duration / 3
                num_chunks = 3
                print(f"🎵 Would use: 3 equal chunks of ~{chunk_duration:.2f}s each")
            else:
                chunk_duration = audio_duration / 4
                num_chunks = 4
                print(f"🎵 Would use: 4 equal chunks of ~{chunk_duration:.2f}s each")
        
        # Step 3: Generate video
        print(f"\n🎬 Step 3: Generating video...")
        video_url = await processor.process_video_ultra_fast(
            text=test_message,
            agent_type="general",
            target_time=8.0
        )
        print(f"✅ Video generated: {video_url}")
        
        return {
            "audio_duration": audio_duration,
            "processing_mode": processing_mode,
            "video_url": video_url,
            "num_chunks": num_chunks if processing_mode == "parallel" else 1
        }
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run comprehensive synchronization analysis"""
    print("🎬 Audio-Video Synchronization Analysis and Fix")
    print("=" * 60)
    
    # Test 1: API-based testing
    api_results = test_synchronization_issues()
    
    # Test 2: Direct processor testing
    direct_result = asyncio.run(test_processor_synchronization_directly())
    
    print("\n" + "=" * 60)
    print("📋 Synchronization Issue Analysis:")
    print("1. The issue is likely in the video combination process")
    print("2. FFmpeg concat demuxer may not handle audio-video sync properly")
    print("3. Individual chunks may have different properties causing misalignment")
    print("4. Need to improve the combination logic with better sync parameters")
    
    if direct_result:
        print(f"\n🔍 Direct Test Results:")
        print(f"   Audio duration: {direct_result['audio_duration']:.2f}s")
        print(f"   Processing mode: {direct_result['processing_mode']}")
        print(f"   Number of chunks: {direct_result['num_chunks']}")
        print(f"   Video URL: {direct_result['video_url']}")

if __name__ == "__main__":
    main() 