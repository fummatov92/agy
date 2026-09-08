# Yuqori Yuklamali Telegram Bot Uchun Prisma Sxemasi Arxitekturasi va Identifikatorlar Tipologiyasi

**Loyiha manbasi:** `bot_post_using`  
**Muallif / Ekspert tahlili:** Worker 1 & Brains Architecture Team  
**Mavzu doirasi:** Prisma ORM, PostgreSQL relatsion modeli, MongoDB audit/backup, polimorf munosabatlar, kaskadli o'chirish (`Cascade` vs `SetNull`), `messageId` 32-bit vs `chatId` 64-bit, DTO xaritalash va migratsiya strategiyalari.

---

## 1. Kirish: Zamonaviy Telegram Bot Ma'lumotlar Bazasiga Qo'yiladigan Talablar

Telegram botlari faqat oddiy buyruqlarga javob berish doirasidan chiqib, ko'p kanalli va guruhli post tarqatish (broadcasting), rejalashtirilgan nashrlar (scheduling), media galereyalar va AI tahrirlash kabi murakkab biznes jarayonlarini boshqaradigan platformalarga aylandi.

Bunday tizimlarda ma'lumotlar bazasi arxitekturasi quyidagi qat'iy talablarga javob berishi shart:
1. **To'liq tranzaksion yaxlitlik (ACID):** Post bir nechta manzilga (kanal va guruhlarga) yuborilayotganda holatlar chalkashmasligi kerak.
2. **Polimorf chatlarni qo'llab-quvvatlash:** Bitta post bir vaqtning o'zida ham Kanallarga (broadcast channel), ham Guruhlarga (supergroup) yuborilishi mumkin.
3. **Munosabatlarning xavfsiz o'chirilishi (Referential Integrity):** Agar foydalanuvchi postni o'chirsa, uning barcha targetlari tozalanishi, ammo kanal yoki guruh o'chirilganda eski yuborilgan postlar statistikasi saqlanib qolishi kerak.
4. **Gibrid Saqlash (Hybrid Persistence):** Relatsion asosiy ma'lumotlar (PostgreSQL) va tez o'zgaruvchan audit/log ma'lumotlari (MongoDB) o'rtasidagi optimal taqsimot.

Ushbu maqolada `bot_post_using` loyihasida qo'llanilgan va amaliyotda sinovdan o'tgan to'liq Prisma sxemasi, identifikatorlar tipologiyasi va modellashtirishning nozik jihatlari yoritiladi.

---

## 2. To'liq Ishlab Chiqarish (Production-Grade) Prisma Sxemasi

Quyidagi sxema PostgreSQL drayveri asosida ishlab chiqilgan bo'lib, tashqi tizim identifikatorlari (Telegram ID) va ichki birlamchi kalitlar o'rtasidagi farqni to'liq inobatga oladi:

