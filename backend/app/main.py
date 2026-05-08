from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nyayapath-pied.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "backend live"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/actions")
def actions(status: str | None = None):
    return [
        {
            "id": 1,
            "title": "Test Action",
            "status": status or "approved"
        }
    ]
