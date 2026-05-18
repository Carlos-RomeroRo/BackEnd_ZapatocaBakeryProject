from app.domain.entities.carrito import Carrito
from app.domain.repositories.carrito_repository import CarritoRepository


class CrearCarritoUseCase:
    def __init__(self, carrito_repository: CarritoRepository) -> None:
        self._carrito_repository = carrito_repository

    def ejecutar(self) -> Carrito:
        return self._carrito_repository.crear()
