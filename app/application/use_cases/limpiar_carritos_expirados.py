from app.domain.repositories.carrito_repository import CarritoRepository


class LimpiarCarritosExpiradosUseCase:
    def __init__(self, carrito_repository: CarritoRepository) -> None:
        self._carrito_repository = carrito_repository

    def ejecutar(self) -> int:
        return self._carrito_repository.eliminar_carritos_activos_expirados()
