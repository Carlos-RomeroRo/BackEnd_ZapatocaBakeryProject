from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class FilaErrorSchema(BaseModel):
    fila: int
    motivo: str


class ImportarExcelResponse(BaseModel):
    insertados: int
    errores: list[FilaErrorSchema] = Field(default_factory=list)


class EliminarItemCarritoRequest(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto a quitar del carrito")

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre del producto es obligatorio")
        return value.strip()


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


class ProductoCarritoResumenSchema(BaseModel):
    producto_id: int
    nombre: str
    precio_unitario: Decimal = Field(..., description="Precio por unidad")
    cantidad: int = Field(..., description="Cantidad pedida")
    precio_total: Decimal = Field(
        ..., description="Precio total de la línea (unitario × cantidad)"
    )


class ResumenCarritoResponse(BaseModel):
    carrito_id: str
    estado: str
    productos: list[ProductoCarritoResumenSchema] = Field(
        default_factory=list,
        description="Lista de productos en el carrito",
    )
    total_compra: Decimal = Field(
        ..., description="Precio total de la compra (suma de líneas)"
    )
    expira_en: datetime | None = None


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


class TrabajadorListadoSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str
    rol: str
    foto: str = Field(..., description="URL pública de la imagen")


class TipoProductoSchema(BaseModel):
    id: str = Field(..., description="Identificador para filtros (ej. panes)")
    nombre: str = Field(..., description="Etiqueta visible en el clasificador")


class ProductoListadoSchema(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: Decimal
    tipo: str
    tipo_etiqueta: str
    foto: str = Field(..., description="URL pública de la imagen")
