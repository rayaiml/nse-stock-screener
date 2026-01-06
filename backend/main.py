from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "precomputed_results.json"

@app.get("/screen")
def screen(
    adx: bool = True,
    macd: bool = True,
    volume: bool = True
):
    with open(DATA_FILE) as f:
        data = json.load(f)

    results = []
    for s in data:
        if adx and not (22 < s["adx"] < 30):
            continue
        if macd and not s["macd_above_signal"]:
            continue
        if volume and not (s["current_volume"] > s["avg_volume_21"]):
            continue
        results.append(s)

    if not results:
        return {"message": "No stocks currently meet your requirements."}

    return results
