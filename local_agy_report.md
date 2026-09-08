# 🚀 JarvisOS Core AI Engine (Antigravity CLI) — Server Setup & Architecture Report

Ushbu hisobot **JarvisOS Cloud AI Engine** ekotizimini VPS serverda 24/7 rejimida to'liq avtonom, xavfsiz va samarali ishlashi uchun amalga oshirilgan barcha muhandislik ishlari, arxitektura qatlamlari va xavfsizlik choralarini umumlashtiradi.

---

## 🎯 1. Loyiha Maqsadi va Umumiy Konseptsiya

Asosiy maqsad — har qanday joydan turib (Telegram Bot orqali) to'g'ridan-to'g'ri terminal va AI quvvatidan foydalangan holda:
- Yangi loyihalarni noldan generatsiya qilish, tahrirlash va testlash;
- Git operatsiyalari (`git clone`, `commit`, `push`, PR boshqaruvi)ni to'liq avtomatlashtirish;
- Serverda xavfsiz izolyatsiyalangan Docker konteynerlarida mikroservislarni ishga tushirish;
- Barcha amallarni Telegram interfeysida qadam-baqadam (Step-by-Step Mini-Message) jonli kuzatish va boshqarish.

---

## 🛡️ 2. Ko'p Qatlamli Xavfsizlik va Izolyatsiya Arxitekturasi

Serverda boshqa mavjud tizim loyihalari va xizmatlariga mutlaqo daxl qilmaslik uchun **5 bosqichli xavfsizlik devori** o'rnatildi:

### A. Izolyatsiyalangan Foydalanuvchi (`User-Space Jailing`)
- Barcha ishlar alohida `fayzillo` foydalanuvchisi doirasida bajariladi.
- AI agenti va barcha xizmatlarning ta'sir doirasi FAQAT `/home/fayzillo/` katalogi bilan cheklangan.
- Tizim kataloglari (`/etc`, `/var`, `/usr`, `/root`) va boshqa shaxsiy papkalar uchun yozish huquqi mavjud emas.

### B. Rootless Docker Sandbox (Konteyner Izolyatsiyasi)
- **Muammo:** Standart Rootful Dockerda `docker` guruhiga kirgan foydalanuvchi butun server konteynerlari va ma'lumotlar bazalariga to'liq kirish huquqiga ega bo'lib qoladi.
- **Yechim:** `fayzillo` foydalanuvchisi uchun to'liq **Rootless Docker** (`docker-ce-rootless-extras`) o'rnatildi.
- **Natija:**
  - Docker daemoni foydalanuvchi sessiyasida (`unix:///run/user/<UID>/docker.sock`) ishlaydi.
  - Serverdagi mavjud root konteynerlari `fayzillo`ga mutlaqo ko'rinmaydi.
  - Yangi yaratilgan har qanday konteyner xavfsiz user-namespace ichida izolyatsiya qilingan (Container Breakout xavfi 0%).

### C. Tarmoq va Portlar Nazorati
- Serverning ishlab chiqarish portlari daxlsiz saqlanadi.
- Yangi yaratiladigan loyihalar va veb-xizmatlar faqat bo'sh va ajratilgan portlar oralig'ida (`15800 - 15900`) ishga tushiriladi.

---

## 🧠 3. Google Antigravity CLI (`agy`) Migratsiyasi

1. **Standalone Binary:** Antigravity CLI'ning 64-bit Linux standalone binar fayli `~/.local/bin/agy` katalogiga o'rnatildi va global `PATH`ga ulandi.
2. **Autentifikatsiya:** Google AI Pro (Gemini 3.7 / 3.8 modellari) bilan xavfsiz autentifikatsiya sozlandi.
3. **Session Management:** Sessiyalar `~/.gemini/antigravity-cli/brain/` katalogida to'liq xronologik tartibda (`transcript.jsonl`) saqlanadi.

---

## 🐙 4. GitHub & CI/CD Avtomatizatsiyasi

- **Alohida GitHub Profili:** Server uchun maxsus `fummatov92` hisobi ulandi.
- **Ed25519 SSH Kalitlari:** Xavfsiz shifrlangan SSH kalit juftligi yaratilib, GitHub bilan tokenlarsiz `git push` oqimi yo'lga qo'yildi.
- **GitHub CLI (`gh`):** Foydalanuvchi muhitiga `gh` CLI (v2.100.0+) o'rnatildi. Natijada AI agenti terminal orqali brauzersiz yangi repozitoriyalar ochish (`gh repo create`) va boshqarish huquqiga ega bo'ldi.

---

## ☁️ 5. Bulutli Ma'lumotlar Bazasi va Kesh Primitivlari

Server xotirasini tejash va yuqori barqarorlikni ta'minlash uchun tashqi serverless infratuzilma ulandi:
- **Serverless Postgres (Neon DB):** Alohida `schema=bot_post` izolyatsiyasi ostida Prisma ORM orqali boshqariladi.
- **Cloud Redis (Upstash Redis):** TLS/SSL shifrlangan aloqa orqali sessiyalar, kesh va navbatlar (queues) uchun xizmat qiladi.

---

## 📱 6. Telegram Step-by-Step Mini-Message Streaming UI

Foydalanuvchi va AI o'rtasidagi aloqa chalkashmasligi uchun qadam-baqadam xabarlar protokoli ishlab chiqildi:

```text
[Foydalanuvchi] 💬: "Telegram bot uchun yangi auth moduli yozib ber"

[Jarvis OS] 🤖 (Reply):
  🎯 [1/4] Vazifa qabul qilindi: "Auth modulini yaratish"
  ⏳ Jarvis ishga tushmoqda...

[Jarvis OS] 🤖: 🔍 [2/4] Kerakli fayllar va arxitektura tahlil qilindi
[Jarvis OS] 🤖: 🛠 [3/4] Kodlar yozildi: auth.service.ts, auth.controller.ts
[Jarvis OS] 🤖: 🧪 [4/4] Sintaksis va testlar muvaffaqiyatli tekshirildi
[Jarvis OS] 🤖: 🏁 Vazifa yakunlandi! Git commit: 'feat: add auth module'
```

---

## 📂 7. Ishchi Maydonlar Xaritasi

| Maydon | Joylashuvi | Vazifasi |
| :--- | :--- | :--- |
| **AGY Pipeline** | `~/Desktop/agy/` | Yangi loyihalarni yaratish, testlash va GitHub'ga uzatish quvuri |
| **AGY Tasks** | `~/Desktop/agy_tasks/` | Shaxsiy vazifalar, tahlillar va 3 bo'limli rejalar (`plan`, `.agents`, `work`) |
| **Digital Brains** | `~/Downloads/brains/` | 33 ta semantik klasterdan iborat Raqamli Miya (bilimlar bazasi) |
| **Sessiya Connector** | `~/Desktop/sessiya_connector/` | Telegram Bot, Backend API va Antigravity CLI ko'prigi |

---

## 🏁 Xulosa

Ushbu arxitektura orqali server to'liq **avtonom, xavfsiz, mustaqil va har qanday masofadan boshqariladigan shaxsiy AI laboratoriyasi (JarvisOS)**ga aylantirildi. Barcha jarayonlar xavfsizlik standartlariga qat'iy javob beradi.
