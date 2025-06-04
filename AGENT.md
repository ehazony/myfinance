# Agent Guidelines

## Overview
This repository contains a Django backend and a React frontend. The backend lives in various Python packages such as `finance`, `app`, `core` and `telegram_bot`. The frontend is located in `front/dashboard`. Docker compose files are provided for local development and testing.

## Structure
- `manage.py` – entry point for Django commands.
- `finance/` – main Django project settings and Celery configuration.
- `core/` – additional Django project used by templates.
- `app/` – domain models and business logic.
- `finance_common/` – shared SQLAlchemy models and DB utilities.
- `agents/` – LangChain-based finance agents and orchestrator logic.
- `telegram_bot/` – code for interacting with Telegram.
- `front/dashboard/` – Legacy React dashboard application.
- `front/FinanceAgent/` – Modern Next.js/Expo app for the new finance dashboard (web and mobile).
- `docker-compose.yml` – runs the application with Redis, Celery and Nginx.
- `docker-compose.test.yml` – test environment.
- `.env.prod` – environment variables used by docker-compose.

## Running the application
Use Docker Compose for development. Each service has its own folder under
`services/` with a dedicated requirements file.

Use Docker Compose for development:

```bash
docker-compose up --build
```

This will start the Django server, Celery workers and other services defined in `docker-compose.yml`. The server listens on port `8000` via Nginx.

## Running tests
Execute the tests using the test compose file:

```bash
docker-compose -f docker-compose.test.yml run --build test
```

Alternatively you can run `docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit` to see the output of the tests. After the tests finish clean up containers with:

```bash
docker-compose -f docker-compose.test.yml down
```

## Frontend
The legacy React dashboard resides in `front/dashboard`. See its `README.md` for package.json scripts and development instructions.
The new FinanceAgent app resides in `front/FinanceAgent`. See its `README.md` for Next.js/Expo usage and development instructions.

## FinanceAgent App

The new FinanceAgent app is a modern, unified codebase for both web and mobile finance dashboards. It uses Next.js for the web frontend and Expo (React Native) for mobile, sharing most business logic and UI components.

- **Location:** `front/FinanceAgent`
- **Purpose:** Modern replacement for the old dashboard, supporting both web and mobile from a single codebase.
- **Web (Next.js):**
  - Install dependencies: `npm install` or `pnpm install`
  - Start dev server: `npm run dev` or `pnpm dev`
  - Runs at http://localhost:3000/
- **Mobile (Expo):**
  - Install dependencies: `npm install` or `pnpm install`
  - Start Expo: `npx expo start`
  - Use Expo Go app or an emulator to preview on your device.
- **See** `front/FinanceAgent/README.md` **for more details and advanced usage.**

## Reference Materials

The `docs/references/` directory contains external documentation and code references for agent development:

### Google ADK Python Reference
- **File:** `docs/references/google-adk-python-complete-reference.md`
- **Content:** Complete codebase analysis of Google's Agent Development Kit (ADK) Python toolkit
- **Source:** Generated from https://github.com/google/adk-python (468 files, ~5.5M tokens)
- **Usage:** Reference for integrating Google ADK patterns, tools, and multi-agent architectures
- **Key Areas:**
  - Multi-agent system orchestration patterns
  - Google ecosystem tool integrations (BigQuery, Search, etc.)
  - Code-first agent development approaches
  - Advanced agent architectures and workflows
  - Sample implementations and best practices

**For Agents:** This reference provides comprehensive examples of how to build sophisticated agent systems using Google's ADK framework. Use it to understand modern agent patterns, tool integrations, and architectural approaches that could enhance the existing finance agent system.

## ADK-Based Agent System (Next Generation)

The `agents_adk/` directory contains a modern, ADK-based agent system that replaces the current `agents/` implementation:

### Overview
- **Location:** `agents_adk/`
- **Framework:** Google Agent Development Kit (ADK)
- **Purpose:** Production-ready multi-agent finance system with enhanced capabilities
- **Status:** ✅ Implemented and ready for migration

### Key Features
- **Native Multi-Agent Architecture:** Built-in sub_agents coordination
- **Rich Development UI:** Web interface for testing and debugging
- **Google Ecosystem Integration:** Native tools for Search, BigQuery, etc.
- **Production Deployment:** Built-in Cloud Run and Vertex AI Agent Engine support
- **Evaluation Framework:** Built-in testing and performance evaluation
- **Session Management:** Persistent conversations and memory

### Quick Start
```bash
# Set up environment
cp agents_adk/env_template agents_adk/.env
# Add your Google API key to .env

# Install minimal dependencies for the ADK agent system
pip install -r requirements/adk.txt

# Test the system
cd agents_adk && python test_adk.py

# Interactive CLI
adk run agents_adk

# Web development UI
adk web agents_adk
```

### Architecture
- **Root Agent:** `root_agent` - Main orchestrator
- **Specialist Agents:** Onboarding, Cash Flow, Goal Setting, Reporting, Investment
- **Django Integration:** `django_integration.py` - Centralized database access
- **Tools:** Real-time data access to transactions, accounts, goals, reports

### Migration
- **Current Status:** Phase 1 - Parallel implementation complete
- **Migration Guide:** See `agents_adk/MIGRATION_GUIDE.md` for detailed transition plan
- **Compatibility:** Designed to replace current `agents/` system with minimal frontend changes

**For Developers:** The ADK system offers significant improvements in development experience, production readiness, and feature capabilities. See the migration guide for detailed comparison and transition steps.

## Modular Services

The repository is being split into smaller services under the `services/` directory.
Each service contains its own README and `requirements` file. Refer to
`docs/design.md` for the migration checklist and progress.

## Important notes
- Keep sensitive information such as credentials out of commits. Environment variables are stored in `.env.prod`.
- If you add or change setup steps, test commands, or repository structure, update both this `AGENT.md` file and the root `README.md` accordingly. If you change the FinanceAgent app setup, update its README as well.
- The `agents/` package relies on `langchain`, `langgraph`, and `litellm`. These
  live in `requirements/agents.txt`.
- Ensure new code includes tests where possible.
- If you encounter missing libraries during setup or while running code or tests,
  add them to the appropriate file under `requirements/`.

## Setup Troubleshooting & Recommendations

If you encounter any problems during setup or configuration, please document the issue in the `AGENT_SETUP_RECOMMENDATIONS.md` file at the project root. Clearly describe what is missing or problematic, and provide your recommended solution or fix. This helps future users and agents resolve setup issues more efficiently.

