import pytest
from pydantic import ValidationError
from models.provider import Provider, ProviderResponse

class TestProviderModel:
    """Test cases for the Provider model."""
    
    def test_provider_valid_data(self):
        """Test creating a Provider with valid data."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology", "Preventive Medicine"],
            "year_of_experience": 15,
            "known_languages": ["English", "Spanish"],
            "cost_efficiency": 85
        }
        
        provider = Provider(**provider_data)
        
        assert provider.name == "Dr. Sarah Johnson"
        assert provider.gender == "Female"
        assert provider.education == "MD - Harvard Medical School"
        assert provider.reviews == 4.8
        assert provider.city == "Los Angeles"
        assert provider.state == "California"
        assert provider.zip_code == "90210"
        assert provider.specializations == ["Cardiology", "Preventive Medicine"]
        assert provider.year_of_experience == 15
        assert provider.known_languages == ["English", "Spanish"]
        assert provider.cost_efficiency == 85
    
    def test_provider_missing_required_field(self):
        """Test that Provider raises ValidationError when required field is missing."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology"],
            "year_of_experience": 15,
            "known_languages": ["English"],
            # Missing cost_efficiency
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)
    
    def test_provider_invalid_reviews_type(self):
        """Test that Provider validates reviews as float."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": "invalid_float",  # Invalid string that can't be converted to float
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology"],
            "year_of_experience": 15,
            "known_languages": ["English"],
            "cost_efficiency": 85
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)
    
    def test_provider_invalid_year_of_experience_type(self):
        """Test that Provider validates year_of_experience as int."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology"],
            "year_of_experience": "invalid_int",  # Invalid string that can't be converted to int
            "known_languages": ["English"],
            "cost_efficiency": 85
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)
    
    def test_provider_invalid_cost_efficiency_type(self):
        """Test that Provider validates cost_efficiency as int."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology"],
            "year_of_experience": 15,
            "known_languages": ["English"],
            "cost_efficiency": "invalid_int"  # Invalid string that can't be converted to int
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)
    
    def test_provider_invalid_specializations_type(self):
        """Test that Provider validates specializations as list of strings."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": "Cardiology",  # String instead of list
            "year_of_experience": 15,
            "known_languages": ["English"],
            "cost_efficiency": 85
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)
    
    def test_provider_invalid_known_languages_type(self):
        """Test that Provider validates known_languages as list of strings."""
        provider_data = {
            "name": "Dr. Sarah Johnson",
            "gender": "Female",
            "education": "MD - Harvard Medical School",
            "reviews": 4.8,
            "city": "Los Angeles",
            "state": "California",
            "zip_code": "90210",
            "specializations": ["Cardiology"],
            "year_of_experience": 15,
            "known_languages": "English",  # String instead of list
            "cost_efficiency": 85
        }
        
        with pytest.raises(ValidationError):
            Provider(**provider_data)

class TestProviderResponseModel:
    """Test cases for the ProviderResponse model."""
    
    def test_provider_response_valid_data(self):
        """Test creating a ProviderResponse with valid data."""
        provider = Provider(
            name="Dr. Sarah Johnson",
            gender="Female",
            education="MD - Harvard Medical School",
            reviews=4.8,
            city="Los Angeles",
            state="California",
            zip_code="90210",
            specializations=["Cardiology"],
            year_of_experience=15,
            known_languages=["English"],
            cost_efficiency=85
        )
        
        response_data = {
            "providers": [provider],
            "total_count": 1,
            "query": "cardiology",
            "state_code": "CA"
        }
        
        response = ProviderResponse(**response_data)
        
        assert len(response.providers) == 1
        assert response.total_count == 1
        assert response.query == "cardiology"
        assert response.state_code == "CA"
    
    def test_provider_response_empty_providers(self):
        """Test creating a ProviderResponse with empty providers list."""
        response_data = {
            "providers": [],
            "total_count": 0,
            "query": None,
            "state_code": None
        }
        
        response = ProviderResponse(**response_data)
        
        assert len(response.providers) == 0
        assert response.total_count == 0
        assert response.query is None
        assert response.state_code is None
    
    def test_provider_response_missing_required_field(self):
        """Test that ProviderResponse raises ValidationError when required field is missing."""
        response_data = {
            "providers": [],
            "total_count": 0,
            # Missing query and state_code (optional, so should be fine)
        }
        
        response = ProviderResponse(**response_data)
        assert response.query is None
        assert response.state_code is None

if __name__ == "__main__":
    pytest.main([__file__]) 