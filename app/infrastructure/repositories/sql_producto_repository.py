from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.producto import Producto
from app.domain.repositories.producto_repository import ProductoRepository
from app.infrastructure.database.models import ProductoModel
from app.infrastructure.repositories.mappers import producto_to_entity, producto_to_model


class SqlProductoRepository(ProductoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(self, producto: Producto) -> Producto:
        if producto.id is not None:
            model = self._session.get(ProductoModel, producto.id)
            if model is None:
                raise ValueError(f"Producto con id {producto.id} no encontrado")
            model.nombre = producto.nombre
            model.descripcion = producto.descripcion
            model.precio = producto.precio
            model.foto = producto.foto or ""
        else:
            model = producto_to_model(producto)
            model.id = None
            self._session.add(model)

        self._commit()
        self._session.refresh(model)
        return producto_to_entity(model)

    def _commit(self) -> None:
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ValueError("Conflicto al guardar en base de datos.") from exc

    def guardar_muchos(self, productos: list[Producto]) -> list[Producto]:
        models = []
        for producto in productos:
            model = producto_to_model(producto)
            model.id = None
            models.append(model)
            self._session.add(model)

        self._commit()
        for model in models:
            self._session.refresh(model)
        return [producto_to_entity(model) for model in models]

    def obtener_por_id(self, producto_id: int) -> Producto | None:
        model = self._session.get(ProductoModel, producto_id)
        return producto_to_entity(model) if model else None

    def obtener_por_nombre(self, nombre: str) -> Producto | None:
        nombre = nombre.strip()
        stmt = select(ProductoModel).where(
            func.lower(ProductoModel.nombre) == nombre.lower()
        )
        model = self._session.scalars(stmt).first()
        return producto_to_entity(model) if model else None

    def listar_todos(self) -> list[Producto]:
        stmt = select(ProductoModel).order_by(ProductoModel.nombre)
        models = self._session.scalars(stmt).all()
        return [producto_to_entity(model) for model in models]

    def existe_por_nombre(self, nombre: str) -> bool:
        return self.obtener_por_nombre(nombre) is not None
