# NyayPath Backend

FastAPI backend for PDF judgment extraction, OCR fallback, rule-based action generation, and human verification.

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Windows PowerShell

If `pip` or `uvicorn` is not recognized, install Python and use module commands:

```powershell
cd C:\Users\bhaja\Downloads\67676767676\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

You can also run:

```powershell
.\start-dev.ps1
```

See `../WINDOWS_SETUP.md` for the full Windows guide.

## Production-style Run

Create a production environment file from `.env.example`, then set those variables in your hosting environment. For local testing, you can copy `.env.example` to `.env`.

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Important production settings:

- `ENVIRONMENT=production`
- `DEBUG=false`
- `ALLOWED_ORIGINS=https://your-frontend-domain.example`
- `ALLOWED_HOSTS=your-backend-domain.example`
- `MAX_UPLOAD_MB=25`
- `DATABASE_URL=sqlite:///./nyaypath.db` for local SQLite, or a managed database URL later.

For hosted backend deployments, use Python 3.11. The repo includes `runtime.txt` for platforms like Render.

Health endpoints:

- `GET /health`
- `GET /ready`

Run backend tests:

```bash
pytest
```

## Notes

- SQLite is created automatically at `backend/nyaypath.db`.
- Uploaded PDFs are stored in `backend/uploads`.
- OCR fallback requires Tesseract installed on your machine and available on `PATH`.
- spaCy is loaded with a blank English pipeline so the app runs without downloading paid or external AI services.
- API docs are available at `/docs` only when `DEBUG=true`.
