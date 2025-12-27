# Supabase Demo Web App - Implementation Plan

## 📋 Project Overview

This project demonstrates the core capabilities of **Supabase** as a backend-as-a-service (BaaS) platform using Python. The demo will be a simple **Task Management App** that showcases authentication, database operations (CRUD), real-time subscriptions, and file storage.

---

## 🎯 Features to Demonstrate

| Feature | Supabase Capability | Description |
|---------|---------------------|-------------|
| User Authentication | Supabase Auth | Sign up, sign in, sign out, session management |
| Database CRUD | Supabase Database (PostgreSQL) | Create, read, update, delete tasks |
| Row Level Security | RLS Policies | Users can only access their own tasks |
| Real-time Updates | Supabase Realtime | Live task updates without page refresh |
| File Storage | Supabase Storage | Upload/download task attachments |

---

## 🏗️ Technical Architecture

```
                         ┌─────────────────────────────────┐
                         │         User's Browser          │
                         │      (Jinja2 + HTMX + CSS)      │
                         └─────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                              RAILWAY                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        FastAPI Web Server                            │  │
│  │   ┌─────────────┐   ┌─────────────┐   ┌───────────────────────┐     │  │
│  │   │   Routes    │   │  Services   │   │   Supabase Client     │     │  │
│  │   │  (Views)    │◄──┤  (Business  │◄──┤   (supabase-py)       │     │  │
│  │   │             │   │   Logic)    │   │                       │     │  │
│  │   └─────────────┘   └─────────────┘   └───────────────────────┘     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  Your Python code lives here: routes, business logic, templates           │
└───────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                            SUPABASE CLOUD                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │     Auth     │  │   Database   │  │   Realtime   │  │   Storage    │   │
│  │  (JWT/OAuth) │  │ (PostgreSQL) │  │ (WebSockets) │  │  (S3-like)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                            │
│  Data layer only: authentication, database, realtime, file storage        │
└───────────────────────────────────────────────────────────────────────────┘
```

### Why Railway + Supabase?

| Component | Railway | Supabase |
|-----------|---------|----------|
| **Python Code** | ✅ Full FastAPI server | ❌ Not supported |
| **Database** | ❌ Use Supabase instead | ✅ PostgreSQL with RLS |
| **Authentication** | ❌ Build yourself | ✅ Built-in (OAuth, magic links) |
| **Realtime** | ❌ Build yourself | ✅ WebSocket subscriptions |
| **File Storage** | ❌ Need S3/MinIO | ✅ Built-in with CDN |
| **Hosting** | ✅ Container hosting | ❌ Not supported |

**Summary**: Railway runs your Python app; Supabase handles data, auth, and storage.

---

## 🛠️ Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Deployment** | Railway | Easy Python hosting, auto-deploy from GitHub |
| **Backend Services** | Supabase | Auth, Database, Realtime, Storage in one |
| **Web Framework** | FastAPI | Modern, async, great DX, automatic OpenAPI docs |
| **Supabase Client** | supabase-py | Official Python SDK |
| **Templating** | Jinja2 | Server-side rendering, simple and fast |
| **Interactivity** | HTMX | Minimal JS, progressive enhancement |
| **Styling** | Tailwind CSS (CDN) | Rapid UI development |
| **Package Manager** | uv | Modern, fast Python tooling |

---

## 📁 Project Structure

```
hello-super/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # Dependency injection (Supabase client)
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── tasks.py         # Task CRUD routes
│   │   └── storage.py       # File upload/download routes
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Auth business logic
│   │   ├── task_service.py  # Task business logic
│   │   └── storage_service.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   │
│   ├── templates/
│   │   ├── base.html        # Base layout
│   │   ├── index.html       # Landing page
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── tasks/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── partials/    # HTMX partial templates
│   │   │       ├── task_item.html
│   │   │       └── task_form.html
│   │   └── components/
│   │       └── navbar.html
│   │
│   └── static/
│       └── css/
│           └── styles.css   # Custom styles (if needed)
│
├── scripts/
│   └── setup_supabase.sql   # Database schema & RLS policies
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
│
├── .env.example             # Environment template
├── .gitignore
├── pyproject.toml           # Dependencies
├── Procfile                 # Railway/Heroku process definition
├── railway.toml             # Railway deployment configuration
├── README.md                # Setup & usage instructions
└── agent.md                 # This file
```

