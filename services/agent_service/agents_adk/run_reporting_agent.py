import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'True')

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from agents_adk.agent import create_reporting_agent

try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
except ImportError as e:
    print(f"❌ ADK import error: {e}")
    sys.exit(1)

async def main():
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found!")
        print("Please add your API key to the .env file.")
        return
    
    print(f"✅ API key loaded: {api_key[:20]}...")
    
    agent = create_reporting_agent()
    user_id = "1"
    prompt = "Please get the user transactions for user ID 1 and tell me what was the last (most recent) transaction reported, and what date it occurred."
    
    print(f"🔄 Running reporting agent for user {user_id}...")
    print(f"📝 Prompt: {prompt}")
    
    session_service = InMemorySessionService()
    session_id = f"session_{user_id}_reporting"
    session = await session_service.create_session(app_name="ReportingAgentTest", user_id=user_id, session_id=session_id)
    runner = Runner(agent=agent, app_name="ReportingAgentTest", session_service=session_service)
    user_message = types.Content(role='user', parts=[types.Part(text=prompt)])
    events = runner.run(user_id=user_id, session_id=session_id, new_message=user_message)
    
    for event in events:
        if event.is_final_response():
            print(f"\n💡 Reporting Agent Response:")
            print("=" * 50)
            print(event.content.parts[0].text)
            print("=" * 50)
            break
    else:
        print("No final response from reporting agent.")

if __name__ == "__main__":
    asyncio.run(main()) 