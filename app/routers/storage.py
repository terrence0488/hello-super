"""File storage routes for upload/download."""

from typing import Optional

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import Client

from app.dependencies import get_supabase, get_supabase_admin
from app.services.auth_service import AuthService
from app.services.storage_service import StorageService

router = APIRouter(prefix="/storage", tags=["storage"])

# Cookie name (must match auth.py)
COOKIE_NAME = "session_token"

# Max file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Allowed file types
ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
]


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


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    supabase: Client = Depends(get_supabase),
    storage_service: StorageService = Depends(get_storage_service),
):
    """Upload a file to storage."""
    user = get_current_user(request, supabase)
    if not user:
        return {"success": False, "message": "Unauthorized"}
    
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        return {
            "success": False, 
            "message": f"File type not allowed. Allowed: {', '.join(ALLOWED_TYPES)}"
        }
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        return {
            "success": False,
            "message": f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        }
    
    # Upload file
    success, message, file_path = storage_service.upload_file(
        user_id=user["id"],
        file_content=content,
        file_name=file.filename or "unnamed",
        content_type=file.content_type or "application/octet-stream",
    )
    
    if success:
        return {
            "success": True,
            "message": message,
            "file_path": file_path,
        }
    else:
        return {"success": False, "message": message}


@router.get("/download/{file_path:path}")
async def download_file(
    request: Request,
    file_path: str,
    supabase: Client = Depends(get_supabase),
    storage_service: StorageService = Depends(get_storage_service),
):
    """Get a signed download URL for a file."""
    user = get_current_user(request, supabase)
    if not user:
        return {"success": False, "message": "Unauthorized"}
    
    # Security: Ensure user can only access their own files
    if not file_path.startswith(user["id"]):
        return {"success": False, "message": "Access denied"}
    
    success, message, url = storage_service.get_file_url(file_path)
    
    if success and url:
        # Redirect to signed URL
        return RedirectResponse(url=url)
    else:
        return {"success": False, "message": message}


@router.get("/url/{file_path:path}")
async def get_file_url(
    request: Request,
    file_path: str,
    supabase: Client = Depends(get_supabase),
    storage_service: StorageService = Depends(get_storage_service),
):
    """Get a signed URL for a file (JSON response)."""
    user = get_current_user(request, supabase)
    if not user:
        return {"success": False, "message": "Unauthorized"}
    
    # Security: Ensure user can only access their own files
    if not file_path.startswith(user["id"]):
        return {"success": False, "message": "Access denied"}
    
    success, message, url = storage_service.get_file_url(file_path)
    
    if success:
        return {"success": True, "url": url}
    else:
        return {"success": False, "message": message}


@router.delete("/{file_path:path}")
async def delete_file(
    request: Request,
    file_path: str,
    supabase: Client = Depends(get_supabase),
    storage_service: StorageService = Depends(get_storage_service),
):
    """Delete a file from storage."""
    user = get_current_user(request, supabase)
    if not user:
        return {"success": False, "message": "Unauthorized"}
    
    # Security: Ensure user can only delete their own files
    if not file_path.startswith(user["id"]):
        return {"success": False, "message": "Access denied"}
    
    success, message = storage_service.delete_file(file_path)
    
    return {"success": success, "message": message}

