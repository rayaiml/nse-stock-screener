from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start_scheduler, save_results
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start scheduled scans
start_scheduler()

RESULT_FILE = "results.json"


@app.get("/cached")
def get_cached():
    """
    FAST: Read last cached scan
    """
    if not os.path.exists(RESULT_FILE):
        return {"message": "No cached data available yet."}

    with open(RESULT_FILE) as f:
        return json.load(f)


import threading

@app.post("/scan-latest")
def scan_latest():
    """
    Trigger full NSE scan in background
    """
    threading.Thread(
        target=save_results,
        args=("MANUAL",),
        daemon=True
    ).start()

    return {
        "message": "Scan started in background. Results will be updated when complete."
    }

@app.get("/ping")
def ping():
    return {"status": "alive"}
