from typing import Any

from app.application.ports.excel_ports import ProductoExcelPort
from app.infrastructure.excel._utils import (
    dataframe_a_filas,
    escribir_excel,
    leer_dataframe,
)

COLUMNAS = ["nombre", "descripcion", "precio", "foto"]

FILA_EJEMPLO = {
    "nombre": "Pan integral",
    "descripcion": "Pan artesanal de masa madre",
    "precio": 3500,
    "foto": "https://ejemplo.com/pan.jpg",
}


class PandasProductoExcelService(ProductoExcelPort):
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
                "precio": f.get("precio", ""),
                "foto": f.get("foto", ""),
            }
            for f in filas
        ]
        return escribir_excel(normalizadas, COLUMNAS)
