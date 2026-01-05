from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import threading

from scheduler import start_scheduler, save_results

# -----------------------
# App setup
# -----------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULT_FILE = "results.json"

# -----------------------
# Start scheduled jobs
# -----------------------
start_scheduler()

# -----------------------
# Health / keep-alive
# -----------------------
@app.get("/ping")
def ping():
    return {"status": "alive"}

# -----------------------
# Quick scan (cached data)
# -----------------------
@app.get("/cached")
def get_cached():
    if not os.path.exists(RESULT_FILE):
        return {
            "message": "No cached data available yet. Please wait for scheduled scan."
        }

    with open(RESULT_FILE, "r") as f:
        return json.load(f)

# -----------------------
# Manual full NSE scan (BACKGROUND)
# -----------------------
@app.post("/scan-latest")
def scan_latest():
    """
    Starts full NSE scan in background.
    Returns immediately to avoid browser timeout.
    """

    threading.Thread(
        target=save_results,
        args=("MANUAL",),
        daemon=True
    ).start()

    return {
        "message": (
            "Full NSE scan started in background. "
            "This may take 20–40 minutes. "
            "Please use 'Quick Scan (Cached)' later to view results."
        )
    }

STATUS_FILE = "status.json"

@app.get("/status")
def scan_status():
    if not os.path.exists(STATUS_FILE):
        return {"status": "IDLE"}

    with open(STATUS_FILE) as f:
        return json.load(f)
