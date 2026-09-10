# 🚀 ZDES Ekotizimi Deployment va Xavfsizlik Hisoboti | Ishchi Agent ID: `e7debb0d-eddb-42ca-bc35-da05af9061fe`

Ushbu hisobot **Fayzillo Ummatov**ning VPS serverida (`fayzillo@<HOST_NAME>`, IP: `<SERVER_IP>`) **ZDES (HR / Attendance / Payroll)** to'liq platformasini (Backend + Frontend) deploy qilish, izolyatsiyalash, domen va SSL bog'lash hamda mavjud barcha loyihalar xavfsizligini ta'minlash bo'yicha amalga oshirilgan barcha ishlarning yakuniy texnik hujjati hisoblanadi.

---

## 📌 1. Sessiya va Mas'ul Agent Ma'lumotlari
* **Ishchi Agent ID:** `e7debb0d-eddb-42ca-bc35-da05af9061fe`
* **Vazifa bajarilgan vaqt:** 10–11 Sentyabr, 2026-yil
* **Server muhiti:** Ubuntu Linux x86_64 (`<HOST_NAME>`)
* **Tashqi IPv4:** `<SERVER_IP>`
* **Boshqaruv maydoni:** `/home/fayzillo/Desktop/` (Server qoidalari asosida to'liq izolyatsiyalangan)

---

## 🏗️ 2. ZDES Platformasi Arxitekturasi va Sozlamalari

### A. Backend (`zdes_backend`):
* **Texnologiya:** NestJS 11 (Express), TypeScript, Prisma ORM.
* **Joylashuvi:** `/home/fayzillo/Desktop/Loyihalar/zdes_backend`
* **Konteynerlar (Docker Compose):**
  1. `zdes_backend_app`: NestJS API servisi (ichki tarmoqda `3000`-port).
  2. `zdes_backend_nginx`: Izolyatsiya qilingan Nginx reverse proxy (`127.0.0.1:15810:80`).
* **Ma'lumotlar bazasi:** Neon Cloud PostgreSQL (`<NEON_DB_ENDPOINT>`).
  * Mavjud ma'lumotlar: **1 012 ta foydalanuvchi**, **8 ta kompaniya**, to'liq tayyor sxemalar.
  * Ulanish: PgBouncer connection pooling (`&pgbouncer=true&connection_limit=5&pool_timeout=10`).
* **Kesh tizimi:** Upstash Cloud Redis (`<UPSTASH_REDIS_ENDPOINT>`, TLS).
  * Prefiks: `cache:<resource>:*` (boshqa botlarning `bull:*` va `session:*` kalitlaridan 100% izolyatsiya qilingan).
* **Statik fayllar (Uploads):**
  * Fayl yuklash server diskini to'ldirmasligi uchun hostdagi `/home/fayzillo/Desktop/temp/uploadss-zdes` katalogiga ulandi.
  * Nginx orqali yuqori tezlikda statik tarqatish yo'lga qo'yildi (`alias /app/uploads/`).
* **Xavfsizlik:** AWS kalitlari bo'lmaganda startda qulamasligi uchun maxsus dummy himoyasi qo'yildi.

### B. Frontend (`zdes_frontend`):
* **Texnologiya:** Angular 21 SSR (`@angular/ssr`), Node.js Express Server.
* **Repozitoriy:** `fummatov92/zdes-frontend` (GitHub CLI orqali yangi private repo yaratildi va kodlar tortib olindi).
* **Joylashuvi:** `/home/fayzillo/Desktop/Loyihalar/zdes_frontend`
* **Konteyner:** `zdes_frontend_app` (`127.0.0.1:15820:4000`).
* **API ulanishi:** `src/environments/environment.ts` dagi manzil `https://zdes-backend.safira.uz/api/v1` ga ulandi.

---

## 🌐 3. Domenlar, DNS va SSL Arxitekturasi (Caddy)

Barcha tashqi so'rovlar hostdagi **Caddy web-serveri** orqali boshqariladi:

| Xizmat | Domen | Ichki yo'naltirish | SSL Sertifikati | Holati |
| :--- | :--- | :--- | :---: | :---: |
| **ZDES Frontend** | `https://zdes.safira.uz` | `localhost:15820` | Let's Encrypt (Avtomatik) | **200 OK** |
| **ZDES Backend** | `https://zdes-backend.safira.uz` | `localhost:15810` | Let's Encrypt (Avtomatik) | **200 OK** |
| **Swagger Docs** | `https://zdes-backend.safira.uz/api/v1/docs` | `localhost:15810/api/v1/docs` | Let's Encrypt (Avtomatik) | **200 OK** (`login:[REDACTED]`) |

### Caddy Zero-Downtime protokoli:
Mavjud loyihalarga zarracha uzilish keltirmaslik uchun:
1. `sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak.*` (Zaxira nusxa olindi).
2. Yangi bloklar fayl oxiriga qo'shildi.
3. `caddy validate --config /etc/caddy/Caddyfile` orqali sintaksis to'liq tasdiqlandi.
4. `sudo systemctl reload caddy` orqali uzilishsiz qayta yuklandi.

---

## 🪵 4. Nginx Logger Infratuzilmasi (`/home/fayzillo/Desktop/logs/zdes/`)

Barcha HTTP trafigi va xatolar alohida log fayllariga yozilishi ta'minlandi:
* **Backend:** `/home/fayzillo/Desktop/logs/zdes/backend/`
  * `access.log` — barcha kelib tushayotgan HTTP so'rovlar (status, IP, vaqt, user-agent).
  * `error.log` — Nginx xato va ogohlantirishlari (`warn` darajasi va undan yuqori).
* **Frontend:** `/home/fayzillo/Desktop/logs/zdes/frontend/`
  * `access.log` — frontend Nginx reverse proxy so'rovlari.
  * `error.log` — frontend Nginx xato va ogohlantirishlari (`warn` darajasi va undan yuqori).
* **Host va Konteyner bog'liqligi:** Docker Compose orqali log papkalar hostdagi `/home/fayzillo/Desktop/logs/zdes/` ga bind mount qilingan, konteyner qayta o'chib-yonsa ham loglar saqlanib qoladi.

---

## 🛡️ 5. Serverdagi Boshqa Loyihalar Xavfsizligi va Kesh Auditi

Serverda ishlab turgan barcha parallel loyihalar xavfsizligi fakt-cheking asosida tekshirildi:
* **`mahala` (`localhost:4000`):**
  * Kod darajasida tekshirildi (`/opt/mahala/src/common/cache/cache.service.ts`).
  * Cache-aside (`wrap()`) va In-memory (`Map`) fallback mavjud — restart va kesh yo'qolishiga 100% chidamli.
* **`sifat` / `online-magazin` (`localhost:8090`):**
  * Kod darajasida tekshirildi (`grep -rn "redis"` ➔ bo'sh).
  * Redis yoki keshga mutlaqo bog'liq emas, to'g'ridan-to'g'ri PostgreSQL va S3 bilan ishlaydi.
* **`sessiya_connector` (`15976`, `15977`):**
  * Xotiradagi (in-memory) kesh 3 soniyada o'zini tiklaydi, PM2 ostida uzluksiz ishlamoqda.
* **`telegram_userbot`:**
  * Ma'lumotlar va sessiyalar diskdagi SQLite bazasida (`.db`, `.session`) xavfsiz saqlanmoqda.

---

## 📊 6. Tizim Resurs Sarfi Xulosasi

* **ZDES Konteynerlari:**
  * `zdes_frontend_app`: **~34 MB RAM** | **0.00% CPU**
  * `zdes_backend_nginx`: **~11 MB RAM** | **0.00% CPU**
  * `zdes_backend_app`: **~173 MB RAM** | **0.00% CPU**
  * **Jami ZDES:** Bor-yo'g'i **~218 MB RAM** (server quvvatining 1.8% qismi).
* **Umumiy Server (Host):**
  * Jami RAM: `12 GB` | Bo'sh RAM: **~9.5 GB** (Zaxira 80%+)
  * SSD disk: Jami `193 GB` | Bo'sh disk: **167 GB (86%)**
  * Protsessor yuklamasi (Load average): `0.4` (Server sokin va optimal).

---

## 🎯 Yakuniy Xulosa
ZDES ekotizimi to'liq ishlab chiqarish (production) muhitiga muvaffaqiyatli topshirildi. Hech qanday parallel tizimga yoki portga daxl qilinmadi. Tizim avtonom, xavfsiz va barqaror ishlamoqda.

*Hujjat tuzuvchi: AGY Core AI Engine (Agent ID: `e7debb0d-eddb-42ca-bc35-da05af9061fe`)*