---

## 🗄️ Database Schema

### `tasks` Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| user_id | UUID | NOT NULL, REFERENCES auth.users(id) |
| title | TEXT | NOT NULL |
| description | TEXT | |
| is_completed | BOOLEAN | DEFAULT false |
| attachment_path | TEXT | Path in Supabase Storage |
| created_at | TIMESTAMPTZ | DEFAULT now() |
| updated_at | TIMESTAMPTZ | DEFAULT now() |

### Row Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own tasks
CREATE POLICY "Users can view own tasks" ON tasks
  FOR SELECT USING (auth.uid() = user_id);

-- Policy: Users can insert their own tasks  
CREATE POLICY "Users can create own tasks" ON tasks
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own tasks
CREATE POLICY "Users can update own tasks" ON tasks
  FOR UPDATE USING (auth.uid() = user_id);

-- Policy: Users can delete their own tasks
CREATE POLICY "Users can delete own tasks" ON tasks
  FOR DELETE USING (auth.uid() = user_id);
```

---

## 🔐 Environment Variables

### Local Development (`.env` file)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key  # For admin operations only
SECRET_KEY=your-secret-key-for-sessions
DEBUG=true
```

### Production (Railway Dashboard)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=different-production-secret-key  # Must be different from dev!
DEBUG=false
PORT=8000  # Railway sets this automatically
```

---

## 📦 Dependencies

```toml
[project]
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "supabase>=2.10.0",
    "python-dotenv>=1.0.0",
    "jinja2>=3.1.0",
    "python-multipart>=0.0.9",  # For file uploads
    "httpx>=0.27.0",            # Async HTTP client
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",  # For TestClient
]
```

---

## 🚀 Implementation Phases

### Phase 1: Project Setup ✅ COMPLETED
- [x] Create `agent.md` (this file)
- [x] Update `pyproject.toml` with dependencies
- [x] Create project structure (folders, `__init__.py` files)
- [x] Set up configuration (`config.py`, `.env.example`)
- [x] Initialize Supabase client (`dependencies.py`)
- [x] Create base templates (`base.html`, `index.html`)
- [x] Create `.gitignore`
- [x] Create deployment files (`Procfile`, `railway.toml`)

### Phase 2: Authentication ✅ COMPLETED
- [x] Create Pydantic schemas (`models/schemas.py`)
- [x] Create auth service with signup/signin/signout (`services/auth_service.py`)
- [x] Create auth routes (`routers/auth.py`)
- [x] Create login/register templates
- [x] Implement session management (cookie-based)

### Phase 3: Task CRUD ✅ COMPLETED
- [x] Create task service (`services/task_service.py`)
- [x] Create task routes (`routers/tasks.py`)
- [x] Create task templates with HTMX interactivity
- [x] Provide SQL setup script (`scripts/setup_supabase.sql`)

### Phase 4: File Storage ✅ COMPLETED
- [x] Create storage service (`services/storage_service.py`)
- [x] Create storage routes (`routers/storage.py`)
- [x] Add file upload to task creation
- [x] Implement file download with signed URLs

### Phase 5: Real-time ✅ COMPLETED
- [x] Create realtime service (`services/realtime_service.py`)
- [x] Add SSE route for live updates (`routers/realtime.py`)
- [x] Update task list with live status indicator
- [x] Implement auto-updating task stats

### Phase 6: Polish & Documentation ✅ COMPLETED
- [x] Create comprehensive README with setup instructions
- [x] Improve error handling and user feedback
- [x] Add toast notification system
- [x] Add basic test suite

### Phase 7: Deployment (Railway + Supabase) ✅ READY
- [x] Create deployment guide (`DEPLOYMENT.md`)
- [x] Verify deployment files (`Procfile`, `railway.toml`)
- [x] Ensure `.gitignore` excludes sensitive files
- [ ] Push code to GitHub repository (user action required)
- [ ] Create Railway project and connect to GitHub (user action required)
- [ ] Configure environment variables in Railway dashboard (user action required)
- [ ] Deploy and verify production URL (user action required)
- [ ] (Optional) Set up custom domain (user action required)

---

## 🎨 UI Design Direction

- **Theme**: Clean, minimal dark theme with accent colors
- **Layout**: Single-page dashboard feel with sidebar navigation
- **Interactions**: HTMX for smooth partial updates (no full page reloads)
- **Feedback**: Toast notifications for actions, loading states

---

## ⚙️ Supabase Setup Requirements

Before running the app, users need to:

1. Create a Supabase project at https://supabase.com
2. Run the SQL schema script in Supabase SQL Editor
3. Create a storage bucket named `task-attachments`
4. Copy project URL and anon key to `.env`

---

## 🚂 Railway Deployment Guide

### Prerequisites
- GitHub account with code pushed to a repository
- Railway account (https://railway.app) - sign up with GitHub

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/hello-super.git
   git push -u origin main
   ```

