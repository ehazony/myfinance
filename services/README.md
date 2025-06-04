# Services Overview

This folder contains separate services extracted from the monolithic project.
Each service has its own requirements and Dockerfile.

- `core_api` – Django REST API and database migrations.
- `agent_service` – ADK/LangChain agents using the API or shared models.
- `scraper_service` – bank scraping utilities with Selenium.
- `telegram_bot_service` – lightweight Telegram bot.

See `docs/design.md` for the overall architecture and migration plan.
