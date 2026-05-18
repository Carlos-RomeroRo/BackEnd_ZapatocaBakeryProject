from app.application.ports.excel_ports import TrabajadorExcelPort
from app.domain.repositories.trabajador_repository import TrabajadorRepository


class ExportarTrabajadoresExcelUseCase:
    def __init__(
        self,
        excel: TrabajadorExcelPort,
        repository: TrabajadorRepository,
    ) -> None:
        self._excel = excel
        self._repository = repository

    def ejecutar_plantilla(self) -> bytes:
        return self._excel.generar_plantilla()

    def ejecutar_exportacion(self) -> bytes:
        trabajadores = self._repository.listar_todos()
        filas = [
            {
                "nombre": t.nombre,
                "descripcion": t.descripcion,
                "documento": t.documento,
                "email": t.email,
                "rol": t.rol,
                "foto": t.foto,
            }
            for t in trabajadores
        ]
        return self._excel.generar_exportacion(filas)
