#!/usr/bin/env python3
"""
Simple test to verify function calling works in our ADK setup
"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def simple_test_tool(message: str) -> str:
    """A simple test tool that just returns a message."""
    return f"Tool called successfully with message: {message}"

async def test_function_calling():
    """Test if function calling works at all."""
    print("🧪 Testing basic function calling...")
    
    # Create a simple agent with one tool
    test_agent = Agent(
        model='gemini-2.0-flash-001',
        name='test_agent',
        description='Simple test agent',
        instruction='''
        You are a test agent. When the user says "test tool", IMMEDIATELY call the simple_test_tool with the message "hello world". 
        Do not ask questions, just call the tool.
        ''',
        tools=[simple_test_tool]
    )
    
    # Set up session
    session_service = InMemorySessionService()
    session_id = "test_session"
    session = await session_service.create_session(
        app_name="ToolTest", 
        user_id="test_user", 
        session_id=session_id
    )
    
    # Create runner
    runner = Runner(
        agent=test_agent, 
        app_name="ToolTest", 
        session_service=session_service
    )
    
    # Test message
    user_message = types.Content(
        role='user', 
        parts=[types.Part(text="test tool")]
    )
    
    # Run and check for function calls
    print("📤 Sending: 'test tool'")
    function_calls_seen = 0
    final_response = ""
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=user_message
    ):
        # Check for function calls
        if hasattr(event, 'content') and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_calls_seen += 1
                    print(f"🔧 Function call: {part.function_call.name}({part.function_call.args})")
                elif hasattr(part, 'function_response') and part.function_response:
                    print(f"📥 Function response: {part.function_response.response}")
        
        # Get final response
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    final_response = part.text
                    break
    
    print(f"📊 Function calls made: {function_calls_seen}")
    print(f"💬 Final response: {final_response}")
    
    if function_calls_seen > 0:
        print("✅ Function calling is working!")
        return True
    else:
        print("❌ Function calling is NOT working!")
        return False

if __name__ == "__main__":
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found!")
        exit(1)
    
    asyncio.run(test_function_calling()) 