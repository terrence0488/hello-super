"""Realtime service for Supabase live updates.

Note: Supabase Realtime in Python requires the realtime-py library
which is included in the supabase-py package. However, for server-side
rendering with HTMX, we'll use a polling-based approach with
Server-Sent Events (SSE) as a simpler alternative.

For a production app, you might want to use:
1. WebSockets with the Supabase realtime client
2. Or pass realtime to the frontend via JavaScript
"""

import asyncio
from datetime import datetime
from typing import AsyncGenerator, Optional

from supabase import Client


class RealtimeService:
    """Service for handling realtime updates."""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "tasks"

    async def watch_tasks(
        self, 
        user_id: str, 
        interval: float = 2.0
    ) -> AsyncGenerator[dict, None]:
        """
        Watch for task changes using polling.
        
        Yields task list updates at the specified interval.
        This is a simple polling approach that works with SSE.
        
        Args:
            user_id: The user ID to watch tasks for
            interval: Polling interval in seconds
            
        Yields:
            Dict with tasks list and timestamp
        """
        last_check = None
        
        while True:
            try:
                # Fetch current tasks
                response = self.supabase.table(self.table)\
                    .select("*")\
                    .eq("user_id", user_id)\
                    .order("created_at", desc=True)\
                    .execute()
                
                tasks = response.data or []
                current_time = datetime.utcnow().isoformat()
                
                yield {
                    "tasks": tasks,
                    "timestamp": current_time,
                    "count": len(tasks),
                }
                
                last_check = current_time
                
            except Exception as e:
                yield {
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            
            await asyncio.sleep(interval)

    def get_task_stats(self, user_id: str) -> dict:
        """
        Get task statistics for a user.
        
        Returns:
            Dict with task counts
        """
        try:
            response = self.supabase.table(self.table)\
                .select("id, is_completed")\
                .eq("user_id", user_id)\
                .execute()
            
            tasks = response.data or []
            total = len(tasks)
            completed = sum(1 for t in tasks if t.get("is_completed"))
            pending = total - completed
            
            return {
                "total": total,
                "completed": completed,
                "pending": pending,
            }
        except Exception:
            return {"total": 0, "completed": 0, "pending": 0}

