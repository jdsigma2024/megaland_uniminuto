from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from domain.entities import AsistenteFestival
from infrastructure.motor_reglas_adapter import MotorReglasEngineAdapter
from application.evaluar_admision_caso_uso import EvaluarAdmisionVIP

app = FastAPI(
    title="Sistema Inteligente UNIMINUTO - Asistente y Gobierno Algorítmico",
    description="Demostración académica de Arquitectura Hexagonal, Motor de Reglas y Redes Neuronales.",
    version="2.2.0"
)

app = FastAPI(
    title="Sistema Inteligente UNIMINUTO - Arquitectura Hexagonal Pura",
    description="Demostración con Puertos, Adaptadores y Rule Engine externo.",
    version="3.2.0"
)

templates = Jinja2Templates(directory="templates")

# Instanciamos el Adaptador de Infraestructura
ruta_conocimiento = "infrastructure/reglas_festival.json"
motor_adapter = MotorReglasEngineAdapter(ruta_conocimiento)

# Inyectamos el adaptador en el caso de uso
evaluador_caso_uso = EvaluarAdmisionVIP(evaluador_reglas=motor_adapter)

class SolicitudEntradaDTO(BaseModel):
    nombre: str = Field(..., example="Sofia Rincon")
    edad: int = Field(..., ge=10, le=100, example=20)
    asistencias_previas: int = Field(..., ge=0, example=4)
    gusta_reggaeton: bool = Field(..., example=True)
    hora_llegada_pm: float = Field(..., ge=1.0, le=11.0, example=2.0)

@app.post("/api/v1/evaluar")
def evaluar_asistente_endpoint(solicitud: SolicitudEntradaDTO):
    asistente = AsistenteFestival(
        nombre=solicitud.nombre,
        edad=solicitud.edad,
        asistencias_previas=solicitud.asistencias_previas,
        gusta_reggaeton=solicitud.gusta_reggaeton,
        hora_llegada_pm=solicitud.hora_llegada_pm
    )
    resultado = evaluador_caso_uso.ejecutar(asistente)
    return {"resultado": resultado}

@app.get("/", response_class=HTMLResponse)
def servir_pantalla_web(request: Request):
    return templates.TemplateResponse(request, "index.html")