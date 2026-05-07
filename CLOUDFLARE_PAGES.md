# Cloudflare Pages Deployment

Deploy **only the frontend** on Cloudflare Pages.

## Required Settings

In Cloudflare Pages, set:

```text
Framework preset: Vite
Root directory: frontend
Build command: npm run build
Build output directory: dist
```

Environment variables:

```text
VITE_API_BASE_URL=https://nyayapath-swwf.onrender.com
VITE_REQUEST_TIMEOUT_MS=60000
```

## If Cloudflare Still Runs pip

If the build log contains:

```text
Installing project dependencies: pip install -r requirements.txt
```

then Cloudflare is not using `frontend` as the root directory.

Fix it in Cloudflare:

1. Open the Pages project.
2. Go to `Settings`.
3. Go to `Builds & deployments`.
4. Under `Build configurations`, set `Root directory` to:

```text
frontend
```

5. Set `Build command` to:

```text
npm run build
```

6. Set `Build output directory` to:

```text
dist
```

7. Save.
8. Go to `Deployments`.
9. Click `Retry deployment` or push a new commit.

## Alternative Root Build Settings

If you cannot set Root directory, use these instead:

```text
Root directory: /
Build command: npm --prefix frontend install && npm --prefix frontend run build
Build output directory: frontend/dist
```

But the recommended setup is still:

```text
Root directory: frontend
```

## Backend

The FastAPI backend must stay on Render or another Python server.

Cloudflare Pages should not install:

```text
backend/requirements.txt
```

