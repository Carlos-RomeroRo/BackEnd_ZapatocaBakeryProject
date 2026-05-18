from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.entities.trabajador import Trabajador
from app.domain.repositories.trabajador_repository import TrabajadorRepository
from app.infrastructure.database.models import TrabajadorModel
from app.infrastructure.repositories.mappers import trabajador_to_entity, trabajador_to_model


class SqlTrabajadorRepository(TrabajadorRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(self, trabajador: Trabajador) -> Trabajador:
        if trabajador.id is not None:
            model = self._session.get(TrabajadorModel, trabajador.id)
            if model is None:
                raise ValueError(f"Trabajador con id {trabajador.id} no encontrado")
            model.nombre = trabajador.nombre
            model.descripcion = trabajador.descripcion
            model.rol = trabajador.rol
            model.documento = trabajador.documento.strip() or None
            model.email = trabajador.email.strip() or None
            model.foto = trabajador.foto or ""
        else:
            model = trabajador_to_model(trabajador)
            model.id = None
            self._session.add(model)

        self._commit()
        self._session.refresh(model)
        return trabajador_to_entity(model)

    def _commit(self) -> None:
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ValueError("Conflicto al guardar en base de datos.") from exc

    def guardar_muchos(self, trabajadores: list[Trabajador]) -> list[Trabajador]:
        models = []
        for trabajador in trabajadores:
            model = trabajador_to_model(trabajador)
            model.id = None
            models.append(model)
            self._session.add(model)

        self._commit()
        for model in models:
            self._session.refresh(model)
        return [trabajador_to_entity(model) for model in models]

    def obtener_por_id(self, trabajador_id: int) -> Trabajador | None:
        model = self._session.get(TrabajadorModel, trabajador_id)
        return trabajador_to_entity(model) if model else None

    def obtener_por_documento(self, documento: str) -> Trabajador | None:
        documento = documento.strip()
        if not documento:
            return None
        stmt = select(TrabajadorModel).where(TrabajadorModel.documento == documento)
        model = self._session.scalars(stmt).first()
        return trabajador_to_entity(model) if model else None

    def obtener_por_email(self, email: str) -> Trabajador | None:
        email = email.strip()
        if not email:
            return None
        stmt = select(TrabajadorModel).where(TrabajadorModel.email == email)
        model = self._session.scalars(stmt).first()
        return trabajador_to_entity(model) if model else None

    def listar_todos(self) -> list[Trabajador]:
        stmt = select(TrabajadorModel).order_by(TrabajadorModel.nombre)
        models = self._session.scalars(stmt).all()
        return [trabajador_to_entity(model) for model in models]

    def existe_por_documento(self, documento: str) -> bool:
        return self.obtener_por_documento(documento) is not None

    def existe_por_email(self, email: str) -> bool:
        return self.obtener_por_email(email) is not None
