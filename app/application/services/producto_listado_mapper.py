from app.application.dtos.catalogo import ProductoListado
from app.application.services.foto_url import resolver_url_foto
from app.application.settings.imagenes import PLACEHOLDER_FOTO_PRODUCTO
from app.domain.entities.producto import Producto
from app.domain.value_objects.tipo_producto import ETIQUETAS_TIPO


def producto_a_listado(producto: Producto) -> ProductoListado:
    if producto.id is None:
        raise ValueError("El producto no tiene identificador válido")
    return ProductoListado(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        tipo=producto.tipo,
        tipo_etiqueta=ETIQUETAS_TIPO.get(producto.tipo, producto.tipo),
        foto=resolver_url_foto(producto.foto, PLACEHOLDER_FOTO_PRODUCTO),
    )
