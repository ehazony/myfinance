"""Minimal stub of the langgraph library for tests."""

END = "END"
START = "START"

class StateGraph:
    def __init__(self, state):
        self.state = state
    def add_node(self, name, node):
        pass
    def add_edge(self, start, end):
        pass
    def add_conditional_edges(self, name, cond, edges):
        pass
    def compile(self):
        class Dummy:
            def stream(self, state):
                return []
        return Dummy()
