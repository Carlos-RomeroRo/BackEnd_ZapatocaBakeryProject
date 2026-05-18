import base64
import secrets
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_REALM = "Panadería Zapatoca API Docs"


def _is_docs_path(path: str) -> bool:
    return path == "/openapi.json" or path.startswith("/docs") or path.startswith("/redoc")


def _unauthorized() -> Response:
    return Response(
        status_code=401,
        headers={"WWW-Authenticate": f'Basic realm="{_REALM}"'},
        content="Autenticación requerida para la documentación.",
    )


class DocsBasicAuthMiddleware(BaseHTTPMiddleware):
    """HTTP Basic Auth solo para Swagger, ReDoc y OpenAPI schema."""

    def __init__(
        self,
        app,
        username: str,
        password: str,
        *,
        enabled: bool = True,
    ):
        super().__init__(app)
        self._username = username
        self._password = password
        self._enabled = enabled

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self._enabled or not _is_docs_path(request.url.path):
            return await call_next(request)

        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Basic "):
            return _unauthorized()

        try:
            decoded = base64.b64decode(authorization[6:]).decode("utf-8")
            user, _, pwd = decoded.partition(":")
        except (ValueError, UnicodeDecodeError):
            return _unauthorized()

        user_ok = secrets.compare_digest(user, self._username)
        pwd_ok = secrets.compare_digest(pwd, self._password)
        if not (user_ok and pwd_ok):
            return _unauthorized()

        return await call_next(request)