```prisma
// datasource va generator konfiguratsiyasi
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

// -------------------------------------------------------------
// ENUMLAR (Holatlar va Turlar)
// -------------------------------------------------------------

enum TargetType {
  CHANNEL
  GROUP
}

enum PostStatus {
  DRAFT
  SCHEDULED
  SENT
  FAILED
  CANCELLED
}

// -------------------------------------------------------------
// MODELLAR
// -------------------------------------------------------------

/// Foydalanuvchi modeli (Adminlar va mualliflar)
model User {
  id          String   @id @default(uuid())
  telegramId  String   @unique @map("telegram_id") @db.VarChar(64)
  firstName   String?  @map("first_name")
  lastName    String?  @map("last_name")
  username    String?  @map("username")
  isAllowed   Boolean  @default(false) @map("is_allowed")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  posts       Post[]

  @@map("users")
}

/// Telegram Kanallari modeli
model Channel {
  id          String      @id @default(uuid())
  chatId      String      @unique @map("chat_id") @db.VarChar(64)
  title       String      @map("title")
  username    String?     @map("username")
  type        TargetType  @default(CHANNEL) @map("type")
  hasAdmin    Boolean     @default(true) @map("has_admin")
  canPost     Boolean     @default(true) @map("can_post")
  createdAt   DateTime    @default(now()) @map("created_at")
  updatedAt   DateTime    @updatedAt @map("updated_at")

  postTargets PostTarget[]

  @@map("channels")
}

/// Telegram Guruhlari va Superguruhlari modeli
model Group {
  id          String      @id @default(uuid())
  chatId      String      @unique @map("chat_id") @db.VarChar(64)
  title       String      @map("title")
  username    String?     @map("username")
  type        TargetType  @default(GROUP) @map("type")
  hasAdmin    Boolean     @default(true) @map("has_admin")
  canPost     Boolean     @default(true) @map("can_post")
  createdAt   DateTime    @default(now()) @map("created_at")
  updatedAt   DateTime    @updatedAt @map("updated_at")

  postTargets PostTarget[]

  @@map("groups")
}

/// Postlar (E'lonlar) asosiy modeli
model Post {
  id           String      @id @default(uuid())
  text         String?     @db.Text @map("text")
  mediaType    String?     @map("media_type") // PHOTO, VIDEO, DOCUMENT, VOICE
  mediaFileId  String?     @map("media_file_id") // Telegram file_id
  scheduledAt  DateTime?   @map("scheduled_at")
  sentAt       DateTime?   @map("sent_at")
  status       PostStatus  @default(DRAFT) @map("status")
  createdBy    String      @map("created_by") @db.VarChar(64)
  createdAt    DateTime    @default(now()) @map("created_at")
  updatedAt    DateTime    @updatedAt @map("updated_at")

  user         User?       @relation(fields: [createdBy], references: [telegramId])
  targets      PostTarget[]

  @@index([status, scheduledAt])
  @@map("posts")
}

/// Postning har bir chatga yuborilish natijasi (Polimorf bog'liqlik)
model PostTarget {
  id           String      @id @default(uuid())
  postId       String      @map("post_id")
  targetType   TargetType  @map("target_type")
  channelId    String?     @map("channel_id")
  groupId      String?     @map("group_id")
  status       PostStatus  @default(SCHEDULED) @map("status")
  errorMessage String?     @db.Text @map("error_message")
  messageId    Int?        @map("message_id") // Chat ichidagi 32-bit xabar ID si
  createdAt    DateTime    @default(now()) @map("created_at")
  updatedAt    DateTime    @updatedAt @map("updated_at")

  post         Post        @relation(fields: [postId], references: [id], onDelete: Cascade)
  channel      Channel?    @relation(fields: [channelId], references: [id], onDelete: SetNull)
  group        Group?      @relation(fields: [groupId], references: [id], onDelete: SetNull)

  @@index([postId])
  @@index([status])
  @@map("post_targets")
}
```

---

## 3. Identifikatorlar Tipologiyasi va `messageId` Maxsus Holati

Ushbu sxemada identifikatorlar bir xil emas — ularning har biri o'zining domen vazifasiga moslashtirilgan:

### 3.1 Birlamchi Kalitlar (UUID v4)
- Barcha modellarning birlamchi kaliti (`id`) sifatida `String @id @default(uuid())` tanlangan.
- **Nega autoincrement `Int` emas?** 
  Autoincrement sonlar raqamli bo'lib, tizim hajmini fosh qiladi (Insecure Direct Object Reference xavfi) hamda gorizontal bo'lingan (sharded) yoki taqsimlangan tizimlarda ID to'qnashuvlariga olib keladi. UUID v4 butun dunyo bo'yicha yagonalikni ta'minlaydi.

### 3.2 Telegram Foydalanuvchi va Chat ID lari (`telegramId`, `chatId`)
- Qat'iy ravishda `String @db.VarChar(64)` sifatida belgilangan.
- Oldingi tahlillarda ko'rib o'tilganidek, `BigInt` o'rniga `String` ishlatilishi Node.js, Express, Redis, BullMQ va Mongoose o'rtasidagi to'liq tip muvofiqligini (type-safety) kafolatlaydi.

### 3.3 Telegram `messageId` Maydoni Nega `Int?` (32-bit Integer)?
`PostTarget` modelidagi `messageId` maydoniga e'tibor qarating:
```prisma
messageId Int? @map("message_id")
```
Ko'pchilikda savol tug'iladi: *"Nega `chatId` String qilinib, `messageId` Int qilib qoldirildi?"*

