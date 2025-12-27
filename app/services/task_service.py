"""Task service for CRUD operations using Supabase."""

from typing import List, Optional, Tuple

from supabase import Client


class TaskService:
    """Service for handling task operations with Supabase."""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "tasks"

    def get_all_tasks(self, user_id: str) -> Tuple[bool, str, List[dict]]:
        """
        Get all tasks for a user.
        
        Returns:
            Tuple of (success, message, tasks_list)
        """
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .execute()
            
            return True, "Tasks retrieved successfully", response.data or []
        except Exception as e:
            return False, f"Error retrieving tasks: {str(e)}", []

    def get_task(self, task_id: str, user_id: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Get a single task by ID.
        
        Returns:
            Tuple of (success, message, task)
        """
        try:
            response = self.supabase.table(self.table)\
                .select("*")\
                .eq("id", task_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            return True, "Task retrieved successfully", response.data
        except Exception as e:
            return False, f"Error retrieving task: {str(e)}", None

    def create_task(
        self, 
        user_id: str, 
        title: str, 
        description: Optional[str] = None,
        attachment_path: Optional[str] = None
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Create a new task.
        
        Returns:
            Tuple of (success, message, created_task)
        """
        try:
            task_data = {
                "user_id": user_id,
                "title": title,
                "description": description,
                "is_completed": False,
                "attachment_path": attachment_path,
            }
            
            response = self.supabase.table(self.table)\
                .insert(task_data)\
                .execute()
            
            if response.data:
                return True, "Task created successfully", response.data[0]
            return False, "Failed to create task - no data returned", None
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error messages
            if "relation" in error_msg and "does not exist" in error_msg:
                return False, "Database table 'tasks' not found. Please run the SQL setup script in Supabase.", None
            if "permission denied" in error_msg.lower() or "rls" in error_msg.lower():
                return False, "Permission denied. Check RLS policies and SUPABASE_SERVICE_KEY in .env.", None
            return False, f"Error creating task: {error_msg}", None

    def update_task(
        self,
        task_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_completed: Optional[bool] = None,
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Update an existing task.
        
        Returns:
            Tuple of (success, message, updated_task)
        """
        try:
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if is_completed is not None:
                update_data["is_completed"] = is_completed
            
            if not update_data:
                return False, "No fields to update", None
            
            response = self.supabase.table(self.table)\
                .update(update_data)\
                .eq("id", task_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if response.data:
                return True, "Task updated successfully", response.data[0]
            return False, "Task not found", None
        except Exception as e:
            return False, f"Error updating task: {str(e)}", None

    def toggle_task(self, task_id: str, user_id: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Toggle task completion status.
        
        Returns:
            Tuple of (success, message, updated_task)
        """
        try:
            # First get the current task
            success, message, task = self.get_task(task_id, user_id)
            if not success or not task:
                return False, "Task not found", None
            
            # Toggle the status
            new_status = not task.get("is_completed", False)
            
            response = self.supabase.table(self.table)\
                .update({"is_completed": new_status})\
                .eq("id", task_id)\
                .eq("user_id", user_id)\
                .execute()
            
            if response.data:
                return True, "Task toggled successfully", response.data[0]
            return False, "Failed to toggle task", None
        except Exception as e:
            return False, f"Error toggling task: {str(e)}", None

    def delete_task(self, task_id: str, user_id: str) -> Tuple[bool, str]:
        """
        Delete a task.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            response = self.supabase.table(self.table)\
                .delete()\
                .eq("id", task_id)\
                .eq("user_id", user_id)\
                .execute()
            
            return True, "Task deleted successfully"
        except Exception as e:
            return False, f"Error deleting task: {str(e)}"

