# Modular Architecture Proposal

This document outlines a plan to split the monolithic `myfinance` project into
smaller services so each part has a minimal dependency set. The goal is to make
building, testing, and deployment easier and to avoid maintaining one large
`requirements.txt`.

## 1. Current Situation

The repository combines several concerns:

- **Django apps** for core models (`finance`, `app`, `core`).
- **Agent logic** in `agents` and the newer `agents_adk` package.
- **Bank scraping utilities** under `bank_scraper` with Selenium and browser
dependencies.
- **Telegram bot** code.
- **Front‑end** projects in the `front` directory.

All Python dependencies are aggregated under `requirements/all.txt`, which pulls
in heavy libraries (Selenium, scraping utilities, LangChain, etc.) even when only
a subset is needed.

## 2. Proposed Split

1. **Core API Service**
   - Framework: Django (reuse the existing project).
   - Responsibilities: user management, accounts, transactions, REST API, admin
     site.
  - Requirements: a dedicated `requirements/services/core_api.txt` file listing
    only the Django and Celery packages needed by the API (no shared base file).
   - Optional: expose a small RPC layer (REST/GraphQL) used by other services.

2. **Agent Service**
   - Framework: keep the `agents_adk` implementation as a standalone service.
   - Communicates with the Core API via HTTP or message queue to fetch data.
  - Requirements: `requirements/services/agent_service.txt` containing only the
    agent and ADK libraries (e.g. `langchain`, `langgraph`, `litellm`,
    `google-adk`).
   - Runs its own worker process (Celery or ADK runtime).

3. **Bank Scraper Service**
   - Contains code from `bank_scraper` only.
   - Uses Selenium or headless browsers; packaged with its own Dockerfile so the
     Core API does not depend on browser drivers.
   - Exposes scraped data via API or pushes results to a shared database.
  - Requirements: `requirements/services/scraper_service.txt` with Selenium and
    scraping utilities only.

4. **Telegram Bot Service**
   - Lightweight service dedicated to Telegram interactions.
   - Imports the shared models (or uses the Core API) but does not depend on the
     scraping or agent libraries.
  - Requirements: `requirements/services/telegram_bot_service.txt` with
    `python-telegram-bot` and a few helpers.

5. **Shared Library**
   - Extract common models and utility functions into a small package
     (`finance_common`).
   - Implement database access via SQLAlchemy or Django ORM but keep it isolated
     so non‑Django services can reuse the models without pulling in all of
     Django.

## 3. Database Layer Options

- **Keep Django ORM** for the Core API and expose data via REST; other services
  consume the API.
- Or **introduce SQLAlchemy** in the shared library so services can connect
  directly without requiring Django.  This would allow microservices that do not
  need the full Django stack.
- Use environment variables and a small `settings` module for each service to
  configure the database connection.

## 4. Build & Deployment

- Each service gets its own Dockerfile and `requirements.txt` listing only the
  needed packages.
- A docker compose file can orchestrate all services in development.
- CI can run tests per service to keep feedback fast.

## 5. Benefits

- Smaller, focused dependency lists.
- Faster builds and lighter containers.
- Clear boundaries between scraping, core API, agents, and messaging bots.
- Easier scaling: heavy services (scraping, agents) can be deployed
  independently.

## 6. Migration Steps

1. Move code into separate folders (`services/core_api`, `services/agents`,
   `services/scraper`, `services/telegram_bot`).
2. Create individual `requirements.txt` files for each service.
3. Extract shared models/utilities into `finance_common`.
4. Set up docker compose with one container per service and a shared database.
5. Gradually update import paths and deployment scripts.

---

This modular approach keeps each part of the system small and maintainable while
allowing independent development and deployment.

## 7. Detailed Migration Checklist

Use the following checklist to track progress while splitting the repository.
The steps are ordered to minimise downtime and avoid breaking the existing
database schema.

### 7.1 Original Migration Steps

1. **Audit dependencies** and create a `requirements/services/<service>.txt`
   for each service containing only the packages it actually needs.
2. **Create a `services/` directory** containing `core_api`, `agents`,
   `scraper`, and `telegram_bot` packages.
