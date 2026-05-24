from app.application.ports.excel_ports import ProductoExcelPort
from app.domain.value_objects.tipo_producto import ETIQUETAS_TIPO
from app.domain.repositories.producto_repository import ProductoRepository


class ExportarProductosExcelUseCase:
    def __init__(
        self,
        excel: ProductoExcelPort,
        repository: ProductoRepository,
    ) -> None:
        self._excel = excel
        self._repository = repository

    def ejecutar_plantilla(self) -> bytes:
        return self._excel.generar_plantilla()

    def ejecutar_exportacion(self) -> bytes:
        productos = self._repository.listar_todos()
        filas = [
            {
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "precio": float(p.precio),
                "tipo": ETIQUETAS_TIPO.get(p.tipo, p.tipo),
                "foto": p.foto,
            }
            for p in productos
        ]
        return self._excel.generar_exportacion(filas)
