import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config.settings import ALLOWED_HOSTS, ALLOWED_ORIGINS, APP_NAME, APP_VERSION, DEBUG
from app.database.session import Base, engine
from app.middleware.security import RequestContextMiddleware, SecurityHeadersMiddleware
from app.routes import actions, health, judgments

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI-assisted legal workflow API for judgment understanding and human-verified compliance actions.",
    version=APP_VERSION,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(judgments.router)
app.include_router(actions.router)
@app.get("/")
def root():
    return {"message": "backend live"}
