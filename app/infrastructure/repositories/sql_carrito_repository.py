import secrets
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.domain.entities.carrito import Carrito, ESTADO_ACTIVO, ESTADO_CONVERTIDO
from app.domain.repositories.carrito_repository import CarritoRepository
from app.infrastructure.database.config import CART_TTL_MINUTES
from app.infrastructure.database.models import CarritoItemModel, CarritoModel
from app.infrastructure.repositories.mappers import carrito_to_entity


class CarritoExpiradoError(Exception):
    pass


class CarritoTokenInvalidoError(Exception):
    pass


class SqlCarritoRepository(CarritoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def crear(self) -> Carrito:
        ahora = datetime.now(timezone.utc)
        model = CarritoModel(
            id=str(uuid.uuid4()),
            token_acceso=secrets.token_urlsafe(32),
            estado=ESTADO_ACTIVO,
            expira_en=ahora + timedelta(minutes=CART_TTL_MINUTES),
        )
        self._session.add(model)
        self._commit()
        self._session.refresh(model)
        return carrito_to_entity(model, incluir_token=True)

    def obtener_por_id(self, carrito_id: str, token_acceso: str) -> Carrito | None:
        model = self._cargar_carrito(carrito_id)
        if model is None:
            return None
        try:
            self._validar_acceso(model, token_acceso)
        except (CarritoTokenInvalidoError, CarritoExpiradoError):
            raise
        return carrito_to_entity(model)

    def agregar_item(
        self,
        carrito_id: str,
        token_acceso: str,
        producto_id: int,
        cantidad: int,
        precio_unitario: Decimal,
    ) -> Carrito:
        model = self._cargar_carrito(carrito_id)
        if model is None:
            raise ValueError(f"Carrito con id {carrito_id} no encontrado")

        self._validar_acceso(model, token_acceso)
        if model.estado != ESTADO_ACTIVO:
            raise ValueError("El carrito ya no está activo.")

        item_existente = next(
            (item for item in model.items if item.producto_id == producto_id),
            None,
        )
        if item_existente:
            item_existente.cantidad += cantidad
        else:
            self._session.add(
                CarritoItemModel(
                    carrito_id=carrito_id,
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                )
            )

        self._commit()
        model = self._cargar_carrito(carrito_id)
        if model is None:
            raise ValueError(f"Carrito con id {carrito_id} no encontrado")
        return carrito_to_entity(model)

    def eliminar_item(
        self, carrito_id: str, token_acceso: str, producto_id: int
    ) -> Carrito:
        model = self._cargar_carrito(carrito_id)
        if model is None:
            raise ValueError(f"Carrito con id {carrito_id} no encontrado")

        self._validar_acceso(model, token_acceso)
        if model.estado != ESTADO_ACTIVO:
            raise ValueError("El carrito ya no está activo.")

        item = next(
            (linea for linea in model.items if linea.producto_id == producto_id),
            None,
        )
        if item is None:
            raise LookupError("El producto no está en el carrito.")

        self._session.delete(item)
        self._commit()

        model = self._cargar_carrito(carrito_id)
        if model is None:
            raise ValueError(f"Carrito con id {carrito_id} no encontrado")
        return carrito_to_entity(model)

    def marcar_convertido(self, carrito_id: str, token_acceso: str) -> Carrito:
        model = self._cargar_carrito(carrito_id)
        if model is None:
            raise ValueError(f"Carrito con id {carrito_id} no encontrado")

        self._validar_acceso(model, token_acceso)
        if model.estado == ESTADO_CONVERTIDO:
            return carrito_to_entity(model)

        model.estado = ESTADO_CONVERTIDO
        self._commit()
        self._session.refresh(model)
        return carrito_to_entity(model)

    def eliminar_carritos_activos_expirados(
        self, ahora: datetime | None = None
    ) -> int:
        momento = ahora or datetime.now(timezone.utc)
        stmt = delete(CarritoModel).where(
            CarritoModel.estado == ESTADO_ACTIVO,
            CarritoModel.expira_en < momento,
        )
        resultado = self._session.execute(stmt)
        self._session.commit()
        return resultado.rowcount or 0

    def _validar_acceso(self, model: CarritoModel, token_acceso: str) -> None:
        if not secrets.compare_digest(model.token_acceso, token_acceso):
            raise CarritoTokenInvalidoError("Token de carrito inválido.")

        if model.estado == ESTADO_ACTIVO and self._esta_expirado(model):
            self._session.delete(model)
            self._session.commit()
            raise CarritoExpiradoError(
                "El carrito expiró por inactividad. Cree uno nuevo para continuar."
            )

    def _esta_expirado(self, model: CarritoModel) -> bool:
        expira = model.expira_en
        if expira.tzinfo is None:
            expira = expira.replace(tzinfo=timezone.utc)
        return expira < datetime.now(timezone.utc)

    def _cargar_carrito(self, carrito_id: str) -> CarritoModel | None:
        stmt = (
            select(CarritoModel)
            .where(CarritoModel.id == carrito_id)
            .options(
                selectinload(CarritoModel.items).selectinload(CarritoItemModel.producto)
            )
        )
        return self._session.scalars(stmt).first()

    def _commit(self) -> None:
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ValueError("Conflicto al guardar el carrito en base de datos.") from exc
