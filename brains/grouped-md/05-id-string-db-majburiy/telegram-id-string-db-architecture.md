# Telegram Bot Arxitekturasida ID Turlari: Nega Telegram User va Chat ID lari Ma'lumotlar Bazasida Qat'iy String/VARCHAR Bo'lishi Shart?

**Loyiha manbasi:** `bot_post_using`  
**Muallif / Ekspert tahlili:** Worker 1 & Brains Architecture Team  
**Mavzu doirasi:** Ma'lumotlar bazasi turlari, JavaScript xotira cheklovlari, Prisma BigInt serialization tuzoqlari, DDD identifikatorlari va 3-bosqichli holat mashinasi (3-Tier State Architecture).

---

## 1. Kirish va Muammoning Qo'yilishi

Zamonaviy Telegram botlari va mikroservis tizimlarida eng ko'p uchraydigan, ammo kutilmaganda halokatli oqibatlarga olib keladigan arxitekturaviy xatolardan biri bu — **Telegram identifikatorlarini (User ID, Chat ID, Channel ID, Group ID) ma'lumotlar bazasida raqamli (`INTEGER` yoki `BIGINT`) formatda saqlashdir**.

Ko'plab dasturchilar Telegram Bot API hujjatlaridagi `id: Integer` yoki `chat_id: Integer or String` degan yozuvni ko'rib, relatsion ma'lumotlar bazalarida (PostgreSQL, MySQL) `BIGINT` (yoki `int8`) turini tanlaydilar. Biroq, dastur Node.js / TypeScript, Prisma ORM, Redis kesh, BullMQ navbatlari va MongoDB zaxira bazasi bilan integratsiya qilinganda, `BIGINT` kutilmagan qulashlar, yashirin bit-yo'qotishlar (bit truncation) va seriyalashtirish xatolariga (`TypeError: Do not know how to serialize a BigInt`) sabab bo'ladi.

`bot_post_using` loyihasining amaliy tajribasi va ishlab chiqish tarixi (`history/task_001` - `task_021`) ushbu muammoning qanchalik jiddiy ekanligini hamda uni bartaraf etish uchun qanday qo'shimcha "yamoqlar" (workarounds) talab qilinganini yaqqol ko'rsatib berdi.

Ushbu maqolada Telegram identifikatorlarini saqlashda nima uchun `String` / `VARCHAR` yagona to'g'ri tanlov ekanligi matematik, texnik, dasturiy ta'minot arxitekturasi va Domain-Driven Design (DDD) nuqtai nazaridan to'liq isbotlab beriladi.

---

## 2. Matematik va Xotira Cheklovi: JavaScript `MAX_SAFE_INTEGER` Xavfi

### 2.1 IEEE 754 Standarti va 53-Bitli Cheklov
JavaScript tili ECMAScript spetsifikatsiyasiga binoan barcha oddiy sonlarni (`number` turi) **IEEE 754 ikki karra aniqlikdagi suzuvchi nuqtali (Double Precision 64-bit Float)** formatida saqlaydi. 
Ushbu 64 bitning:
- **1 biti:** ishora (sign) uchun;
- **11 biti:** tartib darajasi (exponent) uchun;
- **52 biti:** mantissa (aniqlik fraksiyasi) uchun ajratilgan.

Yashirin 1 bit (implicit bit) bilan birga JavaScript arifmetik yo'qotishlarsiz saqlashi mumkin bo'lgan maksimal butun son:

$$\text{Number.MAX\_SAFE\_INTEGER} = 2^{53} - 1 = 9,007,199,254,740,991 \text{ (taxminan } 9 \times 10^{15}\text{)}$$

Har qanday son $9,007,199,254,740,991$ dan oshganda, JavaScript oxirgi bitlarni yaxlitlab tashlaydi (bit-truncation).

### 2.2 Telegram ID larining Haqiqiy Ko'lami
Telegram platformasi 64-bitli butun sonlar maydonidan (`int64`) foydalanadi:
- **Foydalanuvchi ID lari:** Hozirgi kunda 6-8 milliarddan oshgan va yaqin kelajakda $2^{53}-1$ ga qarab o'sib bormoqda.
- **Kanal va Guruh ID lari:** Telegram kanallari va superguruhlari `-100` prefiksi bilan boshlanadi va odatda 13-14 xonali manfiy sonlardan iborat bo'ladi (masalan, `-1002234567890`).

### 2.3 Bit Truncation Falokati (Amaliy Misol)
Tasavvur qiling, tashqi tizim yoki kelajakdagi Telegram User ID raqami $9,007,199,254,740,995$ ga teng. Node.js yoki brauzer konsolida quyidagi kodni ishga tushiring:

