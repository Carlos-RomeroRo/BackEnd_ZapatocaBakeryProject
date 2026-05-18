from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.application.use_cases.agregar_item_carrito import AgregarItemCarritoUseCase
from app.application.use_cases.crear_carrito import CrearCarritoUseCase
from app.application.use_cases.obtener_carrito import ObtenerCarritoUseCase
from app.domain.entities.carrito import Carrito
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sql_carrito_repository import (
    CarritoExpiradoError,
    CarritoTokenInvalidoError,
    SqlCarritoRepository,
)
from app.infrastructure.repositories.sql_producto_repository import SqlProductoRepository
from app.presentation.api.schemas import (
    AgregarItemCarritoRequest,
    CarritoResponse,
    CrearCarritoResponse,
    ItemCarritoLineaSchema,
)

router = APIRouter(prefix="/carritos", tags=["Carritos"])


def _carrito_a_response(
    carrito: Carrito, *, incluir_token: bool = False
) -> CarritoResponse | CrearCarritoResponse:
    items = [
        ItemCarritoLineaSchema(
            producto_id=item.producto_id,
            nombre=item.nombre,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=item.subtotal,
        )
        for item in carrito.items
    ]
    base = {
        "carrito_id": carrito.id,
        "estado": carrito.estado,
        "items": items,
        "total_productos": carrito.total_productos(),
        "expira_en": carrito.expira_en,
    }
    if incluir_token:
        return CrearCarritoResponse(**base, token_acceso=carrito.token_acceso)
    return CarritoResponse(**base)


def _manejar_errores_carrito(exc: Exception) -> HTTPException:
    if isinstance(exc, CarritoTokenInvalidoError):
        return HTTPException(status_code=403, detail=str(exc))
    if isinstance(exc, CarritoExpiradoError):
        return HTTPException(status_code=410, detail=str(exc))
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


@router.post("", response_model=CrearCarritoResponse, status_code=201)
def crear_carrito(db: Session = Depends(get_db)):
    repo = SqlCarritoRepository(db)
    use_case = CrearCarritoUseCase(repo)
    carrito = use_case.ejecutar()
    return _carrito_a_response(carrito, incluir_token=True)


@router.get("/{carrito_id}", response_model=CarritoResponse)
def obtener_carrito(
    carrito_id: str,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    repo = SqlCarritoRepository(db)
    use_case = ObtenerCarritoUseCase(repo)
    try:
        carrito = use_case.ejecutar(carrito_id, x_carrito_token)
    except (CarritoTokenInvalidoError, CarritoExpiradoError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    if carrito is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe un carrito con id '{carrito_id}'.",
        )
    return _carrito_a_response(carrito)


@router.post("/{carrito_id}/items", response_model=CarritoResponse)
def agregar_item_carrito(
    carrito_id: str,
    body: AgregarItemCarritoRequest,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    carrito_repo = SqlCarritoRepository(db)
    producto_repo = SqlProductoRepository(db)
    use_case = AgregarItemCarritoUseCase(carrito_repo, producto_repo)

    try:
        carrito = use_case.ejecutar(
            carrito_id, x_carrito_token, body.nombre, body.cantidad
        )
    except (CarritoTokenInvalidoError, CarritoExpiradoError, LookupError, ValueError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    return _carrito_a_response(carrito)
