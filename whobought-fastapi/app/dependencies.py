from fastapi import Depends, HTTPException, status
import os
import logging
from .database import get_cosmos_manager, CosmosDBManager

logger = logging.getLogger(__name__)

def get_db():
    """Dependency to get the database connection"""
    cosmos_manager = get_cosmos_manager()
    
    # Check if connection string is set
    if not cosmos_manager.connection_string:
        logger.error("COSMOS_CONNECTION_STRING environment variable is not set")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection string is not configured"
        )
    
    # Initialize connection if needed
    if not cosmos_manager.client:
        try:
            cosmos_manager._initialize_connection()
        except Exception as e:
            logger.error(f"Failed to connect to Cosmos DB: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database connection error: {str(e)}"
            )
    
    return cosmos_manager
