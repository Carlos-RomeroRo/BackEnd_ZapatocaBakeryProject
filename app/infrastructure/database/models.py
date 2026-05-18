from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    foto: Mapped[str] = mapped_column(String(500), nullable=False, default="")


class TrabajadorModel(Base):
    __tablename__ = "trabajadores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    rol: Mapped[str] = mapped_column(String(100), nullable=False)
    documento: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    foto: Mapped[str] = mapped_column(String(500), nullable=False, default="")
