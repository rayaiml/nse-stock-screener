from fastapi import FastAPI
from screener import run_scan
from scheduler import start_scheduler
import json, os

app = FastAPI()
start_scheduler()

@app.get("/scan")
def scan():
    data = run_scan()
    if not data:
        return {"message": "No stocks currently meet your requirements."}
    return data

@app.get("/daily")
def daily():
    if not os.path.exists("results.json"):
        return {"message": "Daily scan not executed yet."}
    with open("results.json") as f:
        return json.load(f)
