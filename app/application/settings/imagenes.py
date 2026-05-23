import os

from dotenv import load_dotenv

load_dotenv()

# URL por defecto si en Excel/BD no hay foto o no es http(s) (p. ej. alojada en Supabase Storage).
PLACEHOLDER_FOTO_TRABAJADOR = os.getenv(
    "PLACEHOLDER_FOTO_TRABAJADOR",
    "https://placehold.co/400x400/e8e8e8/666666?text=Equipo",
).strip()
PLACEHOLDER_FOTO_PRODUCTO = os.getenv(
    "PLACEHOLDER_FOTO_PRODUCTO",
    "https://placehold.co/400x300/e8e8e8/666666?text=Producto",
).strip()

# Opcional: si guardas rutas relativas en BD (ej. trabajadores/juan.jpg), prefijo del bucket público.
ASSETS_BASE_URL = os.getenv("ASSETS_BASE_URL", "").strip().rstrip("/")