**Javob — Telegram Protokoli arxitekturasida:**
1. **Global vs Local doira:** Telegramda `chatId` global miqyosdagi noyob hisob bo'lib, $2^{64}$ maydonida joylashgan va manfiy belgilar (`-100...`) bilan keladi.
2. **Sequential Counter:** Xabar ID si (`message_id`) esa faqat **bitta aniq chat ichidagi oddiy hisoblagichdir (chat-scoped counter)**. Chatda har bir yuborilgan xabar 1, 2, 3 tartibida o'sib boradi.
3. **Chegara:** Hatto eng faol guruhlarda ham 10 yil davomida xabarlar soni 1-2 milliarddan oshmaydi. 32-bitli imzolangan butun son (`int4`) maksimal $2,147,483,647$ gacha qiymat oladi.
4. **Xotira va API:** Telegram Bot API barcha xabarlarni yuborish, tahrirlash (`editMessageText`) va o'chirish (`deleteMessage`) metodlarida `message_id` parametrini oddiy JavaScript `number` (32-bit int) ko'rinishida qaytaradi va qabul qiladi.
5. Shuning uchun `messageId` maydoni uchun PostgreSQL da `int4` (`Int`) ishlatish ham xotira tejamkorligi, ham API mosligi nuqtai nazaridan ideal hisoblanadi.

---

## 4. Polimorf Munosabatlar va Kaskadli O'chirish Strategiyasi

### 4.1 Polimorf Chat Maqsadlari (Polymorphic Targets)
Bir post ham kanalga, ham guruhga yuborilishi mumkin. Relatsion bazalarda buni ifodalashning 3 xil usuli mavjud:
1. Yagona `Chat` jadvali (Single Table Inheritance).
2. Alohida jadvallar va oraliq polimorf model (`PostTarget`).
3. JSON maydonida saqlash.

`bot_post_using` loyihasida **2-usul (Alohida jadvallar + PostTarget)** tanlangan. Sababi — Kanallar va Guruhlar Telegram Bot API da turlicha huquqlar va imkoniyatlarga ega:
- Kanallarda `can_post_messages` va `hasAdmin` tekshiriladi;
- Guruhlarda esa oddiy a'zo bo'lish, `can_send_messages` cheklovi yoki superguruhga aylanish xususiyatlari mavjud.

`PostTarget` modelida bu munosabat quyidagicha ajratilgan:
```prisma
targetType TargetType @map("target_type") // CHANNEL yoki GROUP
channelId  String?    @map("channel_id")
groupId    String?    @map("group_id")
```

### 4.2 Kaskadli O'chirish (`Cascade`) vs Aloqani Uzish (`SetNull`)
Bazadagi relyatsion bog'lanishlarda eng muhim jihat — o'chirish harakati (`onDelete`):

#### A. `Post` -> `PostTarget`: `@relation(..., onDelete: Cascade)`
Post o'chirilganda uning maqsadli chatlari va jo'natish loglarining bazada yetim (orphan) bo'lib qolishiga yo'l qo'yilmaydi. Post o'chishi bilan uning barcha `PostTarget` yozuvlari avtomatik o'chiriladi.

#### B. `Channel` / `Group` -> `PostTarget`: `@relation(..., onDelete: SetNull)`
Agar tizimdan biror kanal yoki guruh o'chirilsa, avval shu kanalga yuborilgan tarixiy postlar va ularning hisobotlari o'chib ketmasligi kerak! `onDelete: SetNull` qo'yilganda, kanal o'chirilgach `PostTarget.channelId` shunchaki `NULL` ga aylanadi, ammo qaysi post qachon yuborilgani va qanday `messageId` olgani arxiv sifatida saqlanib qoladi.

---

## 5. PostgreSQL (Asosiy Tranzaksion) va MongoDB (Audit va Zaxira) Farqlari

Loyihada gibrid ma'lumotlar bazasi arxitekturasi qo'llanilgan:

