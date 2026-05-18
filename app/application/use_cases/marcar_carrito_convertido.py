from app.domain.entities.carrito import Carrito
from app.domain.repositories.carrito_repository import CarritoRepository


class MarcarCarritoConvertidoUseCase:
    """Usar al confirmar un pedido para cerrar el carrito."""

    def __init__(self, carrito_repository: CarritoRepository) -> None:
        self._carrito_repository = carrito_repository

    def ejecutar(self, carrito_id: str, token_acceso: str) -> Carrito:
        return self._carrito_repository.marcar_convertido(carrito_id, token_acceso)
