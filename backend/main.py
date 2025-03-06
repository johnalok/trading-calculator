from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class StrategyInput(BaseModel):
    tp1: float
    tp2: float
    be: float
    tp: float
    tp1_percent: float
    tp2_percent: float
    tp_past: float
    sl_past: float
    be_past: float
    direction_past: str

class StrategyOutput(BaseModel):
    message: str
    data: StrategyInput
    hit_sl: bool
    hit_be_without_profit: bool
    hit_tp1_then_be: bool
    hit_tp2: bool
    outcome: str

@app.post("/calculate-strategy", response_model=StrategyOutput)
async def calculate_strategy(data: StrategyInput):
    # Placeholder values (logic to be added later)
    hit_sl = False
    hit_be_without_profit = False
    hit_tp1_then_be = False
    hit_tp2 = False
    outcome = "Pending Calculation"

    return {
        "message": "Strategy received",
        "data": data,
        "hit_sl": hit_sl,
        "hit_be_without_profit": hit_be_without_profit,
        "hit_tp1_then_be": hit_tp1_then_be,
        "hit_tp2": hit_tp2,
        "outcome": outcome
    }