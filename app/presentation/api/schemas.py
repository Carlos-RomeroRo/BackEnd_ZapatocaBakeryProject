from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class FilaErrorSchema(BaseModel):
    fila: int
    motivo: str


class ImportarExcelResponse(BaseModel):
    insertados: int
    errores: list[FilaErrorSchema] = Field(default_factory=list)


class AgregarItemCarritoRequest(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto en catálogo")
    cantidad: int = Field(..., gt=0, description="Cantidad a agregar (entero mayor a 0)")

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre del producto es obligatorio")
        return value.strip()


class ItemCarritoLineaSchema(BaseModel):
    producto_id: int
    nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal


class CarritoResponse(BaseModel):
    carrito_id: str
    estado: str
    items: list[ItemCarritoLineaSchema] = Field(default_factory=list)
    total_productos: Decimal
    expira_en: datetime | None = None


class CrearCarritoResponse(CarritoResponse):
    token_acceso: str = Field(
        ...,
        description="Guardar en el cliente; obligatorio en header X-Carrito-Token",
    )