| Mezon | PostgreSQL (Prisma ORM) | MongoDB (Mongoose ODM) |
|---|---|---|
| **Vazifasi** | Asosiy biznes ma'lumotlari: Foydalanuvchilar, Kanallar, Postlar, Rejalashtirish | Vaqtinchalik holatlar zaxirasi (`StateBackup`), Post ijrosi loglari (`PostBackup`) |
| **Tranzaksiyalar** | Qat'iy ACID, Foreign Key cheklovlari | Dokumentga yo'naltirilgan, tranzaksiyasiz tezkor append |
| **Sessiya va TTL** | Doimiy saqlash (cheksiz) | 3 kunlik TTL indeksi (`expireAfterSeconds: 259200`) |
| **Sxema moslashuvchanligi** | Qat'iy sxema va migratsiyalar | Dinamik `executionLogs` massivi (har bir urinish xatosi va vaqti) |

### MongoDB Zaxira Sxemasi Namunasi (`src/core/schemas/post-backup.schema.ts`):
```typescript
@Schema({ timestamps: true, collection: 'post_backups' })
export class PostBackup {
  @Prop({ required: true, unique: true, index: true })
  postId: string;

  @Prop({ required: true, index: true })
  createdBy: string; // Doimo string!

  @Prop({ type: Object })
  payload: Record<string, any>;

  @Prop({ type: Array, default: [] })
  executionLogs: Array<{
    targetId: string;
    targetType: string;
    attemptAt: Date;
    status: string;
    error?: string;
  }>;
}
```

Bu yondashuv asosiy PostgreSQL bazasini millionlab vaqtinchalik loglar bilan shishib ketishidan (database bloat) asraydi.

---

## 6. DTO Xaritalash va Tip Xavfsizligi (Type Safety)

Prisma Client avtomatik ravishda TypeScript interfeyslarini hosil qiladi. DTO larda String turini qat'iy ushlab turish orqali kontroller va servislar o'rtasida konvertatsiya xatolarining oldi olinadi:

```typescript
// CreateChannelDto
export class CreateChannelDto {
  @IsString()
  @IsNotEmpty()
  chatId: string; // "-1002234567890"

  @IsString()
  @IsNotEmpty()
  title: string;

  @IsString()
  @IsOptional()
  username?: string;
}

// Post Target Selection Interface
export interface SelectedTarget {
  id: string; // Database UUID
  chatId: string; // Telegram String ID
  type: 'CHANNEL' | 'GROUP';
  title: string;
}
```

---

## 7. Migratsiya Strategiyasi: `prisma db push` vs `prisma migrate dev`

`bot_post_using` loyihasining rivojlanish bosqichida `npx prisma db push` ishlatilgan. Ammo tizim production darajasiga yetganda quyidagi farqlarni bilish shart:

1. **`prisma db push` (Prototip va Dastlabki Ishlab Chiqish):**
   - Sxemani to'g'ridan-to'g'ri bazaga suradi, migratsiya fayllari yaratmaydi.
   - Tez o'zgarishlar uchun qulay, ammo productionda ma'lumotlarni tasodifan yo'qotish (data loss) xavfi mavjud.
2. **`prisma migrate dev` (Ishlab Chiqarish va CI/CD Standarti):**
   - Har bir o'zgarish uchun SQL migratsiya faylini yaratadi (`prisma/migrations/202609..._init/migration.sql`).
   - Versiyalarni kuzatish (migration history) va rollback imkonini beradi.
   - `telegramId` ni `BigInt` dan `VarChar(64)` ga o'tkazish kabi jiddiy o'zgarishlarda SQL dagi `USING telegram_id::varchar(64)` iborasi bilan xavfsiz konvertatsiyani ta'minlaydi:
     ```sql
     ALTER TABLE "users" ALTER COLUMN "telegram_id" TYPE VARCHAR(64) USING "telegram_id"::VARCHAR(64);
     ```

---

## 8. Xulosa

Yuqori yuklamali Telegram botlarida Prisma ORM sxemasini loyihalashda quyidagi qoidalarga amal qilish tavsiya etiladi:
- Ichki birlamchi kalitlar uchun UUID v4 (`String @id @default(uuid())`).
- Barcha Telegram User va Chat identifikatorlari uchun `String @db.VarChar(64)`.
- Xabar identifikatorlari uchun chat ichidagi chegarani hisobga olgan holda `Int?`.
- Post va uning chatlari o'rtasida `onDelete: Cascade`, chat va post hisobotlari o'rtasida esa `onDelete: SetNull`.
- Asosiy relatsion ma'lumotlar uchun PostgreSQL, holat zaxirasi va harakat loglari uchun MongoDB TTL kolleksiyalari.
