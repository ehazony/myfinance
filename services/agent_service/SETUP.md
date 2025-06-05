# Agent Service Setup

This document explains how to set up the agent service with its dependencies, including the local `finance_common` package.

## Quick Setup (Recommended)

Use the provided setup script that handles everything automatically:

```bash
# From the project root
./services/agent_service/setup.sh
```

This script will:
- ✅ Validate that `finance_common` exists and is properly configured
- ✅ Install `finance_common` as an editable package
- ✅ Install all other dependencies from `requirements.txt`
- ✅ Work in both local and remote environments

## Manual Setup Options

### Option 1: Standard Installation
```bash
# Install finance_common first
pip install -e finance_common

# Then install agent service dependencies
pip install -r services/agent_service/requirements.txt
```

### Option 2: Development Installation
For local development when you need to modify `finance_common`:
```bash
pip install -r services/agent_service/requirements-dev.txt
```

## Remote Environment Setup

The setup script is designed to work in remote environments (Docker, CI/CD, cloud deployments) by:

1. **Dynamic path resolution**: Calculates paths relative to the script location
2. **Validation**: Checks that `finance_common` exists and is properly configured
3. **Error handling**: Provides clear error messages if setup fails
4. **No hardcoded paths**: Works regardless of where the project is located

### For Docker

Add this to your Dockerfile:
```dockerfile
COPY . /app
WORKDIR /app
RUN ./services/agent_service/setup.sh
```

### For CI/CD

Add this to your workflow:
```yaml
- name: Setup agent service
  run: ./services/agent_service/setup.sh
```

## Files Overview

- `requirements.txt` - Standard dependencies (no local packages)
- `requirements-dev.txt` - Development dependencies (includes editable finance_common)
- `setup.sh` - Automated setup script (works everywhere)
- `SETUP.md` - This documentation

## Troubleshooting

### "finance_common directory not found"
- Ensure you're running the script from the correct location
- Check that the `finance_common` directory exists at the project root

### "setup.py not found in finance_common"
- The `finance_common` package is not properly configured
- Ensure `finance_common/setup.py` exists

### Permission errors on setup.sh
```bash
chmod +x services/agent_service/setup.sh
```

## Why This Approach?

The previous approach using `-e ../../finance_common` in requirements.txt had issues with:
- ❌ Newer pip versions being stricter about relative paths
- ❌ Different path resolution in various environments
- ❌ Remote deployment environments not recognizing the relative path

This setup script approach provides:
- ✅ Reliable installation across all environments
- ✅ Clear error messages and validation
- ✅ Separation of concerns (standard deps vs local packages)
- ✅ Both development and production installation options 