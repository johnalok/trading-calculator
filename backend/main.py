from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StrategyInput(BaseModel):
    tp1: float
    tp2: float
    be: float
    tp: float
    tp1_percentage: float
    tp2_percentage: float

@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    return {"message": "Strategy received", "data": data}
