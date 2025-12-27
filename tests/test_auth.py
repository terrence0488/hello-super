"""Tests for authentication routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_login_page(client):
    """Test login page loads."""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Sign in" in response.text or "Welcome back" in response.text


def test_register_page(client):
    """Test registration page loads."""
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "Create an account" in response.text or "Sign up" in response.text


def test_logout_redirects(client):
    """Test logout redirects to home."""
    response = client.get("/auth/logout", follow_redirects=False)
    assert response.status_code == 303  # Redirect
    assert response.headers["location"] == "/"


def test_me_endpoint_unauthorized(client):
    """Test /auth/me returns unauthorized when not logged in."""
    response = client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False
    assert data["user"] is None

