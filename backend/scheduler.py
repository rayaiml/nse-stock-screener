from apscheduler.schedulers.background import BackgroundScheduler
from screener import run_scan
from datetime import datetime
import json

RESULT_FILE = "results.json"

def save_results(tag):
    data = run_scan()
    payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_type": tag,   # MORNING or EOD
        "results": data
    }
    with open(RESULT_FILE, "w") as f:
        json.dump(payload, f)

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # Morning scan at 10:00 AM (Mon–Fri)
    scheduler.add_job(
        save_results,
        "cron",
        day_of_week="mon-fri",
        hour=10,
        minute=0,
        args=["MORNING"]
    )

    # End-of-day scan at 3:30 PM (Mon–Fri)
    scheduler.add_job(
        save_results,
        "cron",
        day_of_week="mon-fri",
        hour=15,
        minute=30,
        args=["EOD"]
    )

    scheduler.start()
