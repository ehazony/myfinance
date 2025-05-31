# FinanceAgent Design V2

This document describes the second iteration of the FinanceAgent architecture. The goal is to keep data manipulation logic strictly separated from conversational output while providing a more natural user experience.

## 0. High-level Stack

```
┌───────────┐   user ──►│ Orchestrator / Router │◄─── system memory + schemas
└───────────┘
        │
┌───────────────────────────────────────────────────┐
│                   AGENT LANES                    │
│──────────────────────────┬────────────────────────│
│  Conversational Lane     │     Data-/Logic Lane   │
│  (plain-text JSON)       │  (schema JSON only)    │
│                          │                        │
│  • Greeting Agent        │  • Onboarding & Baseline
│  • Conversation Agent    │  • Cash-Flow & Budget
│    (ongoing dialogue)    │  • Goal-Setting
│                          │  • Safety-Layer
│                          │  • Debt-Strategy
│                          │  • Tax & Pension Opt.
│                          │  • Investment Arch.
│                          │  • Reporting & Viz
└──────────────────────────┴────────────────────────┘
        │
 backend services (provider connectors, Postgres, files, cron, security audit)
```

Agents in the **Conversation Lane** only return `{ "messages": [ ... ] }` JSON. Agents in the **Data Lane** return strict schemas with no prose. The Router chooses the lane based on user intent and ensures that free text never leaks from the data agents.

## 1. Agent Responsibilities

| #  | Agent                        | I/O Schema                         | Description                                                                            |
|----|------------------------------|-----------------------------------|----------------------------------------------------------------------------------------|
| 0  | Orchestrator / Router        | JSON ↔ JSON                        | Detect intent and choose lane.                                                         |
| 1  | Greeting Agent               | `{ "messages": [] }`              | Initial welcome. Exits after user selects an action.                                   |
| 2  | Conversation Agent           | `{ "messages": [] }`              | Summarises data-lane outputs and guides the user in natural language.                  |
| 3-10 | Specialist Data Agents     | strict schemas (BaselineSnapshot, GoalList, ...) | Perform calculations and data updates only.                                            |
| 11 | Compliance Guard             | SecurityAuditRecord                | Scrub sensitive events.                                                                |

## 2. Intent → Lane Map (excerpt)

| Intent               | Lane         | Target Agent              |
|----------------------|-------------|---------------------------|
| `greet`, `help`      | Conversation| Greeting → Conversation   |
| `explain_snapshot`   | Conversation| Conversation              |
| `connect_provider`   | Data        | Onboarding & Baseline     |
| `categorize_txns`    | Data        | Cash-Flow & Budget        |
| _(other specialist)_ | Data        | ...                       |

Conversation Lane outputs are restricted to `{"messages": [...]}` while Data Lane outputs conform to their schemas.

## 3. Conversation Agent – Prompt Excerpt

```
You are the Conversation Agent.

1. Input formats
   • From the user → free text.
   • From the Router → a JSON object:
     {
       "source":   "Data",
       "agent":    "<DataAgentName>",
       "payload":  <strict-schema JSON>
     }
2. Goals on every turn
   • Detect confusion or next request from user text.
   • When receiving Data payload, summarise the result and surface `missing_info[]` if present.
   • Suggest a short next step.
3. Output
   Return exactly:
   {
     "messages": ["<bubble 1>", "<bubble 2>"]
   }
   Max 3 bubbles. If you cannot produce valid JSON, reply with `{}`.
```

A simplified Greeting Agent uses the same format for the very first interaction.

## 4. End-to-End Example

1. User: "Hi"
2. Router → Greeting Agent (`greet` intent)
3. Greeting Agent → `{ "messages": ["Hi! I can …", "What next?"] }`
4. User: "Connect my bank"
5. Router identifies `connect_provider` → Onboarding Agent
6. Onboarding Agent returns `BaselineSnapshot` with `missing_info`
7. Router wraps payload → Conversation Agent (`explain_snapshot` intent)
8. Conversation Agent replies:
   ```json
   {
     "messages": [
       "✅ Connected Bank Leumi checking (₪12,346).",
       "I didn't see any credit-cards or loans—would you like to add those next?"
     ]
   }
   ```
9. User responds and the cycle continues.

## 5. Benefits of This Design

- **Consistent UX** – all conversational text flows through a single agent.
- **Data Integrity** – data agents never output prose; conversation agent never alters data.
- **Easy Maintenance** – new data agents only require router updates.
- **Internationalisation** – multiple conversation agents can handle different languages.
- **Security & Performance** – provider calls and long-running tasks remain in backend services.

## 6. Remaining Implementation Tasks

1. Add a `missing_info` array to `BaselineSnapshot` and other relevant schemas.
2. Implement the Conversation Agent prompt and integrate it with the router.
3. Ensure every Data-Lane response is passed through the Conversation Agent before reaching the user interface.

This document supersedes the older `docs/agent.md` diagram. Use it as the main reference for building the FinanceAgent multi-agent system.