```javascript
const originalId = 9007199254740995;
console.log(originalId); 
// Natija: 9007199254740996  <--- XATO! Oxirgi raqam buzildi!

console.log(9007199254740995 === 9007199254740996);
// Natija: true              <--- Ikkita mutlaqo boshqa foydalanuvchi bitta deb hisoblanadi!
```

**Arxitekturaviy xavf:** Agar backend yoki REST API bu ID ni JSON orqali frontendga uzatsa, yoki JSON parser `Number` sifatida qabul qilsa, foydalanuvchining ID raqami buziladi. Natijada boshqa odamning maxfiy posti mutlaqo notanish begona shaxsga yuborilishi yoki bazadan noto'g'ri hisob o'chirilishi mumkin!

---

## 3. Prisma va Node.js da `BigInt` Seriyalashtirish Fojeasi

PostgreSQL bazasida `int8` (`BIGINT`) ishlatilganda, Prisma Client modeli ushbu maydonni JavaScript `bigint` primitiv turi (masalan, `123456789n`) sifatida kodga taqdim etadi.

### 3.1 `TypeError: Do not know how to serialize a BigInt`
ECMAScript spetsifikatsiyasiga ko'ra, standart `JSON.stringify()` funksiyasi `BigInt` turini qabul qilmaydi. Sababi — JSON formatida sonlar turi aniqlanmagan va JavaScript uni xavfsiz son sifatida tiklay olmasligi mumkin.

```javascript
const user = { id: "uuid", telegramId: 1234567890123n };
JSON.stringify(user);
// ❌ TypeError: Do not know how to serialize a BigInt
```

### 3.2 Koddagi Asoratlar va `bot_post_using` dagi Real Yamoqlar

`bot_post_using` loyihasida `telegramId` va `chatId` maydonlari `BigInt` deb olinganligi sababli dasturchilar butun loyiha bo'ylab o'nlab joylarda qo'lda o'zgartirishlar qilishga majbur bo'lishgan:

#### 1. Redis Kesh va Holat Boshqaruvida (`src/core/state.service.ts:76-80`):
Redis faqat matn qabul qiladi. Holatni saqlash uchun uni JSON qilish kerak, lekin `state.userId` BigInt bo'lgani sababli `JSON.stringify(state)` qulardi:
```typescript
// Dasturchi majburan manual transformer yozgan:
const serializableState = {
  ...state,
  userId: state.userId.toString(), // BigInt -> String
};
await this.redisService.set(`session:${userKey}`, JSON.stringify(serializableState), 86400);

// Redis dan o'qilganda yana qaytarish kerak bo'lgan (state.service.ts:31):
const parsed = JSON.parse(redisData) as UserSessionState;
parsed.userId = BigInt(parsed.userId); // String -> BigInt
```

#### 2. REST API Kontrollerlarida (`src/modules/users/users.service.ts:126-134`):
NestJS yoki Express kontrolleri orqali `prisma.user.findMany()` natijasini to'g'ridan-to'g'ri qaytarib bo'lmaydi. Chunki Express `res.json()` chaqirganda server 500 Internal Server Error beradi. Shu sababli har bir so'rovda massivni `.map()` qilishga to'g'ri kelgan:
```typescript
const formatted = dbUsers.map((u) => ({
  id: u.id,
  telegramId: u.telegramId.toString(), // Majburiy qo'lda stringga o'girish
  firstName: u.firstName,
  lastName: u.lastName,
  username: u.username,
  isAllowed: u.isAllowed,
}));
return formatted;
```

#### 3. BullMQ Asinxron Navbatida (`src/core/message_queue.service.ts:163`):
BullMQ vazifa parametrlarini Redis ga JSON sifatida yozadi. Agar jobga `BigInt` uzatilsa, job navbatga kirmasdan xato beradi:
```typescript
await this.queue.add(
  'send_post',
  { postId: post.id, createdBy: post.createdBy.toString() }, // Majburiy .toString()
  { delay, jobId: `post_${post.id}` },
);
```

#### 4. MongoDB Zaxira Sxemalarida (`src/core/schemas/state-backup.schema.ts`):
MongoDB Mongoose drayverida ham `BigInt` bilan ishlash noqulay bo'lgani sababli, sxemada to'g'ridan-to'g'ri `string` ishlatilgan:
```typescript
@Prop({ required: true, unique: true, index: true })
userId: string; // Relatsion bazada BigInt, MongoDB da String!
```

