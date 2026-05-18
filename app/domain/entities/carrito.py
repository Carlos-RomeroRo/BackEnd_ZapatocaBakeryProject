from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domain.entities.item_carrito import ItemCarrito

ESTADO_ACTIVO = "activo"
ESTADO_CONVERTIDO = "convertido"


@dataclass
class Carrito:
    id: str
    items: list[ItemCarrito] = field(default_factory=list)
    estado: str = ESTADO_ACTIVO
    token_acceso: str = ""
    expira_en: datetime | None = None

    def total_productos(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0"))

    def esta_activo(self) -> bool:
        return self.estado == ESTADO_ACTIVO
