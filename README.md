# 🟢 XATI - Kick Discord Rich Presence (RPC)

<div align="center">
  <img src="icon.png" width="128" height="128" alt="XATI Logo">
  <br><br>
  
  ![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
  ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
  ![Language](https://img.shields.io/badge/Language-English%20%7C%20Turkish-orange.svg)
  ![Developed By](https://img.shields.io/badge/Developed_by-Berk_YILDIZ_XATHENA-purple.svg)

  **The ultimate, lightweight, UI-driven Python application to sync your Kick.com livestream status directly to your Discord profile.**
  <br />
  <a href="#english-instructions">🇬🇧 English</a> &nbsp;&middot;&nbsp; <a href="#türkçe-talimatlar">🇹🇷 Türkçe</a>
</div>

---

<h2 id="english-instructions">🇬🇧 English Instructions</h2>

### What is this?
**XATI** automatically detects when you are live on Kick.com and instantly updates your Discord profile to show your "Streaming" or "Playing" status. It fetches your live viewers, stream title, category, and elapsed time dynamically via a modern, easy-to-use graphical interface!

### 🌟 Features
- **Modern UI/UX:** A beautiful, responsive, and compact Graphical User Interface. No more `.env` files or confusing terminal windows.
- **Two Distinct Modes:** 
  - **Mode 1 (Gateway):** Forces the purple "Streaming" status even if you are offline.
  - **Mode 2 (IPC - Recommended):** Safely uses the Discord desktop app to show standard clickable rich presence buttons and custom image assets.
- **Auto-Save Config:** Your settings are securely saved locally to `config.json`.
- **Multi-Language Support:** Fully supports English and Turkish layouts.
- **Standalone Executable:** Run it directly on Windows without installing Python!

### ⚙️ How to Use (Pre-Compiled EXE)
1. Download `XATI.exe` from the **[Releases](../../releases)** tab.
2. Run `XATI.exe` (it will automatically create a `config.json` in the same folder to save your settings).
3. Fill in the fields in the UI (Kick Username, Discord Client ID). 
4. Select your Mode and click **START**!

### 🔑 Security & Legal
> [!IMPORTANT]
> **Mode 2 (IPC) is highly recommended** because it uses standard Discord Rich Presence, which is officially supported by Discord. 

> [!WARNING]
> **Mode 1 (Gateway) Security Notice:** Mode 1 connects via the Discord Gateway using a user token (Self-botting), which is against Discord's Terms of Service. Use at your own risk. This application NEVER shares your data anywhere over the internet.

---

<h2 id="türkçe-talimatlar">🇹🇷 Türkçe Talimatlar</h2>

### Bu nedir?
**XATI**, Kick.com üzerinde yayın açtığınızı otomatik olarak algılar ve Discord profilinizi anında günceller. Canlı izleyici sayınızı, yayın başlığınızı, kategorinizi ve yayında geçen süreyi yepyeni, kullanımı aşırı kolay görsel bir arayüzle dinamik olarak gösterir!

### 🌟 Özellikler
- **Modern Arayüz (GUI):** `.env` dosyalarıyla veya siyah komut satırlarıyla uğraşmanıza gerek yok. Modern ve şık bir arayüz!
- **İki Farklı Çalışma Modu:** 
  - **Mod 1 (Gateway):** Yayın açmasanız bile Discord profilinizi mor renkli "Yayın Yapıyor" durumuna zorlar.
  - **Mod 2 (IPC - Önerilen):** Standart Discord masaüstü uygulamanızı kullanarak profilinize güvenli bir şekilde tıklanabilir butonlar ve kapak fotoğrafları ekler.
- **Otomatik Kayıt:** Girdiğiniz bilgiler bir sonraki sefere otomatik hatırlanması için yerel olarak `config.json` dosyasına kaydedilir.
- **Çoklu Dil:** Tek tıkla İngilizce ve Türkçe arasında geçiş.
- **Kurulumsuz EXE:** Python kurmanıza gerek kalmadan tek tıklamayla çalışır!

### ⚙️ Nasıl Kullanılır (Hazır EXE ile)
1. **[Releases](../../releases)** sekmesinden `XATI.exe` dosyasını indirin.
2. `XATI.exe`'yi çalıştırın (ayarlarınızın kaydedilmesi için otomatik olarak bir `config.json` oluşturacaktır).
3. Arayüzdeki bilgileri doldurun (Kick Kullanıcı Adı, Discord Client ID vb.).
4. Kullanmak istediğiniz modu seçin ve **BAŞLAT** butonuna basın!

### 🔑 Güvenlik Uyarıları
> [!IMPORTANT]
> **Mod 2 (IPC) kullanmanızı kesinlikle öneririz**, çünkü resmi Discord Rich Presence altyapısını kullanır ve tamamen güvenlidir.

> [!WARNING]
> **Mod 1 (Gateway) Güvenlik Uyarısı:** Mod 1, Discord sistemine kullanıcı tokeniniz üzerinden bağlanır (Self-bot). Bu durum Discord Kullanım Şartlarına (TOS) aykırı olabilir. Tüm sorumluluk kullanıcıya aittir. Bu program bilgilerinizi ASLA internete veya 3. şahıslara göndermez.

---

<div align="center">
  <b>Developed with ❤️ by Berk YILDIZ XATHENA</b><br>
  <i>Copyright (c) 2026 - MIT License</i>
</div>
