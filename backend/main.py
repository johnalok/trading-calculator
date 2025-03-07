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
    past_tp: float
    past_sl: float
    past_be: float
    past_direction: str  # Keeping it as a string for "long" or "short"

@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    return {
        "message": "Strategy received",
        "hit_sl": 0,  # Placeholder until we implement calculations
        "hit_be_no_profit": 0,
        "hit_tp1_then_be": 0,
        "hit_tp2": 0,
        "outcome": "TBD"
    }