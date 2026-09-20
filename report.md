# 📊 Server Holati, AGY Imkoniyatlari va Xavfsizlik Hisoboti

Ushbu hujjat **Fayzillo Ummatov**ning shaxsiy Contabo VPS serverida (`fayzillo@<HOST_NAME>`) tashkil etilgan **JarvisOS Core AI Engine (Antigravity CLI)** ekotizimi, ishchi imkoniyatlari va ko'p qatlamli xavfsizlik arxitekturasini to'liq ifodalaydi.

---

## 🖥️ 1. Jonli Server Holati (Live Infrastructure)

- **Operatsion Tizim:** Ubuntu Linux x86_64
- **Ishchi Foydalanuvchi:** `fayzillo` (izolyatsiyalangan muhit)
- **Operativ Xotira (RAM):** Jami: **12 GB** | Band: **~2.1 GB** | Bo'sh: **~9.9 GB** (Xotira zaxirasi 80%+)
- **Disk Xotirasi (SSD/NVMe):** Jami: **193 GB** | Band: **20 GB (11%)** | Bo'sh: **174 GB (89%)**
- **Uptime:** 7+ kun uzluksiz barqaror faoliyat

---

## 🚀 2. AGY Quvur Ishchi Maydoni (Pipeline Workspace — `~/Desktop/agy/`)

### 🎯 Vazifasi va Mohiyati:
`~/Desktop/agy/` — foydalanuvchi Telegram Bot (`@safira_support_bot`) yoki CLI orqali bergan topshiriqlari asosida yangi dasturlar, xizmatlar yoki loyihalarni ishlab chiqish, avtomatik test qilish va GitHub'ga uzatish quvuridir.

### ⚙️ Ishlash Sikli:
1. **Topshiriq:** Foydalanuvchi botga yangi loyiha yaratishni yozadi (masalan: *"Menga React + Tailwind'da yangi landing page qurib ber"*).
2. **Ishlab Chiqish:** AI loyihani to'g'ridan-to'g'ri `~/Desktop/agy/` ichida quradi, bog'liqliklarni o'rnatadi va sintaksisni sinaydi.
3. **Avtomatik Push:** Tayyor loyiha `git@github.com:fummatov92/agy.git` repozitoriyasiga avtomatik commit qilinadi va `git push` qilinadi.
4. **Masofaviy Foydalanish:** Foydalanuvchi o'zining shaxsiy noutbuki yoki ishchi kompyuterida quyidagi buyruq bilan kodni darhol yuklab oladi:
   ```bash
   git clone git@github.com:fummatov92/agy.git
   # yoki yangilanishlarni olish uchun:
   git pull
   ```

---

## 🐙 3. GitHub Integratsiyasi (`gh` CLI va SSH)

Server to'liq avtonom GitHub operatsiyalari uchun sozlangan:

- **SSH Autentifikatsiyasi:** `~/.ssh/id_ed25519` (Ed25519 xavfsiz shifrlangan kalit, GitHub'da `Contabo Server (JarvisOS Engine)` nomi bilan tasdiqlangan).
- **GitHub CLI (`gh`):** `~/.local/bin/gh` (v2.100.0) foydalanuvchi doirasida o'rnatilgan.
- **Ulangan Akkaunt:** `fummatov92` (Scopes: `repo`, `read:org`, `gist`).
- **Imkoniyatlar:**
  - `gh repo create <nomi> --public/--private` — brauzersiz yangi repolar ochish.
  - `gh repo list fummatov92` — barcha repolar ro'yxatini nazorat qilish.
  - Masofadan turib Pull Request (PR), Issue va Release'lar boshqarish.

---

## 🛡️ 4. Xavfsizlik va Izolyatsiya Arxitekturasi (Security & Sandbox)

Tizimda **5 bosqichli qat'iy xavfsizlik devori** o'rnatilgan:

### 1. Fayllar Tizimi Izolyatsiyasi (Directory Jailing)
- AI agentining barcha amaliy harakatlari **FAQAT `/home/fayzillo/Desktop/`** papkasi bilan chegaralangan.
- Tizim kataloglari (`/etc`, `/var`, `/usr`, `/root`), boshqa shaxsiy papkalar (`~/.ssh`) va hamkasb loyihalariga (`/opt/mahala`, `/opt/online-magazin`, `/srv/`) kirish yoki ularni tahrirlash AI qoidalarida qat'iy bloklangan.

### 2. Sudo va Root Huquqlaridan Himoya
- Serverda `sudo` buyruqlari parolsiz ishlamaydi (`SUDO_NEEDS_PASSWD`).
- AI tizimi hech kimning parolini bila olmaydi, o'g'irlay olmaydi yoki tizim darajasidagi buzuvchi buyruqlarni erkin bajara olmaydi.

### 3. Portlar va Tarmoq Izolyatsiyasi
- Yangi loyihalar, API'lar yoki veb-xizmatlar FAQAT **15800 dan 15900 gacha** bo'lgan portlar oralig'ida ochiladi (masalan: `15801`, `15802`...).
- Serverning tizimli va ishlab chiqarish portlariga (`4000`, `8090`, `5432`, `5433`, `6379`) teginish taqiqlangan.

### 4. Multi-User Sessiyalar Ajratilishi
- Botingizda har bir foydalanuvchi alohida, mustaqil AI sessiyasiga ega:
  - **Admin Foydalanuvchi:** To'liq boshqaruv va Core AI Engine huquqi.
  - **Boshqa foydalanuvchilar:** Izolyatsiyalangan alohida sessiya, boshqa shaxsning xabarlari yoki fayllari ularga mutlaqo ko'rinmaydi.

### 5. Xato Tuzatish Protokoli (Safe Editing Protocol)
- Xatolik yoki nosozlik yuz berganda, AI hech qachon kodni darhol o'zgartirmaydi.
- Avval muammoning aniq tashxisi va yechim varianti foydalanuvchiga taqdim etiladi, faqat foydalanuvchi aniq tasdiq berganidan so'nggina tahrir amalga oshiriladi.

### 6. Rootless Docker Izolyatsiyasi (Rootless Container Architecture)
- **Haqiqiy Holat:** Serverda Docker to'liq **Rootless** (`Security Options: rootless`) rejimida sozlangan.
- **Xavfsizlik Kafolati:** Docker daemoni tizimning `root` huquqlarisiz, alohida foydalanuvchi muhitida (user namespace) ishlaydi.
- **Container Breakout Himoyasi:** Hatto konteyner ichida dasturiy nosozlik sodir bo'lib, konteyner ichida `root` huquqi olinsa ham, u asosiy VPS operatsion tizimiga va serverning boshqa resurslariga chiqa olmaydi (Container Breakout xavfi bartaraf etilgan).

---

## 🧠 5. Mavjud Ishchi Maydonlar Xaritasi

| Maydon | Joylashuvi | Vazifasi |
| :--- | :--- | :--- |
| **AGY Pipeline** | `~/Desktop/agy/` | Yangi loyihalarni yaratish, testlash va GitHub'ga uzatish quvuri |
| **AGY Tasks** | `~/Desktop/agy_tasks/` | Shaxsiy tahlillar, tadqiqotlar va 3 bo'limli rejalar (`plan`, `.agents`, `work`) |
| **Brains** | `~/Downloads/brains/` | 33 ta klasterdan iborat shaxsiy Raqamli Miya (bilimlar bazasi) |
| **Sessiya Connector** | `~/Desktop/sessiya_connector/` | Telegram Bot, Backend API va Antigravity CLI ko'prigi |

---

*Hisobot tayyorlandi: 2026-09-08 | Tizim: JarvisOS Core AI Engine*