2. **Create Railway Project**
   - Go to https://railway.app/new
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your repository
   - Select the `hello-super` repository

3. **Configure Environment Variables**
   - In Railway dashboard, go to your project → Variables
   - Add all required environment variables:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `SECRET_KEY` (generate a new one for production!)
     - `DEBUG=false`

4. **Deploy**
   - Railway auto-detects Python and deploys using the `Procfile`
   - Wait for build to complete (~2-3 minutes)
   - Click "Generate Domain" to get a public URL

5. **Verify**
   - Visit your Railway URL (e.g., `https://hello-super-production.up.railway.app`)
   - Test health endpoint: `https://your-url.up.railway.app/health`

### Deployment Files

**Procfile** - Tells Railway how to run the app:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**railway.toml** - Railway-specific configuration:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

### Cost Estimate

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Railway** | $5 credits/month | $20/month + usage |
| **Supabase** | 500MB DB, 1GB storage | $25/month Pro |
| **Total** | $0 for small demos | ~$45/month for production |

---

## ✅ Approval Checklist

- [x] Tech stack choice (FastAPI + HTMX + Jinja2) - **Approved**
- [x] Project structure - **Approved**
- [x] Features scope (Auth, CRUD, Storage, Realtime) - **Approved**
- [x] Database schema design - **Approved**
- [x] Implementation phases order - **Approved**

---

## 📝 Implementation Log

### Phase 1 Completed (2025-12-26)

Files created:
- `pyproject.toml` - Updated with all dependencies
- `app/__init__.py` - Package init
- `app/main.py` - FastAPI entry point with landing page route
- `app/config.py` - Environment configuration with Settings class
- `app/dependencies.py` - Supabase client dependency injection
- `app/routers/__init__.py` - Routers package
- `app/services/__init__.py` - Services package
- `app/models/__init__.py` - Models package
- `app/templates/base.html` - Base HTML template with Tailwind + HTMX
- `app/templates/index.html` - Landing page
- `tests/__init__.py` - Test package
- `.env.example` - Environment template
- `.gitignore` - Git ignore rules
- `Procfile` - Railway/Heroku process definition
- `railway.toml` - Railway deployment configuration

### Phase 2 Completed (2025-12-26)

Files created:
- `app/models/schemas.py` - Pydantic schemas for auth and tasks
- `app/services/auth_service.py` - Authentication service using Supabase Auth
- `app/routers/auth.py` - Auth routes (login, register, logout, me)
- `app/templates/auth/login.html` - Login page with form
- `app/templates/auth/register.html` - Registration page with form

Features implemented:
- User registration with email/password
- User login with session cookie
- User logout with cookie deletion
- Session validation via access token
- Error handling and user feedback

Routes added:
- `GET /auth/login` - Login page
- `POST /auth/login` - Login form submission
- `GET /auth/register` - Registration page
- `POST /auth/register` - Registration form submission
- `GET /auth/logout` - Logout and redirect
- `GET /auth/me` - Get current user info

