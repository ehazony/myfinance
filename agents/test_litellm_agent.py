from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../.')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
import django
django.setup()

from agents.workflow import run_workflow

# Ensure your OPENAI_API_KEY is set before running this test.

def test_full_workflow():
    state = run_workflow("I want to sign up and then see a chart")
    print("Conversation:", state.conversation)
    print("Result:", state.result)

if __name__ == "__main__":
    test_full_workflow()
