# OpenAPI-First Finance Agent Architecture

## Overview

This document describes the implementation of an OpenAPI-first architecture for the Finance Agent Service, where all communication between the agent service and the Django Core API is handled through auto-generated clients from OpenAPI specifications.

## Architecture Components

### 1. Django Core API (Backend)
- **Location**: `services/core_api/`
- **Role**: Provides comprehensive financial data APIs with OpenAPI documentation
- **Key Features**:
  - Agent-specific endpoints (`/api/agent/`)
  - Automatic OpenAPI schema generation via `drf-spectacular`
  - Token-based authentication
  - Structured data models for all financial entities

### 2. Generated OpenAPI Client
- **Location**: `services/agent_service/_client/`
- **Generation Tool**: `openapi-python-client`
- **Key Features**:
  - Fully typed Python client with Pydantic models
  - Async and sync support
  - Proper authentication handling
  - Error handling and status codes

### 3. Finance Data Client Wrapper
- **Location**: `services/agent_service/tools/finance_data_client.py`
- **Role**: Provides a clean interface around the generated client
- **Key Features**:
  - Synchronous wrappers for agent compatibility
  - Token-based authentication management
  - Error handling and logging
  - Data transformation for agent consumption

### 4. Agent Finance Tools
- **Location**: `services/agent_service/agents_adk/tools/finance_tools.py`
- **Role**: Agent-facing tools that use the OpenAPI client
- **Key Features**:
  - Maintains existing tool signatures for backward compatibility
  - JSON string responses for agent consumption
  - Comprehensive error handling

## Data Flow

```
Agent Request → Finance Tools → OpenAPI Client → HTTP Request → Django API
Django Response ← HTTP Response ← OpenAPI Client ← Finance Tools ← Agent
```

## Key Benefits

### ✅ Type Safety
- Generated Pydantic models ensure data consistency
- Compile-time type checking for all API interactions
- Automatic validation of request/response data

### ✅ Auto-Synchronization
- Client regenerates automatically when API changes
- No manual maintenance of API interfaces
- Always in sync with backend capabilities

### ✅ Service Decoupling
- Agent service has no direct database dependencies
- Services can be deployed and scaled independently
- Clear separation of concerns

### ✅ Proper Authentication
- Token-based authentication with Django backend
- Secure communication between services
- User context preserved across service boundaries

### ✅ Error Handling
- Structured error responses and logging
- Graceful degradation when services are unavailable
- Clear error propagation to agents

### ✅ Testing & Development
- Easy to mock and test individual components
- Clear interfaces for integration testing
- Development environment flexibility

## Implementation Details

### OpenAPI Schema Generation

The Django backend automatically generates OpenAPI schemas using `drf-spectacular`:

```bash
# Generate schema file
cd services/core_api
python manage.py spectacular --file openapi-schema.yaml
```

### Client Generation

The Python client is generated using `openapi-python-client`:

```bash
# Generate client
cd services/agent_service
openapi-python-client generate --path ../core_api/openapi-schema.yaml --meta none
```

### Authentication

The client uses Django's token authentication:

```python
client = AuthenticatedClient(
    base_url="http://localhost:8000",
    token=user_token,
    prefix="Token"  # Django uses "Token" prefix
)
```

### Agent Tool Integration

Finance tools maintain backward compatibility while using the OpenAPI client:

```python
def get_user_transactions(user_id: str, **kwargs) -> str:
    """Get user transactions (using generated OpenAPI client)."""
    client = get_finance_client()
    transactions = client.get_filtered_transactions_sync(token=user_id, **kwargs)
    return json.dumps({'transactions': transactions})
```

## Available Endpoints

### Agent API Endpoints
- `GET /api/agent/financial-context/` - Complete financial context
- `GET /api/agent/transactions/` - Filtered transactions
- `GET /api/agent/budget-analysis/` - Budget vs actual analysis
- `GET /api/agent/account-summary/` - Account balances and stats
- `GET /api/agent/conversation-context/` - Conversation history

### Schema and Documentation
- `GET /api/schema/` - OpenAPI schema (YAML/JSON)
- `GET /api/schema/swagger-ui/` - Interactive API documentation
- `GET /api/schema/redoc/` - Alternative API documentation

## Development Workflow

### 1. Adding New Endpoints

1. Add endpoint to Django Core API
2. Update OpenAPI documentation with `@extend_schema`
3. Regenerate schema: `python manage.py spectacular --file openapi-schema.yaml`
4. Regenerate client: `openapi-python-client generate --path ../core_api/openapi-schema.yaml --meta none`
5. Update finance tools to use new endpoints

### 2. Testing

```bash
# Test generated client
cd services/agent_service
python test_generated_client.py

# Demo architecture
python demo_openapi_architecture.py
```

### 3. Running Services

```bash
# Start Django Core API
cd services/core_api
python manage.py runserver 8000

# Start Agent Service
cd services/agent_service
python main.py
```

## File Structure

```
services/
├── core_api/
│   ├── app/agent_api.py           # Agent-specific API endpoints
│   ├── finance/urls.py            # OpenAPI schema URLs
│   └── openapi-schema.yaml        # Generated schema
└── agent_service/
    ├── _client/                   # Generated OpenAPI client
    │   ├── client.py              # Client classes
    │   ├── models/                # Pydantic models
    │   ├── api/api/               # API functions
    │   ├── types.py               # Type definitions
    │   └── errors.py              # Error handling
    ├── tools/
    │   └── finance_data_client.py # Client wrapper
    ├── agents_adk/tools/
    │   └── finance_tools.py       # Agent tools
    ├── services/
    │   └── adk_chat_service.py    # Chat service integration
    └── main.py                    # FastAPI service
```

## Configuration

### Environment Variables

```bash
# Django Core API
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url

# Agent Service
CORE_API_BASE_URL=http://localhost:8000
AGENT_SERVICE_PORT=8001
```

### Dependencies

```bash
# Core API
pip install drf-spectacular

# Agent Service
pip install openapi-python-client httpx pydantic
```

## Troubleshooting

### Common Issues

1. **401 Authentication Errors**
   - Ensure valid user tokens are being passed
   - Check Django authentication configuration

2. **Event Loop Errors**
   - Use sync wrappers for non-async contexts
   - Ensure proper async/await usage

3. **Import Errors**
   - Regenerate client if schema has changed
   - Check Python path configuration

### Regenerating Client

If you encounter issues with the generated client:

```bash
cd services/agent_service
rm -rf _client
openapi-python-client generate --path ../core_api/openapi-schema.yaml --meta none
```

## Future Enhancements

1. **Automatic Client Regeneration**: Set up CI/CD to regenerate client on schema changes
2. **Client Versioning**: Version clients to handle backward compatibility
3. **Caching**: Add response caching for frequently accessed data
4. **Monitoring**: Add metrics and monitoring for API calls
5. **Rate Limiting**: Implement rate limiting for API endpoints

## Conclusion

This OpenAPI-first architecture provides a robust, scalable, and maintainable foundation for the Finance Agent Service. It ensures type safety, automatic synchronization, and clear separation of concerns while maintaining backward compatibility with existing agent tools. 