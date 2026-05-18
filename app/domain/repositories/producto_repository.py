from abc import ABC, abstractmethod

from app.domain.entities.producto import Producto


class ProductoRepository(ABC):
    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """Persiste un producto y devuelve la entidad con id asignado."""

    @abstractmethod
    def guardar_muchos(self, productos: list[Producto]) -> list[Producto]:
        """Persiste varios productos (cargue masivo)."""

    @abstractmethod
    def obtener_por_id(self, producto_id: int) -> Producto | None:
        pass

    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Producto | None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Producto]:
        pass

    @abstractmethod
    def existe_por_nombre(self, nombre: str) -> bool:
        pass
