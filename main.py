import os
import sys
import time
import json
import threading
import webbrowser
from datetime import datetime, timezone

from curl_cffi import requests
import websocket
import websocket
from pypresence import Presence
import customtkinter as ctk
from PIL import Image

# Reconfigure stdout for UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

KICK_API_BASE = "https://kick.com/api/v2/channels/"
DISCORD_GATEWAY = "wss://gateway.discord.gg/?v=9&encoding=json"
TWITCH_DUMMY_URL = "https://twitch.tv/xathenaone"
CONFIG_FILE = "config.json"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


LANGUAGES = {
    'en': {
        'title': 'XATI',
        'guide_btn': '📘 Guide / Wiki',
        'faq_btn': '❓ FAQ',
        'legal_btn': '⚖️ Legal & TOS',
        'kick_username': 'Kick Username:',
        'kick_username_hint': '💡 E.g: xathena',
        'client_id': 'Discord Client ID:',
        'client_id_hint': '💡 E.g: 1324103130983207033',
        'discord_invite': 'Discord Invite Link:',
        'discord_invite_hint': '💡 E.g: https://discord.gg/yourserver (For Mode 2)',
        'token': 'Discord Token (Mode 1):',
        'token_hint': '💡 Only needed for Mode 1 (Purple Color)',
        'mode_title': 'Select Presence Mode:',
        'mode_1': 'Mode 1: Gateway (Purple Color, No Custom Buttons)',
        'mode_2': 'Mode 2: IPC (Normal Color, Clickable Buttons & Images)',
        'start': 'START',
        'stop': 'STOP',
        'logs': 'System Logs:',
        'show_logs': '🔽 Show Logs',
        'hide_logs': '🔼 Hide Logs',
        'footer_copy': '© 2026 Berk Yıldız',
        'err_token': 'ERROR: Discord Token is required for Mode 1!',
        'err_username': 'ERROR: Please enter your Kick Username!',
        'err_discord': '[ERROR] Discord not found! Is Discord open?',
        'log_connected': 'Discord Gateway connected. (Purple Color Active)',
        'log_disconnected': 'Gateway disconnected. Reconnecting in 5 seconds...',
        'log_ipc_connected': 'Discord Desktop (IPC) connected. (Buttons Active)',
        'log_asset_fail': '[Gateway] Failed to resolve Asset ID:',
        'log_settings_fail': 'Failed to load settings:',
        'log_settings_save_fail': 'Failed to save settings:',
        'log_fetch_fail': 'Error fetching Kick data:',
        'log_gateway_update': '[Gateway] Status updated. Viewers:',
        'log_ipc_update': '[IPC] Status updated. Title:',
        'rpc_streaming': 'Streaming on Kick!',
        'rpc_verified': 'Verified Streamer',
        'rpc_join': 'Join Stream!',
        'rpc_discord': 'Our Discord Server',
        'rpc_live': '🔴 LIVE',
        'rpc_live_kick': '🔴 LIVE (Kick.com)',
        'rpc_viewers': 'Viewers',
        'wiki_title': 'Guide / Wiki',
        'faq_title': 'FAQ',
        'legal_title': 'Legal & TOS',
        'wiki_text': """📘 KICK DISCORD RICH PRESENCE - GUIDE & WIKI

# How to use?
1. Paste your Application ID from Discord Developer Portal into the Client ID field.
2. If using Mode 1, you must enter your Discord Token. (Found via browser console).
3. Mode 2 doesn't require a Token, it works natively via Discord Desktop.
4. After entering details, click the START button.

# How to upload Assets?
1. Go to discord.com/developers/applications
2. Select your app -> Rich Presence -> Art Assets.
3. Upload your large image named EXACTLY 'kick_logo'.
4. Upload your small image (verified tick) named EXACTLY 'verified'.
5. Save changes.

# Privacy & Security
- None of your info (Token, Client ID) is shared over the internet or with 3rd parties.
- All data is saved locally to 'config.json'.
""",
        'faq_text': """❓ FREQUENTLY ASKED QUESTIONS (FAQ)

Q: Why can't I see my own buttons?
A: Discord rules prevent the account running the Rich Presence from clicking or seeing its own buttons. To test if they work, ask a friend or check from an alt account.

Q: Why can't I add custom buttons in Mode 1?
A: Mode 1 (Gateway) only allows a single Watch button globally by Discord.

Q: Why does the purple color go away if I put a Kick link in Watch?
A: Discord only colorizes twitch.tv and youtube.com links purple. That's why we send a dummy twitch link in Mode 1. Use Mode 2 for real clickable links.

Q: Will my presence disappear if I close the app?
A: Yes, this app must remain open in the background.
""",
        'legal_text': """⚖️ LEGAL, TOS & PRIVACY POLICY

TERMS OF SERVICE:
- Provided 'AS IS' without warranty.
- Mode 1 requires a Discord user token. Using self-bots is against Discord TOS. The user assumes all risks using Mode 1. We recommend Mode 2 (IPC) for complete safety.

PRIVACY POLICY:
- This app DOES NOT send your data anywhere.
- Config is saved locally unencrypted in 'config.json'.
- No telemetry or external tracking exists. Connects only to Kick API (for stream status) and Discord API.

LEGAL NOTICE:
- Not affiliated with Kick or Discord.
"""
    },
    'tr': {
        'title': 'XATI',
        'guide_btn': '📘 Rehber / Wiki',
        'faq_btn': '❓ S.S.S',
        'legal_btn': '⚖️ Yasal Bilgiler',
        'kick_username': 'Kick Kullanıcı Adı:',
        'kick_username_hint': '💡 Örn: xathena',
        'client_id': 'Discord Client ID:',
        'client_id_hint': '💡 Örn: 1324103130983207033',
        'discord_invite': 'Discord Davet Linki:',
        'discord_invite_hint': '💡 Örn: https://discord.gg/sunucunuz (Sadece Mod 2)',
        'token': 'Discord Token (Mod 1):',
        'token_hint': '💡 Sadece Mod 1 (Mor Renk) için gereklidir.',
        'mode_title': 'Çalışma Modunu Seçin:',
        'mode_1': 'Mod 1: Gateway (Mor Renk Modu, Özel Buton Yok)',
        'mode_2': 'Mod 2: IPC (Normal Renk, Tıklanabilir Butonlar & Resimler)',
        'start': 'BAŞLAT',
        'stop': 'DURDUR',
        'logs': 'Sistem Kayıtları (Logs):',
        'show_logs': '🔽 Logları Göster',
        'hide_logs': '🔼 Logları Gizle',
        'footer_copy': '© 2026 Berk Yıldız',
        'err_token': 'HATA: Mor renk modu için Discord Token gereklidir!',
        'err_username': 'HATA: Lütfen Kick Kullanıcı Adınızı girin!',
        'err_discord': '[HATA] Discord bulunamadı! Discord açık mı?',
        'log_connected': 'Discord Gateway bağlantısı kuruldu. (Mor Renk Aktif)',
        'log_disconnected': 'Gateway bağlantısı koptu. 5 saniye içinde tekrar bağlanılıyor...',
        'log_ipc_connected': 'Discord Masaüstü (IPC) bağlantısı kuruldu. (Butonlar Aktif)',
        'log_asset_fail': '[Gateway] Asset ID çekilemedi:',
        'log_settings_fail': 'Ayarlar yüklenemedi:',
        'log_settings_save_fail': 'Ayarlar kaydedilemedi:',
        'log_fetch_fail': 'Kick verisi alınırken hata:',
        'log_gateway_update': '[Gateway] Durum güncellendi. İzleyici:',
        'log_ipc_update': '[IPC] Durum güncellendi. Başlık:',
        'rpc_streaming': 'Kick\'te Yayındayım!',
        'rpc_verified': 'Onaylı Yayıncı',
        'rpc_join': 'Yayına Katıl!',
        'rpc_discord': 'Discord Sunucumuz',
        'rpc_live': '🔴 YAYINDA',
        'rpc_live_kick': '🔴 YAYINDA (Kick.com)',
        'rpc_viewers': 'İzleyici',
        'wiki_title': 'Rehber / Wiki',
        'faq_title': 'S.S.S (Sıkça Sorulan Sorular)',
        'legal_title': 'Yasal Bilgiler',
        'wiki_text': """📘 KICK DISCORD RICH PRESENCE - REHBER & WIKI

# Nasıl Kullanılır?
1. Client ID kısmına Discord Developer Portal'dan aldığınız uygulamanın Application ID'sini yapıştırın.
2. Mod 1'i kullanacaksanız Discord Token'ınızı bulup girmeniz gerekir.
3. Mod 2'de Token'a ihtiyacınız yoktur, direkt çalışır.
4. Bilgilerinizi girdikten sonra "Başlat" butonuna tıklamanız yeterlidir.

# Resimler (Assets) Nasıl Yüklenir?
1. discord.com/developers/applications adresine gidin.
2. Uygulamanızı seçin ve "Rich Presence" -> "Art Assets" kısmına gelin.
3. Büyük resim için dosya adını TAM OLARAK "kick_logo" yapıp yükleyin.
4. Küçük resim (onay tiki vb.) için adını TAM OLARAK "verified" yapıp yükleyin.
5. Save Changes butonuna basın.

# Güvenlik ve Gizlilik
- Hiçbir bilginiz (Token, Client ID) internet üzerinden bizimle veya 3. şahıslarla paylaşılmaz.
- Tüm verileriniz sadece kendi bilgisayarınızdaki "config.json" dosyasına kaydedilir.
""",
        'faq_text': """❓ SIKÇA SORULAN SORULAR (S.S.S)

Soru: Neden Kendi Butonlarımı Göremiyorum?
Cevap: Discord kuralları gereği, Rich Presence açan hesap kendi butonlarına basamaz ve butonları profilinde göremez.

Soru: Mor Modda Neden Kendi Butonlarımı Ekleyemiyorum?
Cevap: Mor Mod (Gateway) sadece TEK BİR buton olan "İzle" (Watch) butonuna izin verir.

Soru: Mor Moddaki İzle Butonuna Neden Kick Linkimi Koyunca Mor Renk Gidiyor?
Cevap: Discord, sadece "Twitch.tv" ve "YouTube.com" linklerini Resmi Canlı Yayın olarak algılar. "Kick.com" linki eklerseniz rengi griye çevirir. Bu yüzden sahte bir Twitch linki gönderiyoruz.

Soru: Uygulamayı kapatırsam Rich Presence gider mi?
Cevap: Evet, uygulamanın arka planda açık kalması gerekmektedir.
""",
        'legal_text': """⚖️ YASAL BİLGİLER, TOS & GİZLİLİK POLİTİKASI

KULLANIM ŞARTLARI (TOS):
- Bu yazılım "OLDUĞU GİBİ" (AS IS) hiçbir garanti verilmeden sunulmaktadır.
- Discord Gateway (Mor Mod) kullanımı sırasında Discord hesabınızın Token'ı gereklidir. Kendi token'ınızla otomasyon kullanmak Discord Hizmet Şartları'na aykırı olabilir (Self-bot kuralları). Sorumluluk kullanıcıya aittir.

GİZLİLİK POLİTİKASI (PRIVACY POLICY):
- Uygulama KESİNLİKLE internete veri göndermez.
- Girdiğiniz Token, Client ID ve diğer bilgiler bilgisayarınızdaki "config.json" dosyasına kaydedilir. 

LEGAL NOTICE:
- Bu uygulama Kick veya Discord tarafından resmi olarak desteklenmemekte, onaylanmamakta veya ilişkisi bulunmamaktadır.
"""
    }
}


