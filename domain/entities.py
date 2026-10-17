from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AsistenteFestival:
    nombre: str
    edad: int
    asistencias_previas: int
    gusta_reggaeton: bool
    hora_llegada_pm: float

@dataclass(frozen=True)
class ResultadoEvaluacion:
    asistente: str
    puntaje_mlp: float
    zona_asignada: str
    estado: str
    diagnostico: str
    contrafactual_accionable: Optional[str]