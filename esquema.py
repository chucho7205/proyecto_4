

from typing import Literal
from pydantic import BaseModel, Field


class SolicitudPrediccion(BaseModel):
    Tiempo_en_el_sitio: float = Field(..., ge=0, le=200, description="Tiempo en el sitio (minutos)", examples=[68.95],)
    Edad: int = Field(..., ge=15, le=80,  description="Edad del usuario", examples=[35],)
    Ingresos_de_la_zona: float = Field(..., ge=0, le=150_000, description="Ingresos de la zona", examples=[61833.90],)
    Uso_de_Internet: float = Field(..., ge=0, le=400, description="Uso de Internet", examples=[256.09],)
    Sexo: Literal["F", "M"] = Field(..., description="Sexo (F o M, igual que en el entrenamiento)", examples=["F"],)