class KickDiscordPresence:
    def __init__(self, logger_callback=None):
        self.logger = logger_callback
        self.app = None
        self.running = False
        
        self.kick_username = ""
        self.client_id = ""
        self.discord_invite = ""
        self.token = ""
        self.mode = "2" # Default IPC
        
        self.start_time = int(time.time())
        self.ws = None
        self.rpc = None
        

    def get_text(self, key):
        if not hasattr(self, 'app') or not self.app: return LANGUAGES['en'].get(key, key)
        return LANGUAGES[self.app.lang].get(key, key)

    def log(self, message):
        if self.logger:
            self.logger(message)
        else:
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
                    start_ts = self.start_time
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
                        "title": livestream.get("session_title", self.get_text("rpc_live")),
                        "category": category,
                        "viewers": livestream.get("viewer_count", 0),
                        "start_time": start_ts
                    }
        except Exception as e:
            self.log(f"{self.get_text('log_fetch_fail')} {e}")
            
        return {
            "is_live": False,
            "title": self.get_text("rpc_live_kick"), 
            "category": "IRL",
            "viewers": 0,
            "start_time": self.start_time
        }

    # ==========================
    # MODE 1: GATEWAY (MOR RENK)
    # ==========================
    def update_gateway_loop(self):
        while self.running:
            if not self.ws or not getattr(self.ws, 'sock', None) or not self.ws.sock.connected:
                break
                
            info = self.fetch_kick_data()
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
            info = self.fetch_kick_data()
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
                self.log(f"[IPC] Durum güncellendi. İzleyici: {info['viewers']}")
            except Exception as e:
                self.log(f"[IPC] Discord güncellenirken hata: {e}")
                
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
                    self.log(f"[IPC] Bağlantı koptu veya hata oluştu: {e}")
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
        self.log("Sistem durduruldu.")

