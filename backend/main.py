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

# Define data structure for incoming request
class StrategyInput(BaseModel):
    tp1: float
    tp2: float
    be: float
    sl: float
    tp1_percent: float
    tp2_percent: float
    past_tp: float
    past_sl: float
    past_be: float

# Function to calculate "Hit SL"
def calculate_hit_sl(past_sl , sl, be, past_tp):
    if past_sl >= sl or past_tp < be:
        return -1
    
    return None  # Or return "" if you prefer an empty string

def calculate_hit_be_no_profit(hit_sl, be, tp1, past_tp):
    if hit_sl == -1:
        return None  # SL was hit, so no BE calculation

    if (be >= be and be < tp1) or (past_tp >= be and past_tp < tp1):
        return 0  # BE condition met

    return None  # Default case

# API Endpoint to process strategy data
@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    # Compute "Hit SL"
    hit_sl = calculate_hit_sl(data.past_sl, data.sl, data.be, data.past_tp)

    # Compute Hit BE without profit
    hit_be_no_profit = calculate_hit_be_no_profit(hit_sl, data.be, data.tp1, data.past_tp)

    return {
        "message": "Strategy received",
        "hit_sl": hit_sl,
        "hit_be_without_profit": hit_be_no_profit,
    }