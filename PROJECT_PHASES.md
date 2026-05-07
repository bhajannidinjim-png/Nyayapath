# NyayPath Incremental Phases

This file maps the implemented codebase to the requested hackathon phases.

## Phase 1: Frontend + Backend Setup

New files:
- `backend/app/main.py`, `backend/app/config/settings.py`, `backend/app/database/session.py`
- `frontend/package.json`, `frontend/vite.config.js`, `frontend/index.html`, `frontend/src/main.jsx`, `frontend/src/App.jsx`
- shared layout and CSS files under `frontend/src/layouts`, `frontend/src/components`, `frontend/src/styles`

Install:
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

Run:
```bash
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

Explanation: FastAPI exposes modular routes and React Router provides six pages inside a government-dashboard layout.

## Phase 2: PDF Upload + Extraction

New files:
- `backend/app/routes/judgments.py`
- `backend/app/services/judgment_service.py`
- `backend/app/extraction/pdf_extractor.py`
- `backend/app/utils/file_utils.py`
- `frontend/src/pages/UploadJudgment.jsx`
- `frontend/src/pages/ExtractionReview.jsx`

Explanation: Uploads are validated as PDFs, saved to `backend/uploads`, extracted page by page using PyMuPDF, and shown in the review UI.

## Phase 3: OCR Fallback

New files:
- `backend/app/services/ocr_service.py`

Explanation: Pages with very little embedded text are marked as scanned and passed through pytesseract. If Tesseract is missing, extraction continues and the error is kept page-local.

Common fix: Install Tesseract OCR and make sure `tesseract` is available on PATH.

## Phase 4: Metadata Extraction

New files:
- `backend/app/extraction/metadata_extractor.py`

Explanation: Court name, case number, parties, and date are extracted with explainable regex patterns. Each field stores value, confidence, source text, reason, and page reference.

## Phase 5: Action Extraction Engine

New files:
- `backend/app/extraction/action_engine.py`

Explanation: The engine scores directive paragraphs, classifies action type, infers department, extracts deadlines, assigns priority, and creates confidence-scored action drafts with source evidence.

## Phase 6: Human Verification

New files:
- `backend/app/routes/actions.py`
- `backend/app/services/action_service.py`
- `frontend/src/pages/HumanVerification.jsx`
- `frontend/src/components/EditActionModal.jsx`

Explanation: Reviewers can approve, edit-and-approve, reject, or leave items pending. Only approved items are used by dashboard endpoints.

## Phase 7: Dashboard

New files:
- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/pages/ApprovedActions.jsx`
- `frontend/src/pages/ActionDetails.jsx`

Explanation: Approved actions appear in cards, registry table, filters, search, and detail pages.

## Phase 8: UI Polish + Final Optimization

New files:
- `frontend/src/components/ActionCard.jsx`
- `frontend/src/components/ConfidenceBadge.jsx`
- `frontend/src/components/EvidenceAccordion.jsx`
- `frontend/src/components/Filters.jsx`
- `frontend/src/components/StateBlock.jsx`
- `frontend/src/components/WorkflowTracker.jsx`
- `frontend/src/styles/global.css`

Explanation: The UI includes responsive navigation, workflow tracking, loading states, empty states, error states, badges, accordions, modals, tables, and accessible contrast.

## Common Errors + Fixes

- `ModuleNotFoundError: app`: run backend commands from the `backend` folder.
- OCR returns empty text: install Tesseract OCR and ensure it is on PATH.
- CORS errors: confirm FastAPI is running on `http://127.0.0.1:8000` and Vite on `http://localhost:5173`.
- Frontend cannot connect: create `frontend/.env` with `VITE_API_BASE_URL=http://127.0.0.1:8000` if using a different backend URL.
- SQLite table issues after changing models: delete `backend/nyaypath.db` during development and restart the backend.

