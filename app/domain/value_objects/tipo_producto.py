import re
import unicodedata

TIPO_PANES = "panes"
TIPO_REPOSTERIA = "reposteria"
TIPO_COMIDAS_RAPIDAS = "comidas_rapidas"
TIPO_OTROS = "otros"

TIPOS_PRODUCTO: tuple[str, ...] = (
    TIPO_PANES,
    TIPO_REPOSTERIA,
    TIPO_COMIDAS_RAPIDAS,
    TIPO_OTROS,
)

ETIQUETAS_TIPO: dict[str, str] = {
    TIPO_PANES: "Panes",
    TIPO_REPOSTERIA: "Reposteria",
    TIPO_COMIDAS_RAPIDAS: "Comidas rapidas",
    TIPO_OTROS: "Otros",
}

_ALIASES_TIPO: dict[str, str] = {
    "pan": TIPO_PANES,
    "panes": TIPO_PANES,
    "reposteria": TIPO_REPOSTERIA,
    "repostería": TIPO_REPOSTERIA,
    "pasteleria": TIPO_REPOSTERIA,
    "pastelería": TIPO_REPOSTERIA,
    "comida rapida": TIPO_COMIDAS_RAPIDAS,
    "comidas rapidas": TIPO_COMIDAS_RAPIDAS,
    "comidas_rapidas": TIPO_COMIDAS_RAPIDAS,
    "comida rápida": TIPO_COMIDAS_RAPIDAS,
    "comidas rápidas": TIPO_COMIDAS_RAPIDAS,
    "otro": TIPO_OTROS,
    "otros": TIPO_OTROS,
}


def _sin_tildes(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def normalizar_tipo_producto(valor: str) -> str:
    clave = _sin_tildes(str(valor or "").strip().lower())
    clave = re.sub(r"[-_]+", " ", clave)
    clave = re.sub(r"\s+", " ", clave)
    if not clave:
        raise ValueError("El tipo de producto es obligatorio")
    if clave in _ALIASES_TIPO:
        return _ALIASES_TIPO[clave]
    opciones = ", ".join(ETIQUETAS_TIPO[t] for t in TIPOS_PRODUCTO)
    raise ValueError(
        f"Tipo '{valor}' no válido. Use uno de: {opciones}"
    )


def es_tipo_producto_valido(tipo: str) -> bool:
    return tipo in TIPOS_PRODUCTO
