# 🛡️ Server Isolation Road & JarvisOS Core AI Engine Architecture

> **VPS Muhiti:** Contabo Linux Ubuntu 24.04 LTS x86_64 (`vmi3346315`)  
> **Asosiy Foydalanuvchi:** `fayzillo` (izolyatsiyalangan Sandbox)  
> **Loyiha Egasi:** Fayzillo Ummatov (`fummatov92`)  
> **AI Dvigateli:** Google Antigravity CLI (`agy`) — Gemini 3.7 / 3.8 Flash  
> **Telegram Bot:** `@safira_support_bot` (JarvisOS Assistant)  

---

## 🎯 Loyiha Haqida

Ushbu repozitoriy serverda `fayzillo` foydalanuvchisi ochilgan birinchi soniyalardan (2026-09-07) boshlab, hozirgi kungacha amalga oshirilgan barcha tizimli o'zgarishlar, xavfsizlik izolyatsiyalari, Rootless Docker arxitekturasi, Antigravity AI dvigateli va GitHub quvur ish oqimining **to'liq va mukammal arxitektura ensiklopediyasi** hisoblanadi.

---

## 📚 Hujjatlar Mundarijasi (Documentation Index)

Barcha jarayonlar bosqichma-bosqich, to'liq texnik tafsilotlar bilan alohida modullarga ajratilgan:

| # | Hujjat | Tavsif |
|---|---|---|
| **01** | [**01_USER_PROVISIONING_AND_JAILING.md**](docs/01_USER_PROVISIONING_AND_JAILING.md) | Foydalanuvchi yaratilishi, Linux Sandbox, `Desktop/` doirasi, sudo parollari va portlar (15800-15900) cheklovi. |
| **02** | [**02_ROOTLESS_DOCKER_ARCHITECTURE.md**](docs/02_ROOTLESS_DOCKER_ARCHITECTURE.md) | Nega Rootless Docker tanlandi? User namespace, Container Breakout himoyasi va tizim konteynerlari izolyatsiyasi. |
| **03** | [**03_JARVISOS_BRIDGE_ECOSYSTEM.md**](docs/03_JARVISOS_BRIDGE_ECOSYSTEM.md) | Sessiya Connector (Backend 15976, Frontend 15977, Telegram Bot, Ovozli xabarlar, YouTube stream va PM2). |
| **04** | [**04_AGY_AND_SESSIONS_CHRONOLOGY.md**](docs/04_AGY_AND_SESSIONS_CHRONOLOGY.md) | Antigravity CLI tarixi, sessiyalar arxivi (`agy_history`), context boshqaruvi va step-by-step reporting protokoli. |
| **05** | [**05_GITHUB_AND_PIPELINE_WORKFLOW.md**](docs/05_GITHUB_AND_PIPELINE_WORKFLOW.md) | GitHub CLI (`gh`), Ed25519 SSH kalitlari va `~/Desktop/agy/` orqali yangi loyihalarni yaratib uzatish quvuri. |
| **06** | [**ROADMAP.md**](ROADMAP.md) | Tizimning bosqichma-bosqich rivojlanish xaritasi va kelajakdagi rejalari. |

---

## 🏗️ Umumiy Tizim Arxitekturasi

```text
               ┌──────────────────────────────────────────────┐
               │    Telegram Foydalanuvchisi (Fayzillo/Nur)    │
               └──────────────────────┬───────────────────────┘
                                      │ (TLS/HTTPS)
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  JarvisOS Bot Connector (@safira_support_bot)│
               └──────────────────────┬───────────────────────┘
                                      │ (REST / SSE Stream)
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  Backend Bridge (Port: 15976) & Web Chat UI  │
               └──────────────────────┬───────────────────────┘
                                      │ (Queue / Antigravity SDK)
                                      ▼
               ┌──────────────────────────────────────────────┐
               │  JarvisOS Core AI Engine (Antigravity CLI)   │
               └──────┬───────────────────────┬───────────────┘
                      │                       │
                      ▼                       ▼
    ┌───────────────────────────┐   ┌───────────────────────────┐
    │  AGY Quvur (Pipeline)     │   │  Rootless Docker Sandbox  │
    │  ~/Desktop/agy/           │   │  (User-namespace izolyats)│
    │  Push: fummatov92/agy     │   │  Ports: 15800 - 15900     │
    └───────────────────────────┘   └───────────────────────────┘
```

---

## 🛡️ Asosiy Xavfsizlik Kafolatlari

1. **Rootless Docker:** Konteyner ichidagi root huquqi host tizimga o'ta olmaydi.
2. **Directory Jailing:** AI harakatlari faqat `/home/fayzillo/Desktop/` doirasida cheklangan.
3. **Port Isolation:** Boshqa loyihalar band qilgan portlarga teginish taqiqlangan.
4. **Multi-User Isolation:** Har bir foydalanuvchi alohida shaxsiy sessiyaga ega.
5. **Safe Editing Protocol:** Kodlar faqat foydalanuvchi tasdig'i bilan o'zgartiriladi.

---

*Hujjatlar to'plami yaratildi: 2026-09-08 | Repozitoriy: `fummatov92/server_izolation_road`*
