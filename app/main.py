from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database.config import CORS_ORIGINS
from app.infrastructure.database.session import init_db
from app.presentation.api.productos_router import router as productos_router
from app.presentation.api.trabajadores_router import router as trabajadores_router


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

app.include_router(productos_router)
app.include_router(trabajadores_router)


@app.get("/")
def root():
    return {"message": "API funcionando"}
