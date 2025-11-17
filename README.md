# op-schema

## Quick Start

./run.bat

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- PostgreSQL
- Node.js (for frontend, if applicable)

### Backend Setup

1. **Install uv** (if not already installed)

   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd op-schema
   ```

3. **Set up environment variables**

   ```bash
   cp .example.env .env
   ```

   Edit `.env` and configure:

   - `DB_URL` - Your PostgreSQL connection string
   - `SECRET_KEY` - Generate a secure random key
   - `SMTP_*` - Your email server credentials (if using email features)

4. **Install dependencies with uv**

   ```bash
   uv sync
   ```

5. **Run database migrations**

   ```bash
   uv run alembic upgrade head
   ```

6. **Start the backend server**
   ```bash
   uv run uvicorn Backend.app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Environment Variables

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
