from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
import django
django.setup()
from agents.onboarding import OnboardingAgent

# Ensure your OPENAI_API_KEY is set in the environment before running this test
# Optionally set LLM_MODEL, e.g., os.environ["LLM_MODEL"] = "gpt-3.5-turbo"

def test_generate_payload():
    agent = OnboardingAgent()
    result = agent.generate_payload("Hi, I want to optimize my finances")
    print("Generated payload:", result)

if __name__ == "__main__":
    test_generate_payload() 