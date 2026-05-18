from datetime import timezone
from decimal import Decimal

from app.domain.entities.carrito import Carrito
from app.domain.entities.item_carrito import ItemCarrito
from app.domain.entities.producto import Producto
from app.domain.entities.trabajador import Trabajador
from app.infrastructure.database.models import (
    CarritoItemModel,
    CarritoModel,
    ProductoModel,
    TrabajadorModel,
)


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


def carrito_item_to_entity(item_model: CarritoItemModel) -> ItemCarrito:
    producto = item_model.producto
    precio = Decimal(str(item_model.precio_unitario))
    return ItemCarrito(
        producto_id=item_model.producto_id,
        cantidad=item_model.cantidad,
        nombre=producto.nombre if producto else "",
        precio_unitario=precio,
    )


def carrito_to_entity(model: CarritoModel, *, incluir_token: bool = False) -> Carrito:
    expira = model.expira_en
    if expira is not None and expira.tzinfo is None:
        expira = expira.replace(tzinfo=timezone.utc)
    return Carrito(
        id=model.id,
        estado=model.estado,
        items=[carrito_item_to_entity(item) for item in model.items],
        token_acceso=model.token_acceso if incluir_token else "",
        expira_en=expira,
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
