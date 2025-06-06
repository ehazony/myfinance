#!/usr/bin/env python3
"""
Test script for the FastAPI Agent Service
"""

import requests
import json
import time

# Configuration
AGENT_SERVICE_URL = "http://localhost:8001"
TEST_USER_ID = "test_user_123"

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{AGENT_SERVICE_URL}/api/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_chat_send():
    """Test sending a chat message."""
    print("\n💬 Testing chat send endpoint...")
    
    test_messages = [
        "Hello, I need help with my finances",
        "What's my spending this month?",
        "Can you help me create a budget?"
    ]
    
    for message in test_messages:
        data = {
            "user_id": TEST_USER_ID,
            "text": message
        }
        
        print(f"Sending: {message}")
        response = requests.post(
            f"{AGENT_SERVICE_URL}/api/chat/send",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result['payload']['text'][:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
        
        time.sleep(1)  # Brief pause between requests

def test_chat_history():
    """Test retrieving chat history."""
    print(f"\n📚 Testing chat history for user {TEST_USER_ID}...")
    
    response = requests.get(f"{AGENT_SERVICE_URL}/api/chat/history?user_id={TEST_USER_ID}")
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Retrieved {len(messages)} messages")
        for i, msg in enumerate(messages[-4:], 1):  # Show last 4 messages
            sender = msg['sender']
            text = msg['payload']['text'][:80] + "..." if len(msg['payload']['text']) > 80 else msg['payload']['text']
            print(f"  {i}. {sender}: {text}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_clear_history():
    """Test clearing chat history."""
    print(f"\n🗑️  Testing clear history for user {TEST_USER_ID}...")
    
    response = requests.delete(f"{AGENT_SERVICE_URL}/api/chat/history/{TEST_USER_ID}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def main():
    """Run all tests."""
    print("🚀 Testing FastAPI Agent Service")
    print("=" * 50)
    
    try:
        # Test each endpoint
        if test_health():
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
        
        test_chat_send()
        test_chat_history()
        test_clear_history()
        
        # Verify history is cleared
        print(f"\n🔍 Verifying history is cleared...")
        response = requests.get(f"{AGENT_SERVICE_URL}/api/chat/history?user_id={TEST_USER_ID}")
        if response.status_code == 200:
            messages = response.json()
            print(f"✅ History cleared - now has {len(messages)} messages")
        
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to agent service. Is it running on port 8001?")
        print("Start it with: uvicorn main:app --reload --port 8001")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 