# NyayPath Production Readiness Checklist

## Backend

- Use `ENVIRONMENT=production` and `DEBUG=false`.
- Set `ALLOWED_ORIGINS` to the exact frontend domain.
- Set `ALLOWED_HOSTS` to the exact backend host.
- Keep `MAX_UPLOAD_MB` aligned with hosting limits.
- Install Tesseract OCR on the server and confirm `tesseract --version` works.
- Back up `nyaypath.db` if using SQLite for demos or pilots.
- Move to PostgreSQL before multi-user government deployment.
- Put the API behind HTTPS.
- Keep uploaded PDFs outside public web roots.

## Frontend

- Set `VITE_API_BASE_URL` to the production API URL.
- Run `npm run build` and deploy `frontend/dist`.
- Configure SPA fallback routing on the static host.
- Test upload, review, approve, dashboard, and details routes after deploy.

## Data And Safety

- This system supports judgment understanding and workflow assistance only.
- Keep human verification mandatory.
- Do not present extracted actions as legal advice.
- Log operational failures without logging full judgment text in shared logs.
- Review retention rules before storing real court documents.

## Commands

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Frontend:

```bash
cd frontend
npm install
npm run build
npm run serve
```
