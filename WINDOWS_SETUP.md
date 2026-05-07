# NyayPath Windows Setup

This guide fixes the common PowerShell errors:

- `pip : The term 'pip' is not recognized`
- `uvicorn : The term 'uvicorn' is not recognized`
- `npm : The term 'npm' is not recognized`
- `cd frontend` failing while you are inside `backend`

## 1. Install Python

Install Python 3.11 or newer from:

```text
https://www.python.org/downloads/
```

During installation, enable:

```text
Add python.exe to PATH
```

If PowerShell shows this message:

```text
Python was not found; run without arguments to install from the Microsoft Store
```

Python is not installed correctly for command-line use, or the Microsoft Store alias is intercepting the command.

Fix:

1. Install Python from `python.org`.
2. Enable `Add python.exe to PATH`.
3. Close and reopen PowerShell.
4. If it still fails, open Windows Settings and search for `App execution aliases`.
5. Turn off the aliases for `python.exe` and `python3.exe`.

Then open a new PowerShell window and check:

```powershell
python --version
python -m pip --version
```

If `python` still does not work, try:

```powershell
py --version
py -m pip --version
```

## 2. Install Node.js

Install the Node.js LTS version from:

```text
https://nodejs.org/
```

Then open a new PowerShell window and check:

```powershell
node --version
npm --version
```

## Quick Prerequisite Check

From the project root:

```powershell
cd C:\Users\bhaja\Downloads\67676767676
.\check-prerequisites.ps1
```

## 3. Run Backend

From the project root:

```powershell
cd C:\Users\bhaja\Downloads\67676767676
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Keep this PowerShell window open.

Backend URL:

```text
http://127.0.0.1:8000
```

API docs in development:

```text
http://127.0.0.1:8000/docs
```

## 4. Run Frontend

Open a second PowerShell window.

From the project root:

```powershell
cd C:\Users\bhaja\Downloads\67676767676
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Important Path Note

If you are currently inside:

```text
C:\Users\bhaja\Downloads\67676767676\backend
```

Then this is wrong:

```powershell
cd frontend
```

Use this instead:

```powershell
cd ..\frontend
```

Or go back to the project root first:

```powershell
cd ..
cd frontend
```

## If PowerShell Blocks Virtual Environment Activation

Run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Production-style Backend Command

After dependencies are installed:

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Using `python -m uvicorn` is more reliable on Windows than calling `uvicorn` directly.
