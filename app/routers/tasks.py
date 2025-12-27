"""Task CRUD routes with HTMX support."""

from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase import Client

from app.dependencies import get_supabase, get_supabase_admin
from app.services.auth_service import AuthService
from app.services.task_service import TaskService
from app.services.storage_service import StorageService

router = APIRouter(prefix="/tasks", tags=["tasks"])
templates = Jinja2Templates(directory="app/templates")

# Cookie name (must match auth.py)
COOKIE_NAME = "session_token"


def get_task_service(supabase: Client = Depends(get_supabase_admin)) -> TaskService:
    """Dependency to get task service (uses admin client to bypass RLS)."""
    return TaskService(supabase)


def get_storage_service(supabase: Client = Depends(get_supabase_admin)) -> StorageService:
    """Dependency to get storage service (uses admin client)."""
    return StorageService(supabase)


def get_current_user(request: Request, supabase: Client = Depends(get_supabase)) -> Optional[dict]:
    """Get current user from session cookie."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    
    auth_service = AuthService(supabase)
    return auth_service.get_user_from_token(token)


def require_auth(request: Request, supabase: Client = Depends(get_supabase)) -> dict:
    """Require authentication, redirect to login if not authenticated."""
    user = get_current_user(request, supabase)
    if not user:
        raise RedirectToLogin()
    return user


class RedirectToLogin(Exception):
    """Exception to trigger redirect to login page."""
    pass


# =============================================================================
# Page Routes (HTML)
# =============================================================================

@router.get("", response_class=HTMLResponse)
async def tasks_list(
    request: Request,
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
):
    """Render tasks list page."""
    user = get_current_user(request, supabase)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    success, message, tasks = task_service.get_all_tasks(user["id"])
    
    return templates.TemplateResponse(
        request=request,
        name="tasks/list.html",
        context={
            "user": user,
            "tasks": tasks,
            "error": None if success else message,
        },
    )


# =============================================================================
# HTMX Partial Routes
# =============================================================================

@router.post("/create", response_class=HTMLResponse)
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    attachment: UploadFile = File(default=None),
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
    storage_service: StorageService = Depends(get_storage_service),
):
    """Create a new task with optional file attachment (HTMX)."""
    user = get_current_user(request, supabase)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    # Handle file upload if present
    attachment_path = None
    try:
        if attachment and attachment.filename and attachment.size and attachment.size > 0:
            content = await attachment.read()
            if content:  # Only upload if file has content
                upload_success, upload_message, file_path = storage_service.upload_file(
                    user_id=user["id"],
                    file_content=content,
                    file_name=attachment.filename,
                    content_type=attachment.content_type or "application/octet-stream",
                )
                if upload_success:
                    attachment_path = file_path
                # Don't fail task creation if file upload fails
    except Exception:
        # Ignore file upload errors, still create the task
        pass
    
    success, message, task = task_service.create_task(
        user_id=user["id"],
        title=title,
        description=description if description else None,
        attachment_path=attachment_path,
    )
    
    if success and task:
        # Return the new task item partial
        return templates.TemplateResponse(
            request=request,
            name="tasks/partials/task_item.html",
            context={"task": task},
        )
    else:
        return HTMLResponse(content=f"<div class='text-red-400 p-4 rounded-xl bg-red-500/10 border border-red-500/20'>{message}</div>", status_code=400)


@router.post("/{task_id}/toggle", response_class=HTMLResponse)
async def toggle_task(
    request: Request,
    task_id: str,
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
):
    """Toggle task completion (HTMX)."""
    user = get_current_user(request, supabase)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    success, message, task = task_service.toggle_task(task_id, user["id"])
    
    if success and task:
        return templates.TemplateResponse(
            request=request,
            name="tasks/partials/task_item.html",
            context={"task": task},
        )
    else:
        return HTMLResponse(content=f"<div class='text-red-400'>{message}</div>", status_code=400)


@router.put("/{task_id}", response_class=HTMLResponse)
async def update_task(
    request: Request,
    task_id: str,
    title: str = Form(...),
    description: str = Form(""),
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
):
    """Update a task (HTMX)."""
    user = get_current_user(request, supabase)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    success, message, task = task_service.update_task(
        task_id=task_id,
        user_id=user["id"],
        title=title,
        description=description if description else None,
    )
    
    if success and task:
        return templates.TemplateResponse(
            request=request,
            name="tasks/partials/task_item.html",
            context={"task": task},
        )
    else:
        return HTMLResponse(content=f"<div class='text-red-400'>{message}</div>", status_code=400)


@router.delete("/{task_id}", response_class=HTMLResponse)
async def delete_task(
    request: Request,
    task_id: str,
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
):
    """Delete a task (HTMX)."""
    user = get_current_user(request, supabase)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    success, message = task_service.delete_task(task_id, user["id"])
    
    if success:
        # Return empty content to remove the task from DOM
        return HTMLResponse(content="")
    else:
        return HTMLResponse(content=f"<div class='text-red-400'>{message}</div>", status_code=400)


@router.get("/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_form(
    request: Request,
    task_id: str,
    supabase: Client = Depends(get_supabase),
    task_service: TaskService = Depends(get_task_service),
):
    """Get edit form for a task (HTMX)."""
    user = get_current_user(request, supabase)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    
    success, message, task = task_service.get_task(task_id, user["id"])
    
    if success and task:
        return templates.TemplateResponse(
            request=request,
            name="tasks/partials/task_edit.html",
            context={"task": task},
        )
    else:
        return HTMLResponse(content=f"<div class='text-red-400'>{message}</div>", status_code=404)

