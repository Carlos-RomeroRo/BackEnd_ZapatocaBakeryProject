import re
from dataclasses import dataclass

MAX_DESCRIPCION = 100
MAX_FOTO_LONGITUD = 500
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Trabajador:
    nombre: str
    descripcion: str
    rol: str
    documento: str = ""
    email: str = ""
    foto: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar_nombre()
        self._validar_descripcion()
        self._validar_documento_o_email()
        self._validar_rol()
        self._validar_foto()

    def _validar_nombre(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del trabajador es obligatorio")
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

    def _validar_documento_o_email(self) -> None:
        self.documento = (self.documento or "").strip()
        self.email = (self.email or "").strip()

        if not self.documento and not self.email:
            raise ValueError("Debe indicar documento o email del trabajador")

        if self.email and not _EMAIL_PATTERN.match(self.email):
            raise ValueError("El email no tiene un formato válido")

    def _validar_rol(self) -> None:
        if not self.rol or not self.rol.strip():
            raise ValueError("El rol del trabajador es obligatorio")
        self.rol = self.rol.strip()

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
