import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.use_cases.limpiar_carritos_expirados import LimpiarCarritosExpiradosUseCase
from app.infrastructure.database.config import (
    CART_CLEANUP_INTERVAL_SECONDS,
    CORS_ORIGINS,
    DOCS_AUTH_ENABLED,
    DOCS_PASSWORD,
    DOCS_USER,
)
from app.infrastructure.database.session import SessionLocal, init_db
from app.infrastructure.repositories.sql_carrito_repository import SqlCarritoRepository
from app.presentation.api.carritos_router import router as carritos_router
from app.presentation.api.productos_router import router as productos_router
from app.presentation.api.trabajadores_router import router as trabajadores_router
from app.presentation.middleware.docs_basic_auth import DocsBasicAuthMiddleware


def _limpiar_carritos_expirados_sync() -> None:
    db = SessionLocal()
    try:
        LimpiarCarritosExpiradosUseCase(SqlCarritoRepository(db)).ejecutar()
    finally:
        db.close()


async def _tarea_limpieza_carritos() -> None:
    while True:
        await asyncio.sleep(CART_CLEANUP_INTERVAL_SECONDS)
        await asyncio.to_thread(_limpiar_carritos_expirados_sync)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    await asyncio.to_thread(_limpiar_carritos_expirados_sync)
    tarea = asyncio.create_task(_tarea_limpieza_carritos())
    yield
    tarea.cancel()
    with suppress(asyncio.CancelledError):
        await tarea


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
app.include_router(carritos_router)


@app.get("/")
def root():
    return {"message": "API funcionando"}
