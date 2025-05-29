from langgraph.graph import StateGraph, END, START

from .workflow_state import WorkflowState
from .graph_nodes import orchestrator_node, AGENT_NODES


def build_workflow():
    graph = StateGraph(WorkflowState)

    # Register nodes
    graph.add_node("orchestrator", orchestrator_node)
    for name, node in AGENT_NODES.items():
        graph.add_node(name, node)

    # Add entrypoint edge
    graph.add_edge(START, "orchestrator")

    # Route from orchestrator based on detected intent
    graph.add_conditional_edges(
        "orchestrator", lambda state: state.next_agent, {name: name for name in AGENT_NODES}
    )

    # After onboarding -> reporting; all others end
    graph.add_conditional_edges(
        "onboarding",
        lambda state: "reporting" if state.next_agent == "reporting" else END,
        {"reporting": "reporting", END: END},
    )

    for name in AGENT_NODES:
        if name not in {"onboarding", "reporting"}:
            graph.add_edge(name, END)
    graph.add_edge("reporting", END)

    return graph.compile()


workflow = build_workflow()


def run_workflow(text: str) -> WorkflowState:
    """Execute the workflow for the given user text."""
    state = WorkflowState(user_input=text)
    for update in workflow.stream(state):
        # `update` is a mapping of node name to a dict representing the state
        state_dict = list(update.values())[0]
        for key, value in state_dict.items():
            setattr(state, key, value)
        if state.done:
            break
    return state
