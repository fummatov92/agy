# 📋 TEXNIK VAZIFA (TZ): Safira.uz — Regional Service Aggregator & Marketplace Platform
**Asosiy Domen:** `https://safira.uz`  
**Loyiha Muallifi:** Fayzillo Ummatov  
**Arxitektura Turi:** Modular Monolith / Gibrid Mikroservislar Ekotizimi  
**Versiya:** 3.0 (Official Technical Specification)  

---

## 1. LOYIHA MOHIYATI VA KONSEPSIYASI

### 1.1. Safira.uz Nima?
**"Safira.uz"** — O'zbekistonning barcha hududlari (viloyatlar va shaharlar) kesimida onlayn va oflayn xizmatlarni (Davlat xizmatlari, Ishlab chiqarish, Rekonstruksiya/Ta'mirlash, IT, Ta'lim, Maishiy va Ijtimoiy xizmatlar) birlashtiruvchi, xizmat ko'rsatuvchilar (Providers) va mijozlarni (Users) yagona raqamli muhitda bog'lovchi **Milliy Xizmatlar Agregatori va Marketplace Platformasi** hisoblanadi.

> **Ekotizim Bog'liqligi:**  
> `Zdes` (`zdes.safira.uz`) — ushbu katta Safira ekotizimining ichki korxonalarga mo'ljallangan ixtisoslashgan sub-servisi (HRM/Biometrik Davomat moduli) hisoblanadi. Asosiy **Safira.uz** esa ommaviy servislar marketplace'i bo'lib xizmat qiladi.

---

## 2. ASOSIY VAZIFALAR VA FOYDALANUVCHILAR OQIMI

1. **Viloyatlar / Hududlar kesimida qidiruv:**
   - Har bir hudud o'zining mustaqil qidiruv va xizmatlar vitrinasiga ega (`safira.uz/toshkent`, `safira.uz/andijon`, `safira.uz/samarqand` yoki subdomenlar).
2. **Kategoriyalar va Filtrlar:**
   - Onlayn va oflayn xizmatlar, narx oralig'i, reyting, bepul konsultatsiya, tezkor xizmat.
3. **Premium Obuna va Tavsiya Tizimi (Recommendation Engine):**
   - Premium xizmat ko'rsatuvchilar bosh sahifada (Hero Section / Trending) va hududlar vitrinasida birinchi o'rinda tavsiya qilinadi.
4. **Real-Time Aloqa (Chat & WebSockets):**
   - Mijoz va xizmat ko'rsatuvchi o'rtasida to'g'ridan-to'g'ri lahzalik xabarlashuv tizimi.
5. **Avtomatlashtirilgan Telegram Boti:**
   - Yangi e'lonlar, so'rovlar va bildirishnomalarni Telegram kanallari va foydalanuvchi lichkasiga yetkazish.

---

## 3. TIZIM ARXITEKTURASI VA TEXNOLOGIK STEK

```
+-----------------------------------------------------------------------------------+
|                           FRONTEND (Next.js App Router)                           |
|  * SSR & SEO Optimization (Har bir viloyat va xizmat uchun individual meta-teglar)|
|  * UI: React 19, TypeScript, Tailwind CSS, shadcn/ui                             |
|  * Routing: /[province], /[province]/services, /[province]/services/[slug]        |
|  * Xavfsizlik: HttpOnly Cookie orqali Shared JWT Token                            |
+-----------------------------------------------------------------------------------+
                                         │  HTTPS / REST / WebSocket
                                         ▼
+-----------------------------------------------------------------------------------+
|                         CORE BACKEND (NestJS Modular API)                         |
|  * Modullar: Auth, Users, Services, Categories, Provinces, Premium, Admin, Chat   |
|  * Cross-Service Shared JWT Auth (Access Token + Sliding Refresh Token)           |
|  * WebSockets Gateway (Foydalanuvchilar o'rtasida real-time chat)                 |
|  * Upload Service (Tasvirlarni siqish va saqlash)                                 |
+-----------------------------------------------------------------------------------+
                                         │  Prisma ORM
                                         ▼
+-----------------------------------------------------------------------------------+
|                             MA'LUMOTLAR VA KESH QATLAMI                           |
|  * PostgreSQL: Relatsion ma'lumotlar, viloyatlar va xizmatlar jadvali            |
|  * B-Tree Indekslar: (province_id, category_id, is_premium, created_at)          |
|  * Redis: Kesh, sessiyalar, tez-tez chaqiriluvchi xizmatlar vitrinasi             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        AVTOMATIZATSIYA (Python Bot & Workers)                     |
|  * Telegram Notification Bot (Yangi xizmatlar, buyurtmalar, verifikatsiya)       |
|  * PM2 Cluster Mode & Docker Containerization                                     |
+-----------------------------------------------------------------------------------+
```

