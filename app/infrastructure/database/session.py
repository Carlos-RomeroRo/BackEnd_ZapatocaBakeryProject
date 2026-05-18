from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.base import Base
from app.infrastructure.database.config import DATABASE_URL
from app.infrastructure.database import models  # noqa: F401 — registra tablas en metadata

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def _migrate_trabajadores_descripcion() -> None:
    inspector = inspect(engine)
    if "trabajadores" not in inspector.get_table_names():
        return
    columnas = {col["name"] for col in inspector.get_columns("trabajadores")}
    if "descripcion" in columnas:
        return
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE trabajadores ADD COLUMN descripcion "
                "VARCHAR(100) NOT NULL DEFAULT ''"
            )
        )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _migrate_trabajadores_descripcion()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
