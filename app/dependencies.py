"""Dependency injection for the application."""

from functools import lru_cache
from typing import Generator

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    """
    Create and return a cached Supabase client instance.
    
    Uses the anon/public key for auth operations.
    RLS policies will be enforced.
    """
    settings = get_settings()
    settings.validate()
    return create_client(settings.supabase_url, settings.supabase_key)


@lru_cache
def get_supabase_admin_client() -> Client:
    """
    Create and return a cached Supabase admin client instance.
    
    Uses the service_role key which bypasses RLS.
    Use this for server-side CRUD operations where we've already
    validated the user ourselves.
    """
    settings = get_settings()
    settings.validate()
    # Use service key if available, otherwise fall back to anon key
    key = settings.supabase_service_key or settings.supabase_key
    return create_client(settings.supabase_url, key)


def get_supabase() -> Generator[Client, None, None]:
    """
    Dependency that provides a Supabase client (anon key).
    
    Use for auth operations.
    """
    yield get_supabase_client()


def get_supabase_admin() -> Generator[Client, None, None]:
    """
    Dependency that provides a Supabase admin client (service role key).
    
    Use for CRUD operations where we've already validated the user.
    This bypasses RLS since we handle authorization in our code.
    """
    yield get_supabase_admin_client()
