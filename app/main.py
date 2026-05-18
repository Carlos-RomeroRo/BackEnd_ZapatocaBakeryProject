from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database.config import (
    CORS_ORIGINS,
    DOCS_AUTH_ENABLED,
    DOCS_PASSWORD,
    DOCS_USER,
)
from app.infrastructure.database.session import init_db
from app.presentation.api.productos_router import router as productos_router
from app.presentation.api.trabajadores_router import router as trabajadores_router
from app.presentation.middleware.docs_basic_auth import DocsBasicAuthMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Panadería Zapatoca API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if DOCS_AUTH_ENABLED:
    app.add_middleware(
        DocsBasicAuthMiddleware,
        username=DOCS_USER,
        password=DOCS_PASSWORD,
        enabled=True,
    )

app.include_router(productos_router)
app.include_router(trabajadores_router)


@app.get("/")
def root():
    return {"message": "API funcionando"}
