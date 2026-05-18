import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_SQLITE = f"sqlite:///{(_PROJECT_ROOT / 'panaderia.db').as_posix()}"

DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT_SQLITE)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:4200,http://127.0.0.1:4200",
    ).split(",")
    if origin.strip()
]
