from apscheduler.schedulers.background import BackgroundScheduler
from screener import run_scan
from datetime import datetime
import json

def daily_scan():
    data = run_scan()
    with open("results.json", "w") as f:
        json.dump({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "results": data
        }, f)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_scan, "cron", hour=18, minute=0)
    scheduler.start()
