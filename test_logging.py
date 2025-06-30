#!/usr/bin/env python3
"""
Test script to verify improved logging functionality
"""

import requests
import json
import time

def test_chat_logging():
    """Test chat endpoint logging"""
    print("🧪 Testing Chat Endpoint Logging...")
    
    # Test 1: Simple question
    response1 = requests.post(
        "http://localhost:8000/api/v1/chat",
        json={
            "message": "What is 2+2?",
            "agent_type": "general"
        }
    )
    print(f"✅ Test 1 completed: {response1.status_code}")
    
    time.sleep(1)
    
    # Test 2: Another question
    response2 = requests.post(
        "http://localhost:8000/api/v1/chat",
        json={
            "message": "Tell me a joke",
            "agent_type": "general"
        }
    )
    print(f"✅ Test 2 completed: {response2.status_code}")
    
    time.sleep(1)
    
    # Test 3: Video generation
    response3 = requests.post(
        "http://localhost:8000/api/v1/generate_video",
        json={
            "message": "Hello world test message",
            "agent_type": "general"
        }
    )
    print(f"✅ Test 3 completed: {response3.status_code}")
    
    print("\n🎯 Check the backend terminal for the improved logging output!")
    print("   You should see:")
    print("   - 💬 USER QUESTION (CHAT): What is 2+2?")
    print("   - 💬 USER QUESTION (CHAT): Tell me a joke") 
    print("   - 🎬 VIDEO GENERATION REQUEST: Hello world test message")

if __name__ == "__main__":
    test_chat_logging() 