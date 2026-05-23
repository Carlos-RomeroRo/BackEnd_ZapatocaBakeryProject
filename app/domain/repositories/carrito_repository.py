from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from app.domain.entities.carrito import Carrito


class CarritoRepository(ABC):
    @abstractmethod
    def crear(self) -> Carrito:
        """Crea un carrito vacío con token de acceso y fecha de expiración."""

    @abstractmethod
    def obtener_por_id(self, carrito_id: str, token_acceso: str) -> Carrito | None:
        pass

    @abstractmethod
    def agregar_item(
        self,
        carrito_id: str,
        token_acceso: str,
        producto_id: int,
        cantidad: int,
        precio_unitario: Decimal,
    ) -> Carrito:
        """Agrega cantidad al ítem existente o crea una nueva línea con precio fijado."""

    @abstractmethod
    def eliminar_item(
        self, carrito_id: str, token_acceso: str, producto_id: int
    ) -> Carrito:
        """Elimina la línea del producto del carrito."""

    @abstractmethod
    def marcar_convertido(self, carrito_id: str, token_acceso: str) -> Carrito:
        """Marca el carrito como convertido en pedido (deja de aceptar cambios)."""

    @abstractmethod
    def eliminar_carritos_activos_expirados(self, ahora: datetime | None = None) -> int:
        """Elimina carritos activos cuya expiración ya pasó. Devuelve cantidad eliminada."""
