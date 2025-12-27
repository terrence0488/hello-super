"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.routers import auth, tasks, storage, realtime

# Initialize FastAPI app
app = FastAPI(
    title="Hello Super",
    description="A demo web app showcasing Supabase capabilities",
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(storage.router)
app.include_router(realtime.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """Landing page."""
    settings = get_settings()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"debug": settings.debug},
    )


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}

