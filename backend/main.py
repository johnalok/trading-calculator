from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
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
def calculate_hit_sl(past_sl: float, sl: float, be: float, past_tp: float) -> int:
    return -1 if past_sl >= sl or past_tp < be else 0

def calculate_hit_be_no_profit(hit_sl: int, past_be: float, be: float, tp1: float, past_tp: float) -> Union[int, str]:
    if hit_sl == -1:
        return ""
    return 0 if (past_be < tp1 and past_be >= be) or (past_tp < tp1 and past_tp >= be) else ""

def calculate_hit_tp1_then_be(hit_sl: int, hit_be_without_profit: Union[int, str], past_tp: float, tp1: float, sl: float, tp1_percent: float) -> float:
    if hit_sl == -1 or hit_be_without_profit == 0 or sl == 0:
        return 0
    return (tp1 / sl) * (tp1_percent / 100) if past_tp >= tp1 else 0

def calculate_hit_tp2(hit_sl: int, hit_be_without_profit: Union[int, str], past_tp: float, tp2: float, sl: float, tp2_percent: float) -> float:
    if hit_sl == -1 or hit_be_without_profit == 0 or sl == 0:
        return 0
    return (tp2 / sl) * (tp2_percent / 100) if past_tp >= tp2 else 0

def calculate_outcome(hit_sl: int, hit_be_without_profit: Union[int, str], hit_tp1_then_be: float, hit_tp2: float) -> float:
    return round(sum([
        hit_sl, 
        0 if hit_be_without_profit == "" else hit_be_without_profit, 
        hit_tp1_then_be, 
        hit_tp2
    ]), 2)

# API Endpoint
@app.post("/calculate-strategy")
async def calculate_strategy(data: StrategyInput):
    # Filter out empty past trade rows
    valid_trades = [trade for trade in data.past_trades if any([trade.past_tp, trade.past_sl, trade.past_be])]

    # Initialize totals
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
        total_hit_be_without_profit += 0 if hit_be_no_profit == "" else hit_be_no_profit
        total_hit_tp1_then_be += hit_tp1_then_be
        total_hit_tp2 += hit_tp2
        total_outcome += outcome

    # Format response to show empty fields for 0 values
    def format_value(value: float) -> Union[str, float]:
        return "" if value == 0 else round(value, 2)

    return {
        "message": "Strategy received",
        "hit_sl": format_value(total_hit_sl),
        "hit_be_without_profit": format_value(total_hit_be_without_profit),
        "hit_tp1_then_be": format_value(total_hit_tp1_then_be),
        "hit_tp2": format_value(total_hit_tp2),
        "outcome": format_value(total_outcome),
    }
