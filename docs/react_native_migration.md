# React Native Migration Design

## Overview

This document outlines the plan to rewrite the existing web-based React dashboard located under `front/dashboard` into a modern React Native application written in TypeScript. The new application should run on Android, iOS and the web (via React Native Web) while preserving all functionality of the current dashboard.

The rewrite will involve creating a new project (using Expo for simplicity) and porting logic and screens from the existing codebase into React Native components. The goal is to maintain business logic while replacing Material-UI and DOM specific code with React Native equivalents.

## Technology Stack

- **React Native** (latest stable version)
- **Expo** for cross-platform development and build tooling
- **TypeScript** for type safety
- **FlashList** for high‑performance lists
- **NativeWind** (or **Tamagui**) for utility‑first styling and design tokens
- **Reanimated 3** + **Moti** for performant animations and gestures
- **Zod** for schema validation (used with React Hook Form)
- **Hermes** JavaScript engine (enabled by default in React Native 0.74)
- **Sentry** (or **Bugsnag**) for crash/error monitoring
- **Detox** + **Storybook 7** for end‑to‑end and visual testing
- **drf‑spectacular** for OpenAPI 3.1 schema generation from Django REST Framework (backend)
- **msw-openapi** for mocking API requests based on OpenAPI specs

## API Contract Workflow

### Backend — Export *openapi.yaml*

1. Install **drf‑spectacular**  
   ```bash
   pip install drf-spectacular
   ```
2. In `settings.py`, set the schema class:  
   ```python
   REST_FRAMEWORK = {
       "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
   }
   ```
3. Generate and commit the spec:  
   ```bash
   python manage.py spectacular --file api/openapi.yaml
   git add api/openapi.yaml
   ```

### Front‑end — Generate the Zod‑typed client

1. Add the dev dependency:  
   ```bash
   pnpm add -D openapi-zod-client
   ```
2. Add a script in **package.json**:  
   ```jsonc
   {
     "scripts": {
       "generate:api": "openapi-zod-client api/openapi.yaml -o src/api/client.ts"
     }
   }
   ```
3. Run it whenever `openapi.yaml` changes:  
   ```bash
   pnpm generate:api
   ```
4. Use the client:  
   ```ts
   import { api } from "@/api/client";
   const user = await api.getUser({ params: { id: "123" } });
   ```

### CI / Pre‑build hook
Add `pnpm generate:api` to the **mobile app’s** `prebuild` script and to backend CI so the generated client is always in sync.

## App Architecture

1. **Project Structure**
   - `src/` – all TypeScript source files
   - `src/components/` – reusable UI components
   - `src/screens/` – screen components (equivalent to pages)
   - `src/navigation/` – navigators and routing setup
   - `src/store/` – Redux Toolkit slices and store configuration
   - `src/services/` – API clients and network utilities
   - `src/assets/` – images, fonts, icons
   - `src/hooks/` – custom hooks
   - `src/types/` – shared TypeScript type definitions

2. **Navigation**
   - Use **Expo Router** for file‑based routing. It automatically builds React Navigation 7 stacks/tabs, deep links and web URLs.
   - For modal or drawer patterns, create additional React Navigation navigators inside Expo Router layout files.
   - Remove the old React Router linking tables—the file system is the source of truth.

3. **State Management**
   - Migrate existing Redux logic to Redux Toolkit slices in TypeScript.
   - Use Recoil for granular state if required, mirroring current usage.
   - Prefer **TanStack Query** for all server‑state. If most of your Redux slices are server data, migrate them and keep Redux (or small **Zustand/Jotai** stores) only for local UI state.

4. **Styles**
   - Adopt **NativeWind** (Tailwind syntax) or **Tamagui** for styling. Both compile static styles for web and mobile and expose design‑system tokens.
   - Replace CSS modules and styled-components with React Native StyleSheet or UI library theming.
   - Keep React Native Paper (MD3) components, or combine Paper primitives with NativeWind utility classes.
   - Theme should support light/dark modes and follow modern mobile design patterns.

5. **Forms and Validation**
   - Port Formik + Yup forms to **React Hook Form** using **Zod** resolvers. This provides type‑safe schemas and better React Native performance.

6. **Network Layer**
   - Create a centralized API service using fetch or Axios with TypeScript interfaces.
   - Incorporate token handling (the current app uses cookie-based auth) using secure storage on mobile.

7. **Testing**
   - Write tests using Jest and React Native Testing Library.
   - Reuse logic tests from the existing project where possible.
   - Add **Detox** or **Expo Test Runner** for device‑level end‑to‑end tests.
   - Integrate **Storybook 7** for component isolation and visual regression.

