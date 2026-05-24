import re
import unicodedata
from io import BytesIO
from typing import Any

import pandas as pd


def _sin_tildes(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def normalizar_columnas(columnas: list[str]) -> list[str]:
    resultado: list[str] = []
    for columna in columnas:
        nombre = _sin_tildes(str(columna).strip().lower())
        nombre = re.sub(r"\s+", "_", nombre)
        resultado.append(nombre)
    return resultado


def leer_dataframe(contenido: bytes, columnas_requeridas: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_excel(BytesIO(contenido), engine="openpyxl")
    except Exception as exc:
        raise ValueError("No se pudo leer el archivo Excel. Use formato .xlsx válido.") from exc

    if df.empty:
        raise ValueError("El archivo Excel no contiene filas de datos.")

    df.columns = normalizar_columnas(list(df.columns))
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    if faltantes:
        raise ValueError(
            f"Faltan columnas obligatorias: {', '.join(faltantes)}. "
            f"Se esperan: {', '.join(columnas_requeridas)}"
        )

    return df[columnas_requeridas].copy()


def dataframe_a_filas(df: pd.DataFrame) -> list[dict[str, Any]]:
    filas: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        if row.isna().all():
            continue
        fila = {col: _celda_a_python(row[col]) for col in df.columns}
        if not str(fila.get("nombre", "")).strip() and all(
            v in (None, "", 0) for k, v in fila.items() if k != "nombre"
        ):
            continue
        filas.append(fila)
    return filas


def _celda_a_python(valor: Any) -> Any:
    if pd.isna(valor):
        return ""
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    return valor


def escribir_excel(filas: list[dict[str, Any]], columnas: list[str]) -> bytes:
    df = pd.DataFrame(filas, columns=columnas)
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer.getvalue()
