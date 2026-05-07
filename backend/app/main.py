from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.actions import router as actions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nyayapath-pied.vercel.app"
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

app.include_router(actions_router)
