# Agent Guidelines

## Overview
This repository contains a Django backend and a React frontend. The backend lives in various Python packages such as `finance`, `app`, `core` and `telegram_bot`. The frontend is located in `front/dashboard`. Docker compose files are provided for local development and testing.

## Structure
- `manage.py` – entry point for Django commands.
- `finance/` – main Django project settings and Celery configuration.
- `core/` – additional Django project used by templates.
- `app/` – domain models and business logic.
- `telegram_bot/` – code for interacting with Telegram.
- `front/dashboard/` – Legacy React dashboard application.
- `front/FinanceTracker/` – Modern Next.js/Expo app for the new finance dashboard (web and mobile).
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
The legacy React dashboard resides in `front/dashboard`. See its `README.md` for package.json scripts and development instructions.
The new FinanceTracker app resides in `front/FinanceTracker`. See its `README.md` for Next.js/Expo usage and development instructions.

## FinanceTracker App

The new FinanceTracker app is a modern, unified codebase for both web and mobile finance dashboards. It uses Next.js for the web frontend and Expo (React Native) for mobile, sharing most business logic and UI components.

- **Location:** `front/FinanceTracker`
- **Purpose:** Modern replacement for the old dashboard, supporting both web and mobile from a single codebase.
- **Web (Next.js):**
  - Install dependencies: `npm install` or `pnpm install`
  - Start dev server: `npm run dev` or `pnpm dev`
  - Runs at http://localhost:3000/
- **Mobile (Expo):**
  - Install dependencies: `npm install` or `pnpm install`
  - Start Expo: `npx expo start`
  - Use Expo Go app or an emulator to preview on your device.
- **See** `front/FinanceTracker/README.md` **for more details and advanced usage.**

## Important notes
- Keep sensitive information such as credentials out of commits. Environment variables are stored in `.env.prod`.
- If you add or change setup steps, test commands, or repository structure, update both this `AGENT.md` file and the root `README.md` accordingly. If you change the FinanceTracker app setup, update its README as well.
- Ensure new code includes tests where possible.

