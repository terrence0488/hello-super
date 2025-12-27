"""Realtime routes for Server-Sent Events (SSE) updates."""

import asyncio
import json
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from supabase import Client

from app.dependencies import get_supabase, get_supabase_admin
from app.services.auth_service import AuthService
from app.services.realtime_service import RealtimeService

router = APIRouter(prefix="/realtime", tags=["realtime"])

# Cookie name (must match auth.py)
COOKIE_NAME = "session_token"


def get_realtime_service(supabase: Client = Depends(get_supabase_admin)) -> RealtimeService:
    """Dependency to get realtime service."""
    return RealtimeService(supabase)


def get_current_user(request: Request, supabase: Client = Depends(get_supabase)) -> Optional[dict]:
    """Get current user from session cookie."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    
    auth_service = AuthService(supabase)
    return auth_service.get_user_from_token(token)


async def event_generator(user_id: str, realtime_service: RealtimeService):
    """Generate SSE events for task updates."""
    try:
        async for update in realtime_service.watch_tasks(user_id, interval=3.0):
            # Format as SSE
            data = json.dumps(update)
            yield f"data: {data}\n\n"
    except asyncio.CancelledError:
        # Client disconnected
        pass


@router.get("/tasks/stream")
async def stream_tasks(
    request: Request,
    supabase: Client = Depends(get_supabase),
    realtime_service: RealtimeService = Depends(get_realtime_service),
):
    """
    Stream task updates via Server-Sent Events (SSE).
    
    This endpoint provides real-time task updates without WebSockets.
    Connect to this endpoint using EventSource in JavaScript:
    
    ```javascript
    const eventSource = new EventSource('/realtime/tasks/stream');
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Tasks updated:', data);
    };
    ```
    """
    user = get_current_user(request, supabase)
    if not user:
        return {"error": "Unauthorized"}
    
    return StreamingResponse(
        event_generator(user["id"], realtime_service),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.get("/tasks/stats")
async def get_task_stats(
    request: Request,
    supabase: Client = Depends(get_supabase),
    realtime_service: RealtimeService = Depends(get_realtime_service),
):
    """Get current task statistics."""
    user = get_current_user(request, supabase)
    if not user:
        return {"error": "Unauthorized"}
    
    stats = realtime_service.get_task_stats(user["id"])
    return stats

