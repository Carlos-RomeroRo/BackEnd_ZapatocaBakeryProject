from typing import Any

from app.application.ports.excel_ports import TrabajadorExcelPort
from app.infrastructure.excel._utils import (
    dataframe_a_filas,
    escribir_excel,
    leer_dataframe,
)

COLUMNAS = ["nombre", "descripcion", "documento", "email", "rol", "foto"]

FILA_EJEMPLO = {
    "nombre": "Ana García",
    "descripcion": "Atención al cliente en caja",
    "documento": "12345678",
    "email": "ana@panaderia.com",
    "rol": "Cajera",
    "foto": "",
}


class PandasTrabajadorExcelService(TrabajadorExcelPort):
    def leer_filas(self, contenido: bytes) -> list[dict[str, Any]]:
        df = leer_dataframe(contenido, COLUMNAS)
        return dataframe_a_filas(df)

    def generar_plantilla(self) -> bytes:
        return escribir_excel([FILA_EJEMPLO], COLUMNAS)

    def generar_exportacion(self, filas: list[dict[str, Any]]) -> bytes:
        normalizadas = [
            {
                "nombre": f.get("nombre", ""),
                "descripcion": f.get("descripcion", ""),
                "documento": f.get("documento", ""),
                "email": f.get("email", ""),
                "rol": f.get("rol", ""),
                "foto": f.get("foto", ""),
            }
            for f in filas
        ]
        return escribir_excel(normalizadas, COLUMNAS)
