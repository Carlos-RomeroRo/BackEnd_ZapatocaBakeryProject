from dataclasses import dataclass
from decimal import Decimal

MAX_DESCRIPCION = 100
MAX_FOTO_LONGITUD = 500


@dataclass
class Producto:
    nombre: str
    descripcion: str
    precio: Decimal
    foto: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar_nombre()
        self._validar_descripcion()
        self._validar_precio()
        self._validar_foto()

    def _validar_nombre(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del producto es obligatorio")
        self.nombre = self.nombre.strip()

    def _validar_descripcion(self) -> None:
        if self.descripcion is None:
            raise ValueError("La descripción es obligatoria")
        self.descripcion = self.descripcion.strip()
        if not self.descripcion:
            raise ValueError("La descripción es obligatoria")
        if len(self.descripcion) > MAX_DESCRIPCION:
            raise ValueError(
                f"La descripción no puede superar {MAX_DESCRIPCION} caracteres"
            )

    def _validar_precio(self) -> None:
        if not isinstance(self.precio, Decimal):
            self.precio = Decimal(str(self.precio))
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")

    def _validar_foto(self) -> None:
        if self.foto is None:
            self.foto = ""
            return
        self.foto = self.foto.strip()
        if not self.foto:
            return
        if len(self.foto) > MAX_FOTO_LONGITUD:
            raise ValueError("La URL o ruta de la foto es demasiado larga")
        if self.foto.startswith(("http://", "https://")):
            return
        if any(c in self.foto for c in ("\n", "\r", "\0")):
            raise ValueError("La ruta de la foto tiene un formato inválido")
