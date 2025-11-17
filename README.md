# op-schema

A full-stack customer lifecycle management application with a **FastAPI** backend (managed by **uv**) and a **React + TypeScript + Tailwind CSS** frontend.

## Quick Start

Run both backend and frontend together:

```bash
./run.bat
```

This will start:
- **Backend** at `http://localhost:8000`
- **Frontend** at `http://localhost:5173`

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package installer and manager (replaces pip/venv)
- **PostgreSQL** - Database server
- **Node.js 18+** and **npm** - For the frontend

---

## Installation

### 1. Install uv (if not already installed)

This project uses **uv** for Python dependency management instead of pip/virtualenv.

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```bash
git clone <repository-url>
cd op-schema
```

### 3. Set up environment variables

```bash
cp .example.env .env
```

Edit `.env` and configure:

- `DB_URL` - Your PostgreSQL connection string (e.g., `postgresql://user:password@localhost:5432/dbname`)
- `SECRET_KEY` - Generate a secure random key
- `SMTP_*` - Your email server credentials (if using email features)

---

## Backend Setup

### 1. Install Python dependencies with uv

```bash
uv sync
```

This command will:
- Create a virtual environment (`.venv`)
- Install all dependencies from `pyproject.toml`
- Generate a lock file (`uv.lock`)

### 2. Run database migrations

```bash
uv run alembic upgrade head
```

### 3. Start the backend server

```bash
uv run uvicorn Backend.app.main:app --reload
```

The API will be available at **`http://localhost:8000`**

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Frontend Setup

### 1. Navigate to the Frontend directory

```bash
cd Frontend
```

### 2. Install Node.js dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The frontend will be available at **`http://localhost:5173`**

### Frontend Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

---

## Project Structure

```
op-schema/
├── Backend/           # FastAPI backend application
├── Frontend/          # React + Vite frontend application
├── alembic/           # Database migration files
├── .env               # Environment variables (create from .example.env)
├── pyproject.toml     # Python dependencies (managed by uv)
├── uv.lock            # Lock file for Python dependencies
└── run.bat            # Start both backend and frontend
```

---

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **uv** - Python package manager

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **TanStack Query** - Data fetching and caching
- **React Router** - Client-side routing

---

## Environment Variables

See `.example.env` for all required configuration options.

## Customer lifecycle management

The system provides two different ways to “remove” a customer:

### 🔹 Deactivate (soft delete)

- **Endpoint**: `PUT /customers/{id}/deactivate`
- Sets the field `is_active = False`.
- The customer record remains in the database.
- All schedules, history, and relationships are preserved.
- **Use cases**:
  - The customer is no longer active (e.g., moved away, deceased, or no longer receiving services).
  - You want to retain historical and statistical data.

### 🔹 Delete (hard delete)

- **Endpoint**: `DELETE /customers/{id}`
- Permanently removes the customer from the database.
- **Should only be used when**:
  - The customer record was created by mistake (duplicate entry, incorrect details).
- ⚠️ **Warning**: This also removes related data such as schedules and visits associated with the customer.

### Best practices

- **Default action**: use `deactivate`.
- **Exception**: use `delete` only when the data is invalid and must be permanently removed.
- Frontend should always request explicit confirmation before invoking `delete`.
  Example: _“Are you sure you want to permanently delete this customer?”_
