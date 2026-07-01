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
