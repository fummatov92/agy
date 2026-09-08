# 🐙 5. GitHub Integratsiyasi va AGY Quvur Ish Oqimi (Pipeline Workflow)

## 📌 Yangilik va Qulaylik
Serverda AI orqali dastur yaratilganda, dasturchi uni qo'lda zip qilib yoki FTP orqali ko'chirib yurmasligi uchun to'liq **avtomatlashtirilgan GitHub quvuri (Pipeline Workspace)** tashkil qilindi.

---

## 🔑 1. Autentifikatsiya va Kalitlar

1. **Ed25519 SSH Kaliti:**
   - Joylashuvi: `~/.ssh/id_ed25519` (va `id_ed25519.pub`).
   - GitHub'da: `Contabo Server (JarvisOS Engine)`.
   - Vazifasi: Repozitoriyalarni parolsiz va xavfsiz `push`/`pull` qilish.
   - Ulanish holati:
     ```text
     Hi fummatov92! You've successfully authenticated, but GitHub does not provide shell access.
     ```

2. **GitHub CLI (`gh`):**
   - Joylashuvi: `~/.local/bin/gh` (v2.100.0).
   - Ulangan Akkaunt: `fummatov92`.
   - Token saqlanishi: `~/.config/gh/hosts.yml` (faqat `fayzillo` foydalanuvchisi uchun `0600` ruxsati bilan himoyalangan).
   - Imkoniyati: Brauzersiz terminaldan turib istalgan vaqt yangi repo ochish (`gh repo create`) va repolar ro'yxatini olish (`gh repo list`).

---

## 🚀 2. AGY Quvuri (Pipeline Workspace — `~/Desktop/agy/`)

- **Repozitoriy:** `git@github.com:fummatov92/agy.git`
- **Vazifasi:** Vaqtinchalik ishchi quvur (pipeline).
- **Ishlash Sikli:**
  ```text
  [ Telegram Bot ] ──▶ "Yangi dastur yozib ber"
          │
          ▼
  [ ~/Desktop/agy/ ] ──▶ Loyiha yaratiladi, testlanadi, build qilinadi
          │
          ▼
  [ Git Auto-Commit & Push ] ──▶ git@github.com:fummatov92/agy.git
          │
          ▼
  [ Foydalanuvchi Shaxsiy Kompyuteri ] ──▶ git clone / git pull
  ```

---

## 🛠️ Foydali Buyruqlar

1. **Yangi loyiha repozitoriyasini ochish:**
   ```bash
   gh repo create <loyiha_nomi> --public --source=. --push
   ```

2. **Mavjud repolarni tekshirish:**
   ```bash
   gh repo list fummatov92
   ```

3. **Quvurni yangilash va tortib olish:**
   ```bash
   git pull origin main
   ```
