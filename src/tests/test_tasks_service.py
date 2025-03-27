# tests/test_task_service.py
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.core.services.mongodb_service import MongoDBService
from src.services.task_service import TaskService
from src.core.db.mongodb.models.task import Task
from bson import ObjectId


@pytest.fixture
def task_db_service_mock():
    """Fixture for mocking MongoDBService."""
    return MagicMock(spec=MongoDBService)


@pytest.fixture
def task_service(task_db_service_mock):
    """Fixture for the TaskService."""
    return TaskService(task_db_service=task_db_service_mock)


@pytest.fixture
def task():
    """Fixture for creating a Task instance."""
    return Task(title="Test Task", description="Test description", status="completada")


@pytest.mark.asyncio
async def test_create_task(task_service, task, task_db_service_mock):
    # Mock the create method of MongoDBService
    task_dict = task.dict()
    task_dict["_id"] = str(ObjectId())
    task_db_service_mock.create.return_value = task_dict["_id"]

    # Call the service method
    result = await task_service.create_task(task)

    # Assertions
    assert result["_id"] == str(task_dict["_id"])
    task_db_service_mock.create.assert_called_once_with(task_dict)


@pytest.mark.asyncio
async def test_get_tasks(task_service, task_db_service_mock):
    # Mock the get method of MongoDBService
    mock_task_data = [{"_id": str(ObjectId()), "name": "Task 1"}, {"_id": str(ObjectId()), "name": "Task 2"}]
    task_db_service_mock.get.return_value = mock_task_data

    # Call the service method
    tasks = await task_service.get_tasks()

    # Assertions
    assert len(tasks) == 2
    assert tasks[0]["name"] == "Task 1"
    task_db_service_mock.get.assert_called_once_with(None, 100)


@pytest.mark.asyncio
async def test_get_task_by_id(task_service, task_db_service_mock):
    # Mock the get_by_id method of MongoDBService
    task_id = str(ObjectId())
    mock_task = {"_id": task_id, "name": "Test Task"}
    task_db_service_mock.get_by_id.return_value = mock_task

    # Call the service method
    result = await task_service.get_task_by_id(task_id)

    # Assertions
    assert result["_id"] == task_id
    assert result["name"] == "Test Task"
    task_db_service_mock.get_by_id.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(task_service, task_db_service_mock):
    # Mock the get_by_id method of MongoDBService to return None (task not found)
    task_id = str(ObjectId())
    task_db_service_mock.get_by_id.return_value = None

    # Call the service method and check for HTTPException
    with pytest.raises(HTTPException):
        await task_service.get_task_by_id(task_id)


@pytest.mark.asyncio
async def test_update_task(task_service, task_db_service_mock, task):
    # Mock the update method of MongoDBService
    task_dict = task.dict()
    task_id = str(ObjectId())
    task_db_service_mock.update.return_value = True

    # Call the service method
    result = await task_service.update_task(task_id, task)

    # Assertions
    assert result["message"] == "Task updated successfully"
    task_db_service_mock.update.assert_called_once_with(task_id, task_dict)


@pytest.mark.asyncio
async def test_update_task_error(task_service, task_db_service_mock, task):
    # Simulate an error during the update operation
    task_dict = task.dict()
    task_id = str(ObjectId())
    task_db_service_mock.update.side_effect = Exception("Update failed")

    # Call the service method and check for HTTPException
    with pytest.raises(HTTPException):
        await task_service.update_task(task_id, task)
