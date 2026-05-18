from app.domain.entities.carrito import Carrito
from app.domain.repositories.carrito_repository import CarritoRepository


class ObtenerCarritoUseCase:
    def __init__(self, carrito_repository: CarritoRepository) -> None:
        self._carrito_repository = carrito_repository

    def ejecutar(self, carrito_id: str, token_acceso: str) -> Carrito | None:
        return self._carrito_repository.obtener_por_id(carrito_id, token_acceso)
