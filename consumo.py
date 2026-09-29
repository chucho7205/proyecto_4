
import requests

url = "http://127.0.0.1:8000"  # Cambia a 8080 si usas Docker

# 1. Estado del servicio
r = requests.get(f"{url}/")
print("GET / →", r.status_code, r.json())

# 2. Predicción con datos realistas
cliente = {
    "Tiempo_en_el_sitio": 68.95,
    "Edad": 35,
    "Ingresos_de_la_zona": 61833.90,
    "Uso_de_Internet": 256.09,
    "Sexo": "F",
}

r = requests.post(f"{url}/predecir", json=cliente)
print("POST /predecir →", r.status_code)
print(r.json())