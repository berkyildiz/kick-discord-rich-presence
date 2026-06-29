"""
Kick Discord Rich Presence
Copyright (c) 2026 Berk YILDIZ XATHENA

A highly optimized, clean, and production-ready Python application
to sync Kick.com livestream status with Discord Rich Presence via Gateway.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime, timezone

import websocket
from curl_cffi import requests
from dotenv import load_dotenv

# Reconfigure stdout for UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Constants
KICK_API_BASE = "https://kick.com/api/v2/channels/"
DISCORD_GATEWAY = "wss://gateway.discord.gg/?v=9&encoding=json"
TWITCH_DUMMY_URL = "https://twitch.tv/xathenaone"

# Language Dictionary
I18N = {
    "EN": {
        "err_env": "ERROR: DISCORD_TOKEN or KICK_USERNAME is missing in .env!",
        "err_kick": "Failed to fetch Kick data: {}",
        "err_payload": "Failed to send payload: {}",
        "connected": "Discord Gateway connection established.",
        "disconnected": "Connection lost. Reconnecting in 5 seconds...",
        "status_update": "[Update] Presence updated ({status}). Title: {title}",
        "live": "LIVE",
        "offline": "OFFLINE",
        "category_tpl": "Category: {} | {} Viewers",
        "not_live_title": "Offline",
        "preparing_title": "Preparing Stream / Live"
    },
    "TR": {
        "err_env": "HATA: .env dosyasinda DISCORD_TOKEN veya KICK_USERNAME eksik!",
        "err_kick": "Kick verisi alinirken hata olustu: {}",
        "err_payload": "Payload gonderimi basarisiz: {}",
        "connected": "Discord Gateway baglantisi kuruldu.",
        "disconnected": "Baglanti koptu. 5 saniye icinde tekrar baglaniliyor...",
        "status_update": "[Guncelleme] Durum guncellendi ({status}). Baslik: {title}",
        "live": "CANLI",
        "offline": "CEVRIMDISI",
        "category_tpl": "Kategori: {} | {} Izleyici",
        "not_live_title": "Yayinda Degil",
        "preparing_title": "Yayina Hazirlaniyor / Canli Yayin"
    }
}

class KickDiscordPresence:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_TOKEN")
        self.kick_username = os.getenv("KICK_USERNAME")
        self.lang = os.getenv("LANGUAGE", "EN").upper()
        
        if self.lang not in I18N:
            self.lang = "EN"
        self.i18n = I18N[self.lang]
        
        if not self.token or not self.kick_username:
            print(self.i18n["err_env"])
            sys.exit(1)
            
        self.always_purple = True
        self.start_time = int(time.time() * 1000)
        self.ws = None

    def log(self, message):
        print(message)

    def fetch_kick_data(self):
        url = f"{KICK_API_BASE}{self.kick_username}"
        try:
            response = requests.get(url, impersonate="chrome", timeout=10)
            if response.status_code == 200:
                data = response.json()
                livestream = data.get("livestream")
                
                if livestream and livestream.get("is_live"):
                    start_time_str = livestream.get("start_time")
                    start_ts = int(time.time() * 1000)
                    if start_time_str:
                        try:
                            dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                            dt = dt.replace(tzinfo=timezone.utc)
                            start_ts = int(dt.timestamp() * 1000)
                        except Exception:
                            pass
                    
                    category = "Just Chatting"
                    if livestream.get("categories"):
                        category = livestream["categories"][0].get("name", "Just Chatting")
                    
                    return {
                        "is_live": True,
                        "title": livestream.get("session_title", self.i18n["live"]),
                        "category": category,
                        "viewers": livestream.get("viewer_count", 0),
                        "start_time": start_ts
                    }
                else:
                    return {
                        "is_live": False,
                        "title": self.i18n["not_live_title"],
                        "category": "Kick.com",
                        "viewers": 0,
                        "start_time": self.start_time
                    }
        except Exception as e:
            self.log(self.i18n["err_kick"].format(e))
            
        return {
            "is_live": False,
            "title": self.i18n["preparing_title"],
            "category": "Kick.com",
            "viewers": 0,
            "start_time": self.start_time
        }

    def update_presence_loop(self):
        while True:
            if not self.ws or not self.ws.sock or not self.ws.sock.connected:
                break
                
            info = self.fetch_kick_data()
            is_live = info["is_live"]
            
            activity_type = 1 if (self.always_purple or is_live) else 0
            stream_url = TWITCH_DUMMY_URL if (self.always_purple or is_live) else None

            details = info["title"][:127]
            if is_live:
                state = self.i18n["category_tpl"].format(info["category"], info["viewers"])
                current_start_time = info["start_time"]
            else:
                state = f"kick.com/{self.kick_username}"
                current_start_time = self.start_time
                
            activity = {
                "name": "Kick",
                "type": activity_type,
                "details": details,
                "state": state[:127]
            }
            
            if stream_url:
                activity["url"] = stream_url
                
            if current_start_time:
                activity["timestamps"] = {"start": current_start_time}

            presence_payload = {
                "op": 3,
                "d": {
                    "since": None,
                    "activities": [activity],
                    "status": "online",
                    "afk": False
                }
            }
            
            try:
                self.ws.send(json.dumps(presence_payload))
                status_desc = self.i18n["live"] if is_live else self.i18n["offline"]
                self.log(self.i18n["status_update"].format(status=status_desc, title=details))
            except Exception as e:
                self.log(self.i18n["err_payload"].format(e))
                break
                
            time.sleep(30)

    def heartbeat_loop(self, interval):
        while True:
            time.sleep(interval)
            try:
                if self.ws and self.ws.sock and self.ws.sock.connected:
                    self.ws.send(json.dumps({"op": 1, "d": None}))
                else:
                    break
            except Exception:
                break

    def on_open(self, ws):
        self.ws = ws
        self.log(self.i18n["connected"])
        auth_payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "windows",
                    "$browser": "chrome",
                    "$device": "pc"
                }
            }
        }
        self.ws.send(json.dumps(auth_payload))
        threading.Thread(target=self.update_presence_loop, daemon=True).start()

    def on_message(self, ws, message):
        event = json.loads(message)
        if event.get("op") == 10:
            interval = event["d"]["heartbeat_interval"] / 1000.0
            threading.Thread(target=self.heartbeat_loop, args=(interval,), daemon=True).start()

    def on_close(self, ws, close_status_code, close_msg):
        self.log(self.i18n["disconnected"])
        time.sleep(5)
        self.start()

    def start(self):
        ws_app = websocket.WebSocketApp(
            DISCORD_GATEWAY,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close
        )
        ws_app.run_forever()

if __name__ == "__main__":
    app = KickDiscordPresence()
    app.start()
