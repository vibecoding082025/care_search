from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Provider(BaseModel):
    """Provider model representing a healthcare provider with all mandatory fields."""
    name: str = Field(..., description="Provider name")
    gender: str = Field(..., description="Provider gender")
    education: str = Field(..., description="Provider education")
    reviews: float = Field(..., description="Provider reviews rating")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State name")
    zip_code: str = Field(..., description="Zip code")
    specializations: List[str] = Field(..., description="List of specializations")
    year_of_experience: int = Field(..., description="Years of experience")
    known_languages: List[str] = Field(..., description="List of known languages")
    cost_efficiency: int = Field(..., description="Cost efficiency rating")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
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
        }
    }

class ProviderResponse(BaseModel):
    """Response model for provider search results."""
    providers: List[Provider] = Field(..., description="List of providers")
    total_count: int = Field(..., description="Total number of providers found")
    query: Optional[str] = Field(None, description="Search query used")
    state_code: Optional[str] = Field(None, description="State code filter used")
    
    model_config = {"from_attributes": True} 

class ErrorResponse(BaseModel):
    """Response model for error cases."""
    error: str = Field(..., description="Error message")
    message: str = Field(..., description="Additional information about the error")
    status_code: int = Field(..., description="Status code")    
    model_config = {"from_attributes": True}