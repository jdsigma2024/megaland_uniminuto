import pytest
from unittest.mock import MagicMock
from domain.entities import AsistenteFestival, ResultadoEvaluacion
from application.evaluar_admision_caso_uso import EvaluarAdmisionVIP


def test_evaluar_admision_caso_uso_exitoso():
    # Arrange (Preparar)
    mock_puerto = MagicMock()
    nombre_prueba = "Elizabeth Olsen"  # O "Carlos Pérez", pero deben coincidir

    resultado_esperado = ResultadoEvaluacion(
        asistente=nombre_prueba,
        puntaje_mlp=0.85,
        zona_asignada="VIP / Preferencial",
        estado="ACCESO_AUTORIZADO",
        diagnostico="Prueba unitaria exitosa",
        contrafactual_accionable=None
    )
    mock_puerto.inferir_resultado.return_value = resultado_esperado

    caso_uso = EvaluarAdmisionVIP(evaluador_reglas=mock_puerto)

    asistente = AsistenteFestival(
        nombre=nombre_prueba,
        edad=25,
        asistencias_previas=4,
        gusta_reggaeton=True,
        hora_llegada_pm=2.0
    )

    # Act (Actuar)
    resultado = caso_uso.ejecutar(asistente)

    # Assert (Afirmar)
    assert resultado.asistente == nombre_prueba
    assert resultado.puntaje_mlp == 0.85
    assert resultado.estado == "ACCESO_AUTORIZADO"
    mock_puerto.inferir_resultado.assert_called_once()