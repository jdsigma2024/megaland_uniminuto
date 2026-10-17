from abc import ABC, abstractmethod
from domain.entities import AsistenteFestival, ResultadoEvaluacion

class EvaluadorReglasPort(ABC):
    """Puerto (Interfaz) que define el contrato para cualquier motor de reglas externo."""

    @abstractmethod
    def inferir_resultado(self, asistente: AsistenteFestival, puntaje_mlp: float) -> ResultadoEvaluacion:
        pass