from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from .api.routes import api_router
from .models import base, books, users, loans  # Importer les modèles pour Alembic

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Mount the frontend folder
app.mount("/", StaticFiles(directory=os.path.join("frontend"), html=True), name="frontend")

# Configuration CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Inclusion des routes API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}