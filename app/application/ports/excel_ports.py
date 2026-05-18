from abc import ABC, abstractmethod
from typing import Any


class ProductoExcelPort(ABC):
    @abstractmethod
    def leer_filas(self, contenido: bytes) -> list[dict[str, Any]]:
        """Lee un .xlsx y devuelve una fila por registro (sin número de fila)."""

    @abstractmethod
    def generar_plantilla(self) -> bytes:
        """Excel vacío con encabezados y una fila de ejemplo."""

    @abstractmethod
    def generar_exportacion(self, filas: list[dict[str, Any]]) -> bytes:
        """Excel con los datos indicados."""


class TrabajadorExcelPort(ABC):
    @abstractmethod
    def leer_filas(self, contenido: bytes) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def generar_plantilla(self) -> bytes:
        pass

    @abstractmethod
    def generar_exportacion(self, filas: list[dict[str, Any]]) -> bytes:
        pass
