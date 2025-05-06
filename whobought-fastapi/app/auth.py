import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# JWT Settings (loaded from environment variables)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "SecureJwtKeyWithAtLeast32CharactersForSecurityPurposes")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.environ.get("JWT_EXPIRATION_MINUTES", "60"))
JWT_ISSUER = os.environ.get("JWT_ISSUER", "WhoBoughtApp")
JWT_AUDIENCE = os.environ.get("JWT_AUDIENCE", "WhoBoughtUsers")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        JWT token as string
    """
    to_encode = data.copy()
    
    # Set expiration
    expire = datetime.utcnow()
    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=JWT_EXPIRATION_MINUTES)
    
    # Add standard claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE
    })
    
    # Encode the token
    try:
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=[JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": True, "verify_iss": True},
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependency for getting the current authenticated user
    
    Args:
        token: JWT token from authorization header
        
    Returns:
        User data from token
        
    Raises:
        HTTPException: If token is invalid
    """
    payload = decode_token(token)
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "id": user_id,
        "username": payload.get("username", ""),
        "email": payload.get("email", "")
    }

def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """
    Dependency for optionally getting the current user
    
    Args:
        token: JWT token from authorization header
        
    Returns:
        User data from token, or None if not authenticated
    """
    try:
        return get_current_user(token)
    except HTTPException:
        return None 