### Phase 3 Completed (2025-12-26)

Files created:
- `app/services/task_service.py` - Task CRUD operations with Supabase
- `app/routers/tasks.py` - Task routes with HTMX support
- `app/templates/tasks/list.html` - Tasks dashboard page
- `app/templates/tasks/partials/task_item.html` - Task item component (HTMX)
- `app/templates/tasks/partials/task_edit.html` - Inline edit form (HTMX)
- `scripts/setup_supabase.sql` - Database schema with RLS policies

Features implemented:
- Create new tasks with title and description
- View all tasks in a beautiful list
- Toggle task completion (checkbox)
- Edit task inline (HTMX swap)
- Delete task with confirmation
- Real-time UI updates without page refresh (HTMX)

Routes added:
- `GET /tasks` - Tasks list page
- `POST /tasks/create` - Create task (HTMX)
- `POST /tasks/{id}/toggle` - Toggle completion (HTMX)
- `PUT /tasks/{id}` - Update task (HTMX)
- `DELETE /tasks/{id}` - Delete task (HTMX)
- `GET /tasks/{id}/edit` - Get edit form (HTMX)

### Phase 4 Completed (2025-12-26)

Files created:
- `app/services/storage_service.py` - Supabase Storage operations
- `app/routers/storage.py` - File upload/download routes

Files updated:
- `app/routers/tasks.py` - Added file upload support to task creation
- `app/services/task_service.py` - Added attachment_path parameter
- `app/templates/tasks/list.html` - Added file upload input
- `app/templates/tasks/partials/task_item.html` - Show attachment badge

Features implemented:
- Upload files when creating tasks (images, PDFs)
- Files stored in Supabase Storage bucket
- Signed URLs for secure file downloads
- Attachment badge displayed on tasks
- File type validation (images, PDFs only)
- File size limit (5MB)

Routes added:
- `POST /storage/upload` - Upload a file
- `GET /storage/download/{path}` - Download file (redirect to signed URL)
- `GET /storage/url/{path}` - Get signed URL (JSON)
- `DELETE /storage/{path}` - Delete a file

### Phase 5 Completed (2025-12-26)

Files created:
- `app/services/realtime_service.py` - Realtime polling and stats service
- `app/routers/realtime.py` - Server-Sent Events (SSE) routes

Files updated:
- `app/main.py` - Added realtime router
- `app/templates/tasks/list.html` - Live status indicator and auto-refresh

Features implemented:
- Server-Sent Events (SSE) for live updates
- Real-time task count updates
- Live connection status indicator
- Auto-reconnect on connection loss
- Task statistics endpoint

Routes added:
- `GET /realtime/tasks/stream` - SSE stream for task updates
- `GET /realtime/tasks/stats` - Get current task statistics

### Phase 6 Completed (2025-12-26)

Files created:
- `README.md` - Comprehensive setup and usage documentation
- `tests/conftest.py` - Pytest configuration and fixtures
- `tests/test_main.py` - Tests for main routes
- `tests/test_auth.py` - Tests for authentication routes
- `tests/test_tasks.py` - Tests for task routes

Files updated:
- `app/templates/base.html` - Added toast notification system
- `app/services/task_service.py` - Improved error messages

Features implemented:
- Comprehensive README with setup instructions
- Toast notifications for user feedback
- Better error messages with helpful hints
- Basic test suite covering main routes
- Troubleshooting guide in README

### Phase 7 Deployment Guide Created (2025-12-26)

Files created:
- `DEPLOYMENT.md` - Complete step-by-step deployment guide

Deployment readiness:
- ✅ `Procfile` - Railway process definition
- ✅ `railway.toml` - Railway configuration
- ✅ `.gitignore` - Excludes `.env` and sensitive files
- ✅ `pyproject.toml` - All dependencies defined
- ✅ `README.md` - Includes deployment section

**Next Steps for User:**
1. Review `DEPLOYMENT.md` for detailed instructions
2. Push code to GitHub
3. Deploy to Railway following the guide
4. Configure environment variables
5. Verify deployment

**All implementation phases complete! 🎉**

