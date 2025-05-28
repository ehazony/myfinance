# FinanceAgent Chat View Design

## Overview

This document describes how to implement the chat view that appears immediately after login in the FinanceAgent mobile app. The chat is the primary feature of the application and allows users to interact with an AI-powered financial assistant. The view must support rich message types and integrate with the existing Django backend.

## Frontend Implementation

1. **Location**: `front/FinanceAgent` (Expo / React Native codebase).
2. **New Screen**: Create `ChatScreen.tsx` under `src/screens/main/`.
3. **Navigation**: Update `MainNavigator.tsx` to include a `Chat` tab as the first screen after login. This ensures the chat is the initial destination once a user is authenticated.
4. **UI Library**: Use React Native Paper components to maintain consistent theming. For advanced chat features consider integrating a library such as `react-native-gifted-chat` or building custom components.
5. **Message Types**:
   - Text messages
   - Buttons / quick replies
   - Cards with images
   - Charts (e.g., line, bar, pie) using `react-native-chart-kit` or `victory-native`
   - Rich links or attachments
6. **Styling**: Apply the existing theme from `ThemeContext` to customize bubble colors, fonts, and spacing. Provide both light and dark mode styles.
7. **State Management**: Store conversation state in React context or a Redux slice. Persist messages locally (AsyncStorage) for offline support.
8. **API Interaction**: Use the existing API client in `src/api` to send and receive messages. Implement WebSocket support with `expo-websocket` or `@react-native-community/netinfo` + `socket.io-client` for real-time updates.
9. **Error Handling**: Display a placeholder message if the network is unavailable and queue outgoing messages for later retry.

## Backend Implementation

1. **Models** (in the Django app):
   - `Conversation` representing a chat session linked to a user.
   - `Message` with fields for sender (user or agent), content type (text, chart, button set, etc.), payload (JSON), timestamp, and status.
2. **Views / API Endpoints**:
   - `POST /api/chat/send/` – accepts a user message and returns the agent's response.
   - `GET /api/chat/history/` – fetches recent messages for the conversation.
   - WebSocket endpoint using **Django Channels** for streaming agent replies and updates.
3. **Business Logic**: A service layer under `app/` should handle message creation and call any LLM or external API to generate agent responses. Use Celery tasks for long‑running jobs (e.g., generating charts).
4. **Authentication**: Reuse existing JWT auth. The WebSocket connection must validate the user's token before accepting messages.
5. **Serialization**: Use Django REST Framework serializers with validation for different message types.

## Agent Implementation Steps

1. **Add ChatScreen**:
   - Create the new component with a list of messages and an input box for user text.
   - Integrate quick reply buttons and custom message cards.
2. **Update Navigation**:
   - Modify `MainNavigator.tsx` to include `<Tab.Screen name="Chat" component={ChatScreen} />` as the first tab.
3. **Connect to Backend**:
   - Implement functions in `src/services/chatService.ts` for sending messages and subscribing to updates via WebSocket.
4. **Handle Rich Content**:
   - Define a TypeScript union type for message payloads (text, chart data, button sets). Render the appropriate component based on the message's `content_type`.
5. **Django Models**:
   - Add `Conversation` and `Message` models under `app/models`. Write migrations and register them in the admin interface for debugging.
6. **API Routes**:
   - Use Django REST Framework viewsets or generic views for the REST endpoints. Configure URL routes under `core/urls.py` or a dedicated `chat` app.
7. **WebSockets**:
   - Install and configure `django-channels`. Create a consumer that authenticates the user and relays messages to and from the agent.
8. **Testing**:
   - Add unit tests for the new models and API views using Django's test framework.
   - Create basic integration tests for the chat screen using React Native Testing Library.

## Summary

By following this design, the FinanceAgent mobile app will feature a robust chat interface directly after login. Users can send messages, view financial charts, and interact with buttons or other rich responses. The Django backend manages conversations and real-time communication, enabling an intelligent financial assistant experience.

