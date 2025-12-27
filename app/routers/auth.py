"""Authentication routes."""

from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase import Client

from app.dependencies import get_supabase
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

# Cookie settings
COOKIE_NAME = "session_token"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


def get_auth_service(supabase: Client = Depends(get_supabase)) -> AuthService:
    """Dependency to get auth service."""
    return AuthService(supabase)


def get_current_user(request: Request, supabase: Client = Depends(get_supabase)) -> Optional[dict]:
    """Get current user from session cookie."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    
    auth_service = AuthService(supabase)
    return auth_service.get_user_from_token(token)


# =============================================================================
# Page Routes (HTML)
# =============================================================================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render login page."""
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"error": None},
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render registration page."""
    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
        context={"error": None},
    )


# =============================================================================
# Form Action Routes
# =============================================================================

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Handle login form submission."""
    success, message, session_data = auth_service.sign_in(email, password)
    
    if success and session_data:
        # Create redirect response with session cookie
        redirect = RedirectResponse(url="/tasks", status_code=303)
        redirect.set_cookie(
            key=COOKIE_NAME,
            value=session_data["access_token"],
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            samesite="lax",
        )
        return redirect
    else:
        # Re-render login page with error
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": message, "email": email},
        )


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Handle registration form submission."""
    # Validate passwords match
    if password != password_confirm:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"error": "Passwords do not match", "email": email},
        )
    
    # Validate password length
    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"error": "Password must be at least 6 characters", "email": email},
        )
    
    success, message, user_data = auth_service.sign_up(email, password)
    
    if success:
        # Redirect to login with success message
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"success": message, "email": email},
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"error": message, "email": email},
        )


@router.get("/logout")
async def logout(auth_service: AuthService = Depends(get_auth_service)):
    """Handle logout."""
    auth_service.sign_out()
    
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key=COOKIE_NAME)
    return redirect


# =============================================================================
# Utility Routes
# =============================================================================

@router.get("/me")
async def get_me(
    request: Request,
    user: Optional[dict] = Depends(get_current_user),
):
    """Get current authenticated user."""
    if not user:
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user": user}

