# 🌉 3. JarvisOS Bridge Ekotizimi (`sessiya_connector`)

## 📌 Ekotizim Maqsadi
Masofadan turib (ayniqsa, Telegram orqali) serverdagi Antigravity AI Engine quvvatidan foydalanish, loyihalar qurish, ovozli xabarlar bilan muloqot qilish va live monitoring olib borish uchun to'liq modulli ko'prik yaratildi.

Joylashuvi: `/home/fayzillo/Desktop/sessiya_connector/`

---

## 🏗️ Arxitektura Qatlamlari

```text
[ Telegram Klient ] (Fayzillo / Nurmuhammad)
           │
           ▼
[ Telegram Bot Connector ] (@safira_support_bot)
           │
           ▼  (REST API / Navbat)
[ Backend API Bridge ] (Port: 15976) ─── [ Web UI Chat ] (Port: 15977)
           │
           ▼  (Antigravity CLI SDK)
[ JarvisOS Core AI Engine ] (Gemini 3.7 / 3.8 Flash)
           │
           ▼
[ Server Shell / Git Pipeline / Rootless Docker ]
```

---

## 🔑 Asosiy Modullar va Imkoniyatlar

### 1. Backend API Bridge (`backend/` - Port: `15976`)
- **Texnologiya:** Node.js + Express + Prisma ORM + Antigravity CLI SDK.
- **Vazifasi:** API so'rovlarini qabul qilish, sessiyalarni boshqarish va buyruqlarni navbat (Queue) orqali AIga uzatish.
- **Ma'lumotlar Bazasi:** Serverless Neon Postgres (`schema=bot_post`) + Upstash Cloud Redis (TLS shifrlangan kesh).
- **Muhim Endpointlar:**
  - `POST /api/message` — Yangi buyruq yuborish;
  - `GET /api/events` — Server-Sent Events (SSE) jonli striming;
  - `GET /api/status` — Server va AI sessiyalari salomatligi;
  - `POST /api/approval` — Xavfli buyruqlarni tasdiqlash / rad etish.

### 2. Frontend Web Chat (`front/` - Port: `15977`)
- **Texnologiya:** HTML5 / CSS3 / JavaScript (SPA).
- **Vazifasi:** Veb-brauzer orqali to'g'ridan-to'g'ri AI bilan jonli suhbat, kod bloklarini sintaksis ranglash (highlighting) va javoblarni render qilish.

### 3. Telegram Bot Connector (`bot/` - `@safira_support_bot`)
- **Autentifikatsiya va Ruxsatlar:**
  - `ALLOWED_USER_IDS`: Faqat tasdiqlangan foydalanuvchilar (`7463402937` - Fayzillo, `6455909710` - Nurmuhammad).
  - PIN kod himoyasi (`15975`) va maxfiy parol (`superAdminPass`).
- **Multi-User Izolyatsiyasi:**
  - Fayzillo: `ca9d4209-6f0f-47c1-b988-6e67955eb33b` (Core Engine boshqaruvi)
  - Nurmuhammad: `cc53fd3c-c51f-4360-b24c-020e0bdd40b4` (Alohida izolyatsiyalangan sessiya)
- **Ovozli Xabarlar (Voice / Audio):**
  - Telegram orqali yuborilgan ovozli xabarlar avtomatik yuklab olinadi, AI tomonidan tinglanadi va to'liq ovozli buyruq sifatida bajariladi.
- **YouTube Video/Audio Stream & Backup:**
  - `yt-dlp` va `Deno` orqali YouTube havolasini qabul qilish;
  - Avval zaxira kanaliga (`@upload_C`) Node.js stream orqali yuklash, so'ng chatga uzatish va diskni avtomatik tozalash.
- **Live Message Update Texnologiyasi:**
  - Vazifa boshlanishi bilan bitta xabar ochiladi (`⏳ [Amaliy Qadam]: ...`) va u jarayon davomida yangilanib boradi (chatni xabarlar bilan to'ldirmaydi).

### 4. PM2 Jarayonlar Boshqaruvi
Barcha modullar fonda uzluksiz (24/7) ishlaydi:
- `id: 0` — `sessiya-backend` (online, 15976)
- `id: 1` — `sessiya-bot` (online, Telegram polling)
- `id: 2` — `sessiya-front` (online, 15977)
