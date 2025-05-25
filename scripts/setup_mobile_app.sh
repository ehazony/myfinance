#!/bin/bash
# Bootstrap the React Native mobile app.
# Run this script while network access is available.
# It installs Expo CLI, creates the mobile app directory via Expo, and installs
# all dependencies required for development.
set -e

# Set PNPM_HOME and ensure global bin directory is available
export PNPM_HOME="$HOME/.pnpm-global"
export PATH="$PNPM_HOME/bin:$PATH"
mkdir -p "$PNPM_HOME/bin"

# Install pnpm globally if not present
if ! command -v pnpm >/dev/null; then
  npm install -g pnpm
fi

# Run pnpm setup to initialize environment
pnpm setup

# Ensure pnpm global bin directory exists and is in PATH
PNPM_GLOBAL_BIN=$(pnpm bin -g 2>/dev/null || true)
if [ -z "$PNPM_GLOBAL_BIN" ]; then
  echo "[ERROR] Could not determine pnpm global bin directory." >&2
  exit 1
fi
if [ ! -d "$PNPM_GLOBAL_BIN" ]; then
  mkdir -p "$PNPM_GLOBAL_BIN"
  echo "[INFO] Created pnpm global bin directory: $PNPM_GLOBAL_BIN"
fi
if [[ ":$PATH:" != *":$PNPM_GLOBAL_BIN:"* ]]; then
  export PATH="$PNPM_GLOBAL_BIN:$PATH"
  echo "[INFO] Added pnpm global bin directory to PATH for this script: $PNPM_GLOBAL_BIN"
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

