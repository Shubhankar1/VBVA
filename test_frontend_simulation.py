#!/usr/bin/env python3
"""
Test script to simulate exact frontend behavior
This will help identify where the text truncation is happening
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

def simulate_frontend_flow():
    """Simulate the exact frontend flow to reproduce the issue"""
    print("🧪 Simulating Frontend Flow")
    print("=" * 50)
    
    # Simulate first chat request
    print("📝 First Chat Request...")
    chat_data_1 = {
        "message": "Give me a 3 line poem",
        "agent_type": "general",
        "session_id": None
    }
    
    response_1 = requests.post(f"{API_BASE}/chat", json=chat_data_1)
    if response_1.status_code != 200:
        print(f"❌ First chat failed: {response_1.status_code}")
        return
    
    chat_result_1 = response_1.json()
    message_text_1 = chat_result_1.get("message", "")
    
    print(f"✅ First chat response (length: {len(message_text_1)} chars)")
    print(f"📄 Message: {repr(message_text_1)}")
    print()
    
    # Simulate second chat request (this is where the issue occurs)
    print("📝 Second Chat Request...")
    chat_data_2 = {
        "message": "Give me a 4 line poem",
        "agent_type": "general",
        "session_id": None
    }
    
    response_2 = requests.post(f"{API_BASE}/chat", json=chat_data_2)
    if response_2.status_code != 200:
        print(f"❌ Second chat failed: {response_2.status_code}")
        return
    
    chat_result_2 = response_2.json()
    message_text_2 = chat_result_2.get("message", "")
    
    print(f"✅ Second chat response (length: {len(message_text_2)} chars)")
    print(f"📄 Message: {repr(message_text_2)}")
    print()
    
    # Now simulate video generation with the second response
    print("🎬 Video Generation with Second Response...")
    
    # Simulate what the frontend would send
    video_data = {
        "message": message_text_2,  # This should be the complete text
        "agent_type": "general",
        "session_id": None,
        "enable_parallel": True,
        "chunk_duration": 15
    }
    
    print(f"📤 Sending to video generation (length: {len(message_text_2)} chars)")
    print(f"📄 Text being sent: {repr(message_text_2)}")
    
    video_response = requests.post(f"{API_BASE}/generate_video", json=video_data)
    
    if video_response.status_code == 200:
        video_result = video_response.json()
        print(f"✅ Video generation successful!")
        print(f"🎥 Video URL: {video_result.get('video_url', 'N/A')}")
        print(f"⏱️ Processing time: {video_result.get('processing_time', 'N/A')}s")
        
        # Check if the video was generated with complete text
        if "processing_details" in video_result:
            details = video_result["processing_details"]
            if "validation" in details:
                validation = details["validation"]
                print(f"🔍 Validation: {validation.get('completeness_level', 'N/A')}")
                print(f"🔍 Confidence: {validation.get('confidence_score', 'N/A')}")
    else:
        print(f"❌ Video generation failed: {video_response.status_code}")
        try:
            error_detail = video_response.json()
            print(f"🔍 Error details: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"🔍 Error text: {video_response.text}")

def test_multiple_requests():
    """Test multiple requests to see if there's a pattern"""
    print("\n🧪 Testing Multiple Requests Pattern")
    print("=" * 50)
    
    for i in range(3):
        print(f"\n📝 Request {i+1}...")
        
        # Chat request
        chat_data = {
            "message": f"Give me a {i+2} line poem",
            "agent_type": "general",
            "session_id": None
        }
        
        response = requests.post(f"{API_BASE}/chat", json=chat_data)
        if response.status_code != 200:
            print(f"❌ Chat failed: {response.status_code}")
            continue
        
        chat_result = response.json()
        message_text = chat_result.get("message", "")
        
        print(f"✅ Chat response (length: {len(message_text)} chars)")
        print(f"📄 Message: {repr(message_text[:100])}...")
        
        # Video generation
        video_data = {
            "message": message_text,
            "agent_type": "general",
            "session_id": None
        }
        
        video_response = requests.post(f"{API_BASE}/generate_video", json=video_data)
        
        if video_response.status_code == 200:
            video_result = video_response.json()
            print(f"✅ Video generated: {video_result.get('video_url', 'N/A')}")
        else:
            print(f"❌ Video failed: {video_response.status_code}")
        
        # Small delay between requests
        time.sleep(1)

if __name__ == "__main__":
    try:
        # Test the frontend simulation
        simulate_frontend_flow()
        
        # Test multiple requests
        test_multiple_requests()
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 