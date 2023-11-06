import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, constr, conint
from typing import Literal, List, Union
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle


app = FastAPI(
title="Getaround API",
description="""Welcome to Getaround API !\n
Insert your car details to receive an estimation on daily rental car price.
**Use the endpoint `/predict` to estimate the daily rental price of your car !**
"""
)

@app.get("/")
async def docs_redirected():
    message = """Welcome to the Getaround API. Append /docs to this address to see the documentation for the API on the Pricing dataset."""
    return RedirectResponse(url='/docs')


# Defining required input for the prediction endpoint
class Features(BaseModel):
    model_key: Literal['Citroën','Peugeot','PGO','Renault','Audi','BMW','Mercedes','Opel','Volkswagen','Ferrari','Mitsubishi','Nissan','SEAT','Subaru','Toyota','other'] 
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: Literal['diesel','petrol','other']
    paint_color: Literal['black','grey','white','red','silver','blue','beige','brown','other']
    car_type: Literal['convertible','coupe','estate','hatchback','sedan','subcompact','suv','van']
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool


#endpoint to predict the price of a car
@app.post("/predict")
async def predict(features:Features):
    """ 
Example :

{
  "model_key": "Audi",
  "mileage": 25000,
  "engine_power": 130,
  "fuel": "diesel",
  "paint_color": "blue",
  "car_type": "sedan",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": true,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}

"""


# Make predictions
@app.post("/predict", tags=["Predictions"])
async def predict(cars: List[Features]):

    # Read input data
    car_features = pd.DataFrame(jsonable_encoder(cars))

    model = joblib.load('model.joblib')
    pred = model.predict(cars)
    return {"prediction" : pred[0]}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

