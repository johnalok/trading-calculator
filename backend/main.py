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

# API Endpoint to process strategy data
@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    # Compute "Hit SL"
    hit_sl = calculate_hit_sl(data.past_sl, data.sl, data.be, data.past_tp)

    return {
        "message": "Strategy received",
        "hit_sl": hit_sl
    }