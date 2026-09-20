# 📖 Qo'llanma: Claude va Gemini Gibrid Tizimini Amaliyotda Ishlatish

Ushbu qo'llanma dasturchilarga Claude Code va Gemini CLI (yoki Antigravity) ni parallel tarzda maksimal foyda bilan qanday ishlatishni tushuntiradi.

---

## ❓ Nima Uchun Gibrid Usul?

| Muammo | Faqat Claude Ishlatganda | Faqat Gemini Ishlatganda | Gibrid (Claude + Gemini) |
| :--- | :--- | :--- | :--- |
| **Limitlar** | Tez tugaydi (Sonnet limitlari qattiq) | Katta kontekst va bepul/arzon limit | **Limitlar tejaladi:** Claude faqat boshqaruvda ishlaydi |
| **Ko'rsatmalarga rioya** | 99% qat'iy amal qiladi | Ba'zan ko'p kod yozishda chalg'ishi mumkin | **Mukammal:** Claude tekshiradi va yo'naltiradi |
| **Kod yozish tezligi** | Yirik refaktorda qimmat/sekin | Bir zumda yuzlab qator kod yozadi | **Maksimal:** Gemini bir zumda yozadi, Claude tasdiqlaydi |

---

## 🚀 3 Bosqichli Amaliy Mashg'ulot (Workflow):

### 1-Qadam: Claude'da Reja Tuzish
Claude chatiga loyiha maqsadi yoki muammoni tushuntiring va `orchestrator_prompt.md` qoidasi asosida spetsifikatsiya so'rang.
> *Misol:* "Menga foydalanuvchilar autentifikatsiyasi uchun NestJS moduli kerak. Gemini Executer uchun `TASK_SPEC` tayyorlab ber."

### 2-Qadam: Gemini CLI'da Kodni Yozish
Claude bergan `TASK_SPEC` matnini to'g'ridan-to'g'ri Gemini CLI (yoki Antigravity) ga yuboring.
Gemini barcha fayllarni bir zumda yaratadi, tahrirlaydi va testdan o'tkazadi.

### 3-Qadam: Claude'da Tekshirish (Review)
Gemini bajargan o'zgarishlar diff'ini yoki test natijasini Claude'ga qaytarib ko'rsating.
Claude yakuniy tasdiq beradi yoki tuzatishlarni ko'rsatadi.

---

🎯 **Natija:** 
• Claude tokenlari 80% tejaladi.  
• Loyiha arxitekturasi buzilmaydi.  
• Katta hajmdagi kodlar Gemini tezligida yoziladi.