---

## 4. MA'LUMOTLAR BAZASI STRUKTURASI (PRISMA SCHEMA CORE)

### 4.1. Asosiy Modellar:
- **`User`**: `id`, `email`, `phone`, `passwordHash`, `role` (`USER`, `PROVIDER`, `ADMIN`), `isVerified`, `createdAt`
- **`Profile`**: `id`, `userId`, `firstName`, `lastName`, `avatar`, `bio`, `provinceId`
- **`Province`**: `id`, `name` (Toshkent, Andijon...), `slug`, `isActive`
- **`Category`**: `id`, `name`, `slug`, `icon`, `parentId`
- **`Service`**: `id`, `providerId`, `provinceId`, `categoryId`, `title`, `slug`, `description`, `price`, `priceType` (FIXED, NEGOTIABLE), `serviceFormat` (ONLINE, OFFLINE), `isPremium`, `viewsCount`, `status` (`PENDING`, `ACTIVE`, `REJECTED`), `images`
- **`PremiumSubscription`**: `id`, `serviceId`, `startDate`, `endDate`, `planType`, `status`
- **`ChatRoom` & `Message`**: `id`, `senderId`, `receiverId`, `content`, `createdAt`
- **`ServiceReview`**: `id`, `serviceId`, `userId`, `rating` (1-5), `comment`

---

## 5. FOYDALANUVCHI ROLLARI VA HUQUQLARI (RBAC)

1. **Mehmon (Guest / Public):**
   - Viloyat tanlash, xizmatlarni qidirish va filtrlash, xizmat tafsilotlarini ko'rish.
2. **Foydalanuvchi (User):**
   - Ro'yxatdan o'tish/Kirish, xizmat ko'rsatuvchiga chat orqali yozish, sharh va baho qoldirish, xatcho'pga saqlash.
3. **Xizmat Ko'rsatuvchi (Provider):**
   - Shaxsiy kabinet, yangi xizmat e'lon qilish, narx va ma'lumotlarni tahrirlash, Premium obunani faollashtirish, chat xabarlariga javob berish.
4. **Administrator (Admin):**
   - Xizmatlarni moderatsiyadan o'tkazish (Approve/Reject), foydalanuvchilar va toifalarni boshqarish, umumiy analitika.

---

## 6. MARSHRUTLAR VA URL TUZILMASI

- `/` — Bosh sahifa (Hero Search, Viloyatlar xaritasi, Top xizmatlar, Kategoriyalar)
- `/[province]` — Tanlangan viloyatning asosiy sahifasi (masalan: `/toshkent`)
- `/[province]/services` — Viloyatdagi barcha xizmatlar katalogi (filtrlari bilan)
- `/[province]/services/[slug]` — Aniq xizmat sahifasi (narx, aloqa, buyurtma, chat, galereya)
- `/auth/login` & `/auth/register` — Autentifikatsiya sahifalari
- `/dashboard/provider` — Xizmat ko'rsatuvchi boshqaruv paneli
- `/admin` — Boshqaruv ma'murlari paneli

---

## 7. RIVOJLANISH BOSQICHLARI (ROADMAP)

1. **1-Bosqich (Modular Monolith MVP):**
   - Next.js (App Router) + NestJS Backend + PostgreSQL + Shared JWT Auth + Viloyatlar bo'yicha e'lonlar katalogi.
2. **2-Bosqich (Real-Time & Engagement):**
   - WebSockets Chat tizimi, Tasvirlarni optimallashtiruvchi Upload Service, Premium obunalar va tavsiya mexanizmi.
3. **3-Bosqich (Ekotizim Integratsiyasi & Avtomatlashtirish):**
   - Python Telegram Boti, Zdes HRM va boshqa sub-servislarni Safira Cloud markaziy profiliga (Single Sign-On — SSO) ulash.
