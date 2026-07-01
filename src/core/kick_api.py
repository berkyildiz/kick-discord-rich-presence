from datetime import datetime, timezone
from curl_cffi import requests

KICK_API_BASE = "https://kick.com/api/v2/channels/"

def fetch_kick_data(username, start_time_fallback, get_text_cb, logger_cb):
    """
    Fetches the live status of the given Kick username.
    """
    url = f"{KICK_API_BASE}{username}"
    try:
        response = requests.get(url, impersonate="chrome", timeout=10)
        if response.status_code == 200:
            data = response.json()
            livestream = data.get("livestream")
            
            if livestream and livestream.get("is_live"):
                start_time_str = livestream.get("start_time")
                start_ts = start_time_fallback
                if start_time_str:
                    try:
                        dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                        dt = dt.replace(tzinfo=timezone.utc)
                        start_ts = int(dt.timestamp())
                    except Exception:
                        pass
                
                category = "Just Chatting"
                if livestream.get("categories"):
                    category = livestream["categories"][0].get("name", "Just Chatting")
                
                return {
                    "is_live": True,
                    "title": livestream.get("session_title", get_text_cb("rpc_live")),
                    "category": category,
                    "viewers": livestream.get("viewer_count", 0),
                    "start_time": start_ts
                }
    except Exception as e:
        if logger_cb:
            logger_cb(f"{get_text_cb('log_fetch_fail')} {e}")
        
    return {
        "is_live": False,
        "title": get_text_cb("rpc_live_kick"), 
        "category": "IRL",
        "viewers": 0,
        "start_time": start_time_fallback
    }
