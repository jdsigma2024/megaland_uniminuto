import json
import os
import rule_engine
from typing import List, Dict, Any
from domain.entities import AsistenteFestival, ResultadoEvaluacion
from domain.puertos import EvaluadorReglasPort


class MotorReglasEngineAdapter(EvaluadorReglasPort):
    """Adaptador de infraestructura que implementa el puerto usando la librería externa rule-engine."""

    def __init__(self, ruta_reglas: str):
        self.reglas_compiladas = self._cargar_y_compilar_reglas(ruta_reglas)

    def _cargar_y_compilar_reglas(self, ruta: str) -> List[Dict[str, Any]]:
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró la base de conocimiento en: {ruta}")

        with open(ruta, 'r', encoding='utf-8') as f:
            datos_reglas = json.load(f)

        reglas_procesadas = []
        for item in datos_reglas:
            reglas_procesadas.append({
                "nombre": item["nombre"],
                "regla_compilada": rule_engine.Rule(item["expresion"]),
                "resultado": item["resultado"]
            })
        return reglas_procesadas

    def inferir_resultado(self, asistente: AsistenteFestival, puntaje_mlp: float) -> ResultadoEvaluacion:
        hechos = {
            "edad": asistente.edad,
            "puntaje_mlp": puntaje_mlp,
            "asistencias_previas": asistente.asistencias_previas,
            "gusta_reggaeton": asistente.gusta_reggaeton,
            "hora_llegada_pm": asistente.hora_llegada_pm
        }

        for item in self.reglas_compiladas:
            if item["regla_compilada"].matches(hechos):
                res = item["resultado"]
                return ResultadoEvaluacion(
                    asistente=asistente.nombre,
                    puntaje_mlp=puntaje_mlp,
                    zona_asignada=res["zona_asignada"],
                    estado=res["estado"],
                    diagnostico=res["diagnostico"],
                    contrafactual_accionable=res["contrafactual"]
                )

        raise ValueError("Ninguna regla hizo match en el motor de reglas.")