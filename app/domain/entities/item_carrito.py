from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ItemCarrito:
    producto_id: int
    cantidad: int
    nombre: str = ""
    precio_unitario: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad
