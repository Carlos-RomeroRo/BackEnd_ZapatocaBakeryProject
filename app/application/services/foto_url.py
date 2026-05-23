from app.application.settings.imagenes import ASSETS_BASE_URL


def resolver_url_foto(foto: str, placeholder: str) -> str:
    """
    Devuelve siempre una URL usable por el frontend.
    - https://... → se usa tal cual
    - ruta relativa + ASSETS_BASE_URL → URL pública del bucket/CDN
    - vacío o inválido → placeholder
    """
    foto = (foto or "").strip()
    if foto.startswith(("http://", "https://")):
        return foto
    if foto and ASSETS_BASE_URL:
        return f"{ASSETS_BASE_URL}/{foto.lstrip('/')}"
    return placeholder
