from screener import run_scan
from datetime import datetime
import json

RESULT_FILE = "results.json"
STATUS_FILE = "status.json"

def save_results(trigger):
    # mark scan as RUNNING
    with open(STATUS_FILE, "w") as f:
        json.dump({
            "status": "RUNNING",
            "triggered_by": trigger,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f)

    data = run_scan()

    payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_type": trigger,
        "results": data
    }

    with open(RESULT_FILE, "w") as f:
        json.dump(payload, f)

    # mark scan as COMPLETE
    with open(STATUS_FILE, "w") as f:
        json.dump({
            "status": "IDLE",
            "triggered_by": trigger,
            "completed_at": payload["last_updated"]
        }, f)

