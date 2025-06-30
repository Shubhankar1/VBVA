#!/usr/bin/env python3
"""
Test script for answer validation flow
Tests the complete flow from chat to video generation with validation
"""

import asyncio
import aiohttp
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

async def test_chat_with_validation():
    """Test chat endpoint with validation"""
    print("🧪 Testing chat endpoint with validation...")
    
    async with aiohttp.ClientSession() as session:
        # Test with a short question that might produce incomplete answer
        chat_data = {
            "message": "Give me a 2 line poem",
            "session_id": None,
            "agent_type": "general"
        }
        
        async with session.post(f"{API_BASE}/chat", json=chat_data) as response:
            result = await response.json()
            print(f"📝 Chat Response Status: {response.status}")
            print(f"📝 Message: {result.get('message', '')[:100]}...")
            print(f"📝 Validation Info: {result.get('validation_info', {})}")
            
            return result

async def test_regenerate_complete():
    """Test regenerate complete endpoint"""
    print("\n🔄 Testing regenerate complete endpoint...")
    
    async with aiohttp.ClientSession() as session:
        # Test regeneration with the same question
        regenerate_data = {
            "message": "Give me a 2 line poem",
            "session_id": None,
            "agent_type": "general"
        }
        
        async with session.post(f"{API_BASE}/regenerate_complete", json=regenerate_data) as response:
            result = await response.json()
            print(f"🔄 Regenerate Response Status: {response.status}")
            print(f"🔄 Message: {result.get('message', '')[:100]}...")
            print(f"🔄 Validation Info: {result.get('validation_info', {})}")
            
            return result

async def test_video_generation_with_incomplete():
    """Test video generation with incomplete answer"""
    print("\n🎥 Testing video generation with incomplete answer...")
    
    async with aiohttp.ClientSession() as session:
        # Test with a short, incomplete answer
        video_data = {
            "message": "Short answer.",
            "session_id": None,
            "agent_type": "general"
        }
        
        async with session.post(f"{API_BASE}/generate_video", json=video_data) as response:
            if response.status == 400:
                error_detail = await response.json()
                print(f"🎥 Video Generation Blocked (Expected): {response.status}")
                print(f"🎥 Error: {error_detail.get('detail', {}).get('error', '')}")
                print(f"🎥 Message: {error_detail.get('detail', {}).get('message', '')}")
                print(f"🎥 Issues: {error_detail.get('detail', {}).get('issues', [])}")
                print(f"🎥 Remediation: {error_detail.get('detail', {}).get('remediation', {})}")
                return error_detail.get('detail', {})
            else:
                result = await response.json()
                print(f"🎥 Video Generation Success (Unexpected): {response.status}")
                print(f"🎥 Result: {result}")
                return result

async def test_video_generation_with_complete():
    """Test video generation with complete answer"""
    print("\n🎥 Testing video generation with complete answer...")
    
    async with aiohttp.ClientSession() as session:
        # Test with a longer, more complete answer
        video_data = {
            "message": "This is a comprehensive answer that should pass validation. It contains multiple sentences and provides detailed information that addresses the question thoroughly. The answer is structured well and includes sufficient content to meet the validation requirements for video generation.",
            "session_id": None,
            "agent_type": "general"
        }
        
        async with session.post(f"{API_BASE}/generate_video", json=video_data) as response:
            if response.status == 200:
                result = await response.json()
                print(f"🎥 Video Generation Success: {response.status}")
                print(f"🎥 Video URL: {result.get('video_url', '')}")
                print(f"🎥 Processing Time: {result.get('processing_time', 0):.2f}s")
                return result
            else:
                error_detail = await response.json()
                print(f"🎥 Video Generation Failed: {response.status}")
                print(f"🎥 Error: {error_detail}")
                return error_detail

async def main():
    """Run all tests"""
    print("🚀 Starting Answer Validation Flow Tests")
    print("=" * 50)
    
    try:
        # Test 1: Chat with validation
        chat_result = await test_chat_with_validation()
        
        # Test 2: Regenerate complete
        regenerate_result = await test_regenerate_complete()
        
        # Test 3: Video generation with incomplete answer
        video_incomplete_result = await test_video_generation_with_incomplete()
        
        # Test 4: Video generation with complete answer
        video_complete_result = await test_video_generation_with_complete()
        
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"✅ Chat with validation: {'PASS' if chat_result else 'FAIL'}")
        print(f"✅ Regenerate complete: {'PASS' if regenerate_result else 'FAIL'}")
        print(f"✅ Video generation (incomplete): {'PASS' if video_incomplete_result.get('error') else 'FAIL'}")
        print(f"✅ Video generation (complete): {'PASS' if video_complete_result.get('video_url') else 'FAIL'}")
        
        # Additional validation checks
        if chat_result and chat_result.get('validation_info'):
            print(f"📊 Chat validation: {chat_result['validation_info'].get('completeness_level', 'unknown')}")
        
        if regenerate_result and regenerate_result.get('validation_info'):
            print(f"📊 Regenerate validation: {regenerate_result['validation_info'].get('completeness_level', 'unknown')}")
        
        if video_incomplete_result and video_incomplete_result.get('error'):
            print(f"📊 Video block reason: {video_incomplete_result.get('error', 'unknown')}")
        
        if video_complete_result and video_complete_result.get('video_url'):
            print(f"📊 Video generation time: {video_complete_result.get('processing_time', 0):.2f}s")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 