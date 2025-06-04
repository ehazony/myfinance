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
