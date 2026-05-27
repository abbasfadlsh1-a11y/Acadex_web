import datetime
import json
import os

# Configuration
DATA_FILE = "user_usage_data.json"
DAILY_LIMIT = 20  # للصور فقط

def get_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"solve_count": 0, "last_reset_time": None}

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_solve_limit(has_image=False):
    """
    has_image=False → نص فقط → بلا حد
    has_image=True  → صورة → حد 20 يومياً
    """
    # النص بلا حدود
    if not has_image:
        return True, "Success! No limit for text questions."

    # الصور بحد 20 يومياً
    data = get_user_data()
    now = datetime.datetime.now()

    if data["last_reset_time"] is None:
        data["last_reset_time"] = now.isoformat()
        data["solve_count"] = 1
        save_user_data(data)
        return True, f"Success! You have {DAILY_LIMIT - 1} image attempts remaining."

    last_reset = datetime.datetime.fromisoformat(data["last_reset_time"])
    time_passed = now - last_reset

    if time_passed >= datetime.timedelta(hours=24):
        data["solve_count"] = 1
        data["last_reset_time"] = now.isoformat()
        save_user_data(data)
        return True, "New 24-hour cycle started!"

    if data["solve_count"] < DAILY_LIMIT:
        data["solve_count"] += 1
        save_user_data(data)
        remaining = DAILY_LIMIT - data["solve_count"]
        return True, f"Success! You have {remaining} image attempts remaining."
    else:
        time_to_wait = datetime.timedelta(hours=24) - time_passed
        hours, remainder = divmod(int(time_to_wait.total_seconds()), 3600)
        minutes = remainder // 60
        return False, f"Image limit reached! Please try again in {hours}h {minutes}m."
