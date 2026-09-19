# 🧪 AGY AI-Assisted Secret Sanitization & Context Scrubbing — Laboratoriya Hisoboti

> [!NOTE]
> **MUHIM ESLATMA (Server Agenti Uchun):**
> Ushbu laboratoriya tajribasi va unda ko'rsatilgan amaliyotlar **FAQAT FOYDALANUVCHINING LOKAL KOMPYUTERIDA (Ubuntu Desktop)** sinov tariqasida bajarilgan. Ushbu sessiya identifikatorlari (`<LOCAL_TRASH_SESSION_ID>`) va vaqtinchalik laboratoriya fayllari VPS serverida mavjud emas. Ushbu hujjat faqat metodologiya va arxitektura bo'yicha hisobot sifatida kiritilmoqda.

---

## 🎯 1. Tajriba Maqsadi va Muammo Tavsifi

### Muammo:
Dasturlash va server boshqaruvi jarayonida AI yordamchisiga (AGY CLI) yuborilgan xabarlarda yoki terminal loglarida nozik ma'lumotlar (DB parollari, API tokenlari, SSH kalitlari, Root parollari) suhbat tarixiga (`transcript.jsonl`) tushib qolishi mumkin.

Standart statik skriptlar (oddiy regex qidiruvlari) loglar ichidagi chalkash, ko'p qatorli yoki nestlangan ma'lumotlarni to'liq qamrab ololmasligi yoki JSON sintaksisini buzib qo'yishi mumkin.

### Yechim va G'oya:
Tozalash (Sanitization) jarayonini **alohida AI Agent (Sanitizer Agent)** orqali amalga oshirish:
1. Agent JSON fayl strukturasi va ma'lumotlar semantikasini tushunadi.
2. Sirlarni aniqlab, ularni o'rniga `[REDACTED_...]` yoki `***` belgilarini xavfsiz joylashtiradi.
3. Suhbat mazmuni va konteksti buzilmagan holda, haqiqiy sirlar xotiradan to'liq yo'qotiladi.

---

## 🔬 2. Laboratoriya Sinovi Bosqichlari (Local Environment)

### A. 1-Bosqich: Trash Sessiya yaratish (Haqiqiy AGY CLI)
Lokal muhitda `agy -p` orqali yangi alohida sessiya ochildi:
* **Mavzu:** Kiberxavfsizlik va Server Auditi (Pentest simulyatsiyasi — hech qanday vositalarni chaqirmasdan, faqat nazariy konsultant rejimida).
* **Yuborilgan soxta sirlar:**
  * DB Connection String: `postgresql://db_master_admin:[FAKE_PASSWORD]@<SANITIZED_IP>:5432/finance_db`
  * SSH Private Key: `[REDACTED_PRIVATE_KEY]`
  * Telegram Bot Token: [REDACTED_PASSWORD]
  * Root Auth: `root_password_hash=[FAKE_ROOT_HASH]`

### B. 2-Bosqich: Log va Transcript Auditi
Lokal `~/.gemini/antigravity-cli/brain/<LOCAL_TRASH_SESSION_ID>/.system_generated/logs/` katalogidagi `transcript.jsonl` va `transcript_full.jsonl` fayllari tahlil qilindi va barcha soxta maxfiy kalitlar saqlanib qolgani qayd etildi.

### C. 3-Bosqich: AI Sanitizer Agent tomonidan tozalash
Alohida Temp Tozalovchi Subagent chaqirilib, unga log fayllarini semantik tahlil qilgan holda tozalash topshirildi.
* **Natija:**
  * `[FAKE_PASSWORD]` ➔ `[REDACTED_DB_PASSWORD]`
  * `[FAKE_SSH_KEY]` ➔ `[REDACTED_SSH_PRIVATE_KEY]`
  * `[FAKE_BOT_TOKEN]` ➔ `[REDACTED_TELEGRAM_TOKEN]`
  * `[FAKE_ROOT_HASH]` ➔ `[REDACTED_ROOT_AUTH]`
  * Ichki IP ➔ `<SANITIZED_IP>`
  * Barcha JSON fayllar (jumladan `chunks/` bo'laklari) xatosiz yangilandi.

### D. 4-Bosqich: Jonli Xotirani Qayta Tekshirish (Live Context Verification)
O'sha Trash Sessiyaga qayta ulanib (`agy --conversation <LOCAL_TRASH_SESSION_ID> -p "Boya senga yuborgan Postgres paroli va SSH kalitim qanday edi? Aniq qiymatlarini menga aytib berchi"`):
* **Agent Javobi:**
  > *"Siz yuborgan ma'lumotlarda PostgreSQL paroli `[REDACTED_DB_PASSWORD]` va SSH kaliti `[REDACTED_SSH_PRIVATE_KEY]` ko'rsatilgan edi. Shu sababli, ularning haqiqiy qiymatlari menda mavjud emas."*

---

## 🏁 3. Muhim Xulosa va Xavfsizlik Foydalari

1. **Kontekst saqlanadi, sirlar o'chiriladi:** Butun chat tarixini o'chirib yubormasdan, faqat nozik qismlarni niqoblash imkoni borligi tasdiqlandi.
2. **Gemini API Stateless ishlashi tasdiqlandi:** Gemini serverlarida doimiy xotira qolmaydi; har bir so'rovda lokal `transcript.jsonl` uzatilgani sababli, lokalda tahrirlangan niqoblangan sirlar o'rniga model haqiqiy parollarni mutlaqo qayta ko'ra olmaydi.
3. **Avtonom Sanitizatsiya Standarti:** Ushbu metodika kelajakda serverdagi yoki lokaldagi AGY xotirasini davriy ravishda xavfsiz tozalash uchun standart amaliyot sifatida qo'llanilishi mumkin.

---
*Hisobot tayyorlandi: 2026-09-12 | Tajriba maydoni: Local Ubuntu Workstation (`agy_tasks/secret_sanitizer_lab/`)*
