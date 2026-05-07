# NyayPath Deployment

## Frontend On Vercel

Deploy only the React frontend on Vercel.

Recommended Vercel settings:

```text
Framework Preset: Vite
Root Directory: leave blank if using vercel.json, or set to frontend
Install Command: cd frontend && npm install
Build Command: cd frontend && npm run build
Output Directory: frontend/dist
```

If you set Vercel Root Directory to `frontend`, then use:

```text
Install Command: npm install
Build Command: npm run build
Output Directory: dist
```

Environment variables:

```text
VITE_API_BASE_URL=https://your-backend-url.example
VITE_REQUEST_TIMEOUT_MS=60000
```

Do not let Vercel install `backend/requirements.txt` for the frontend app. The backend has PDF/OCR dependencies and must be deployed separately.

## Frontend On Cloudflare Pages

Use:

```text
Framework preset: Vite
Root directory: frontend
Build command: npm run build
Build output directory: dist
```

If Cloudflare logs `pip install -r requirements.txt`, the root directory is wrong. See `CLOUDFLARE_PAGES.md`.

## Backend On Render

Use `backend` as the root directory.

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Python version is pinned in:

```text
backend/runtime.txt
```

Environment variables:

```text
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app
ALLOWED_HOSTS=your-render-domain.onrender.com
MAX_UPLOAD_MB=25
```

## Why The Pillow Error Happened

The failed log shows:

```text
Python 3.13.3
pip install -r requirements.txt
Pillow==10.3.0
KeyError: '__version__'
```

That means the deploy platform tried to build backend Python packages during a frontend deployment. Python 3.13 also does not match this backend stack. Use Python 3.11 for the backend and keep Vercel focused on the frontend.
