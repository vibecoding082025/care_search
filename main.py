from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import uvicorn
import logging
from dotenv import load_dotenv

# Import services and models
from services.provider_service import ProviderService
from models.provider import ErrorResponse, ProviderResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Care Search API",
    description="A Python API for searching healthcare providers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize provider service
provider_service = ProviderService()

@app.get("/health")
async def health_check():
    """Health check endpoint - returns 200 status."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Provider Search API is running"
    }

@app.get("/providers", response_model=ProviderResponse)
async def fetch_providers(
    query: Optional[str] = Query(None, description="Search query for provider name, specialty, or description"),
    stateCode: Optional[str] = Query(None, description="State code filter (e.g., 'CA', 'NY', 'TX')")
):
    """
    Fetch healthcare providers with optional filtering by query and stateCode.
    
    This endpoint searches providers using the provider service.
    """
    try:
        providers = await provider_service.search_providers(
            query=query,
            state_code=stateCode
        )
        
        return ProviderResponse(
            providers=providers,
            total_count=len(providers),
            query=query,
            state_code=stateCode
        )
    except Exception as e:
        logging.error(f"Error searching providers: {str(e)}")
        return ErrorResponse(
            error="We encountered an unexpected error while searching for providers.",
            message="Please try again later or contact support if the issue persists.",
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 