# NoteApp FastAPI Backend

A modern FastAPI server application that provides a comprehensive note-taking API with AI enrichment capabilities. Built with a modular architecture using dependency injection and includes comprehensive integration testing.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 📝 **Note Management** - Full CRUD operations for user notes
- 🤖 **AI Enrichment** - LLM service for generating note metadata and insights
- 🔐 **User Isolation** - Notes are isolated by user ID with proper authorization
- 📚 **Interactive Docs** - Auto-generated Swagger UI documentation
- 🧪 **Comprehensive Integration Testing** - Full test coverage with pytest testing the entire system through the router
- 🐛 **Debug Support** - Integrated debugpy for development debugging
- 🏗️ **Modular Architecture** - Clean separation of concerns with services and dependency injection

## Architecture

The application uses a modular structure:

```
note-app/
├── main.py                    # Main FastAPI application with CORS, debug support, and global exception handling
├── main_router.py            # Main application router (root endpoint, welcome page)
├── requirements.txt          # Python dependencies including debugpy and pytest
├── README.md                 # This file
├── run-server.sh             # Server startup script with debug options
├── .vscode/                  # VS Code debugger configuration
├── middleware/               # Custom middleware components
│   ├── __init__.py           # Middleware package exports
│   └── exception_handler.py  # Global exception handler middleware
├── notes/                    # Notes module (main functionality)
│   ├── __init__.py           # Module initialization
│   ├── models/               # Pydantic models organized by type
│   │   ├── __init__.py       # Models package exports
│   │   ├── exceptions.py     # Custom exceptions
│   │   ├── enums.py          # Enumerations (e.g., Sentiment)
│   │   ├── note_models.py    # Note-related models
│   │   └── llm_models.py     # LLM enrichment models
│   ├── interfaces/           # Service interface protocols
│   │   ├── __init__.py       # Interfaces package exports
│   │   └── llm_service_protocol.py # LLM service interface
│   ├── services/             # Business logic services
│   │   ├── __init__.py       # Services package exports
│   │   ├── notes_service.py  # Business logic service (singleton)
│   │   ├── gemini_service.py    # Real LLM service using Gemini API with structured output
│   │   └── llm_stub_service.py    # AI enrichment stub service for testing
│   ├── dependencies.py       # Dependency injection
│   ├── router.py             # API endpoints
│   └── tests/                # Comprehensive integration test suite
│       └── test_router_integration.py # Integration tests covering all endpoints and services through the router

```

## API Endpoints

### Notes Module (Main Functionality)

- `POST /notes` - Create a new note
- `GET /notes` - Get all notes for a user (with user_id query parameter)
- `GET /notes/{id}` - Get a specific note by ID
- `PATCH /notes/{id}/enrich` - Enrich note with AI-generated metadata
- `PATCH /notes/{id}` - Update note content
- `DELETE /notes/{id}` - Delete a note

### General

- `GET /` - Welcome page with API information and debug status
- `GET /docs` - Interactive API documentation (Swagger UI)

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application

**Using the startup script (recommended):**

```bash
./run-server.sh
```

**With debug mode:**

```bash
./run-server.sh --debug
```

**Custom debug port:**

```bash
./run-server.sh --debug --debug-port 5679
```

**Using uvicorn directly:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Application

- **Main Page**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs
- **Notes API**: http://localhost:8000/notes

## Development

### Running Tests

The application includes comprehensive integration tests that test the entire system through the router endpoints:

```bash
# Run all integration tests
pytest notes/tests/ -v

# Run the integration test file
pytest notes/tests/test_router_integration.py -v

# Run with coverage
pytest notes/tests/ --cov=notes --cov-report=html
```

**Integration Test Coverage Includes:**

- **Complete System Testing**: Tests all endpoints through the router with properly injected services
- **Service Integration**: Tests how all services work together in real scenarios
- **Error Handling**: Tests router-level error handling and middleware
- **Parameterized Tests**: Multiple input scenarios for comprehensive coverage
- **Mock Dependencies**: Isolated testing with mocked external services (Gemini API)
- **Real Service Logic**: Tests actual service implementations, not mocked business logic

**Test Structure:**

- **TestCreateNote**: Tests note creation with various content types and validation
- **TestGetNotes**: Tests note retrieval and user isolation
- **TestGetNote**: Tests single note retrieval and authorization
- **TestEnrichNote**: Tests AI enrichment functionality
- **TestUpdateNote**: Tests note updates and content modification
- **TestDeleteNote**: Tests note deletion and cleanup
- **TestGetServiceStats**: Tests service statistics
- **TestRouterErrorHandling**: Tests error handling and middleware
- **TestRouterIntegrationScenarios**: Tests complex scenarios like full note lifecycle

