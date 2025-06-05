#!/usr/bin/env python3
"""
Test if function/tool calling works with the current ADK and Gemini backend.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def square(x: int) -> int:
    """Calculate the square of a number. Use this function when asked to find the square of any number."""
    print(f"🔧 TOOL CALLED: square({x}) = {x * x}")
    return x * x

async def main():
    from google.adk.agents import LlmAgent
    from google.adk.tools import FunctionTool
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    # Register the tool with explicit description
    square_tool = FunctionTool(func=square)
    
    print(f"🔍 Tool registered: {square_tool.name}")
    print(f"🔍 Tool schema: {square_tool.schema}")

    # Create the agent with very explicit instruction
    agent = LlmAgent(
        name="simple_tool_agent",
        model="gemini-2.0-flash-001",
        instruction="""You are a math assistant. When someone asks you to calculate the square of a number, 
        you MUST use the 'square' function/tool to calculate it. Always call the square function when asked 
        about squares. Do not calculate squares manually.""",
        description="Agent that must call the square tool for square calculations.",
        tools=[square_tool]
    )
    
    print(f"🔍 Agent tools: {[tool.name for tool in agent.tools]}")

    # Create runner and session
    session_service = InMemorySessionService()
    session_id = f"session_test_user_{hash('tool') % 10000}"
    session = await session_service.create_session(app_name="ToolTest", user_id="test_user", session_id=session_id)
    runner = Runner(agent=agent, app_name="ToolTest", session_service=session_service)

    # Test multiple prompts
    test_prompts = [
        "Calculate the square of 7 using the square function",
        "What is the square of 7?",
        "Use the square tool to find 7 squared",
        "Call the square function with input 7"
    ]

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{'='*50}")
        print(f"🧪 TEST {i}: {prompt}")
        print("="*50)
        
        user_message = types.Content(role='user', parts=[types.Part(text=prompt)])

        try:
            response_parts = []
            tool_called = False
            events = runner.run(user_id="test_user", session_id=session_id, new_message=user_message)
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_parts.append(part.text)
                            print(f"📝 Content: {part.text}")
                if hasattr(event, 'error_details') and event.error_details:
                    print(f"❌ Error: {event.error_details}")
                if hasattr(event, 'tool_call') or 'tool' in str(event).lower():
                    tool_called = True
                    print(f"🔧 Tool call detected: {event}")
                if event.is_final_response():
                    print(f"🤖 Final Response: {event.content.parts[0].text}")
            
            final_response = "\n".join(response_parts) if response_parts else "No response generated."
            print(f"🤖 Final Response: {final_response}")
            print(f"🔧 Tool Called: {'YES' if tool_called else 'NO'}")
            
        except Exception as e:
            print(f"💥 Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 