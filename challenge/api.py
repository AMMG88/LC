from fastapi import FastAPI, HTTPException
from challenge.model import DelayModel
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd

app = FastAPI()

# Carga el modelo
model = DelayModel()
model.load_model()

# Lista de tipos de features
FEATURES_COLS = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

# Define el esquema de entrada
class PredictionRequest(BaseModel):
    flights: List[Dict]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictionRequest) -> dict:
    try:
        # Convertir los datos de entrada a un DataFrame
        data = pd.DataFrame(request.flights)

         # Validar que 'MES' sea menor o igual a 12
        if not all(data["MES"] <= 12):
            raise HTTPException(status_code=400, detail="El valor de 'MES' debe ser menor o igual a 12.")

        # Validar que 'TIPOVUELO' solo contenga valores 'I' o 'N'
        if not all(data["TIPOVUELO"].isin(["I", "N"])):
            raise HTTPException(status_code=400, detail="El valor de 'TIPOVUELO' debe ser 'I' o 'N'.")

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )           

        # Crear un DataFrame con las columnas requeridas y llenar las faltantes con False
        complete_features = pd.DataFrame(False, index=features.index, columns=FEATURES_COLS)
        complete_features.update(features)

        # Realizar la predicción
        predictions = model.predict(complete_features)
        
        # Devolver las predicciones en formato JSON
        return {"predict": predictions}
    except Exception as e:
        # Manejo de errores en caso de fallo
        raise HTTPException(status_code=400, detail=str(e))