from typing import Any

from app.application.dtos.import_result import FilaError, ImportarExcelResultado
from app.application.ports.excel_ports import TrabajadorExcelPort
from app.domain.entities.trabajador import Trabajador
from app.domain.repositories.trabajador_repository import TrabajadorRepository


class ImportarTrabajadoresExcelUseCase:
    def __init__(
        self,
        excel: TrabajadorExcelPort,
        repository: TrabajadorRepository,
    ) -> None:
        self._excel = excel
        self._repository = repository

    def ejecutar(self, contenido: bytes) -> ImportarExcelResultado:
        filas = self._excel.leer_filas(contenido)
        resultado = ImportarExcelResultado()

        if not filas:
            resultado.errores.append(
                FilaError(fila=0, motivo="No hay filas con datos para importar.")
            )
            return resultado

        for indice, fila in enumerate(filas, start=2):
            numero_fila = indice
            try:
                trabajador = self._fila_a_trabajador(fila)
                if self._es_duplicado(trabajador):
                    resultado.errores.append(
                        FilaError(
                            fila=numero_fila,
                            motivo="Ya existe un trabajador con ese documento o email.",
                        )
                    )
                    continue
                self._repository.guardar(trabajador)
                resultado.insertados += 1
            except ValueError as exc:
                resultado.errores.append(FilaError(fila=numero_fila, motivo=str(exc)))

        return resultado

    def _es_duplicado(self, trabajador: Trabajador) -> bool:
        if trabajador.documento and self._repository.existe_por_documento(
            trabajador.documento
        ):
            return True
        if trabajador.email and self._repository.existe_por_email(trabajador.email):
            return True
        return False

    def _fila_a_trabajador(self, fila: dict[str, Any]) -> Trabajador:
        documento = fila.get("documento", "")
        email = fila.get("email", "")
        foto = fila.get("foto", "")
        return Trabajador(
            nombre=str(fila.get("nombre", "")),
            descripcion=str(fila.get("descripcion", "")),
            rol=str(fila.get("rol", "")),
            documento=str(documento) if documento is not None else "",
            email=str(email) if email is not None else "",
            foto=str(foto) if foto is not None else "",
        )
