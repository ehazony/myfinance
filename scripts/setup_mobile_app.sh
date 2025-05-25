#!/bin/bash
# Bootstrap the React Native mobile app.
# Run this script while network access is available.
# It installs Expo CLI, creates the mobile app directory via Expo, and installs
# all dependencies required for development.
set -e

# Install pnpm globally if not present
if ! command -v pnpm >/dev/null; then
  npm install -g pnpm
fi

# Install Expo CLI if not present
if ! command -v expo >/dev/null; then
  pnpm install -g expo-cli
fi

# Create the mobile app if it does not exist
if [ ! -d "mobile" ]; then
  pnpm create expo-app mobile --template
fi

# Install mobile dependencies
cd mobile
pnpm install

# Core libraries
pnpm add @react-navigation/native @reduxjs/toolkit @tanstack/react-query \
  react-native-paper react-hook-form yup

# Additional tooling
pnpm add expo-router @shopify/flash-list nativewind react-native-reanimated \
  moti zod @sentry/react-native

# Dev dependencies
pnpm add -D detox @storybook/react-native openapi-zod-client

cd ..

echo "Mobile app setup complete."

