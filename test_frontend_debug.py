#!/usr/bin/env python3
"""
Test script to debug frontend-backend text flow
Simulates the exact flow that the frontend uses
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

def test_frontend_flow():
    """Test the exact frontend flow to identify text truncation"""
    print("🧪 Testing Frontend-Backend Flow")
    print("=" * 50)
    
    # Step 1: Send chat request (like frontend does)
    print("📝 Step 1: Sending chat request...")
    chat_data = {
        "message": "Give me a 4 line poem",
        "agent_type": "general",
        "session_id": None
    }
    
    response = requests.post(f"{API_BASE}/chat", json=chat_data)
    if response.status_code != 200:
        print(f"❌ Chat failed: {response.status_code}")
        return
    
    chat_result = response.json()
    message_text = chat_result.get("message", "")
    
    print(f"✅ Chat response received (length: {len(message_text)} chars)")
    print(f"📄 Message: {repr(message_text)}")
    print()
    
    # Step 2: Send video generation request (like frontend does)
    print("🎬 Step 2: Sending video generation request...")
    video_data = {
        "message": message_text,  # Use the exact text from chat response
        "agent_type": "general",
        "session_id": None,
        "enable_parallel": True,
        "chunk_duration": 15
    }
    
    print(f"📤 Sending to backend (length: {len(message_text)} chars)")
    print(f"📄 Text being sent: {repr(message_text)}")
    
    video_response = requests.post(f"{API_BASE}/generate_video", json=video_data)
    
    if video_response.status_code == 200:
        video_result = video_response.json()
        print(f"✅ Video generation successful!")
        print(f"🎥 Video URL: {video_result.get('video_url', 'N/A')}")
        print(f"⏱️ Processing time: {video_result.get('processing_time', 'N/A')}s")
    else:
        print(f"❌ Video generation failed: {video_response.status_code}")
        try:
            error_detail = video_response.json()
            print(f"🔍 Error details: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"🔍 Error text: {video_response.text}")

def test_direct_video_generation():
    """Test direct video generation with known complete text"""
    print("\n🧪 Testing Direct Video Generation")
    print("=" * 50)
    
    # Test with a known complete text
    test_text = """In twilight's gentle, whispering hue,
The world takes on a softer view.
Stars emerge in the velvet sky,
A lullaby as night drifts by."""
    
    print(f"📝 Testing with text (length: {len(test_text)} chars):")
    print(f"📄 Text: {repr(test_text)}")
    
    video_data = {
        "message": test_text,
        "agent_type": "general",
        "session_id": None
    }
    
    response = requests.post(f"{API_BASE}/generate_video", json=video_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Direct video generation successful!")
        print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
    else:
        print(f"❌ Direct video generation failed: {response.status_code}")
        print(f"🔍 Error: {response.text}")

if __name__ == "__main__":
    try:
        # Test the frontend flow
        test_frontend_flow()
        
        # Test direct video generation
        test_direct_video_generation()
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 