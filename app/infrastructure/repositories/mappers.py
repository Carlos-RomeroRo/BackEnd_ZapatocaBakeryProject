from decimal import Decimal

from app.domain.entities.producto import Producto
from app.domain.entities.trabajador import Trabajador
from app.infrastructure.database.models import ProductoModel, TrabajadorModel


def producto_to_entity(model: ProductoModel) -> Producto:
    return Producto(
        id=model.id,
        nombre=model.nombre,
        descripcion=model.descripcion,
        precio=Decimal(str(model.precio)),
        foto=model.foto or "",
    )


def producto_to_model(producto: Producto) -> ProductoModel:
    return ProductoModel(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        foto=producto.foto or "",
    )


def trabajador_to_entity(model: TrabajadorModel) -> Trabajador:
    return Trabajador(
        id=model.id,
        nombre=model.nombre,
        descripcion=model.descripcion or "",
        rol=model.rol,
        documento=model.documento or "",
        email=model.email or "",
        foto=model.foto or "",
    )


def trabajador_to_model(trabajador: Trabajador) -> TrabajadorModel:
    documento = trabajador.documento.strip() or None
    email = trabajador.email.strip() or None
    return TrabajadorModel(
        id=trabajador.id,
        nombre=trabajador.nombre,
        descripcion=trabajador.descripcion,
        rol=trabajador.rol,
        documento=documento,
        email=email,
        foto=trabajador.foto or "",
    )
