from dataclasses import dataclass, field


@dataclass
class FilaError:
    fila: int
    motivo: str


@dataclass
class ImportarExcelResultado:
    insertados: int = 0
    errores: list[FilaError] = field(default_factory=list)