3. **Move existing code** from the monolith into the appropriate service
   folders.
4. **Extract shared logic** into a new `finance_common` library.
   - Keep Django models so migrations continue to work.
   - Optionally provide SQLAlchemy equivalents for lightweight services.
5. **Split settings** so each service has its own configuration module.
   - `core_api` reuses most of the current Django settings.
   - Other services load minimal settings from environment variables.
6. **Update imports** across all packages and tests.
7. **Run database migrations** only from `core_api` to avoid conflicts.
8. **Add Dockerfiles** for every service and update `docker-compose.yml`.
9. **Update CI** to run tests for each service separately.
10. **Verify data integrity** against a copy of the production database.
11. **Document new environment variables** and setup steps in the README.

### 7.2 Detailed Implementation Checklist

**Phase 1: Shared Library Setup**
- [x] Create finance_common SQLAlchemy models for Transaction, Credential, Tag, User extensions, Plan, RecurringTransaction, Conversation, Message
- [x] Create finance_common utilities module with shared constants and validation logic
- [x] Create finance_common/tests/ directory and move shared model tests
- [x] Update services requirements files to include finance_common dependency

**Phase 2: Core API Service Migration**
- [x] Move myFinance Django app to services/core_api/myFinance/
- [x] Move app Django app to services/core_api/app/
- [x] Move core Django app to services/core_api/core/  
- [x] Move authentication Django app to services/core_api/authentication/
- [x] Move Django settings from finance/ to services/core_api/finance/
- [x] Move templates directory to services/core_api/templates/
- [x] Move manage.py to services/core_api/manage.py
- [x] Create services/core_api/tests/ directory and move relevant tests from tests/ and app/tests/

**Phase 3: Agent Service Migration**
- [x] Move agents_adk directory to services/agent_service/agents_adk/
- [x] Move agents directory to services/agent_service/agents/
- [x] Create services/agent_service/tests/ directory and move agent-related tests

**Phase 4: Scraper Service Migration**
- [x] Move bank_scraper directory to services/scraper_service/bank_scraper/
- [x] Move bank_statements directory to services/scraper_service/bank_statements/
- [x] Create services/scraper_service/tests/ directory and create scraper tests

**Phase 5: Telegram Bot Service Migration**
- [x] Move telegram_bot Django app to services/telegram_bot_service/telegram_bot/
- [x] Move telegram utilities to services/telegram_bot_service/telegram/
- [x] Create services/telegram_bot_service/tests/ directory and create bot tests

**Phase 6: Integration and Configuration**
- [x] Update import statements in all moved code to use finance_common models
- [x] Create __init__.py files for all new service packages
- [x] Create service-specific settings and configuration files
- [x] Update pytest.ini to recognize new test structure
- [x] Create Dockerfiles for each service
- [x] Update root-level imports and references to point to new service locations

**Phase 7: Testing and Validation**
- [x] Run all tests to ensure functionality is preserved
- [ ] Verify database migrations work correctly from core_api service
- [x] Test inter-service communication and shared library usage
- [ ] Update documentation and setup instructions

## 8. Choosing a Database Layer

For the initial split it is simplest to keep using the **Django ORM** in the
`core_api` service. Other services can interact with the database through the
Core API or by importing models from `finance_common`.

If direct access without Django is required, provide **SQLAlchemy** models in
`finance_common`. This hybrid approach allows gradual migration while still
benefiting from Django's migration system.

## 9. Example: Shared SQLAlchemy Models

In this approach we keep the SQLAlchemy models in a shared package so every
service uses the same definitions.

```python
# finance_common/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
```

```python
# finance_common/models/account.py
from sqlalchemy import Column, Integer, String
from ..db import Base

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
```

Every microservice can import `SessionLocal` and these models:

```python
from finance_common.db import SessionLocal
from finance_common.models.account import Account

with SessionLocal() as session:
    accounts = session.query(Account).all()
```

The Django service can keep thin wrapper models to reuse admin and migration
features without duplicating fields:

```python
# core_api/models/account.py
from finance_common.models.account import Account as SAAccount
from django.db import models

class Account(models.Model):
    class Meta:
        managed = False  # SQLAlchemy handles the table
        db_table = SAAccount.__tablename__
```

