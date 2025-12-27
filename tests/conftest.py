"""Pytest configuration and fixtures."""

import os
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    with patch('app.dependencies.get_supabase_client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_supabase_admin():
    """Mock Supabase admin client."""
    with patch('app.dependencies.get_supabase_admin_client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("SUPABASE_URL", "https://test.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-anon-key")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "test-service-key")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("DEBUG", "false")

