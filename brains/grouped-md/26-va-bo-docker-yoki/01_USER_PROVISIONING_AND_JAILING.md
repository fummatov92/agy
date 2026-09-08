# 👤 1. Foydalanuvchi Ochilishi va Linux Sandbox Izolyatsiyasi (User Jailing)

## 📌 Tarixiy Xronologiya
- **Yaratilgan Sana:** 2026-yil 7-Sentabr
- **Vaqt:** 17:38:58 (CEST) / 20:38:58 (UZT)
- **Foydalanuvchi:** `fayzillo`
- **Guruh va Huquqlar:** `UID=1001(fayzillo)`, `GID=1001(fayzillo)`
- **Server:** Contabo Cloud VPS (Ubuntu 24.04 LTS x86_64, Host: `vmi3346315`)

---

## 🎯 Izolyatsiya Konsepsiyasi va Muammo
Standart VPS muhitida dasturchi yoki avtomatlashtirilgan AI agentiga to'g'ridan-to'g'ri `root` huquqini berish katta xavflarni keltirib chiqaradi:
1. Serverdagi boshqa mavjud muhim loyihalar (`/opt/mahala`, `/opt/online-magazin`, `/srv/`) va ularning ma'lumotlar bazalariga tasodifiy yoki nojo'ya ta'sir;
2. Tizim paketlari (`apt`, systemd, networking) buzilishi natijasida butun server faoliyatining to'xtab qolishi;
3. Global daemonlar orqali resurslar to'lib qolishi.

**Yechim:** Alohida `fayzillo` foydalanuvchisi yaratildi va uning atrofiga qat'iy chegaralangan **Sandbox (Jailing)** muhiti o'rnatildi.

---

## 🛡️ Jailing Qoidalari va Himoya Qatlamlari

### 1. Fayllar Tizimi Cheklovi (Directory Jailing)
- AI agenti va barcha xizmatlarning amaliy ta'sir doirasi FAQAT `/home/fayzillo/Desktop/` etib belgilandi.
- `/etc`, `/var`, `/usr`, `/root` kabi operatsion tizim papkalari faqat o'qish rejimida bo'lib, yozish/o'chirish huquqi mutlaqo yo'q.
- Hamkasblar loyihalari va tizim papkalariga kirish qat'iyan taqiqlangan.

### 2. Sudo Huquqlarini Nazorat Qilish
- `sudo` buyruqlari parolsiz (`NOPASSWD`) ishlamaydi (`SUDO_NEEDS_PASSWD`).
- AI vositasi root parolini bila olmaydi va uni server ichidan o'qib olishi texnik jihatdan imkonsiz.
- Parolni faqat Contabo boshqaruv paneli orqali xavfsiz tiklash mumkin.

### 3. Portlar Bo'yicha Qat'iy Cheklov (15800 - 15900)
Serverdagi asosiy ishlab chiqarish xizmatlari band qilgan portlar (`4000`, `8090`, `5432`, `5433`, `6379`) daxlsiz saqlanadi. 
`fayzillo` foydalanuvchisi doirasida yaratiladigan barcha yangi loyihalar va API'lar FAQAT quyidagi oraliqda ishga tushiriladi:
- **Port oralig'i:** `15800` dan `15900` gacha.
- Hozirda band qilinganlar:
  - `15976` — Sessiya Connector Backend API Bridge
  - `15977` — Sessiya Connector Frontend Web UI

### 4. Xavfsiz Muhit O'zgaruvchilari (User-level Environment)
- O'rnatilgan vositalar tizim darajasida emas, balki foydalanuvchining shaxsiy `~/.local/bin` va `~/.nvm` kataloglarida joylashgan:
  - `~/.local/bin/agy` (Antigravity CLI)
  - `~/.local/bin/gh` (GitHub CLI)
  - `~/.local/bin/deno` (Deno Runtime)
  - `~/.local/bin/yt-dlp` (Stream engine)
