from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class LineaProductoCarrito:
    producto_id: int
    nombre: str
    precio_unitario: Decimal
    cantidad: int
    precio_total: Decimal


@dataclass(frozen=True)
class ResumenCarrito:
    carrito_id: str
    estado: str
    productos: list[LineaProductoCarrito]
    total_compra: Decimal
    expira_en: datetime | None = None