> **Xulosa:** Bitta noto'g'ri tur tanlovi arxitekturada "turlarning buzilishi" (type impedance mismatch) keltirib chiqargan: PostgreSQL da `int8`, Prisma da `bigint`, Redis da `string`, MongoDB da `string`, Express da `string`, Telegraf da `number | string`. Yangi dasturchi bitta joyda `.toString()` ni esdan chiqarsa, butun tizim qulaydi.

---

## 4. Domain-Driven Design (DDD): Identifikator Miqdor Emas, Shaxsiyat Tokenidir

Dasturiy injiniring va Domain-Driven Design (DDD) falsafasiga ko'ra, ma'lumot turlari ularning biznes ma'nosiga qarab tanlanishi lozim:

| Xususiyat | Raqamli Miqdor (Numeric Quantity) | Identifikator / Token (Identity Token) |
|---|---|---|
| **Misollar** | Narx, hisob balansi, postlar soni, yosh | Telegram User ID, Pasport seriyasi, Telefon raqam, UUID |
| **Arifmetik amallar** | Qo'shish ($A + B$), o'rtachasini olish ($\text{avg}$), taqqoslash ($A > B$) | **Mantiqqa zid!** Telegram ID larni qo'shish yoki ko'paytirish mumkin emas |
| **Tabiati** | O'lchov, skalyar miqdor | **Opaque Identifier (Noaniq shaxsiyat belgisi)** |
| **Format o'zgarishi** | Doim son bo'lib qoladi | Kelajakda prefikslar qo'shilishi mumkin (masalan, `-100...`) |

Telegram User ID hech qachon hisob-kitob qilinmaydi. U faqat **tenglikka tekshirish (`===`)** va **qidiruv (Lookup)** uchun ishlatiladi. Shuning uchun uni son emas, matn (`String` / `VARCHAR`) sifatida qabul qilish DDD qoidalariga 100% mos keladi.

---

## 5. PostgreSQL: `BIGINT` vs `VARCHAR(64)` / `TEXT` Unumdorlik Taqqoslovi

Ko'pchilik bazada `VARCHAR` ishlatish xotirani ko'p yeydi yoki qidiruvni sekinlashtiradi deb xavotir oladi. Keling, bu xavotirni muhandislik nuqtai nazaridan tekshirib ko'ramiz.

### 5.1 Disk va Xotira Sarfi
- **`BIGINT`:** 8 bayt xotira oladi.
- **`VARCHAR(64)` / `TEXT`:** 1 bayt uzunlik sarlavhasi (header) + 10-15 bayt belgilar = jami 11-16 bayt.
- **Farq:** 1 million foydalanuvchi bo'lganda farq bor-yo'g'i ~8 Megabaytni tashkil qiladi! Bugungi serverlar xotirasi (RAM va SSD) sharoitida 8 MB hech qanday ahamiyatga ega emas.

### 5.2 Qidiruv Tezligi (Index Performance)
PostgreSQL da `PRIMARY KEY` yoki `UNIQUE INDEX` qo'yilganda, har ikkala tur ham **B-Tree (Balanced Tree)** indeksi orqali indekslanadi:
- B-Tree qidiruv murakkabligi: $\mathcal{O}(\log N)$.
- Zamonaviy CPU registrlarida 15 ta belgidan iborat satrni taqqoslash nanosekundlar darajasida bajariladi.
- Redis va In-Memory kesh bilan solishtirganda, diskdagi 0.05ms farq umuman sezilmaydi.

### 5.3 Arxitekturaviy Taqqoslash Matritsasi

| Mezon | `BIGINT` (`int8`) | `VARCHAR(64)` / `String` |
|---|---|---|
| **JSON.stringify mosligi** | ❌ `TypeError` beradi, manual o'girish shart | ✅ 100% tabiiy va avtomatik ishlaydi |
| **Redis / BullMQ integratsiyasi** | ❌ Serializatsiya yamoqlari talab etiladi | ✅ To'g'ridan-to'g'ri matn sifatida saqlanadi |
| **Frontend xavfsizligi (JS Float)** | ❌ 53-bitdan oshsa oxirgi raqamlar buziladi | ✅ Matn hech qachon aniqligini yo'qotmaydi |
| **TypeScript / Prisma qulayligi** | ⚠️ `bigint` primitivi, har doim `.toString()` kerak | ✅ `string` primitivi, to'liq tur xavfsizligi |
| **MongoDB / NoSQL zaxiralash** | ❌ Tiplar nomutanosibligi | ✅ Bir xil format |
| **Disk hajmi (1M yozuv)** | ~8 MB | ~16 MB (deyarli bir xil) |
| **Qidiruv tezligi (B-Tree)** | $\mathcal{O}(\log N)$ | $\mathcal{O}(\log N)$ |

---

