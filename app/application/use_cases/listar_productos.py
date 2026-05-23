from app.application.dtos.catalogo import ProductoListado
from app.application.services.foto_url import resolver_url_foto
from app.application.settings.imagenes import PLACEHOLDER_FOTO_PRODUCTO
from app.domain.repositories.producto_repository import ProductoRepository


class ListarProductosUseCase:
    def __init__(self, repository: ProductoRepository) -> None:
        self._repository = repository

    def ejecutar(self) -> list[ProductoListado]:
        productos = self._repository.listar_todos()
        resultado: list[ProductoListado] = []
        for producto in productos:
            if producto.id is None:
                continue
            resultado.append(
                ProductoListado(
                    id=producto.id,
                    nombre=producto.nombre,
                    descripcion=producto.descripcion,
                    precio=producto.precio,
                    foto=resolver_url_foto(producto.foto, PLACEHOLDER_FOTO_PRODUCTO),
                )
            )
        return resultado
