import pytest
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from src.core.middlewares.auth_middleware import get_current_user

@pytest.fixture
def mock_verify_access_token():
    with patch("src.core.utils.jwt.verify_access_token") as mock:
        yield mock

@pytest.mark.asyncio
async def test_get_current_user_invalid(mock_verify_access_token):
    mock_verify_access_token.return_value = None
    
    credentials = HTTPAuthorizationCredentials(scheme='Bearer', credentials='invalid_token')
    
    with pytest.raises(HTTPException):
        await get_current_user(credentials)
