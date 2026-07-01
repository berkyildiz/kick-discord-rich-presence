import sys
from datetime import datetime
import webbrowser
import customtkinter as ctk
from PIL import Image

from ..utils.paths import resource_path
from ..locales.translations import LANGUAGES
from ..config.manager import load_config, save_config
from ..core.rpc import KickDiscordPresence

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

        self.presence = KickDiscordPresence(logger_callback=self.log_message, get_text_callback=self.get_text)
        
        try:
            self.iconbitmap(resource_path("assets/icon.ico"))
        except Exception:
            pass
        
        # Main grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.logs_visible = False

        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        self._load_config()
        self.update_ui_texts()

    def _load_config(self):
        settings = load_config()
        if settings:
            self.kick_entry.insert(0, settings.get("kick_username", ""))
            self.client_id_entry.insert(0, settings.get("client_id", ""))
            self.invite_entry.insert(0, settings.get("discord_invite", ""))
            self.token_entry.insert(0, settings.get("discord_token", ""))
            
            mode = settings.get("mode", "2")
            if mode == "1":
                self.mode1_radio.select()
            else:
                self.mode2_radio.select()
                
            self.lang = settings.get("language", "en")
            if self.lang not in LANGUAGES:
                self.lang = "en"

    def _save_config(self):
        data = {
            "kick_username": self.kick_entry.get().strip(),
            "client_id": self.client_id_entry.get().strip(),
            "discord_invite": self.invite_entry.get().strip(),
            "discord_token": self.token_entry.get().strip(),
            "mode": self.mode_var.get(),
            "language": self.lang
        }
        save_config(data)

    def toggle_language(self):
        self.lang = "tr" if self.lang == "en" else "en"
        self.update_ui_texts()
        self._save_config()

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
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w")
        
        try:
            self.logo_img = ctk.CTkImage(Image.open(resource_path("assets/icon.png")), size=(40, 40))
            self.logo_label = ctk.CTkLabel(logo_frame, text="", image=self.logo_img)
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print("Logo Error:", e)
        
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="e")
        
        self.lang_btn = ctk.CTkButton(nav_frame, text="", width=40, height=28, fg_color="#1f6aa5", hover_color="#144870", command=self.toggle_language)
        self.lang_btn.pack(side="left", padx=2)
        self.guide_btn = ctk.CTkButton(nav_frame, text="", width=60, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_wiki)
        self.guide_btn.pack(side="left", padx=2)
        self.faq_btn = ctk.CTkButton(nav_frame, text="", width=60, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_faq)
        self.faq_btn.pack(side="left", padx=2)
        self.legal_btn = ctk.CTkButton(nav_frame, text="", width=60, height=28, fg_color="#2b2b2b", hover_color="#3b3b3b", command=self.open_legal)
        self.legal_btn.pack(side="left", padx=2)

    def create_main_content(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        input_frame = ctk.CTkFrame(self.scroll_frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.kick_label = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.kick_label.pack(anchor="w", padx=15, pady=(15, 0))
        self.kick_entry = ctk.CTkEntry(input_frame, placeholder_text="xathena")
        self.kick_entry.pack(fill="x", padx=15, pady=2)
        self.kick_hint = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.kick_hint.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.client_id_label = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.client_id_label.pack(anchor="w", padx=15, pady=(5, 0))
        self.client_id_entry = ctk.CTkEntry(input_frame)
        self.client_id_entry.pack(fill="x", padx=15, pady=2)
        self.client_id_hint = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.client_id_hint.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.invite_label = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.invite_label.pack(anchor="w", padx=15, pady=(5, 0))
        self.invite_entry = ctk.CTkEntry(input_frame)
        self.invite_entry.pack(fill="x", padx=15, pady=2)
        self.invite_hint = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.invite_hint.pack(anchor="w", padx=15, pady=(0, 10))
        
        self.token_label = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.token_label.pack(anchor="w", padx=15, pady=(5, 0))
        self.token_entry = ctk.CTkEntry(input_frame, show="*")
        self.token_entry.pack(fill="x", padx=15, pady=2)
        self.token_hint = ctk.CTkLabel(input_frame, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.token_hint.pack(anchor="w", padx=15, pady=(0, 15))
        
        mode_frame = ctk.CTkFrame(self.scroll_frame)
        mode_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        
        self.mode_label = ctk.CTkLabel(mode_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.mode_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.mode_var = ctk.StringVar(value="2")
        self.mode1_radio = ctk.CTkRadioButton(mode_frame, text="", variable=self.mode_var, value="1", fg_color="#9b59b6", hover_color="#8e44ad")
        self.mode1_radio.pack(anchor="w", padx=15, pady=5)
        
        self.mode2_radio = ctk.CTkRadioButton(mode_frame, text="", variable=self.mode_var, value="2")
        self.mode2_radio.pack(anchor="w", padx=15, pady=(5, 15))

        btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="", fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(weight="bold", size=14), height=40, command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="", fg_color="#e74c3c", hover_color="#c0392b", font=ctk.CTkFont(weight="bold", size=14), height=40, state="disabled", command=self.on_stop)
        self.stop_btn.grid(row=0, column=1, padx=5, sticky="ew")

        log_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        log_container.grid(row=3, column=0, sticky="ew", padx=5, pady=(15, 0))
        
        self.log_toggle_btn = ctk.CTkButton(log_container, text="", width=120, height=24, fg_color="transparent", border_width=1, command=self.toggle_logs)
        self.log_toggle_btn.pack(pady=5)
        
        self.log_textbox = ctk.CTkTextbox(log_container, height=120, state="disabled", font=ctk.CTkFont(family="Consolas", size=11))
        
    def create_footer(self):
        footer = ctk.CTkFrame(self, height=30, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew")
        self.copy_label = ctk.CTkLabel(footer, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.copy_label.pack(pady=5)

    def toggle_logs(self):
        self.logs_visible = not self.logs_visible
        if self.logs_visible:
            self.log_textbox.pack(fill="x", padx=5, pady=5)
        else:
            self.log_textbox.pack_forget()
        self.log_toggle_btn.configure(text=self.get_text("hide_logs") if self.logs_visible else self.get_text("show_logs"))

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", formatted)
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def on_start(self):
        kick_user = self.kick_entry.get().strip()
        client_id = self.client_id_entry.get().strip()
        token = self.token_entry.get().strip()
        invite = self.invite_entry.get().strip()
        
        if not kick_user:
            self.log_message(self.get_text("err_username"))
            return
            
        self._save_config()
        
        self.presence.kick_username = kick_user
        self.presence.client_id = client_id
        self.presence.discord_invite = invite
        self.presence.token = token
        self.presence.mode = self.mode_var.get()
        
        self.start_btn.configure(state="disabled", text="RUNNING...")
        self.stop_btn.configure(state="normal")
        self.kick_entry.configure(state="disabled")
        self.client_id_entry.configure(state="disabled")
        self.invite_entry.configure(state="disabled")
        self.token_entry.configure(state="disabled")
        self.mode1_radio.configure(state="disabled")
        self.mode2_radio.configure(state="disabled")
        
        self.log_message("Starting XATI...")
        self.presence.start()

    def on_stop(self):
        self.presence.stop()
        self.start_btn.configure(state="normal", text=self.get_text("start"))
        self.stop_btn.configure(state="disabled")
        self.kick_entry.configure(state="normal")
        self.client_id_entry.configure(state="normal")
        self.invite_entry.configure(state="normal")
        self.token_entry.configure(state="normal")
        self.mode1_radio.configure(state="normal")
        self.mode2_radio.configure(state="normal")

    def open_wiki(self):
        self.show_info_window(self.get_text("wiki_title"), self.get_text("wiki_text"))
        
    def open_faq(self):
        self.show_info_window(self.get_text("faq_title"), self.get_text("faq_text"))

    def open_legal(self):
        self.show_info_window(self.get_text("legal_title"), self.get_text("legal_text"))

    def show_info_window(self, title, text):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("500x600")
        try:
            win.iconbitmap(resource_path("assets/icon.ico"))
        except Exception:
            pass
        win.grid_columnconfigure(0, weight=1)
        win.grid_rowconfigure(0, weight=1)
        
        textbox = ctk.CTkTextbox(win, wrap="word", font=ctk.CTkFont(size=13))
        textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
        
        btn = ctk.CTkButton(win, text="CLOSE", command=win.destroy)
        btn.grid(row=1, column=0, pady=10)
