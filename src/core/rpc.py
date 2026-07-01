import time
import json
import threading
import websocket
from pypresence import Presence
from curl_cffi import requests

from .kick_api import fetch_kick_data

DISCORD_GATEWAY = "wss://gateway.discord.gg/?v=9&encoding=json"
TWITCH_DUMMY_URL = "https://twitch.tv/xathenaone"

class KickDiscordPresence:
    def __init__(self, logger_callback=None, get_text_callback=None):
        self.logger = logger_callback
        self.get_text = get_text_callback if get_text_callback else (lambda k: k)
        
        self.running = False
        
        self.kick_username = ""
        self.client_id = ""
        self.discord_invite = ""
        self.token = ""
        self.mode = "2" # Default IPC
        
        self.start_time = int(time.time())
        self.ws = None
        self.rpc = None

    def log(self, message):
        if self.logger:
            self.logger(message)
        else:
            print(message)

    def _fetch(self):
        return fetch_kick_data(self.kick_username, self.start_time, self.get_text, self.logger)

    # ==========================
    # MODE 1: GATEWAY (MOR RENK)
    # ==========================
    def update_gateway_loop(self):
        while self.running:
            if not self.ws or not getattr(self.ws, 'sock', None) or not self.ws.sock.connected:
                break
                
            info = self._fetch()
            details = info["title"][:127]
            state = f"https://kick.com/{self.kick_username} | {info['viewers']} İzleyici"
            
            current_start_time_ms = info["start_time"] * 1000
                
            activity = {
                "name": "Kick",
                "type": 1,
                "url": TWITCH_DUMMY_URL,
                "details": details,
                "state": state[:127],
                "application_id": self.client_id,
                "timestamps": {"start": current_start_time_ms},
                "assets": {
                    "large_image": getattr(self, 'large_image_key', 'kick_logo'),
                    "large_text": self.get_text("rpc_streaming"),
                    "small_image": getattr(self, 'small_image_key', 'verified'),
                    "small_text": self.get_text("rpc_verified")
                }
            }

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
                self.log(f"{self.get_text('log_gateway_update')} {info['viewers']}")
            except Exception as e:
                self.log(f"[Gateway] Hata: {e}")
                break
                
            for _ in range(30):
                if not self.running:
                    break
                time.sleep(1)

    def heartbeat_loop(self, interval):
        while self.running:
            for _ in range(int(interval)):
                if not self.running:
                    return
                time.sleep(1)
            try:
                if self.ws and getattr(self.ws, 'sock', None) and self.ws.sock.connected:
                    self.ws.send(json.dumps({"op": 1, "d": None}))
                else:
                    break
            except Exception:
                break

    def on_open(self, ws):
        self.ws = ws
        self.log(self.get_text("log_connected"))
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
        threading.Thread(target=self.update_gateway_loop, daemon=True).start()

    def on_message(self, ws, message):
        event = json.loads(message)
        if event.get("op") == 10:
            interval = event["d"]["heartbeat_interval"] / 1000.0
            threading.Thread(target=self.heartbeat_loop, args=(interval,), daemon=True).start()

    def on_close(self, ws, close_status_code, close_msg):
        if self.running:
            self.log(self.get_text("log_disconnected"))
            time.sleep(5)
            if self.running:
                self.start_gateway()

    def start_gateway(self):
        if not self.token:
            self.log(self.get_text("err_token"))
            self.running = False
            return
            
        self.large_image_key = "kick_logo"
        self.small_image_key = "verified"
        try:
            res = requests.get(f"https://discord.com/api/v10/oauth2/applications/{self.client_id}/assets", headers={"Authorization": self.token}, timeout=5)
            if res.status_code == 200:
                for asset in res.json():
                    if asset.get("name") == "kick_logo":
                        self.large_image_key = asset.get("id")
                    elif asset.get("name") == "verified":
                        self.small_image_key = asset.get("id")
        except Exception as e:
            self.log(f"{self.get_text('log_asset_fail')} {e}")
            
        ws_app = websocket.WebSocketApp(
            DISCORD_GATEWAY,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close
        )
        ws_app.run_forever()

    # ==========================
    # MODE 2: IPC (BUTON & ASSET)
    # ==========================
    def update_rpc_loop(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.log(self.get_text("log_ipc_connected"))
        except Exception as e:
            self.log(f"{self.get_text('err_discord')} {e}")
            self.running = False
            return
            
        while self.running:
            info = self._fetch()
            details = info["title"][:127]
            state = f"https://kick.com/{self.kick_username} | {info['viewers']} İzleyici"
                
            buttons = [
                {"label": self.get_text("rpc_join"), "url": f"https://kick.com/{self.kick_username}"},
                {"label": self.get_text("rpc_discord"), "url": self.discord_invite}
            ]
            
            try:
                self.rpc.update(
                    state=state[:127],
                    details=details,
                    start=info["start_time"],
                    large_image="kick_logo",
                    large_text=self.get_text("rpc_streaming"),
                    small_image="verified",
                    small_text=self.get_text("rpc_verified"),
                    buttons=buttons
                )
                self.log(f"[IPC] Status updated. Viewers: {info['viewers']}")
            except Exception as e:
                self.log(f"[IPC] Error updating Discord: {e}")
                
            for _ in range(30):
                if not self.running:
                    break
                time.sleep(1)
        
        if self.rpc:
            self.rpc.close()

    def start_rpc(self):
        while self.running:
            try:
                self.update_rpc_loop()
            except Exception as e:
                if self.running:
                    self.log(f"[IPC] Connection lost or error: {e}")
                    time.sleep(5)

    # ==========================
    # CONTROLS
    # ==========================
    def start(self):
        if self.running:
            return
            
        self.start_time = int(time.time())
        self.running = True
        
        if self.mode == "1":
            threading.Thread(target=self.start_gateway, daemon=True).start()
        else:
            threading.Thread(target=self.start_rpc, daemon=True).start()

    def stop(self):
        self.running = False
        if self.ws and hasattr(self.ws, 'close'):
            self.ws.close()
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
        self.log("System stopped.")
