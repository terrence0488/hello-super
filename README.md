# Hello Super 🚀

A demo web application showcasing **Supabase** capabilities with Python and FastAPI. This project demonstrates authentication, database operations (CRUD), real-time updates, and file storage.

## ✨ Features

- 🔐 **Authentication** - User sign up, sign in, and session management with Supabase Auth
- 📝 **Task Management** - Full CRUD operations for tasks with PostgreSQL
- 🔒 **Row Level Security** - Database-level security policies
- 📎 **File Storage** - Upload and download task attachments (images, PDFs)
- ⚡ **Real-time Updates** - Live task statistics via Server-Sent Events (SSE)
- 🎨 **Modern UI** - Beautiful dark-themed interface with HTMX for smooth interactions

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database & Auth**: Supabase (PostgreSQL + Auth)
- **Templating**: Jinja2
- **Interactivity**: HTMX
- **Styling**: Tailwind CSS
- **Package Manager**: uv

## 📋 Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager (recommended)
- A [Supabase](https://supabase.com) account and project

> **Note**: This project uses `uv` as the package manager. Install it with:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd hello-super
```

### 2. Install Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment (`.venv/`)
- Install all dependencies from `pyproject.toml`
- Make the project available for development

> **Alternative**: If you prefer pip, use `pip install -e .`, but `uv` is recommended for faster installs.

### 3. Set Up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run the setup script:
   ```bash
   cat scripts/setup_supabase.sql
   ```
   Copy and paste the entire SQL script into Supabase SQL Editor and execute it.

3. Create a storage bucket:
   - Go to **Storage** in Supabase Dashboard
   - Click **"New bucket"**
   - Name: `task-attachments`
   - Set to **Private** (not public)
   - Click **Create bucket**

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=your-secret-key-for-sessions
DEBUG=true
```

**Where to find these values:**
- Go to your Supabase project → **Settings** → **API**
- `SUPABASE_URL` = Project URL
- `SUPABASE_KEY` = `anon` `public` key
- `SUPABASE_SERVICE_KEY` = `service_role` key (⚠️ keep secret!)
- `SECRET_KEY` = Generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"`

### 5. Run the Application

```bash
uv run uvicorn app.main:app --reload
```

This uses `uv` to run uvicorn with the project's virtual environment automatically.

> **Alternative**: Activate the venv manually and run:
> ```bash
> source .venv/bin/activate  # On macOS/Linux
> # or
> .venv\Scripts\activate  # On Windows
> uvicorn app.main:app --reload
> ```

Visit **http://127.0.0.1:8000** in your browser!

## 📁 Project Structure

```
hello-super/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # Dependency injection
│   ├── routers/             # API routes
│   │   ├── auth.py         # Authentication routes
│   │   ├── tasks.py        # Task CRUD routes
│   │   ├── storage.py      # File storage routes
│   │   └── realtime.py     # Real-time SSE routes
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── storage_service.py
│   │   └── realtime_service.py
│   ├── models/              # Pydantic schemas
│   │   └── schemas.py
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       └── tasks/
├── scripts/
│   └── setup_supabase.sql   # Database schema
├── tests/                   # Test suite
├── .env.example            # Environment template
├── pyproject.toml         # Dependencies
└── README.md              # This file
```

## 🎯 Usage

### Authentication

1. Visit the landing page at **http://127.0.0.1:8000**
2. Click **"Get Started"** to register
3. Sign in with your credentials
4. You'll be redirected to the tasks dashboard

### Task Management

- **Create Task**: Fill in the form and click "Add Task"
- **Toggle Completion**: Click the checkbox
- **Edit Task**: Hover over a task and click the edit icon
- **Delete Task**: Hover over a task and click the delete icon
- **Attach File**: Select an image or PDF when creating a task

### Real-time Features

- The dashboard shows live task statistics
- Task counts update automatically every 3 seconds
- Green "Live" indicator shows connection status

## 🧪 Testing

Run the test suite with `uv`:

```bash
uv run pytest
```

Or with coverage:

```bash
uv run pytest --cov=app
```

> **Note**: `uv run` automatically uses the project's virtual environment, so you don't need to activate it manually.

## 🚂 Deployment

### Deploy to Railway

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/hello-super.git
   git push -u origin main
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click **"New Project"** → **"Deploy from GitHub repo"**
   - Select your repository

3. **Configure Environment Variables**
   - In Railway dashboard → **Variables**
   - Add all variables from your `.env` file:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `SECRET_KEY` (generate a new one for production!)
     - `DEBUG=false`

4. **Deploy**
   - Railway auto-detects Python and deploys
   - Wait for build to complete (~2-3 minutes)
   - Click **"Generate Domain"** to get a public URL

5. **Verify**
   - Visit your Railway URL
   - Test the health endpoint: `https://your-url.up.railway.app/health`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | ✅ Yes |
| `SUPABASE_KEY` | Supabase anon/public key | ✅ Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service_role key | ✅ Yes |
| `SECRET_KEY` | Secret for session cookies | ✅ Yes |
| `DEBUG` | Enable debug mode | ❌ No (default: false) |

### Supabase Setup Checklist

- [ ] Created Supabase project
- [ ] Ran `scripts/setup_supabase.sql` in SQL Editor
- [ ] Created `task-attachments` storage bucket
- [ ] Copied API keys to `.env` file

## 📚 API Documentation

Once the app is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🐛 Troubleshooting

### "Tasks table not found"
- Run the SQL setup script in Supabase SQL Editor
- Check that the `tasks` table exists in **Table Editor**

### "Row-level security policy violation"
- Ensure `SUPABASE_SERVICE_KEY` is set in `.env`
- Verify RLS policies were created by the SQL script

### "Storage bucket not found"
- Create the `task-attachments` bucket in Supabase Storage
- Ensure it's set to **Private**

### "Cannot connect to Supabase"
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check your Supabase project is active

## 🤝 Contributing

This is a demo project, but contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Supabase](https://supabase.com) for the amazing backend platform
- [FastAPI](https://fastapi.tiangolo.com) for the web framework
- [HTMX](https://htmx.org) for progressive enhancement

## 📖 Learn More

- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [HTMX Documentation](https://htmx.org/docs)

---

**Built with ❤️ using Supabase, FastAPI, and HTMX**

