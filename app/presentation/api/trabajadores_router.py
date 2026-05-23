from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.application.dtos.import_result import ImportarExcelResultado
from app.application.use_cases.exportar_trabajadores_excel import (
    ExportarTrabajadoresExcelUseCase,
)
from app.application.use_cases.importar_trabajadores_excel import (
    ImportarTrabajadoresExcelUseCase,
)
from app.application.use_cases.listar_trabajadores import ListarTrabajadoresUseCase
from app.infrastructure.database.session import get_db
from app.infrastructure.excel.trabajador_excel import PandasTrabajadorExcelService
from app.infrastructure.repositories.sql_trabajador_repository import (
    SqlTrabajadorRepository,
)
from app.presentation.api.excel_response import EXCEL_MEDIA_TYPE, excel_file_headers
from app.presentation.api.schemas import (
    FilaErrorSchema,
    ImportarExcelResponse,
    TrabajadorListadoSchema,
)

router = APIRouter(prefix="/trabajadores", tags=["Trabajadores"])


@router.get("", response_model=list[TrabajadorListadoSchema])
def listar_trabajadores(db: Session = Depends(get_db)):
    """Catálogo JSON para el frontend (equipo de la panadería)."""
    repo = SqlTrabajadorRepository(db)
    use_case = ListarTrabajadoresUseCase(repo)
    return [
        TrabajadorListadoSchema(
            id=t.id,
            nombre=t.nombre,
            descripcion=t.descripcion,
            rol=t.rol,
            foto=t.foto,
        )
        for t in use_case.ejecutar()
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
def descargar_plantilla_trabajadores(db: Session = Depends(get_db)):
    excel = PandasTrabajadorExcelService()
    repo = SqlTrabajadorRepository(db)
    use_case = ExportarTrabajadoresExcelUseCase(excel, repo)
    contenido = use_case.ejecutar_plantilla()
    return Response(
        content=contenido,
        media_type=EXCEL_MEDIA_TYPE,
        headers=excel_file_headers("plantilla_trabajadores.xlsx"),
    )


@router.get("/excel/exportar")
def exportar_trabajadores_excel(db: Session = Depends(get_db)):
    excel = PandasTrabajadorExcelService()
    repo = SqlTrabajadorRepository(db)
    use_case = ExportarTrabajadoresExcelUseCase(excel, repo)
    contenido = use_case.ejecutar_exportacion()
    return Response(
        content=contenido,
        media_type=EXCEL_MEDIA_TYPE,
        headers=excel_file_headers("trabajadores.xlsx"),
    )


@router.post("/excel/importar", response_model=ImportarExcelResponse)
async def importar_trabajadores_excel(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    _validar_archivo_excel(archivo)
    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío")

    excel = PandasTrabajadorExcelService()
    repo = SqlTrabajadorRepository(db)
    use_case = ImportarTrabajadoresExcelUseCase(excel, repo)

    try:
        resultado = use_case.ejecutar(contenido)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return _resultado_a_response(resultado)
