from app.application.dtos.catalogo import TrabajadorListado
from app.application.services.foto_url import resolver_url_foto
from app.application.settings.imagenes import PLACEHOLDER_FOTO_TRABAJADOR
from app.domain.repositories.trabajador_repository import TrabajadorRepository


class ListarTrabajadoresUseCase:
    def __init__(self, repository: TrabajadorRepository) -> None:
        self._repository = repository

    def ejecutar(self) -> list[TrabajadorListado]:
        trabajadores = self._repository.listar_todos()
        resultado: list[TrabajadorListado] = []
        for trabajador in trabajadores:
            if trabajador.id is None:
                continue
            resultado.append(
                TrabajadorListado(
                    id=trabajador.id,
                    nombre=trabajador.nombre,
                    descripcion=trabajador.descripcion,
                    rol=trabajador.rol,
                    foto=resolver_url_foto(trabajador.foto, PLACEHOLDER_FOTO_TRABAJADOR),
                )
            )
        return resultado
