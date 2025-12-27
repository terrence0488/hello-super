"""Tests for main application routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_root_route(client):
    """Test landing page route."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello Super" in response.text


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}


def test_docs_available(client):
    """Test that API docs are available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client):
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data