This pattern avoids copying schema definitions while allowing non-Django
services to use SQLAlchemy sessions directly.

## 10. Implementation Progress

The repository now contains a top-level `services/` directory with empty
packages for `core_api`, `agent_service`, `scraper_service`, and
`telegram_bot_service`.  Each service has its own `requirements/services/*.txt`
listing only the libraries needed by that service.

A shared package `finance_common` now provides a SQLAlchemy-based database layer.
It defines the `SessionLocal` session factory and includes SQLAlchemy versions
of the existing Django models (e.g. `Account`, `Credential`, `Transaction`).
Services import these models directly without loading Django.
`SQLAlchemy` has been added to `requirements/base.txt` to support this package.

## 11. Agent Service Communication Architecture

### Problem Statement
After migrating to microservices, the core API service needs to maintain chat functionality 
while the agent logic has been moved to a separate service. The current Django server 
fails due to reentrant populate() errors caused by import conflicts between services.

### Solution: Inter-Service Communication Layer

**Communication Patterns:**
1. **HTTP API Communication**: Core API calls Agent Service via REST endpoints
2. **Message Queue Integration**: Use existing Celery/Redis for async communication  
3. **Fallback Implementation**: Graceful degradation when Agent Service unavailable

**Service Communication Flow:**
```
Frontend → Core API (/api/chat/send) → Agent Service (/api/chat/send) → LLM/ADK → Response Chain
```

**Implementation Components:**

#### Agent Service HTTP Endpoints
- `POST /api/chat/send` - Process user messages and return agent responses
- `GET /api/chat/history` - Retrieve conversation history for a user
- `GET /api/health` - Service health check endpoint

#### Core API Service Client
- `AgentServiceClient` class to handle HTTP communication with agent service
- Request/response serialization and error handling
- Retry logic and circuit breaker pattern for resilience
- Authentication/authorization for inter-service calls

#### Chat Service Updates
- Modify existing `ChatSendView` to proxy requests to agent service
- Update `ChatHistoryView` to fetch from agent service or local fallback
- Implement graceful degradation when agent service unavailable
- Maintain existing API contracts for frontend compatibility

#### Configuration & Deployment
- Add `AGENT_SERVICE_URL` to core API settings
- Service discovery and health monitoring
- Docker compose orchestration for proper service communication
- Environment-specific configuration for service endpoints

**Benefits:**
- ✅ Maintains existing chat API contracts for frontend
- ✅ Proper service separation and scalability
- ✅ Graceful degradation and fault tolerance
- ✅ Preserves all existing chat functionality
- ✅ Enables independent service deployment and scaling

## 12. Celery Service Migration Strategy

### Current Celery Issues
The existing `celery_app.py` has several problems in the microservices context:
1. Module-level imports of Django models causing reentrant populate() errors
2. References to moved modules (telegram_bot, bank_scraper) 
3. Tasks that span multiple services need redesign

### Celery Task Redistribution Plan

**Core API Celery Tasks (Keep):**
- `debug_task` - Basic health check
- `load_transactions` - Django management command wrapper
- `update_user_code` - User management operations
- `send_category_info` - Financial reporting (modify to use service communication)
- `send_month_day_info` - Financial reporting (modify to use service communication)

**Tasks to Move to Other Services:**
- `load_transactions_by_credential` → Move to Scraper Service
- `send_telegram_message` → Move to Telegram Bot Service

**Inter-Service Task Communication:**
- Use Celery's routing to send tasks to specific service queues
- Implement task result callbacks for cross-service coordination
- Add task status monitoring and error handling

**Implementation Steps:**
1. Fix immediate import issues in core API celery_app.py
2. Create service-specific celery workers for each microservice
3. Implement task routing and queue separation
4. Add inter-service task communication patterns
5. Update task definitions to work with new service boundaries

This approach maintains the benefits of Celery for async processing while respecting 
service boundaries and enabling proper microservices communication.

## 13. Updated Agent Service Architecture: FastAPI Implementation

### Technology Decision: FastAPI over Django for Agent Service

