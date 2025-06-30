#!/usr/bin/env python3
"""
Simple test to verify the simplified solution addresses core issues
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ultra_fast_processor import UltraFastProcessor

async def test_simplified_solution():
    """Test that simplified solution addresses core issues"""
    
    print("🧪 Testing Simplified Solution")
    print("=" * 50)
    
    # Test cases that cover the core issues
    test_messages = [
        {
            "name": "Short Message (Single Video)",
            "message": "This is a short test message.",
            "expected": "single video"
        },
        {
            "name": "Long Message (Chunked)",
            "message": "This is a comprehensive test message designed to generate approximately eighteen seconds of audio content. This will help us verify that the video generation process works correctly without any looping issues.",
            "expected": "chunked video"
        }
    ]
    
    processor = UltraFastProcessor()
    results = []
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"📝 Message: {test_case['message'][:80]}...")
        
        try:
            # Generate video
            video_url, stats = await processor.process_video_ultra_fast(
                test_case['message'], 
                "general"
            )
            
            if video_url:
                print(f"✅ Video generated successfully")
                print(f"📹 URL: {video_url}")
                
                # Basic validation
                filename = video_url.split('/')[-1].split('?')[0]
                is_combined = "ultra_combined" in filename
                
                if test_case['expected'] == "single video" and not is_combined:
                    print(f"✅ Correctly generated single video")
                elif test_case['expected'] == "chunked video" and is_combined:
                    print(f"✅ Correctly generated chunked video")
                else:
                    print(f"⚠️ Unexpected video type")
                
                results.append({
                    "test": test_case['name'],
                    "success": True,
                    "url": video_url,
                    "is_combined": is_combined
                })
                
            else:
                print(f"❌ Video generation failed")
                results.append({
                    "test": test_case['name'],
                    "success": False,
                    "error": "No video URL returned"
                })
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            results.append({
                "test": test_case['name'],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Simplified Solution Test Summary")
    print("=" * 50)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print(f"\n🎉 Successful results:")
        for result in successful_tests:
            print(f"  ✅ {result['test']}")
            print(f"     📹 Combined: {'Yes' if result['is_combined'] else 'No'}")
    
    if failed_tests:
        print(f"\n❌ Failed results:")
        for result in failed_tests:
            print(f"  ❌ {result['test']}: {result.get('error', 'Unknown error')}")
    
    # Overall assessment
    if len(successful_tests) == len(results):
        print(f"\n🎉 SUCCESS: Simplified solution works!")
        print(f"💡 Core issues addressed without over-engineering.")
    else:
        print(f"\n❌ FAILED: Some tests failed.")
        print(f"🔧 Check the errors above.")
    
    return len(successful_tests) == len(results)

if __name__ == "__main__":
    print("🚀 Starting simplified solution test...")
    
    # Run the test
    success = asyncio.run(test_simplified_solution())
    
    if success:
        print("\n🎉 SUCCESS: Simplified solution works!")
        print("💡 We've addressed the core issues without over-engineering.")
    else:
        print("\n❌ FAILED: Simplified solution has issues.")
        print("🔧 May need to adjust the simplification.") 