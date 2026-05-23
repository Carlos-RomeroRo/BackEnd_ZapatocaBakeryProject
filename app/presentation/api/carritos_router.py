from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.application.use_cases.agregar_item_carrito import AgregarItemCarritoUseCase
from app.application.use_cases.crear_carrito import CrearCarritoUseCase
from app.application.use_cases.eliminar_item_carrito import EliminarItemCarritoUseCase
from app.application.dtos.resumen_carrito import ResumenCarrito
from app.application.use_cases.obtener_resumen_carrito import ObtenerResumenCarritoUseCase
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
    EliminarItemCarritoRequest,
    ItemCarritoLineaSchema,
    ProductoCarritoResumenSchema,
    ResumenCarritoResponse,
)

router = APIRouter(prefix="/carritos", tags=["Carritos"])


def _resumen_a_response(resumen: ResumenCarrito) -> ResumenCarritoResponse:
    return ResumenCarritoResponse(
        carrito_id=resumen.carrito_id,
        estado=resumen.estado,
        productos=[
            ProductoCarritoResumenSchema(
                producto_id=linea.producto_id,
                nombre=linea.nombre,
                precio_unitario=linea.precio_unitario,
                cantidad=linea.cantidad,
                precio_total=linea.precio_total,
            )
            for linea in resumen.productos
        ],
        total_compra=resumen.total_compra,
        expira_en=resumen.expira_en,
    )


def _resumen_a_carrito_response(resumen: ResumenCarrito) -> CarritoResponse:
    return CarritoResponse(
        carrito_id=resumen.carrito_id,
        estado=resumen.estado,
        items=[
            ItemCarritoLineaSchema(
                producto_id=linea.producto_id,
                nombre=linea.nombre,
                cantidad=linea.cantidad,
                precio_unitario=linea.precio_unitario,
                subtotal=linea.precio_total,
            )
            for linea in resumen.productos
        ],
        total_productos=resumen.total_compra,
        expira_en=resumen.expira_en,
    )


def _carrito_a_response(
    carrito: Carrito, *, incluir_token: bool = False
) -> CarritoResponse | CrearCarritoResponse:
    resumen = ObtenerResumenCarritoUseCase._construir_resumen(carrito)
    response = _resumen_a_carrito_response(resumen)
    if incluir_token:
        return CrearCarritoResponse(
            **response.model_dump(),
            token_acceso=carrito.token_acceso,
        )
    return response


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


@router.get("/{carrito_id}/resumen", response_model=ResumenCarritoResponse)
def obtener_resumen_carrito(
    carrito_id: str,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    repo = SqlCarritoRepository(db)
    use_case = ObtenerResumenCarritoUseCase(repo)
    try:
        resumen = use_case.ejecutar(carrito_id, x_carrito_token)
    except (CarritoTokenInvalidoError, CarritoExpiradoError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    if resumen is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe un carrito con id '{carrito_id}'.",
        )
    return _resumen_a_response(resumen)


@router.get("/{carrito_id}", response_model=CarritoResponse)
def obtener_carrito(
    carrito_id: str,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    repo = SqlCarritoRepository(db)
    use_case = ObtenerResumenCarritoUseCase(repo)
    try:
        resumen = use_case.ejecutar(carrito_id, x_carrito_token)
    except (CarritoTokenInvalidoError, CarritoExpiradoError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    if resumen is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe un carrito con id '{carrito_id}'.",
        )
    return _resumen_a_carrito_response(resumen)


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


@router.delete("/{carrito_id}/items/{producto_id}", response_model=CarritoResponse)
def eliminar_item_carrito_por_id(
    carrito_id: str,
    producto_id: int,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    carrito_repo = SqlCarritoRepository(db)
    producto_repo = SqlProductoRepository(db)
    use_case = EliminarItemCarritoUseCase(carrito_repo, producto_repo)

    try:
        carrito = use_case.ejecutar_por_producto_id(
            carrito_id, x_carrito_token, producto_id
        )
    except (CarritoTokenInvalidoError, CarritoExpiradoError, LookupError, ValueError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    return _carrito_a_response(carrito)


@router.delete("/{carrito_id}/items", response_model=CarritoResponse)
def eliminar_item_carrito_por_nombre(
    carrito_id: str,
    body: EliminarItemCarritoRequest,
    db: Session = Depends(get_db),
    x_carrito_token: str = Header(..., alias="X-Carrito-Token"),
):
    carrito_repo = SqlCarritoRepository(db)
    producto_repo = SqlProductoRepository(db)
    use_case = EliminarItemCarritoUseCase(carrito_repo, producto_repo)

    try:
        carrito = use_case.ejecutar_por_nombre(
            carrito_id, x_carrito_token, body.nombre
        )
    except (CarritoTokenInvalidoError, CarritoExpiradoError, LookupError, ValueError) as exc:
        raise _manejar_errores_carrito(exc) from exc

    return _carrito_a_response(carrito)
