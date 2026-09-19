# 📋 TEXNIK VAZIFA (TZ): Safira Service — "Zdes" HRM & Biometrik Davomat Platformasi
**Platforma:** `https://zdes.safira.uz`  
**Muallif / Muhandis:** Fayzillo Ummatov  
**Versiya:** 2.5 (Production Specification)  
**Holat:** Ishlab chiqilgan va Tasdiqlangan  

---

## 1. LOYIHA UMUMIY TAVSIFI VA MAQSADI

### 1.1. Loyiha Maqsadi
**"Safira Service" (Zdes)** — korxonalar, kompaniyalar va filiallar uchun xodimlarni boshqarish (HRM), ish vaqti hisobi (Time & Attendance), biometrik yuz tanish (Face ONNX), turniket integratsiyasi, oylik maosh/avans hisob-kitobi (Payroll), topshiriqlar menejmenti (Task & Project Management) hamda korporativ bildirishnomalarni avtomatlashtiruvchi kompleks bulutli korxona platformasidir (Enterprise HRM/ERP).

### 1.2. Asosiy Muammolar va Yechimlar
1. **Xodimlar davomatini soxtalashtirish (Buddy Punching):** Biometrik yuz tanish (MobileFaceNet ONNX) va turniket loglari (`raw-attendance-log`) orqali har bir kirish-chiqishni real-vaqtda tekshirish.
2. **Murakkab ish grafiklari va kechikishlar:** Erkin, smenali va qat'iy ish grafiklari (`work-schedule`), tushlik vaqtlari, kechikishlar va erta ketishlarni avtomatik hisoblash.
3. **Ish haqi (Payroll) va jarima/avanslarni qo'lda hisoblash xatolari:** Davomat soatlari, KPI ko'rsatkichlari, avanslar (`advance`) va tuzatishlar (`salary-adjustment`) asosida avtomatlashtirilgan oylik hisobot.
4. **Tarqoq filiallar:** Ko'p kompaniyali va ko'p filialli (`company`, `branch`, `department`) markazlashgan boshqaruv.

---

## 2. TIZIM ARXITEKTURASI VA TEXNOLOGIK STEK

```
+-----------------------------------------------------------------------------------+
|                                 MIJOZ QATLAMI                                    |
|  * Web Admin Panel (Next.js / React 19 + Tailwind CSS + TanStack Query)           |
|  * Xodimlar Mobil Ilovasi / TMA (Flutter / Telegram Mini Apps)                    |
|  * Turniket & Biometrik Terminallar (Android/Linux Edge Devices - Face ONNX)      |
+-----------------------------------------------------------------------------------+
                                         |  HTTPS / WSS (WebSockets)
                                         v
+-----------------------------------------------------------------------------------+
|                        BACKEND QATLAMI (NestJS Modular)                           |
|  * 22 ta Modul (Auth, Attendance, Payroll, Task, Company, Branch, User, Setting) |
|  * Global Interceptors: ResponseInterceptor, LoggingInterceptor, TransformPipe    |
|  * Xavfsizlik: JWT (10 min TTL) + Sliding Refresh Token + RBAC Guardlar          |
+-----------------------------------------------------------------------------------+
                                         |  Prisma Client
                                         v
+-----------------------------------------------------------------------------------+
|                            MA'LUMOTLAR BAZASI & STORAGE                           |
|  * PostgreSQL (Relational Data, Multi-tenant Company Isolation)                   |
|  * Redis (Kesh, Sessiyalar, WebSocket Real-time Attendance Pub/Sub)              |
|  * Local File Storage / S3 (Foydalanuvchi rasmlari, fayllar, hisobotlar)          |
+-----------------------------------------------------------------------------------+
```

### 2.1. Texnologiyalar:
- **Backend:** Node.js, NestJS, TypeScript, Prisma ORM, WebSockets (`@nestjs/websockets`).
- **Ma'lumotlar Bazasi:** PostgreSQL, Redis.
- **Frontend:** Next.js (App Router), React, Tailwind CSS, TanStack React Query, Lucide Icons.
- **Biometriya & Uskunalar:** ONNX Runtime (MobileFaceNet), Hikvision/Dahua turniket integratsiyalari.

---

## 3. FUNKSIONAL MODULLAR VA TALABLAR (22 TA MODUL)

Tizim jami 22 ta mustaqil va bir-biri bilan integratsiyalashgan modullardan iborat bo'lib, 152 ta API endpointiga ega:

