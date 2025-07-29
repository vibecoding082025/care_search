# Provider Search API

A Python-based REST API for searching healthcare providers, built with FastAPI following async patterns.

## Features

- 🔍 **Provider Search**: Search healthcare providers by query and state code
- 🏥 **Health Check**: Public health check endpoint returning 200 status
- 📚 **Auto-generated Documentation**: Interactive API docs with Swagger UI
- 🧪 **Comprehensive Testing**: Full test coverage with pytest
- ⚡ **Async Architecture**: Built with async/await patterns for high performance

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **uvicorn**: ASGI server
- **pytest**: Testing framework

## Project Structure

```
care_search/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── models/
│   ├── __init__.py
│   └── provider.py        # Pydantic models for providers
├── services/
│   ├── __init__.py
│   └── provider_service.py # Provider search service
└── tests/
    ├── __init__.py
    ├── test_main.py       # API endpoint tests
    ├── test_provider_service.py # Service tests
    └── test_models.py     # Model validation tests
```

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

1. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Returns 200 status, publicly accessible
  - Returns: `{"status": "healthy", "timestamp": "...", "message": "..."}`

### Provider Search
- **GET** `/providers` - Search healthcare providers
  - Query Parameters:
    - `query` (optional): Search query for provider name, specialty, or description
    - `stateCode` (optional): State code filter (e.g., 'CA', 'NY', 'TX')
  - Returns: `ProviderResponse` with list of providers

### API Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation (ReDoc)
- **GET** `/openapi.json` - OpenAPI schema

## Provider Model

The Provider model includes all mandatory fields as specified:

```python
class Provider(BaseModel):
    name: str                    # Provider name
    gender: str                  # Provider gender
    education: str               # Provider education
    reviews: float               # Provider reviews rating
    city: str                    # City name
    state: str                   # State name
    zip_code: str                # Zip code
    specializations: List[str]   # List of specializations
    year_of_experience: int      # Years of experience
    known_languages: List[str]   # List of known languages
    cost_efficiency: int         # Cost efficiency rating
```

## Usage Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Search Providers
```bash
# Search all providers
curl http://localhost:8000/providers

# Search by query
curl "http://localhost:8000/providers?query=cardiology"

# Search by state code
curl "http://localhost:8000/providers?stateCode=CA"

# Search with both parameters
curl "http://localhost:8000/providers?query=cardiology&stateCode=CA"
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run tests with coverage
pytest --cov=.
```

### Test Coverage

The project includes comprehensive tests for:

- **API Endpoints**: Health check and provider search endpoints
- **Service Layer**: Provider service functionality
- **Models**: Data validation and model behavior
- **Error Handling**: Invalid requests and edge cases
- **Async Functionality**: Async/await patterns
- **OpenAPI Documentation**: Documentation accessibility

## Development

### Running in Development Mode

```bash
python main.py
```

The server will start with auto-reload enabled.

### Code Structure

- **Async Patterns**: All endpoints and service methods use async/await
- **Service Layer**: Business logic separated into `ProviderService`
- **Model Validation**: Pydantic models ensure data integrity
- **Error Handling**: Proper HTTP status codes and error messages

### Adding New Features

1. **New Endpoints**: Add to `main.py`
2. **New Services**: Create in `services/` directory
3. **New Models**: Create in `models/` directory
4. **Tests**: Add corresponding tests in `tests/` directory

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The documentation is automatically generated from the FastAPI code and includes:

- All available endpoints
- Request/response schemas
- Query parameter descriptions
- Example requests and responses

## Notes

- The search logic in `ProviderService.search_providers()` is intentionally left empty as per requirements
- All endpoints follow async patterns
- Health check endpoint is publicly accessible and returns 200 status
- Provider search accepts `query` and `stateCode` as query parameters
- Comprehensive test coverage ensures code quality

## License

This project is licensed under the MIT License. 