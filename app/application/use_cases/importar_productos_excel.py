from decimal import Decimal, InvalidOperation
from typing import Any

from app.application.dtos.import_result import FilaError, ImportarExcelResultado
from app.application.ports.excel_ports import ProductoExcelPort
from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository


class ImportarProductosExcelUseCase:
    def __init__(
        self,
        excel: ProductoExcelPort,
        repository: ProductoRepository,
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
                producto = self._fila_a_producto(fila)
                if self._repository.existe_por_nombre(producto.nombre):
                    resultado.errores.append(
                        FilaError(
                            fila=numero_fila,
                            motivo=f"Ya existe un producto con nombre '{producto.nombre}'.",
                        )
                    )
                    continue
                self._repository.guardar(producto)
                resultado.insertados += 1
            except ValueError as exc:
                resultado.errores.append(FilaError(fila=numero_fila, motivo=str(exc)))

        return resultado

    def _fila_a_producto(self, fila: dict[str, Any]) -> Producto:
        precio_raw = fila.get("precio", "")
        if precio_raw == "" or precio_raw is None:
            raise ValueError("El precio es obligatorio")
        try:
            precio = Decimal(str(precio_raw))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("El precio debe ser un número válido") from exc

        foto = fila.get("foto", "")
        return Producto(
            nombre=str(fila.get("nombre", "")),
            descripcion=str(fila.get("descripcion", "")),
            precio=precio,
            tipo=str(fila.get("tipo", "")),
            foto=str(foto) if foto is not None else "",
        )
