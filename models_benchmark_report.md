# 📊 AI Modellar Audit va Benchmark Hisoboti

> **Hisobot Sanasi:** 2026-09-15 21:17 (Toshkent / Server vaqti)  
> **Mas'ul Agent ID:** `83600370-1ece-409e-a79e-754f966f61b7`  
> **Server:** JarvisOS AI Core VPS  
> **Sinov Turi:** Matn generatsiyasi, Vision (Rasm tahlili) va Jonli API Quota/Limit auditi  

---

## 🎯 1. Xulosa va Benchmark Natijalari

Serverdagi barcha 14 ta model real-vaqtda test so'rovlari va haqiqiy rasm fayli (`photo_1789498071942.jpg`) orqali tekshirildi.

### 🟢 1.1. To'liq Ishlayotgan va Rasm Tahliliga Qodir Modellar (Zaxira Ro'yxati)

| # | Model ID | Ko'rinishi | Matn Testi | Rasm Tahlili (Vision) | O'rtacha Vaqt | Tavsiya Qilingan Rol |
|---|---|---|---|---|---|---|
| 1 | `gemini-3.8-flash-medium` | ⚡ 3.8 Flash Medium | ✅ OK | ✅ OK (Multimodal) | ~4.9s | **Asosiy Default Model** |
| 2 | `gemini-3.8-flash-high` | 🔥 3.8 Flash High | ✅ OK | ✅ OK (Multimodal) | ~5.2s | Murakkab tahlil va kodlash |
| 3 | `gemini-3.7-flash-medium` | ⚡ 3.7 Flash Medium | ✅ OK | ✅ OK (Multimodal) | ~4.7s | **1-Darajali Zaxira Model** |
| 4 | `gemini-3.7-flash-high` | 🔥 3.7 Flash High | ✅ OK | ✅ OK (Multimodal) | ~5.1s | Gibrid mantiqiy fikrlash |
| 5 | `gemini-3.7-flash-low` | 💨 3.7 Flash Low | ✅ OK | ✅ OK (Multimodal) | ~4.6s | Tezkor yengil topshiriqlar |
| 6 | `gemini-3.6-flash-medium` | ⚡ 3.6 Flash Medium | ✅ OK | ✅ OK (Multimodal) | ~4.5s | **2-Darajali Zaxira Model** |
| 7 | `gemini-3.6-flash-high` | 🔥 3.6 Flash High | ✅ OK | ✅ OK (Multimodal) | ~5.1s | Barqaror zaxira |
| 8 | `gemini-3.6-flash-low` | 💨 3.6 Flash Low | ✅ OK | ✅ OK (Multimodal) | ~4.6s | Tezkor zaxira |
| 9 | `gemini-3.1-pro-high` | 🧠 3.1 Pro High | ✅ OK | ✅ OK (Multimodal) | ~7.8s | Katta loyihalar va chuqur kod |
| 10| `gemini-3.1-pro-low` | 🧠 3.1 Pro Low | ✅ OK | ✅ OK (Multimodal) | ~6.1s | Pro tezkor rejim |

---

### 🔴 1.2. Hozirda Ishlamayotgan yoki Limitga Tushgan Modellar

| Model ID | Holati | Xatolik Sababi | Qayta Tiklanish / Yechim |
|---|---|---|---|
| `gemini-3.8-flash-low` | ❌ **503 UNAVAILABLE** | Google datacenter klasterida ushbu tejamkor modelga server sig'imi yetishmadi (`No capacity available on the server`). | `gemini-3.8-flash-medium` yoki `gemini-3.7-flash-medium` ga avto-yo'naltirish (Failover). |
| `claude-sonnet-4-6` | ⚠️ **Quota Exceeded (0%)** | 3-Party guruhida haftalik limit to'lgan. | ~3 kun 19 soatdan keyin avtomatik tiklanadi. |
| `claude-opus-4-6-thinking` | ⚠️ **Quota Exceeded (0%)** | 3-Party guruhida haftalik limit to'lgan. | ~3 kun 19 soatdan keyin avtomatik tiklanadi. |
| `gpt-oss-120b-medium` | ⚠️ **Quota Exceeded (0%)** | 3-Party guruhida haftalik limit to'lgan. | ~3 kun 19 soatdan keyin avtomatik tiklanadi. |

---

## 📈 2. Jonli Limitlar va Kvota Holati (Quotas & Limits)

Backend API (`/api/status/usage`) dan olingan rasmiy kvota ko'rsatkichlari:

### 🔹 Gemini Modellar Guruhi (Gemini Flash & Pro):
* **5 Soatlik Limit (5-Hour Rolling Limit):** **`92.8%` qolgan** (Deyarli to'liq bo'sh, faol ishlatish mumkin).
* **Haftalik Limit (Weekly Quota):** **`26.6%` qolgan** (To'liq yangilanish: 3 kun 10 soat ichida).
* **Kontekst oynasi (Context Window):** 1 000 000 – 2 000 000 token.
* **Multimodal qo'llab-quvvatlash:** Matn, Rasm, Audio, Video, Hujjatlar (PDF, ZIP, kod).

### 🔹 Claude va GPT Modellar Guruhi:
* **Haftalik Limit (Weekly Quota):** **`0.0%` qolgan** (Limit to'lgan, yangilanish sanasi: 2026-09-19 14:02 UTC).
* **5 Soatlik Limit:** Haftalik limit tugagani sababli vaqtincha muzlatilgan.

---

## 🛡️ 3. Tavsiya Qilingan Avtomatik Failover Zanjiri (Zaxira Mexanizmi)

Tizim barqarorligini 100% kafolatlash uchun botdagi model almashtirish zanjiri quyidagicha tuzildi:

```text
gemini-3.8-flash-low (503 xato) ──► gemini-3.8-flash-medium ──► gemini-3.7-flash-medium ──► gemini-3.6-flash-medium
claude-sonnet-4-6 (Limit 0%)    ──► gemini-3.8-flash-medium
claude-opus-4-6-thinking        ──► gemini-3.1-pro-high
gpt-oss-120b-medium             ──► gemini-3.7-flash-medium
```

---

## 🏁 4. Xulosa

1. **Rasm tahlili (Vision):** Barcha ishlayotgan Gemini 3.x Flash va Pro modellari (jami 10 ta model) tasvirni tahlil qilish va xulosa chiqarish bo'yicha testdan 100% muvaffaqiyatli o'tdi.
2. **Server barqarorligi:** `gemini-3.8-flash-medium` eng optimal default model sifatida tasdiqlandi.
