"""Tests for task routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_tasks_page_redirects_when_not_authenticated(client):
    """Test tasks page redirects to login when not authenticated."""
    response = client.get("/tasks", follow_redirects=False)
    assert response.status_code == 303  # Redirect
    assert "/auth/login" in response.headers["location"]


def test_create_task_requires_auth(client):
    """Test creating a task requires authentication."""
    response = client.post("/tasks/create", data={"title": "Test task"})
    assert response.status_code == 401  # Unauthorized


def test_toggle_task_requires_auth(client):
    """Test toggling a task requires authentication."""
    response = client.post("/tasks/test-id/toggle")
    assert response.status_code == 401  # Unauthorized


def test_delete_task_requires_auth(client):
    """Test deleting a task requires authentication."""
    response = client.delete("/tasks/test-id")
    assert response.status_code == 401  # Unauthorized

