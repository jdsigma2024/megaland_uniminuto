import os
import pytest
from domain.entities import AsistenteFestival
from infrastructure.motor_reglas_adapter import MotorReglasEngineAdapter

@pytest.fixture
def motor_adapter():
    # Ruta absoluta basada en la ubicación actual del test para evitar errores de directorio
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.abspath(os.path.join(dir_actual, "..", "infrastructure", "reglas_festival.json"))
    return MotorReglasEngineAdapter(ruta_json)

def test_regla_menor_edad(motor_adapter):
    asistente_menor = AsistenteFestival(
        nombre="Ana Menor",
        edad=16,
        asistencias_previas=1,
        gusta_reggaeton=True,
        hora_llegada_pm=3.0
    )
    resultado = motor_adapter.inferir_resultado(asistente_menor, puntaje_mlp=0.40)
    assert resultado.estado == "ACCESO_RESTRINGIDO_VIP"
    assert "Menor de edad" in resultado.diagnostico

def test_regla_acceso_vip(motor_adapter):
    asistente_vip = AsistenteFestival(
        nombre="Juan VIP",
        edad=22,
        asistencias_previas=5,
        gusta_reggaeton=True,
        hora_llegada_pm=1.0
    )
    resultado = motor_adapter.inferir_resultado(asistente_vip, puntaje_mlp=0.90)
    assert resultado.estado == "ACCESO_AUTORIZADO"
    assert "VIP" in resultado.zona_asignada