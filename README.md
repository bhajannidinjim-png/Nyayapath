# NyayPath Frontend

React + Vite frontend for the NyayPath legal workflow dashboard.

## Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Windows PowerShell

The `frontend` folder is beside `backend`, not inside it. If you are inside `backend`, run:

```powershell
cd ..\frontend
```

Then:

```powershell
npm install
npm run dev
```

You can also run:

```powershell
.\start-dev.ps1
```

If `npm` is not recognized, install Node.js LTS and reopen PowerShell.

If npm reports dependency resolution or cache permission errors, run:

```powershell
npm install --cache .npm-cache
npm run dev
```

## Production Build

Create an environment file from `.env.example` and point it to the deployed backend:

```bash
VITE_API_BASE_URL=https://your-backend-domain.example
VITE_REQUEST_TIMEOUT_MS=60000
```

Build and preview:

```bash
npm run build
npm run serve
```

Deploy the generated `dist` folder on a static host. Configure the backend `ALLOWED_ORIGINS` setting to match the frontend URL.
