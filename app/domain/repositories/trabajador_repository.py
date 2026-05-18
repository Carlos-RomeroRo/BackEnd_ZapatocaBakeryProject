from abc import ABC, abstractmethod

from app.domain.entities.trabajador import Trabajador


class TrabajadorRepository(ABC):
    @abstractmethod
    def guardar(self, trabajador: Trabajador) -> Trabajador:
        """Persiste un trabajador y devuelve la entidad con id asignado."""

    @abstractmethod
    def guardar_muchos(self, trabajadores: list[Trabajador]) -> list[Trabajador]:
        """Persiste varios trabajadores (cargue masivo)."""

    @abstractmethod
    def obtener_por_id(self, trabajador_id: int) -> Trabajador | None:
        pass

    @abstractmethod
    def obtener_por_documento(self, documento: str) -> Trabajador | None:
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Trabajador | None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Trabajador]:
        pass

    @abstractmethod
    def existe_por_documento(self, documento: str) -> bool:
        pass

    @abstractmethod
    def existe_por_email(self, email: str) -> bool:
        pass