8. **Continuous Integration**
   - Configure GitHub Actions (or existing CI pipeline) to run Jest tests and Expo build checks.

9. **Performance**
   - Use **FlashList** for any large scrolling collections to reduce memory and jank.
   - Ensure **Hermes** is enabled (default in RN 0.74).
   - Use **Reanimated 3** and **Moti** for 60 fps interactions.
   - Consider **React Native Skia** for GPU‑accelerated charts and graphics.

## Migration Strategy

1. **Project Setup**
   - [ ] Initialize Git repository for the new app (in a separate directory)
   - [ ] Create `README.md` with setup instructions for Expo and yarn
   - Ensure `api/openapi.yaml` is committed from the backend and runnable by the `generate:api` script.

2. **Dependencies**
   - [ ] Install React Navigation, Redux Toolkit, React Query, React Native Paper, React Hook Form, Yup, and testing libraries, msw-openapi
   - [ ] Configure TypeScript path aliases in `tsconfig.json`
   - [ ] Install Expo Router, FlashList, NativeWind (and/or Tamagui), Reanimated 3, Moti, Zod, Sentry, Detox, Storybook 7, openapi‑zod‑client

3. **Basic Infrastructure**
   - [ ] Implement navigation containers and root navigators
   - [ ] Set up Redux Toolkit store and example slice
   - [ ] Create authentication service (login/logout API calls)
   - [ ] Integrate secure storage for auth token
   - [ ] Add and run `generate:api` script to produce `src/api/client.ts` from `api/openapi.yaml`

4. **UI Components**
   - [ ] Build common components (buttons, form inputs, card layouts) using React Native Paper
   - [ ] Implement theming with light/dark mode support

5. **Screens**
   - [ ] Authentication screens: Login, Register, Forgot Password
   - [ ] Dashboard overview with charts and summary widgets
   - [ ] Transactions list with filters and search
   - [ ] Accounts management

6. **Data Handling**
   - [ ] Port existing Redux logic to Toolkit slices (transactions, accounts, user profile)
   - [ ] Replace direct fetch calls with React Query hooks
   - [ ] Set up global error handling and loading indicators

7. **Testing**
   - [ ] Write unit tests for slices and utilities
   - [ ] Add component tests with React Native Testing Library
   - [ ] Configure CI to run tests on push
   - [ ] Configure Detox E2E tests for critical flows
   - [ ] Set up Storybook 7 with on‑device UI screens

8. **Web Support**
   - [ ] Verify all screens render correctly in the browser
   - [ ] Address any platform-specific styling or event issues

9. **Performance**
   - [ ] Enable Hermes engine in `expo-build-properties`
   - [ ] Replace large FlatLists with FlashList
   - [ ] Audit re‑renders with React DevTools and memoize where needed

10. **Deployment Pipeline**
    - [ ] Configure Expo EAS for Android/iOS builds
    - [ ] Add scripts for building the web version
    - [ ] Document the release process

11. **Gradual Rollout**
    - [ ] Deploy beta versions to testers
    - [ ] Collect feedback and fix issues
    - [ ] Finalize migration and archive the old web-only project

## Design Considerations

- **Modern UI**: Follow Material Design 3 or similar guidelines using React Native Paper's theming capabilities. The layout should adapt to various screen sizes, including tablets and desktops.
- **Accessibility**: Ensure text scaling, color contrast, and screen reader support. Provide full RTL support and test Hebrew/Arabic layouts using `I18nManager`.
- **Performance**: FlashList, Reanimated 3, use FlatList optimizations, lazy loading, and caching where possible. Avoid unnecessary re-renders by leveraging React.memo and selectors. Hermes, Skia.
- **Type Safety**: Write all code in strict TypeScript, enabling `noImplicitAny` and other strict compiler options.
- **Code Quality**: Enforce ESLint and Prettier with standard React Native configurations. Use husky + lint-staged to check code before commits.
- **Monitoring & Analytics**: Configure Sentry/Bugsnag before the first beta so crashes in early testing are captured.

## Conclusion

This migration will modernize the dashboard and enable true cross-platform delivery. While the process requires rebuilding the UI layer, the business logic can largely be preserved. Careful planning and incremental development will ensure feature parity while taking advantage of React Native's ecosystem.

By adopting Expo Router, FlashList, NativeWind/Tamagui, Zod, and a modern performance + monitoring stack, the rewritten app will not only match the old dashboard feature‑for‑feature but also meet 2025 standards for speed, reliability and developer velocity.
