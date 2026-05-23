from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.application.dtos.import_result import ImportarExcelResultado
from app.application.use_cases.exportar_productos_excel import ExportarProductosExcelUseCase
from app.application.use_cases.importar_productos_excel import ImportarProductosExcelUseCase
from app.application.use_cases.listar_productos import ListarProductosUseCase
from app.infrastructure.database.session import get_db
from app.infrastructure.excel.producto_excel import PandasProductoExcelService
from app.infrastructure.repositories.sql_producto_repository import SqlProductoRepository
from app.presentation.api.excel_response import EXCEL_MEDIA_TYPE, excel_file_headers
from app.presentation.api.schemas import (
    FilaErrorSchema,
    ImportarExcelResponse,
    ProductoListadoSchema,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=list[ProductoListadoSchema])
def listar_productos(db: Session = Depends(get_db)):
    """Catálogo JSON para el frontend."""
    repo = SqlProductoRepository(db)
    use_case = ListarProductosUseCase(repo)
    return [
        ProductoListadoSchema(
            id=p.id,
            nombre=p.nombre,
            descripcion=p.descripcion,
            precio=p.precio,
            foto=p.foto,
        )
        for p in use_case.ejecutar()
    ]



def _validar_archivo_excel(archivo: UploadFile) -> None:
    if not archivo.filename or not archivo.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Debe subir un archivo Excel con extensión .xlsx",
        )


def _resultado_a_response(resultado: ImportarExcelResultado) -> ImportarExcelResponse:
    return ImportarExcelResponse(
        insertados=resultado.insertados,
        errores=[
            FilaErrorSchema(fila=e.fila, motivo=e.motivo) for e in resultado.errores
        ],
    )


@router.get("/excel/plantilla")
def descargar_plantilla_productos(db: Session = Depends(get_db)):
    excel = PandasProductoExcelService()
    repo = SqlProductoRepository(db)
    use_case = ExportarProductosExcelUseCase(excel, repo)
    contenido = use_case.ejecutar_plantilla()
    return Response(
        content=contenido,
        media_type=EXCEL_MEDIA_TYPE,
        headers=excel_file_headers("plantilla_productos.xlsx"),
    )


@router.get("/excel/exportar")
def exportar_productos_excel(db: Session = Depends(get_db)):
    excel = PandasProductoExcelService()
    repo = SqlProductoRepository(db)
    use_case = ExportarProductosExcelUseCase(excel, repo)
    contenido = use_case.ejecutar_exportacion()
    return Response(
        content=contenido,
        media_type=EXCEL_MEDIA_TYPE,
        headers=excel_file_headers("productos.xlsx"),
    )


@router.post("/excel/importar", response_model=ImportarExcelResponse)
async def importar_productos_excel(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    _validar_archivo_excel(archivo)
    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío")

    excel = PandasProductoExcelService()
    repo = SqlProductoRepository(db)
    use_case = ImportarProductosExcelUseCase(excel, repo)

    try:
        resultado = use_case.ejecutar(contenido)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return _resultado_a_response(resultado)
