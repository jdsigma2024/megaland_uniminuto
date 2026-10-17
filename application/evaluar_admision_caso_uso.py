from domain.entities import AsistenteFestival, ResultadoEvaluacion
from domain.puertos import EvaluadorReglasPort

class EvaluarAdmisionVIP:
    def __init__(self, evaluador_reglas: EvaluadorReglasPort):
        # Inyectamos el puerto, no una implementación concreta de infraestructura
        self.evaluador_reglas = evaluador_reglas

    def ejecutar(self, asistente: AsistenteFestival) -> ResultadoEvaluacion:
        puntaje_mlp = self._calcular_puntaje_red_neural(asistente)
        return self.evaluador_reglas.inferir_resultado(asistente, puntaje_mlp)

    def _calcular_puntaje_red_neural(self, asistente: AsistenteFestival) -> float:
        """Simulación de la capa oculta del Perceptrón Multicapa (MLP)."""
        interes_urbano = 1.0 if asistente.gusta_reggaeton else 0.2
        factor_historial = min(asistente.asistencias_previas / 5.0, 1.0)
        factor_llegada = max(0.0, 1.0 - (asistente.hora_llegada_pm / 6.0))

        puntaje = (interes_urbano * 0.5) + (factor_historial * 0.3) + (factor_llegada * 0.2)
        return round(puntaje, 2)