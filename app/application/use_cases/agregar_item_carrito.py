from app.domain.entities.carrito import Carrito, ESTADO_ACTIVO
from app.domain.repositories.carrito_repository import CarritoRepository
from app.domain.repositories.producto_repository import ProductoRepository


class AgregarItemCarritoUseCase:
    def __init__(
        self,
        carrito_repository: CarritoRepository,
        producto_repository: ProductoRepository,
    ) -> None:
        self._carrito_repository = carrito_repository
        self._producto_repository = producto_repository

    def ejecutar(
        self,
        carrito_id: str,
        token_acceso: str,
        nombre_producto: str,
        cantidad: int,
    ) -> Carrito:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        nombre = nombre_producto.strip()
        if not nombre:
            raise ValueError("El nombre del producto es obligatorio")

        producto = self._producto_repository.obtener_por_nombre(nombre)
        if producto is None:
            raise LookupError(f"No existe un producto con nombre '{nombre}'.")

        if producto.id is None:
            raise ValueError("El producto no tiene identificador válido.")

        carrito = self._carrito_repository.obtener_por_id(carrito_id, token_acceso)
        if carrito is None:
            raise LookupError(f"No existe un carrito con id '{carrito_id}'.")

        if carrito.estado != ESTADO_ACTIVO:
            raise ValueError("El carrito ya no está activo.")

        return self._carrito_repository.agregar_item(
            carrito_id,
            token_acceso,
            producto.id,
            cantidad,
            producto.precio,
        )
