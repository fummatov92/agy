# Reja: "Bot Post Using" Loyihasini Raqamli Miyaga Distillatsiya Qilish

## Maqsad
"Bot Post Using" loyihasida yaratilgan backend, Telegram bot arxitekturasi va yechilgan nozik muammolarni (Telegraf regex collision, guruh/kanal huquqlarini tekshirish, inline editing state boshqaruvi, pagination/breadcrumb va dinamik konfiguratsiya) chuqur tahlil qilib, `~/Downloads/brains/` Raqamli Miya bazasiga va uning RAG tizimiga integratsiya qilish.

## Bosqichlar (Milestones)

### M1: Loyihani chuqur tadqiq qilish va texnik xulosa (Distillatsiya)
- **Vazifa**: `bot_post_using` loyihasining barcha fayllari, arxitekturasi, Prisma modellari, Telegram bot logikasi, middleware va xizmatlarini to'liq o'rganish.
- **Tadqiq qilinadigan nozik jihatlar**:
  1. Telegraf regex to'qnashuvlari (action patternlar, callback_data collision).
  2. Guruh va kanal huquqlarini tekshirish (Telegram API getChatMember, 403 Forbidden, bot adminlik ruxsatlari).
  3. Inline editing va post state boshqaruvi (multistep wizard, draftlar, inline button switches).
  4. Pagination va breadcrumb navigatsiya mexanizmi.
  5. Dinamik konfiguratsiya va i18n/sozlamalar.
  6. Prisma ID va DB arxitekturasi (BigInt vs String vs Int, Telegram ID larni saqlash muammolari).
- **Ijrochi**: `teamwork_preview_explorer` subagentlari.
- **Kutilayotgan natija**: `.agents/explorer_1/analysis.md` va `.agents/explorer_2/analysis.md` hisobotlari.

### M2: Raqamli Miya (`grouped-md/` va `00-INDEX.md`) integratsiyasi
- **Vazifa**:
  - `05-id-string-db-majburiy` klasteriga Telegram ID lar (BigInt/String) bilan ishlash bo'yicha amaliy tajriba va arxitektura qo'llanmasini qo'shish.
  - `23-prisma-id-string-va` klasteriga Prisma va PostgreSQL da Telegram chat/user ID larni String sifatida saqlash va BigInt cheklovlarini yechish bo'yicha tahlilni kiritish.
  - `04-md-va-bo-bu` klasteriga Telegraf bot arxitekturasi, regex collision yechimlari, kanal/guruh huquqlari va inline editing navigatsiyasi bo'yicha qo'llanma kiritish.
  - `00-INDEX.md` faylini barcha yangi qo'shilgan fayllar va semantik havolalar bilan sinxronlashtirish.
- **Ijrochi**: `teamwork_preview_worker`.
- **Kutilayotgan natija**: Yangi `.md` fayllar va yangilangan `00-INDEX.md`.

### M3: RAG-Ready JSONL Chunks generatsiyasi
- **Vazifa**:
  - `~/Downloads/brains/rag-ready/` ichidagi mos klasterlarga yangi bilimlarni valid JSONL chunklar shaklida qo'shish.
  - Har bir chunk uchun aniq metadata (`title`, `cluster`, `category`, `tags`, `source_file`, `timestamp`, `content`).
  - Semantik teglash (kelajakda AI qidiruvi uchun boyitilgan kalit so'zlar).
- **Ijrochi**: `teamwork_preview_worker`.
- **Kutilayotgan natija**: Valid JSONL qatorlari mos `.jsonl` fayllarda.

### M4: Ko'p bosqichli verifikatsiya va Audit
- **Vazifa**:
  - Reviewer: Markdown fayllar sifati, strukturasi, `00-INDEX.md` sinxronligi.
  - Challenger: JSONL fayllar formati, parse qilinishi, semantik teglar boyligi, hech qanday syntax/JSON xatosi yo'qligi.
  - Forensic Auditor: Cheating/dummy implementation yo'qligi, faktik to'g'rilik va yaxlitlik tekshiruvi.
- **Ijrochi**: `teamwork_preview_reviewer`, `teamwork_preview_challenger`, `teamwork_preview_auditor`.
- **Kutilayotgan natija**: APPROVE va CLEAN verifikatsiya xulosalari.
