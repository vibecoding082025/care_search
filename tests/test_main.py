import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_check_returns_200(self):
        """Test that health check endpoint returns 200 status."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "message" in data
        assert data["message"] == "Provider Search API is running"
    
    def test_health_check_publicly_accessible(self):
        """Test that health check endpoint is publicly accessible (no authentication required)."""
        response = client.get("/health")
        assert response.status_code == 200

class TestProvidersEndpoint:
    """Test cases for the providers endpoint."""
    
    def test_fetch_providers_no_parameters(self):
        """Test fetching providers without any query parameters."""
        response = client.get("/providers")
        assert response.status_code == 200
        
        data = response.json()
        assert "providers" in data
        assert "total_count" in data
        assert "query" in data
        assert "state_code" in data
        assert data["total_count"] == 0  # Empty list as per current implementation
        assert isinstance(data["providers"], list)
    
    def test_fetch_providers_with_query(self):
        """Test fetching providers with query parameter."""
        response = client.get("/providers?query=cardiology")
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == "cardiology"
        assert data["state_code"] is None
        assert "providers" in data
        assert "total_count" in data
    
    def test_fetch_providers_with_stateCode(self):
        """Test fetching providers with stateCode parameter."""
        response = client.get("/providers?stateCode=CA")
        assert response.status_code == 200
        
        data = response.json()
        assert data["state_code"] == "CA"
        assert data["query"] is None
        assert "providers" in data
        assert "total_count" in data
    
    def test_fetch_providers_with_both_query_and_stateCode(self):
        """Test fetching providers with both query and stateCode parameters."""
        response = client.get("/providers?query=cardiology&stateCode=CA")
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == "cardiology"
        assert data["state_code"] == "CA"
        assert "providers" in data
        assert "total_count" in data
    
    def test_fetch_providers_with_empty_query(self):
        """Test fetching providers with empty query parameter."""
        response = client.get("/providers?query=")
        assert response.status_code == 200
        
        data = response.json()
        assert data["query"] == ""
        assert "providers" in data
    
    def test_fetch_providers_with_empty_stateCode(self):
        """Test fetching providers with empty stateCode parameter."""
        response = client.get("/providers?stateCode=")
        assert response.status_code == 200
        
        data = response.json()
        assert data["state_code"] == ""
        assert "providers" in data

class TestProviderResponseModel:
    """Test cases for the ProviderResponse model."""
    
    def test_provider_response_structure(self):
        """Test that the provider response has the correct structure."""
        response = client.get("/providers")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = ["providers", "total_count", "query", "state_code"]
        for field in required_fields:
            assert field in data
        
        # Test that providers is a list
        assert isinstance(data["providers"], list)
        
        # Test that total_count is an integer
        assert isinstance(data["total_count"], int)

class TestAPIErrorHandling:
    """Test cases for API error handling."""
    
    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method(self):
        """Test that invalid HTTP methods return 405."""
        response = client.post("/providers")
        assert response.status_code == 405
    
    def test_invalid_method_health(self):
        """Test that invalid HTTP methods on health endpoint return 405."""
        response = client.post("/health")
        assert response.status_code == 405

class TestAsyncFunctionality:
    """Test cases to ensure async functionality is working."""
    
    def test_health_check_async(self):
        """Test that health check endpoint works asynchronously."""
        response = client.get("/health")
        assert response.status_code == 200
        
        # The response should include timestamp from async function
        data = response.json()
        assert "timestamp" in data
    
    def test_providers_async(self):
        """Test that providers endpoint works asynchronously."""
        response = client.get("/providers?query=test")
        assert response.status_code == 200
        
        # The response should come from async service call
        data = response.json()
        assert "providers" in data
        assert "total_count" in data

class TestOpenAPIDocumentation:
    """Test cases for OpenAPI documentation."""
    
    def test_docs_endpoint_accessible(self):
        """Test that the /docs endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint_accessible(self):
        """Test that the /redoc endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_json_accessible(self):
        """Test that the OpenAPI JSON schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

if __name__ == "__main__":
    pytest.main([__file__]) 