### Debug Mode

The application includes debugpy integration for development debugging:

- Use `./run-server.sh --debug` to enable debug mode
- Configure VS Code/Cursor debugger to attach to the specified port
- Debug configuration files are included in `.vscode/launch.json`

### Hot Reload

The application includes hot-reload when using uvicorn with the `--reload` flag, making development faster and more efficient.

## Module Structure

### Main Application Router

- **`main_router.py`**: Handles main application endpoints including the welcome page
- **Root Endpoint**: Serves the HTML welcome page with API information
- **Debug Status**: Displays current debug mode status
- **Endpoint List**: Shows all available API endpoints

### Notes Module (Main Functionality)

- **Models** (`notes/models/`): Pydantic models organized by type (notes, LLM, enums, exceptions)
- **Service** (`notes/notes_service.py`): Business logic service with singleton pattern for data persistence
- **Gemini Service** (`notes/gemini_service.py`): AI enrichment service using Gemini API with structured output
- **Dependencies** (`notes/dependencies.py`): Provides service instances for dependency injection
- **Router** (`notes/router.py`): Defines API endpoints using FastAPI's dependency injection

### Dependency Injection

The application uses FastAPI's `Depends` mechanism to inject services into endpoint functions:

```python
@router.get("/notes")
async def get_notes(
    user_id: str,
    notes_service: NotesService = Depends(get_notes_service)
):
    return notes_service.get_notes_by_user_id(user_id)
```

### Data Models

The notes system uses Pydantic models for data validation:

- `Note`: Complete note with metadata and timestamps
- `NoteCreate`: Input model for creating notes
- `NoteUpdate`: Input model for updating notes
- `NoteMetadata`: AI-generated enrichments (summary, topics, sentiment, etc.)

## Architecture Features

### Global Exception Handling

The application includes custom middleware for consistent error handling:

- **ExceptionHandlerMiddleware**: Catches all unhandled exceptions globally
- **Consistent Responses**: All errors return standardized HTTP 500 responses
- **Comprehensive Logging**: Detailed logging with request context for debugging
- **Clean Endpoints**: Router endpoints focus on business logic, not error handling

### Structured LLM Output

The LLM service uses Gemini's structured output capabilities with JSON schema validation:

- **JSON Schema Generation**: Automatically generates schemas from Pydantic models
- **Structured Prompts**: Clear, focused prompts that guide the model to structured responses
- **Direct Validation**: Responses are validated directly against the Pydantic model
- **No Retry Loops**: Higher success rate eliminates the need for complex retry logic
- **Better Performance**: Faster response times with fewer API calls

## Testing Philosophy

The application uses **integration testing** as the primary testing strategy:

- **System-Level Testing**: Tests the entire system through the router endpoints
- **Real Service Logic**: Tests actual service implementations, not mocked business logic
- **Dependency Injection**: Tests how services work together with proper dependency injection
- **Mock External APIs**: Only external dependencies (like Gemini API) are mocked
- **Comprehensive Coverage**: Tests cover all endpoints, error scenarios, and edge cases
- **Real Data Flow**: Tests the actual data flow from request to response

This approach ensures that:

- **Integration works**: All components work together correctly
- **Real bugs are caught**: Issues in service interactions are discovered
- **API contracts are tested**: Endpoint behavior matches expectations
- **Error handling works**: Middleware and error handling function correctly

## Next Steps

This is a production-ready notes API that you can build upon. Consider adding:

- **Database Integration**: Replace in-memory storage with PostgreSQL, MongoDB, or similar
- **Authentication & Authorization**: JWT tokens, OAuth, or session-based auth
- **File Attachments**: Support for images, documents, or other file types
- **Collaboration**: Shared notes, comments, or real-time editing
- **Advanced AI**: Integration with additional LLM APIs or specialized AI services
- **Search & Filtering**: Full-text search, tags, categories, or advanced filtering
- **Export/Import**: PDF export, markdown import, or API integrations
- **Monitoring & Logging**: Structured logging, metrics, and health checks
- **Docker & Deployment**: Containerization and deployment configurations

## Requirements

- Python 3.11+
- FastAPI 0.104.1+
- Uvicorn 0.24.0+
- Pydantic 2.0+
- debugpy 1.8.0+ (for development debugging)
- pytest 7.4.3+ (for testing)
- google-generativeai 0.3.2+ (for Gemini API integration)
- httpx 0.25.2+ (for FastAPI TestClient)
