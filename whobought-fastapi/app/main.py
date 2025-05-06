from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from datetime import datetime

from .routers import items_router, users_router
from .routers.auth import router as auth_router
from .database import get_cosmos_manager
from .responses import success_response, error_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Log environment variable presence (not values for security)
env_vars = [
    "COSMOS_CONNECTION_STRING", 
    "COSMOS_DATABASE_NAME", 
    "COSMOS_CONTAINER_NAME", 
    "COSMOS_USER_CONTAINER_NAME",
    "JWT_SECRET_KEY",
    "JWT_ALGORITHM",
    "JWT_EXPIRATION_MINUTES",
    "JWT_ISSUER",
    "JWT_AUDIENCE"
]

logger.info("Checking environment variables...")
for var in env_vars:
    if var in os.environ:
        logger.info(f"✓ {var} is set")
    else:
        logger.warning(f"✗ {var} is not set")

# Create FastAPI app
app = FastAPI(
    title="WhoBought API",
    description="API for tracking shared expenses",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
async def root(request: Request):
    return success_response(
        data={"name": "WhoBought API", "version": app.version},
        message="Welcome to WhoBought API"
    )

@app.get("/health")
async def health_check(request: Request):
    """Health check endpoint"""
    # Try to access the database
    try:
        cosmos_manager = get_cosmos_manager()
        db_status = "disconnected"
        
        if cosmos_manager.connection_string:
            if cosmos_manager.client:
                status = "healthy"
                message = "Service is healthy"
                db_status = "connected"
            else:
                status = "degraded"
                message = "Database connection is unavailable"
        else:
            status = "degraded"
            message = "Database connection string is not configured"
            
        return success_response(
            data={
                "status": status,
                "version": app.version,
                "db_status": db_status,
                "environment": {
                    "COSMOS_DATABASE_NAME": cosmos_manager.database_name,
                    "COSMOS_CONTAINER_NAME": cosmos_manager.items_container_name,
                    "COSMOS_USER_CONTAINER_NAME": cosmos_manager.users_container_name,
                    "CONNECTION_STRING_SET": cosmos_manager.connection_string is not None
                }
            },
            message=message
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return error_response(
            message="Service health check failed",
            errors=[str(e)]
        )