After implementing the initial microservices split, we determined that **FastAPI** is the optimal choice for the agent service:

**Why FastAPI:**
- ✅ Lightweight and fast startup (no Django overhead)
- ✅ Native async support for LLM/agent operations
- ✅ Automatic OpenAPI documentation generation
- ✅ Excellent performance for API-only services
- ✅ Simple deployment and containerization
- ✅ Built-in request/response validation with Pydantic

**Agent Service API Design:**
```
FastAPI Agent Service (Port 8001)
├── POST /api/chat/send
│   ├── Request: {"user_id": "123", "text": "What's my spending?"}
│   └── Response: {"content_type": "text", "payload": {"text": "Your spending..."}}
├── GET /api/chat/history?user_id=123
│   └── Response: [{"sender": "user", "content_type": "text", "payload": {...}}]
└── GET /api/health
    └── Response: {"status": "ok", "agents_available": true}
```


### Implementation Roadmap Update

**Phase 1: Core Infrastructure** ✅ COMPLETE
- [x] Django core API service operational
- [x] Chat endpoints with fallback responses
- [x] Celery task refactoring for microservices
- [x] Import isolation and dependency cleanup

**Phase 2: Agent Service Implementation** ✅ COMPLETE
- [x] FastAPI agent service with chat endpoints
- [x] Pydantic models for request/response validation
- [x] Integration of existing agent/orchestrator logic
- [x] Error handling and logging
- [x] Docker containerization

**Phase 3: Service Integration** ✅ COMPLETE
- [x] HTTP-based ADKChatService implementation in core API
- [x] HTTP-based communication between services
- [x] Financial context passing from core API to agent service
- [x] Enhanced fallback responses with transaction data
- [x] End-to-end testing of chat flow
- [x] Health monitoring and service status checks

**Phase 4: Production Hardening** 📅 NEXT PRIORITY
- [ ] Service discovery and load balancing
- [ ] Comprehensive error handling and retries
- [ ] Performance monitoring and logging
- [ ] Cross-service authentication/authorization

### Service Communication Architecture (IMPLEMENTED)

```
Frontend Request Flow:
┌─────────────┐    HTTP     ┌──────────────┐    HTTP     ┌─────────────────┐
│   Frontend  │────────────▶│  Core API    │────────────▶│  Agent Service  │
│             │             │  (Django)    │             │   (FastAPI)     │
│             │             │  Port 8000   │             │   Port 8001     │
└─────────────┘             └──────────────┘             └─────────────────┘
                                    │                             │
                                    ▼                             ▼
                            ┌──────────────┐             ┌─────────────────┐
                            │  PostgreSQL  │             │ LLM/ADK Agents  │
                            │   Database   │             │   & Tools       │
                            └──────────────┘             └─────────────────┘
```

**Implementation Details:**

✅ **Core API HTTP Proxy Service:**
- New `ADKChatService` that maintains original interface
- Makes HTTP requests to FastAPI agent service 
- Passes complete financial context (transactions, budgets, categories)
- Graceful fallback when agent service unavailable
- Maintains Django model persistence for conversations

✅ **FastAPI Agent Service:**
- Accepts financial context in request payload
- Enhanced fallback responses with transaction details
- Processes user queries with full financial context
- Returns structured responses compatible with core API

✅ **Validated Communication:**
- Both services running simultaneously (ports 8000 & 8001)
- Successful HTTP communication with financial context
- Proper error handling and fallback mechanisms
- Context-aware responses including actual transaction data

**Sample Response with Financial Context:**
```json
{
  "content_type": "text",
  "payload": {
    "text": "I can see you have 1 transactions in your history with 0 categorized transaction types and 0 budget targets. Here are your most recent transactions: • 2024-01-15: Coffee Shop (-5.5 USD)"
  }
}
```

### Next Implementation Priority

**Immediate:** Complete production hardening with proper authentication, monitoring, and error handling patterns to prepare for production deployment.

**Future Enhancements:**
- Database integration in agent service for persistent conversation storage
- Advanced agent capabilities with full ADK integration
- Service mesh for advanced routing and monitoring
- Frontend updates to leverage enhanced chat capabilities
