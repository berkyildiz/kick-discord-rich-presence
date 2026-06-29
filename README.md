# 🟢 Kick Discord Rich Presence (RPC)

<div align="center">
  
  ![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
  ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
  ![Language](https://img.shields.io/badge/Language-English%20%7C%20Turkish-orange.svg)
  ![Developed By](https://img.shields.io/badge/Developed_by-Berk_YILDIZ_XATHENA-purple.svg)

  **The ultimate, lightweight, and Cloudflare-bypassing Python script to sync your Kick.com livestream status directly to your Discord profile.**
  <br />
  <a href="#english-instructions">🇬🇧 English</a> &nbsp;&middot;&nbsp; <a href="#türkçe-talimatlar">🇹🇷 Türkçe</a>
</div>

---

<h2 id="english-instructions">🇬🇧 English Instructions</h2>

### What is this?
**Kick Discord Rich Presence** automatically detects when you are live on Kick.com and instantly updates your Discord profile to show the prestigious purple "Streaming" status. It fetches your live viewers, stream title, category, and elapsed time dynamically!

### 🌟 Features
- **Cloudflare Bypass:** Uses `curl-cffi` to flawlessly fetch API data from Kick.com without getting blocked.
- **Production-Ready & Clean Code:** Built with SOLID, DRY, and KISS principles. Highly optimized and memory efficient.
- **Always Purple:** Forces the "Streaming" status even if you are offline, or intelligently switches when you go live.
- **Multi-Language Support:** Fully supports English and Turkish logs/statuses.
- **Standalone Executable:** Run it directly on Windows without installing Python!

### ⚙️ How to Use (Pre-Compiled EXE)
1. Download `KickDiscordPresence.exe` from the **[Releases](../../releases)** tab.
2. Create a `.env` file in the same folder as the `.exe`.
3. Fill your `.env` file like this:
   ```env
   DISCORD_TOKEN=YOUR_DISCORD_TOKEN_HERE
   KICK_USERNAME=YOUR_KICK_USERNAME_HERE
   LANGUAGE=EN
   ```
4. Run `KickDiscordPresence.exe`!

### 🔑 How to get your Tokens
- **DISCORD_TOKEN**: Open Discord in your browser, press `F12` to open Developer Tools, go to the **Network** tab, and type `science` in the filter. Click on any request and look for `Authorization` under **Request Headers**. That text is your token.
- **KICK_USERNAME**: Go to your Kick.com profile. Your username is the part at the end of the URL (e.g., `kick.com/YOUR_USERNAME`).

> [!WARNING]
> **Security Notice:** This application connects via the Discord Gateway using a user token (Self-botting), which is technically against Discord's Terms of Service. Use at your own risk. Do not share your `.env` file or Discord token with anyone!

---

<h2 id="türkçe-talimatlar">🇹🇷 Türkçe Talimatlar</h2>

### Bu nedir?
**Kick Discord Rich Presence**, Kick.com üzerinde yayın açtığınızı otomatik olarak algılar ve Discord profilinizi anında mor renkli "Yayın Yapıyor" durumuna geçirir. Canlı izleyici sayınızı, yayın başlığınızı, kategorinizi ve yayında geçen süreyi dinamik olarak gösterir!

### 🌟 Özellikler
- **Cloudflare Bypass:** `curl-cffi` altyapısı ile Kick.com'un güvenlik duvarını hatasız aşar.
- **Clean Code & Optimize:** SOLID prensipleriyle baştan yazılmış, sıfır gereksiz kod barındıran mimari.
- **Mor Durum:** İsterseniz çevrimdışıyken bile Discord'da havalı mor ikonla gözükün.
- **Çoklu Dil:** %100 Türkçe dil desteği.
- **Kurulumsuz EXE:** Python kurmanıza gerek kalmadan tek tıklamayla çalışır!

### ⚙️ Nasıl Kullanılır (Hazır EXE ile)
1. **[Releases](../../releases)** sekmesinden `KickDiscordPresence.exe` dosyasını indirin.
2. EXE'nin olduğu klasöre `.env` isminde bir dosya oluşturun.
3. İçini şu şekilde doldurun:
   ```env
   DISCORD_TOKEN=DISCORD_TOKEN_BURAYA
   KICK_USERNAME=KICK_KULLANICI_ADI_BURAYA
   LANGUAGE=TR
   ```
4. `KickDiscordPresence.exe`'yi çalıştırın!

### 🔑 Token ve Bilgilerinizi Nasıl Alırsınız?
- **DISCORD_TOKEN**: Tarayıcınızdan Discord'a girin, Geliştirici Araçlarını açın (`F12`), **Ağ (Network)** sekmesine gelin. Filtreye `science` yazın, çıkan isteklerden birine tıklayın ve **Request Headers** kısmındaki `Authorization` değerini kopyalayın. Bu sizin tokeninizdir.
- **KICK_USERNAME**: Kick.com profilinize girin. URL'nin sonundaki isim sizin kullanıcı adınızdır (örneğin `kick.com/KULLANICI_ADINIZ`).

> [!WARNING]
> **Güvenlik Uyarısı:** Bu yazılım, Discord sistemine kullanıcı tokeniniz üzerinden bağlanır (Self-bot). Bu durum Discord Kullanım Şartlarına (TOS) aykırı olabilir. Tüm sorumluluk kullanıcıya aittir. `DISCORD_TOKEN` bilginizi ASLA kimseyle paylaşmayın!

---

<div align="center">
  <b>Developed with ❤️ by Berk YILDIZ XATHENA</b><br>
  <i>Copyright (c) 2026</i>
</div>
