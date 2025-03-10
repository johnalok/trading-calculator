from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Past Trade Structure
class PastTrade(BaseModel):
    past_tp: float
    past_sl: float
    past_be: float

class StrategyInput(BaseModel):
    tp1: float
    tp2: float
    be: float
    sl: float
    tp1_percent: float
    tp2_percent: float
    past_trades: List[PastTrade]

# Calculation Functions
def calculate_hit_sl(past_sl, sl, be, past_tp):
    return -1 if past_sl >= sl or past_tp < be else 0

def calculate_hit_be_no_profit(hit_sl, past_be, be, tp1, past_tp):
    return 0 if hit_sl == -1 else (1 if (past_be >= be and past_be < tp1) or (past_tp >= be and past_tp < tp1) else 0)

def calculate_hit_tp1_then_be(hit_sl, hit_be_without_profit, past_tp, tp1, sl, tp1_percent):
    return 0 if hit_sl == -1 or hit_be_without_profit == 1 else ((tp1 / sl) * (tp1_percent / 100) if past_tp >= tp1 else 0)

def calculate_hit_tp2(hit_sl, hit_be_without_profit, past_tp, tp2, sl, tp2_percent):
    return 0 if hit_sl == -1 or hit_be_without_profit == 1 else ((tp2 / sl) * (tp2_percent / 100) if past_tp >= tp2 else 0)

def calculate_outcome(hit_sl, hit_be_without_profit, hit_tp1_then_be, hit_tp2):
    return round(sum([hit_sl, hit_be_without_profit, hit_tp1_then_be, hit_tp2]), 2)

# API Endpoint
@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    # Filter out empty rows
    valid_trades = [trade for trade in data.past_trades if trade.past_tp or trade.past_sl or trade.past_be]

    total_hit_sl = 0
    total_hit_be_without_profit = 0
    total_hit_tp1_then_be = 0
    total_hit_tp2 = 0
    total_outcome = 0  

    for trade in valid_trades:
        hit_sl = calculate_hit_sl(trade.past_sl, data.sl, data.be, trade.past_tp)
        hit_be_no_profit = calculate_hit_be_no_profit(hit_sl, trade.past_be, data.be, data.tp1, trade.past_tp)
        hit_tp1_then_be = calculate_hit_tp1_then_be(hit_sl, hit_be_no_profit, trade.past_tp, data.tp1, data.sl, data.tp1_percent)
        hit_tp2 = calculate_hit_tp2(hit_sl, hit_be_no_profit, trade.past_tp, data.tp2, data.sl, data.tp2_percent)
        outcome = calculate_outcome(hit_sl, hit_be_no_profit, hit_tp1_then_be, hit_tp2)

        # Sum up results
        total_hit_sl += hit_sl
        total_hit_be_without_profit += hit_be_no_profit
        total_hit_tp1_then_be += hit_tp1_then_be
        total_hit_tp2 += hit_tp2
        total_outcome += outcome

    return {
        "message": "Strategy received",
        "hit_sl": total_hit_sl,
        "hit_be_without_profit": total_hit_be_without_profit,
        "hit_tp1_then_be": round(total_hit_tp1_then_be, 2),
        "hit_tp2": round(total_hit_tp2, 2),
        "outcome": round(total_outcome, 2),
    }