# ==========================================
# GUI APPLICATION (CustomTkinter)
# ==========================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.lang = "en"
        self.title("XATI - Kick Discord Rich Presence")
        
        # Responsive size setup
        self.geometry("600x700")
        self.minsize(450, 500)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.presence = KickDiscordPresence(logger_callback=self.log_message)
        self.presence.app = self
        
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        # Main grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.logs_visible = False

        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        self.load_config()
        self.update_ui_texts()

    def toggle_language(self):
        self.lang = "tr" if self.lang == "en" else "en"
        self.update_ui_texts()
        self.save_config()

    def get_text(self, key):
        return LANGUAGES.get(self.lang, LANGUAGES['en']).get(key, key)

    def update_ui_texts(self):
        self.lang_btn.configure(text="🇹🇷 TR" if self.lang == "en" else "🇬🇧 EN")
        self.guide_btn.configure(text=self.get_text("guide_btn"))
        self.faq_btn.configure(text=self.get_text("faq_btn"))
        self.legal_btn.configure(text=self.get_text("legal_btn"))
        
        self.kick_label.configure(text=self.get_text("kick_username"))
        self.kick_hint.configure(text=self.get_text("kick_username_hint"))
        self.client_id_label.configure(text=self.get_text("client_id"))
        self.client_id_hint.configure(text=self.get_text("client_id_hint"))
        self.invite_label.configure(text=self.get_text("discord_invite"))
        self.invite_hint.configure(text=self.get_text("discord_invite_hint"))
        self.token_label.configure(text=self.get_text("token"))
        self.token_hint.configure(text=self.get_text("token_hint"))
        
        self.mode_label.configure(text=self.get_text("mode_title"))
        self.mode1_radio.configure(text=self.get_text("mode_1"))
        self.mode2_radio.configure(text=self.get_text("mode_2"))
        
        if self.presence.running:
            pass
        else:
            self.start_btn.configure(text=self.get_text("start"))
            self.stop_btn.configure(text=self.get_text("stop"))
        
        self.log_toggle_btn.configure(text=self.get_text("hide_logs") if self.logs_visible else self.get_text("show_logs"))
        self.copy_label.configure(text=self.get_text("footer_copy"))

    def create_header(self):
        # Ultra-compact modern header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        
        # Responsive columns
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        
        # Logo + Title
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w")
        
        try:
            self.logo_img = ctk.CTkImage(Image.open(resource_path("icon.png")), size=(40, 40))
            self.logo_label = ctk.CTkLabel(logo_frame, text="", image=self.logo_img)
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Logo Error:", e)
        
        # Action Buttons
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="e")
        
        # Modern tight spacing
        self.lang_btn = ctk.CTkButton(nav_frame, text="", width=40, height=28, fg_color="#1f6aa5", hover_color="#144870", command=self.toggle_language)
        self.lang_btn.pack(side="left", padx=2)

        self.guide_btn = ctk.CTkButton(nav_frame, text="", width=60, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_wiki)
        self.guide_btn.pack(side="left", padx=2)
        self.faq_btn = ctk.CTkButton(nav_frame, text="", width=50, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_faq)
        self.faq_btn.pack(side="left", padx=2)
        self.legal_btn = ctk.CTkButton(nav_frame, text="", width=80, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_legal)
        self.legal_btn.pack(side="left", padx=2)

    def create_main_content(self):
        # A scrollable frame ensures UI never breaks on small windows
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_scroll.grid_columnconfigure(0, weight=1)

        content_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        content_container.grid(row=0, column=0, sticky="ew")
        content_container.grid_columnconfigure(1, weight=1)

        # 1. Inputs
        self.kick_label = ctk.CTkLabel(content_container, text="", font=ctk.CTkFont(weight="bold", size=12))
        self.kick_label.grid(row=0, column=0, sticky="w", pady=(5, 0), padx=5)
        self.kick_entry = ctk.CTkEntry(content_container, placeholder_text="xathena", height=32)
        self.kick_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=(5, 0))
        self.kick_hint = ctk.CTkLabel(content_container, text="", text_color="gray50", font=ctk.CTkFont(size=11))
        self.kick_hint.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 10))

        self.client_id_label = ctk.CTkLabel(content_container, text="", font=ctk.CTkFont(weight="bold", size=12))
        self.client_id_label.grid(row=2, column=0, sticky="w", pady=(0, 0), padx=5)
        self.client_id_entry = ctk.CTkEntry(content_container, placeholder_text="1324103130983207033", height=32)
        self.client_id_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=(0, 0))
        self.client_id_hint = ctk.CTkLabel(content_container, text="", text_color="gray50", font=ctk.CTkFont(size=11))
        self.client_id_hint.grid(row=3, column=1, sticky="w", padx=5, pady=(0, 10))

        self.invite_label = ctk.CTkLabel(content_container, text="", font=ctk.CTkFont(weight="bold", size=12))
        self.invite_label.grid(row=4, column=0, sticky="w", pady=(0, 0), padx=5)
        self.invite_entry = ctk.CTkEntry(content_container, placeholder_text="https://discord.gg/...", height=32)
        self.invite_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=(0, 0))
        self.invite_hint = ctk.CTkLabel(content_container, text="", text_color="gray50", font=ctk.CTkFont(size=11))
        self.invite_hint.grid(row=5, column=1, sticky="w", padx=5, pady=(0, 10))

        self.token_label = ctk.CTkLabel(content_container, text="", font=ctk.CTkFont(weight="bold", size=12))
        self.token_label.grid(row=6, column=0, sticky="w", pady=(0, 0), padx=5)
        self.token_entry = ctk.CTkEntry(content_container, placeholder_text="MTEz...", show="*", height=32)
        self.token_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=(0, 0))
        self.token_hint = ctk.CTkLabel(content_container, text="", text_color="gray50", font=ctk.CTkFont(size=11))
        self.token_hint.grid(row=7, column=1, sticky="w", padx=5, pady=(0, 15))

        # 2. Mode Selection
        mode_frame = ctk.CTkFrame(content_container, fg_color="#2b2b2b", corner_radius=8)
        mode_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 15))
        
        self.mode_label = ctk.CTkLabel(mode_frame, text="", font=ctk.CTkFont(weight="bold", size=13))
        self.mode_label.pack(anchor="w", padx=15, pady=(8, 5))
        
        self.mode_var = ctk.StringVar(value="2")
        self.mode1_radio = ctk.CTkRadioButton(mode_frame, text="", variable=self.mode_var, value="1", radiobutton_width=18, radiobutton_height=18)
        self.mode1_radio.pack(anchor="w", padx=20, pady=(0, 8))
        self.mode2_radio = ctk.CTkRadioButton(mode_frame, text="", variable=self.mode_var, value="2", radiobutton_width=18, radiobutton_height=18)
        self.mode2_radio.pack(anchor="w", padx=20, pady=(0, 10))

        # 3. Actions (Start/Stop)
        btn_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, sticky="ew", padx=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="", height=45, font=ctk.CTkFont(weight="bold", size=14), fg_color="#28a745", hover_color="#218838", command=self.start_app)
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="", height=45, font=ctk.CTkFont(weight="bold", size=14), fg_color="#dc3545", hover_color="#c82333", state="disabled", command=self.stop_app)
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # 4. Log Toggle
        self.log_toggle_btn = ctk.CTkButton(content_container, text="", height=28, fg_color="transparent", hover_color="#333333", text_color="#1f6aa5", command=self.toggle_logs)
        self.log_toggle_btn.grid(row=10, column=0, columnspan=2, pady=(15, 5))
        
        # 5. Log Box (Initially Hidden)
        self.log_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_box = ctk.CTkTextbox(self.log_frame, height=120, state="disabled", font=ctk.CTkFont(family="Consolas", size=11), fg_color="#1e1e1e")
        self.log_box.grid(row=0, column=0, sticky="ew")

    def toggle_logs(self):
        self.logs_visible = not self.logs_visible
        if self.logs_visible:
            self.log_frame.grid(row=11, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 10))
        else:
            self.log_frame.grid_remove()
        self.update_ui_texts()

    def create_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        self.copy_label = ctk.CTkLabel(footer_frame, text="", text_color="gray50", font=ctk.CTkFont(size=11))
        self.copy_label.grid(row=0, column=0, sticky="w")
        
        git_label = ctk.CTkLabel(footer_frame, text="GitHub: berkyildiz/kick-discord-rich-presence", text_color="#1f6aa5", cursor="hand2", font=ctk.CTkFont(size=11, underline=True))
        git_label.grid(row=0, column=1, sticky="e")
        git_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/berkyildiz/kick-discord-rich-presence"))

    def create_modal(self, title, text_content):
        modal = ctk.CTkToplevel(self)
        modal.title(title)
        modal.geometry("550x450")
        modal.attributes("-topmost", True)
        modal.grid_columnconfigure(0, weight=1)
        modal.grid_rowconfigure(0, weight=1)
        
        textbox = ctk.CTkTextbox(modal, wrap="word", font=ctk.CTkFont(size=13), fg_color="#1e1e1e")
        textbox.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        textbox.insert("0.0", text_content)
        textbox.configure(state="disabled")

    def open_wiki(self):
        self.create_modal(self.get_text("wiki_title"), self.get_text("wiki_text"))

    def open_faq(self):
        self.create_modal(self.get_text("faq_title"), self.get_text("faq_text"))

    def open_legal(self):
        self.create_modal(self.get_text("legal_title"), self.get_text("legal_text"))

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {message}\\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.kick_entry.insert(0, config.get("kick_username", ""))
                    self.client_id_entry.insert(0, config.get("client_id", "1521219374873317427"))
                    self.invite_entry.insert(0, config.get("discord_invite", ""))
                    self.token_entry.insert(0, config.get("token", ""))
                    self.mode_var.set(config.get("mode", "2"))
                    self.lang = config.get("lang", "en")
            except Exception as e:
                self.log_message(f"{self.get_text('log_settings_fail')} {e}")

    def save_config(self):
        config = {
            "kick_username": self.kick_entry.get().strip(),
            "client_id": self.client_id_entry.get().strip(),
            "discord_invite": self.invite_entry.get().strip(),
            "token": self.token_entry.get().strip(),
            "mode": self.mode_var.get(),
            "lang": getattr(self, "lang", "en")
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            self.log_message(f"{self.get_text('log_settings_save_fail')} {e}")

    def start_app(self):
        self.save_config()
        
        kick_user = self.kick_entry.get().strip()
        client_id = self.client_id_entry.get().strip()
        
        if not kick_user:
            self.log_message(self.get_text("err_username"))
            # Auto show logs on error
            if not self.logs_visible:
                self.toggle_logs()
            return
            
        self.presence.kick_username = kick_user
        self.presence.client_id = client_id
        self.presence.discord_invite = self.invite_entry.get().strip()
        self.presence.token = self.token_entry.get().strip()
        self.presence.mode = self.mode_var.get()

        self.presence.start()
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.kick_entry.configure(state="disabled")
        self.client_id_entry.configure(state="disabled")
        self.invite_entry.configure(state="disabled")
        self.token_entry.configure(state="disabled")
        self.mode1_radio.configure(state="disabled")
        self.mode2_radio.configure(state="disabled")

    def stop_app(self):
        self.presence.stop()
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.kick_entry.configure(state="normal")
        self.client_id_entry.configure(state="normal")
        self.invite_entry.configure(state="normal")
        self.token_entry.configure(state="normal")
        self.mode1_radio.configure(state="normal")
        self.mode2_radio.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
