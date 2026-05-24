from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class TrabajadorListado:
    id: int
    nombre: str
    descripcion: str
    rol: str
    foto: str


@dataclass(frozen=True)
class ProductoListado:
    id: int
    nombre: str
    descripcion: str
    precio: Decimal
    tipo: str
    tipo_etiqueta: str
    foto: str