| # | Modul Nomi | Asosiy Vazifasi |
|---|------------|-----------------|
| 1 | **`auth`** | Avtorizatsiya, login, sliding-window token yangilash, xavfsiz parolni tiklash |
| 2 | **`user`** | Xodimlar profili, shaxsiy ma'lumotlar, biometrik deskriptorlar, passport/PINFL |
| 3 | **`company`** | Kompaniyalar boshqaruvi, logotip, rekvizitlar, balans va faollik holati |
| 4 | **`branch`** | Filiallar, geolokatsiya (GPS koordinatalar), radius va ofis chegaralari |
| 5 | **`department`** | Bo'limlar iyerarxiyasi, bo'lim boshliqlari va tarkibi |
| 6 | **`position`** | Lavozimlar, shtat birliklari, bazaviy oylik stavkalar |
| 7 | **`work-schedule`** | Ish grafiklari (5/2, 6/1, smenali 2/2, moslashuvchan grafiklar) |
| 8 | **`attendance`** | Asosiy davomat tahlili, kechikishlar, erta ketishlar, ish soatlari va KPI |
| 9 | **`raw-attendance-log`** | Turniket va biometrik terminallardan keluvchi birlamchi xom loglar |
| 10 | **`terminal`** | Filiallardagi planshet, turniket va biometrik qurilmalar ro'yxati va tokenlari |
| 11 | **`turnstile`** | Turniket apparat drayverlari bilan integratsiya va o'tish loglarini qabul qilish |
| 12 | **`employee-leave`** | Mehnat ta'tillari, kasallik varaqalari, o'z hisobidan ta'tillar va tasdiqlash workflow |
| 13 | **`holiday`** | Rasmiy bayramlar va dam olish kunlari taqvimi (ish haqiga ta'siri bilan) |
| 14 | **`payroll`** | Oylik ish haqi hisob-kitobi, daromad solig'i, INPS, yakuniy to'lov varaqalari |
| 15 | **`advance`** | Avans so'rovlari, ma'qullash va oylikdan chegirib qolish |
| 16 | **`salary-adjustment`** | Mukofotlar (Bonus), ustamalar, jarimalar va qo'shimcha to'lovlar |
| 17 | **`task`** | Vazifalar, loyihalar (`projects`), kanban doskalar, topshiriq ijrosi nazorati |
| 18 | **`notification`** | Tizim ichki bildirishnomalari, ogohlantirishlar va e'lonlar |
| 19 | **`push-token`** | Mobil va web push-xabarnomalar (FCM / WebPush) tokenlari |
| 20 | **`refresh-token`** | Faol sessiyalar, qurilmalar audit logi va tokenni bekor qilish (Revoke) |
| 21 | **`setting`** | Kompaniya global sozlamalari, kechikish chegaralari, avto-tushlik qoidalari |
| 22 | **`app-version`** | Mobil ilovalar versiyalari nazorati va majburiy yangilash (Force Update) |

---

## 4. MA'LUMOTLAR MODELI VA ALOQALAR (PRISMA SCHEMA CORE)

### Asosiy Entitilar va Ularning Bog'lanishi:
- **`Company`** 1 — N **`Branch`** 1 — N **`Terminal`**
- **`Company`** 1 — N **`Department`** 1 — N **`Position`** 1 — N **`User`**
- **`User`** 1 — N **`RawAttendanceLog`**
- **`User`** 1 — N **`Attendance`** (har kunlik yig'ma davomat)
- **`User`** 1 — N **`Payroll`** (har oylik hisob-kitob)
- **`User`** 1 — N **`EmployeeLeave`**
- **`User`** 1 — N **`Task`** (Assignee / Creator)

---

## 5. XAVFSIZLIK VA NON-FUNKSIONAL TALABLAR

1. **Global Response Formati:**
   Barcha backend javoblari yagona standart formatda qaytariladi:
   ```json
   {
     "success": true,
     "statusCode": 200,
     "message": "Amal muvaffaqiyatli bajarildi",
     "data": { ... },
     "timestamp": "2026-09-19T15:46:00.000Z",
     "path": "/api/v1/attendance"
   }
   ```
2. **Autentifikatsiya va Sessiya Xavfsizligi:**
   - Access Token muddati: 10 daqiqa.
   - Refresh Token: [REDACTED_PASSWORD] mexanizmi bilan xavfsiz HTTP-only kuki yoki bearer orqali.
   - Parollar: `argon2id` yoki `bcrypt` (12 salt round).
3. **Multi-Tenant Izolyatsiya:**
   - Har bir so'rovda `companyId` qat'iy tekshiriladi va xodimlar boshqa korxona ma'lumotlarini ko'ra olmaydi.
4. **Audit va Logging:**
   - Har bir muhim o'zgarish (oylik maosh o'zgartirish, ta'til tasdiqlash) `createdById` va `updatedById` bilan imzolanadi.

---

## 6. XULOSA
Ushbu Texnik Vazifa (TZ) **Safira Service / Zdes** platformasining to'liq sanoat standarti bo'yicha arxitekturasini ifodalaydi. Loyiha biznes jarayonlarini 100% raqamlashtirish va korxonalarda inson omilini kamaytirishga mo'ljallangan.
