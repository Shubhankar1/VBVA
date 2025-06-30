#!/usr/bin/env python3
"""
Test script to identify and reproduce the race condition
where individual chunk URLs are being returned instead of combined video URLs.
"""

import asyncio
import time
import os
import sys
import requests

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_video_url_race_condition():
    """Test to reproduce the race condition where chunk URLs are returned instead of combined URLs"""
    
    print("🧪 Testing video URL race condition...")
    
    # Test text that will definitely trigger chunking
    test_text = "This is a longer test message that should definitely trigger parallel processing with multiple chunks. The system should process this in chunks and then combine them into a single video file. This message is long enough to ensure chunking occurs."
    
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
            
            # Test if the URL is accessible
            try:
                response = requests.head(video_url, timeout=10)
                if response.status_code == 200:
                    print("✅ Combined video URL is accessible")
                    return True
                else:
                    print(f"❌ Combined video URL not accessible: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Error testing combined video URL: {str(e)}")
                return False
                
        elif "ultra_wav2lip_" in video_url:
            print("❌ ERROR: Individual chunk URL returned instead of combined video")
            print("🔧 This is the race condition bug!")
            
            # Check if this individual chunk URL is accessible
            try:
                response = requests.head(video_url, timeout=10)
                if response.status_code == 200:
                    print("⚠️ Individual chunk URL is accessible (but should be combined)")
                else:
                    print(f"❌ Individual chunk URL not accessible: {response.status_code}")
            except Exception as e:
                print(f"❌ Error testing individual chunk URL: {str(e)}")
            
            return False
        else:
            print("⚠️ UNKNOWN: URL pattern not recognized")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

async def test_backend_api_directly():
    """Test the backend API directly to see if it returns the correct URL"""
    
    print("\n🧪 Testing backend API directly...")
    
    try:
        # Test the backend API directly
        response = requests.post(
            "http://localhost:8000/api/v1/generate_video",
            json={
                "message": "This is a longer test message that should trigger chunking and parallel processing to ensure we get the correct combined video URL instead of individual chunk URLs.",
                "agent_type": "general",
                "session_id": None
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get("video_url")
            print(f"✅ Backend API response successful")
            print(f"🎬 Video URL from API: {video_url}")
            
            # Check URL pattern
            if "ultra_combined_" in video_url:
                print("✅ SUCCESS: Backend API returned combined video URL")
                return True
            elif "ultra_wav2lip_" in video_url:
                print("❌ ERROR: Backend API returned individual chunk URL")
                return False
            else:
                print("⚠️ UNKNOWN: Backend API returned unknown URL pattern")
                return False
        else:
            print(f"❌ Backend API failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend API: {str(e)}")
        return False

async def test_video_file_existence():
    """Test if the problematic video file actually exists"""
    
    print("\n🧪 Testing video file existence...")
    
    # Test the specific file from the error
    problematic_url = "http://localhost:8000/api/v1/videos/ultra_wav2lip_e1cbbee4_cfc03ca9_461663_fixed.mp4?t=1751244471"
    
    try:
        # Check if file exists in the directory
        filename = "ultra_wav2lip_e1cbbee4_cfc03ca9_461663_fixed.mp4"
        file_path = f"/tmp/wav2lip_ultra_outputs/{filename}"
        
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
            print(f"📊 File size: {os.path.getsize(file_path)} bytes")
            
            # Test if it's accessible via API
            response = requests.head(problematic_url, timeout=10)
            if response.status_code == 200:
                print("✅ File is accessible via API")
            else:
                print(f"❌ File not accessible via API: {response.status_code}")
        else:
            print(f"❌ File does not exist: {file_path}")
            
            # Check what files exist in the directory
            output_dir = "/tmp/wav2lip_ultra_outputs"
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                recent_files = [f for f in files if "ultra_wav2lip_e1cbbee4" in f]
                if recent_files:
                    print(f"📋 Found similar files: {recent_files}")
                else:
                    print(f"📋 No similar files found. Recent files: {files[-5:]}")
            else:
                print(f"❌ Output directory does not exist: {output_dir}")
                
    except Exception as e:
        print(f"❌ Error testing file existence: {str(e)}")

async def main():
    """Run all tests"""
    print("🚀 Starting video URL race condition tests...")
    print("=" * 60)
    
    # Test 1: Check if the problematic file exists
    await test_video_file_existence()
    
    # Test 2: Test backend API directly
    test2_result = await test_backend_api_directly()
    
    # Test 3: Test the processor directly
    test3_result = await test_video_url_race_condition()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"✅ Backend API test: {'PASSED' if test2_result else 'FAILED'}")
    print(f"✅ Processor test: {'PASSED' if test3_result else 'FAILED'}")
    
    if test2_result and test3_result:
        print("🎉 All tests passed!")
        print("\n💡 The issue might be in the frontend caching or session state management.")
    else:
        print("❌ Some tests failed - race condition detected")
        
        if not test2_result:
            print("\n🔍 Backend API is returning individual chunk URLs instead of combined URLs.")
            print("This suggests a race condition in the video generation process.")
        
        if not test3_result:
            print("\n🔍 The processor is returning individual chunk URLs instead of combined URLs.")
            print("This confirms the race condition in the video generation logic.")

if __name__ == "__main__":
    asyncio.run(main()) 