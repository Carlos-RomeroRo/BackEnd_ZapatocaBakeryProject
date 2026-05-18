from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class CarritoModel(Base):
    __tablename__ = "carritos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    token_acceso: Mapped[str] = mapped_column(String(64), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activo")
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expira_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    items: Mapped[list["CarritoItemModel"]] = relationship(
        back_populates="carrito",
        cascade="all, delete-orphan",
    )


class CarritoItemModel(Base):
    __tablename__ = "carrito_items"
    __table_args__ = (
        UniqueConstraint("carrito_id", "producto_id", name="uq_carrito_producto"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    carrito_id: Mapped[str] = mapped_column(
        ForeignKey("carritos.id", ondelete="CASCADE"), nullable=False
    )
    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    carrito: Mapped["CarritoModel"] = relationship(back_populates="items")
    producto: Mapped["ProductoModel"] = relationship()
