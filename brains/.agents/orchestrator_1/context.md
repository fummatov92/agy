# Context

## Loyiha va Kontekst Tafsilotlari

- **Manba loyiha (Source)**: `/home/fayzillo/Desktop/Loyihalar/bot_post_using`
  - Telegram bot backend loyihasi (Telegraf, Node.js / TypeScript, Prisma ORM, PostgreSQL).
  - Yechilgan muhim muammolar:
    - Telegraf regex collision (action nomlarining bir-birini overlap qilishi)
    - Guruh/kanal huquqlarini tekshirish (bot admin huquqi, 403 Forbidden holatlari)
    - Inline editing state boshqaruvi (post yaratish, tahrirlash, dinamik inline tugmalar)
    - Pagination va breadcrumb navigatsiyasi
    - Dinamik konfiguratsiya
- **Maqsadli baza (Target Knowledge Base)**: `/home/fayzillo/Downloads/brains`
  - Shaxsiy Raqamli Miya (33 klaster, 400+ tahlil)
  - Maqsadli klasterlar:
    - `grouped-md/05-id-string-db-majburiy/`
    - `grouped-md/23-prisma-id-string-va/`
    - `grouped-md/04-md-va-bo-bu/`
  - Mundarija: `00-INDEX.md`
  - RAG bazasi: `rag-ready/` (tegishli klasterlarga .jsonl qo'shish)