## 6. Yuqori Yuklamali Botlar Uchun 3-Bosqichli Holat Mashinasi (3-Tier State Architecture)

Faqatgina to'g'ri ID turini tanlash yetarli emas; yuqori yuklamali Telegram botlarida foydalanuvchi sessiyasi (state machine) server qayta yuklanganda yo'qolmasligi va ayni paytda nol kechikish (sub-millisecond latency) bilan ishlashi kerak.

`bot_post_using` loyihasida Telegrafning omonat `session()` middleware'i o'rniga maxsus **3-Tier State Architecture** ishlab chiqilgan:

```
[ Telegram Foydalanuvchisi ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ Tier 1: In-Memory Map (Map<string, UserSessionState>)  │ ──► Tezlik: ~0.001 ms (Nol kechikish)
└────────────────────────────────────────────────────────┘
          │ (Sinxron o'qish / Asinxron yozish)
          ▼
┌────────────────────────────────────────────────────────┐
│ Tier 2: Redis Cache (session:${userId}, TTL: 24 soat)  │ ──► Pod restart va gorizontal miqyoslash
└────────────────────────────────────────────────────────┘
          │ (Asinxron zaxira)
          ▼
┌────────────────────────────────────────────────────────┐
│ Tier 3: MongoDB State Backup (state_backups, TTL index)│ ──► Avariyadan tiklanish va uzoq muddatli audit
└────────────────────────────────────────────────────────┘
```

### 6.1 Har bir Pog'onaning Vazifasi
1. **Tier 1 (In-Memory `Map<string, UserSessionState>`):**
   Foydalanuvchi qadamma-qadam wizardda harakatlanayotganda (masalan, matn kiritish, chatlarni tanlash, vaqt belgilash) har bir xabarda Redis yoki PostgreSQL ga so'rov yuborilmaydi. RAM dan o'qish mikro-sekundlarda kechadi.
2. **Tier 2 (Redis Kesh, 24 soat TTL):**
   Docker konteyner qayta yuklanganda yoki dastur yangi versiyasi deploy qilinganda, xotiradagi ma'lumotlar yo'qoladi. Redis mavjud sessiyalarni darhol xotiraga qayta tiklaydi (`hydrate`).
3. **Tier 3 (MongoDB Persistent Backup):**
   Redis tozalanib ketsa yoki server butunlay qulasa ham, foydalanuvchining chala yozilgan posti (`draftPost`) va qadami MongoDB da saqlanib qoladi.

### 6.2 Ideal Prisma va State Modeli (Tavsiya Qilingan Standart)

```prisma
// schema.prisma — Barcha identifikatorlar String bo'lgan mukammal model
model User {
  id          String   @id @default(uuid())
  telegramId  String   @unique @map("telegram_id") @db.VarChar(64) // ✅ Qat'iy String
  firstName   String?  @map("first_name")
  lastName    String?  @map("last_name")
  username    String?  @map("username")
  isAllowed   Boolean  @default(false) @map("is_allowed")
  createdAt   DateTime @default(now()) @map("created_at")

  posts       Post[]

  @@map("users")
}

model Channel {
  id        String   @id @default(uuid())
  chatId    String   @unique @map("chat_id") @db.VarChar(64) // ✅ Qat'iy String (masalan "-1002234567890")
  title     String   @map("title")
  username  String?  @map("username")
  hasAdmin  Boolean  @default(true) @map("has_admin")
  canPost   Boolean  @default(true) @map("can_post")

  @@map("channels")
}
```

---

## 7. Xulosa va Arxitekturaviy Qoidalar

1. **Qoida 1:** Telegram User ID, Chat ID, Guruh va Kanal ID lari ma'lumotlar bazasida (PostgreSQL, MySQL, MongoDB) **faqat va faqat `String` (`VARCHAR(64)`)** formatida saqlanishi shart.
2. **Qoida 2:** Dastur ichida `BigInt` ishlatishdan qat'iyan saqlaning. U JSON, Redis, BullMQ va REST API qatlamlarida muqarrar xatoliklarga olib keladi.
3. **Qoida 3:** Telegram identifikatorlari miqdor emas, balki shaxsiyat tokenlaridir. Ular ustida arifmetika qilinmaydi.
4. **Qoida 4:** Sessiyalarni boshqarishda 3 pog'onali tizimdan (In-Memory + Redis + MongoDB) foydalanish botning to'xtovsiz (fault-tolerant) ishlashini ta'minlaydi.

Ushbu qoidalarga amal qilish loyihani ortiqcha `.toString()` yamoqlaridan tozalaydi, texnik qarzni yo'qotadi va kelajakdagi kengayishlarga 100% poydevor yaratadi.
