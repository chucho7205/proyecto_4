from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from esquema import SolicitudPrediccion

NOMBRE_BUNDLE = "modelo_mlp_bundle.joblib"
estado_servicio = {"bundle": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print("Bundle cargado correctamente")
    yield
    estado_servicio["bundle"] = None


app = FastAPI(
    title="API de Predicción de click de clientes en publicidad",
    description=(
        "Recibe datos de un cliente y predice la probabilidad de hacer clic en una publicidad"
    ),
    version="1.0.0",
    lifespan=lifespan,
)


class ClienteInput(BaseModel):
    Tiempo_en_el_sitio: float = Field(..., description="Tiempo en el sitio (minutos)")
    Edad: int = Field(..., description="Edad")
    Ingresos_de_la_zona: float = Field(..., description="Ingresos de la zona")
    Uso_de_Internet: float = Field(..., description="Uso de Internet")
    Sexo: Literal["F", "M"] = Field(..., description="Sexo (Femenino o Masculino, como en el entrenamiento)")



class ClienteOutput(BaseModel):
    click_predicho: int
    probabilidad: float
    probabilidad_click: str
    model_version: str


@app.get("/")
def estado():
    bundle = estado_servicio["bundle"]

    if bundle is None:
        return {
            "servicio": "API de predicción de click de clientes en publicidad",
            "modelo_cargado": False,
            "model_version": None,
        }

    return {
        "servicio": "API de predicción de click de clientes en publicidad",
        "modelo_cargado": bundle is not None,
        "model_version": bundle["metadata"]["model_version"] ,
    }


@app.post("/predecir", response_model=ClienteOutput)
def predecir(cliente: ClienteInput):
    bundle = estado_servicio["bundle"]

    if bundle is None:
        raise HTTPException(status_code=503, detail="El modelo aún no está cargado")

    fila = cliente.model_dump()

    # Usar la misma clave con la que guardaste el bundle ("columns" o "columnas")
    columnas = bundle.get("columns") or bundle.get("columnas")
    if columnas is None:
        raise HTTPException(status_code=500, detail="El bundle no tiene la lista de columnas")

    X_nuevo = pd.DataFrame([fila])[columnas]

    modelo = bundle["pipeline"]  # clave correcta

    prediccion = int(modelo.predict(X_nuevo)[0])
    probabilidad = float(modelo.predict_proba(X_nuevo)[0, 1])

    return ClienteOutput(
        click_predicho=prediccion,
        probabilidad=round(probabilidad, 4),
        probabilidad_click=("alto" if prediccion == 1 else "bajo"),
        model_version=bundle["metadata"]["model_version"],
    )
