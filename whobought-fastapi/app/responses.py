from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .models import ApiResponse, ResponseModel


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a standardized success response.
    
    Args:
        data: The response data
        message: A success message
        status_code: HTTP status code
        
    Returns:
        JSONResponse with standardized format
    """
    response = ApiResponse(
        data=data,
        message=message,
        success=True,
        status_code=status_code
    )
    
    return JSONResponse(
        content=response.dict(),
        status_code=status_code
    )


def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        message: An error message
        status_code: HTTP status code
        errors: List of specific error messages
        
    Returns:
        JSONResponse with standardized format
    """
    response = ApiResponse(
        data=None,
        message=message,
        success=False,
        status_code=status_code,
        errors=errors
    )
    
    return JSONResponse(
        content=response.dict(),
        status_code=status_code
    )


def not_found_response(
    message: str = "Resource not found"
) -> JSONResponse:
    """
    Create a standardized 404 not found response.
    
    Args:
        message: Not found message
        
    Returns:
        JSONResponse with standardized format
    """
    return error_response(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND
    )


def bad_request_response(
    message: str = "Bad request",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized 400 bad request response.
    
    Args:
        message: Bad request message
        errors: List of validation errors
        
    Returns:
        JSONResponse with standardized format
    """
    return error_response(
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        errors=errors
    )


def created_response(
    data: Any = None,
    message: str = "Resource created successfully"
) -> JSONResponse:
    """
    Create a standardized 201 created response.
    
    Args:
        data: The created resource data
        message: Success message
        
    Returns:
        JSONResponse with standardized format
    """
    return success_response(
        data=data,
        message=message,
        status_code=status.HTTP_201_CREATED
    ) 