# React Native Migration Design

## Overview

This document outlines the plan to rewrite the existing web-based React dashboard located under `front/dashboard` into a modern React Native application written in TypeScript. The new application should run on Android, iOS and the web (via React Native Web) while preserving all functionality of the current dashboard.

The rewrite will involve creating a new project (using Expo for simplicity) and porting logic and screens from the existing codebase into React Native components. The goal is to maintain business logic while replacing Material-UI and DOM specific code with React Native equivalents.

## Technology Stack

- **React Native** (latest stable version)
- **Expo** for cross-platform development and build tooling
- **TypeScript** for type safety
- **React Native Web** to support browser rendering
- **React Navigation v6** for routing and navigation
- **Redux Toolkit** (and optionally Recoil) for state management
- **React Query** for data fetching and caching
- **React Hook Form** + **Yup** for form management and validation
- **React Native Paper** or **NativeBase** as the UI component library
- **Jest** with **React Native Testing Library** for unit tests
- **Expo EAS** for building and submitting mobile apps

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
   - Use React Navigation's stack and tab navigators.
   - For web support, configure `createNativeStackNavigator` with linking settings.
   - Replace React Router routes with screen components mapped in navigators.

3. **State Management**
   - Migrate existing Redux logic to Redux Toolkit slices in TypeScript.
   - Use Recoil for granular state if required, mirroring current usage.

4. **Styles**
   - Replace CSS modules and styled-components with React Native StyleSheet or UI library theming.
   - Theme should support light/dark modes and follow modern mobile design patterns.

5. **Forms and Validation**
   - Port Formik + Yup forms to React Hook Form with resolver for Yup to leverage React Native performance.

6. **Network Layer**
   - Create a centralized API service using fetch or Axios with TypeScript interfaces.
   - Incorporate token handling (the current app uses cookie-based auth) using secure storage on mobile.

7. **Testing**
   - Write tests using Jest and React Native Testing Library.
   - Reuse logic tests from the existing project where possible.

8. **Continuous Integration**
   - Configure GitHub Actions (or existing CI pipeline) to run Jest tests and Expo build checks.

## Migration Strategy

1. **Bootstrap New Project**
   - Create a new Expo app with TypeScript template: `npx create-expo-app@latest -t expo-template-blank-typescript myApp`.
   - Add dependencies listed above.

2. **Set Up Navigation and State**
   - Configure `navigation` folder with stack/tab navigators.
   - Set up Redux Toolkit store and create initial slices corresponding to existing Redux modules.

3. **Port Authentication Flow**
   - Reimplement login and registration screens using React Native Paper components.
   - Connect to backend endpoints already used in `AuthLogin.js` and `AuthRegister.js`.
   - Store authentication token securely (AsyncStorage or Expo SecureStore) and set up automatic token refresh if applicable.

4. **Port Dashboard Screens**
   - Convert charts and widgets under `src/pages/dashboard` using libraries such as `react-native-svg` and `victory-native` or `react-native-chart-kit`.
   - Replace Material‑UI components with React Native equivalents.

5. **Port Transactions and Account Screens**
   - Implement list views using `FlatList` or `SectionList`.
   - Preserve filtering/sorting logic in TypeScript.

6. **Port Additional Pages**
   - Convert the remaining pages under `src/pages` to screens: account tables, components overview, extra pages, etc.

7. **Implement Web Compatibility**
   - Configure `app.json` / `app.config.ts` to enable web builds.
   - Ensure navigation linking works in the browser.
   - Use platform-specific styles and components where necessary (e.g., `Platform.OS === 'web'`).

8. **Testing and Validation**
   - Write unit tests for all Redux slices and major components.
   - Use Expo's web, iOS, and Android simulators for manual testing.
   - Ensure parity with existing web app functionality before decommissioning old code.

9. **Deployment**
   - Use Expo EAS build for Android and iOS apps.
   - Deploy the web version to hosting platforms such as Vercel or Netlify.

## Detailed Task List

1. **Project Setup**
   - [ ] Initialize Git repository for the new app (in a separate directory)
   - [ ] Create `README.md` with setup instructions for Expo and yarn

2. **Dependencies**
   - [ ] Install React Navigation, Redux Toolkit, React Query, React Native Paper, React Hook Form, Yup, and testing libraries
   - [ ] Configure TypeScript path aliases in `tsconfig.json`

3. **Basic Infrastructure**
   - [ ] Implement navigation containers and root navigators
   - [ ] Set up Redux Toolkit store and example slice
   - [ ] Create authentication service (login/logout API calls)
   - [ ] Integrate secure storage for auth token

4. **UI Components**
   - [ ] Build common components (buttons, form inputs, card layouts) using React Native Paper
   - [ ] Implement theming with light/dark mode support

5. **Screens**
   - [ ] Authentication screens: Login, Register, Forgot Password
   - [ ] Dashboard overview with charts and summary widgets
   - [ ] Transactions list with filters and search
   - [ ] Accounts management
   - [ ] Additional screens from `components-overview` and `extra-pages`

6. **Data Handling**
   - [ ] Port existing Redux logic to Toolkit slices (transactions, accounts, user profile)
   - [ ] Replace direct fetch calls with React Query hooks
   - [ ] Set up global error handling and loading indicators

7. **Testing**
   - [ ] Write unit tests for slices and utilities
   - [ ] Add component tests with React Native Testing Library
   - [ ] Configure CI to run tests on push

8. **Web Support**
   - [ ] Verify all screens render correctly in the browser
   - [ ] Address any platform-specific styling or event issues

9. **Deployment Pipeline**
   - [ ] Configure Expo EAS for Android/iOS builds
   - [ ] Add scripts for building the web version
   - [ ] Document the release process

10. **Gradual Rollout**
   - [ ] Deploy beta versions to testers
   - [ ] Collect feedback and fix issues
   - [ ] Finalize migration and archive the old web-only project

## Design Considerations

- **Modern UI**: Follow Material Design 3 or similar guidelines using React Native Paper's theming capabilities. The layout should adapt to various screen sizes, including tablets and desktops.
- **Accessibility**: Ensure text scaling, color contrast, and screen reader support.
- **Performance**: Use FlatList optimizations, lazy loading, and caching where possible. Avoid unnecessary re-renders by leveraging React.memo and selectors.
- **Type Safety**: Write all code in strict TypeScript, enabling `noImplicitAny` and other strict compiler options.
- **Code Quality**: Enforce ESLint and Prettier with standard React Native configurations. Use husky + lint-staged to check code before commits.

## Conclusion

This migration will modernize the dashboard and enable true cross-platform delivery. While the process requires rebuilding the UI layer, the business logic can largely be preserved. Careful planning and incremental development will ensure feature parity while taking advantage of React Native's ecosystem.

