import secrets
from collections.abc import Generator
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.base import Base
from app.infrastructure.database.config import CART_TTL_MINUTES, DATABASE_URL
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


def _migrate_carritos_seguridad() -> None:
    inspector = inspect(engine)
    if "carritos" not in inspector.get_table_names():
        return

    columnas_carrito = {col["name"] for col in inspector.get_columns("carritos")}
    expira_default = (
        datetime.now(timezone.utc) + timedelta(minutes=CART_TTL_MINUTES)
    ).isoformat()

    with engine.begin() as conn:
        if "token_acceso" not in columnas_carrito:
            conn.execute(
                text(
                    "ALTER TABLE carritos ADD COLUMN token_acceso "
                    "VARCHAR(64) NOT NULL DEFAULT ''"
                )
            )
        if "expira_en" not in columnas_carrito:
            if DATABASE_URL.startswith("sqlite"):
                conn.execute(
                    text(
                        "ALTER TABLE carritos ADD COLUMN expira_en "
                        f"DATETIME NOT NULL DEFAULT '{expira_default}'"
                    )
                )
            else:
                conn.execute(
                    text(
                        "ALTER TABLE carritos ADD COLUMN expira_en "
                        "TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
                    )
                )

        filas = conn.execute(
            text("SELECT id FROM carritos WHERE token_acceso = '' OR token_acceso IS NULL")
        ).fetchall()
        for (carrito_id,) in filas:
            conn.execute(
                text("UPDATE carritos SET token_acceso = :token WHERE id = :id"),
                {"token": secrets.token_urlsafe(32), "id": carrito_id},
            )

    if "carrito_items" not in inspector.get_table_names():
        return

    columnas_items = {col["name"] for col in inspector.get_columns("carrito_items")}
    if "precio_unitario" not in columnas_items:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE carrito_items ADD COLUMN precio_unitario "
                    "NUMERIC(12, 2)"
                )
            )
            conn.execute(
                text(
                    """
                    UPDATE carrito_items
                    SET precio_unitario = (
                        SELECT precio FROM productos
                        WHERE productos.id = carrito_items.producto_id
                    )
                    WHERE precio_unitario IS NULL
                    """
                )
            )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _migrate_trabajadores_descripcion()
    _migrate_carritos_seguridad()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
