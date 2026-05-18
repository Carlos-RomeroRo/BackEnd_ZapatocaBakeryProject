from pydantic import BaseModel, Field


class FilaErrorSchema(BaseModel):
    fila: int
    motivo: str


class ImportarExcelResponse(BaseModel):
    insertados: int
    errores: list[FilaErrorSchema] = Field(default_factory=list)
