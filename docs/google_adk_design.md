# Google ADK Integration Design

## Overview

This document outlines a migration strategy to adopt Google's **Agent Development Kit (ADK)** for the FinanceAgent project. The goal is to modernize the agent system, leverage ADK's built‑in orchestration, and streamline the way agents communicate with the Django backend.

## Objectives

1. Replace existing LangChain/LangGraph orchestration with ADK features.
2. Preserve domain logic in each agent while improving modularity.
3. Maintain compatibility with the current Django models and APIs.
4. Enable easier scaling and monitoring of agent workflows.

## Current Architecture

The project currently uses custom LangChain-based agents orchestrated by a router component. Each agent is responsible for a specific finance domain (Cash-Flow, Investment, Tax, etc.) and communicates with the user through a Conversation Agent.

## ADK Highlights

Google ADK provides tools for building multi-agent systems with standardized message schemas, conversation memory, and event-based task handling. It includes:

- **Agent runtime** with structured conversations.
- **Built-in memory** management for context.
- **Task orchestration** via event hooks and workflows.
- **Monitoring utilities** for tracing agent interactions.

## Migration Plan

1. **Evaluate ADK APIs**
   - Review ADK documentation and samples.
   - Identify equivalents for the current router and agent classes.
2. **Prepare Dependencies**
   - Add `google-adk` to `requirements/agents.txt` and `requirements/all.txt`.
   - Update Docker images if necessary.
3. **Implement ADK-based Orchestrator**
   - Replace the existing orchestrator logic with an ADK workflow.
   - Map intents to ADK tasks or event triggers.
4. **Port Individual Agents**
   - Recreate each domain agent (Cash-Flow, Investment, etc.) as an ADK agent class.
   - Ensure they use the same Django models for data access.
5. **Conversation Handling**
   - Use ADK's memory and conversation modules to replace the current Conversation Agent pipeline.
   - Keep text generation logic but wrap it in ADK-compliant message objects.
6. **Testing & Validation**
   - Update the test suite to mock ADK interactions similar to the current `litellm` mocks.
   - Verify that workflows execute correctly and produce the same advice and reports.
7. **Monitoring & Metrics**
   - Integrate ADK's tracing utilities with existing logging.
   - Expose metrics via Prometheus or another monitoring tool.

## Recommended Steps

1. Prototype a small workflow using ADK with one or two agents (e.g., Onboarding & Cash-Flow) to validate compatibility.
2. Gradually migrate the remaining agents, ensuring each step passes tests.
3. Remove deprecated LangChain/LangGraph code once parity is achieved.

## Benefits

- **Simpler Orchestration** – ADK's workflow engine reduces boilerplate code.
- **Scalability** – built-in monitoring and event hooks facilitate production deployment.
- **Future-proofing** – aligning with Google's agent ecosystem opens the door for new features like tool integrations and advanced memory modules.

## Milestones

1. **Week 1–2** – Research ADK and create prototype workflow.
2. **Week 3–4** – Migrate orchestrator and core agents.
3. **Week 5–6** – Migrate remaining agents and conversation logic.
4. **Week 7** – Update documentation and finalize testing.

## Risks & Considerations

- **Library Stability** – ensure the ADK release used is stable enough for production.
- **Learning Curve** – developers will need time to become familiar with ADK paradigms.
- **Compatibility** – monitor for edge cases where ADK's abstractions differ from current expectations.

## Conclusion

Adopting Google ADK offers a modern foundation for the FinanceAgent system. By methodically migrating each component and leveraging ADK's built-in orchestration and monitoring features, the project can achieve a more maintainable and scalable architecture.

