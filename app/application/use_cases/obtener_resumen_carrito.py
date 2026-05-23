from app.application.dtos.resumen_carrito import LineaProductoCarrito, ResumenCarrito
from app.domain.entities.carrito import Carrito
from app.domain.repositories.carrito_repository import CarritoRepository


class ObtenerResumenCarritoUseCase:
    """Lista productos del carrito con precios unitarios, cantidades y totales."""

    def __init__(self, carrito_repository: CarritoRepository) -> None:
        self._carrito_repository = carrito_repository

    def ejecutar(self, carrito_id: str, token_acceso: str) -> ResumenCarrito | None:
        carrito = self._carrito_repository.obtener_por_id(carrito_id, token_acceso)
        if carrito is None:
            return None
        return self._construir_resumen(carrito)

    @staticmethod
    def _construir_resumen(carrito: Carrito) -> ResumenCarrito:
        productos = [
            LineaProductoCarrito(
                producto_id=item.producto_id,
                nombre=item.nombre,
                precio_unitario=item.precio_unitario,
                cantidad=item.cantidad,
                precio_total=item.subtotal,
            )
            for item in carrito.items
        ]
        return ResumenCarrito(
            carrito_id=carrito.id,
            estado=carrito.estado,
            productos=productos,
            total_compra=carrito.total_productos(),
            expira_en=carrito.expira_en,
        )
