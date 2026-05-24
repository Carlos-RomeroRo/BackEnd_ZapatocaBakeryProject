from app.application.dtos.catalogo import ProductoListado
from app.application.services.producto_listado_mapper import producto_a_listado
from app.domain.repositories.producto_repository import ProductoRepository
from app.domain.value_objects.tipo_producto import normalizar_tipo_producto


class ListarProductosPorTipoUseCase:
    def __init__(self, repository: ProductoRepository) -> None:
        self._repository = repository

    def ejecutar(self, tipo: str) -> list[ProductoListado]:
        tipo_normalizado = normalizar_tipo_producto(tipo)
        productos = self._repository.listar_por_tipo(tipo_normalizado)
        return [producto_a_listado(p) for p in productos if p.id is not None]
