# Agent Guidelines

## Overview
This repository contains a Django backend and a React frontend. The backend lives in various Python packages such as `finance`, `app`, `core` and `telegram_bot`. The frontend is located in `front/dashboard`. Docker compose files are provided for local development and testing.

## Structure
- `manage.py` – entry point for Django commands.
- `finance/` – main Django project settings and Celery configuration.
- `core/` – additional Django project used by templates.
- `app/` – domain models and business logic.
- `telegram_bot/` – code for interacting with Telegram.
- `front/dashboard/` – React dashboard application.
- `docker-compose.yml` – runs the application with Redis, Celery and Nginx.
- `docker-compose.test.yml` – test environment.
- `.env.prod` – environment variables used by docker-compose.

## Running the application
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
The React dashboard resides in `front/dashboard`. See its `README.md` for package.json scripts and development instructions.
The repository also contains `scripts/setup_mobile_app.sh` which bootstraps a
React Native project described in `docs/react_native_migration.md`. Run this
script **while network access is available** to create the `mobile/` directory
and install dependencies.

## Important notes
- Keep sensitive information such as credentials out of commits. Environment variables are stored in `.env.prod`.
- If you add or change setup steps, test commands, or repository structure, update both this `AGENT.md` file and the root `README.md` accordingly.
- Ensure new code includes tests where possible.

