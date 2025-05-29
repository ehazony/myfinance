"""Simple example demonstrating the LangGraph workflow."""
from pprint import pprint

from .workflow import run_workflow


def main():
    state = run_workflow("I want to sign up and then see a chart")
    pprint(state.conversation)
    pprint(state.result)


if __name__ == "__main__":
    main()
