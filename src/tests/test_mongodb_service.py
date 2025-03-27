import pytest
from unittest.mock import AsyncMock
from pymongo.errors import PyMongoError
from fastapi import HTTPException
from bson import ObjectId
from src.core.services.mongodb_service import MongoDBService

@pytest.fixture
def mock_collection():
    return AsyncMock()

@pytest.fixture
def mongodb_service(mock_collection):
    return MongoDBService(mock_collection)

# Test for the `create` method
@pytest.mark.asyncio
async def test_create_success(mongodb_service, mock_collection):
    document = {"name": "Test"}
    mock_collection.insert_one.return_value.inserted_id = ObjectId("60f72b2f9b1d8c9eae345f30")
    
    result = await mongodb_service.create(document)
    
    assert result == "60f72b2f9b1d8c9eae345f30"
    mock_collection.insert_one.assert_called_once_with(document)

@pytest.mark.asyncio
async def test_create_mongodb_error(mongodb_service, mock_collection):
    document = {"name": "Test"}
    mock_collection.insert_one.side_effect = PyMongoError("MongoDB error")

    with pytest.raises(HTTPException):
        await mongodb_service.create(document)

# Test for the `get_by_id` method
@pytest.mark.asyncio
async def test_get_by_id_success(mongodb_service, mock_collection):
    mock_collection.find_one.return_value = {"_id": ObjectId("60f72b2f9b1d8c9eae345f30"), "name": "Test"}
    
    result = await mongodb_service.get_by_id("60f72b2f9b1d8c9eae345f30")
    
    assert result["_id"] == "60f72b2f9b1d8c9eae345f30"
    mock_collection.find_one.assert_called_once_with({"_id": ObjectId("60f72b2f9b1d8c9eae345f30")})

@pytest.mark.asyncio
async def test_get_by_id_invalid_id_format(mongodb_service):
    with pytest.raises(HTTPException):
        await mongodb_service.get_by_id("invalid_id")

@pytest.mark.asyncio
async def test_get_by_id_mongodb_error(mongodb_service, mock_collection):
    mock_collection.find_one.side_effect = PyMongoError("MongoDB error")
    
    with pytest.raises(HTTPException):
        await mongodb_service.get_by_id("60f72b2f9b1d8c9eae345f30")

# Test for the `update` method
@pytest.mark.asyncio
async def test_update_success(mongodb_service, mock_collection):
    mock_collection.update_one.return_value.modified_count = 1
    
    result = await mongodb_service.update("60f72b2f9b1d8c9eae345f30", {"name": "Updated"})
    
    assert result is True
    mock_collection.update_one.assert_called_once_with({"_id": ObjectId("60f72b2f9b1d8c9eae345f30")}, {"$set": {"name": "Updated"}})

@pytest.mark.asyncio
async def test_update_mongodb_error(mongodb_service, mock_collection):
    mock_collection.update_one.side_effect = PyMongoError("MongoDB error")
    
    with pytest.raises(HTTPException):
        await mongodb_service.update("60f72b2f9b1d8c9eae345f30", {"name": "Updated"})
