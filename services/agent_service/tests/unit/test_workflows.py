"""Unit tests for simplified finance workflows."""

import asyncio
from services.agent_service.agents_adk.workflows.finance_workflows import (
    OnboardingWorkflow,
    BudgetCreationWorkflow,
    GoalTrackingWorkflow,
    FinancialHealthCheckWorkflow,
    SimpleFinanceWorkflow,
)
from services.agent_service.agents_adk.state.workflow_state import WorkflowState


def run_workflow(workflow):
    return asyncio.run(workflow.run("u1"))


def test_all_workflows_success():
    workflows = [
        (OnboardingWorkflow(), "user_onboarding"),
        (BudgetCreationWorkflow(), "budget_creation"),
        (GoalTrackingWorkflow(), "goal_tracking"),
        (FinancialHealthCheckWorkflow(), "financial_health_check"),
    ]
    for wf, name in workflows:
        result = run_workflow(wf)
        assert result["success"] is True
        assert result["workflow"] == name
        assert result["session"].user_id == "u1"
        assert "completed successfully" in result["message"]


def test_workflow_handles_error(monkeypatch):
    workflow = OnboardingWorkflow()

    def boom(self, step, next_agent=None):
        raise RuntimeError("fail")

    monkeypatch.setattr(WorkflowState, "advance_to_step", boom)

    result = asyncio.run(workflow.run("err"))
    assert result["success"] is False
    assert result["workflow"] == "user_onboarding"
    assert "fail" in result["error"]
