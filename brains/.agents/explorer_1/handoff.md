# 📋 Texnik Tekshiruv Hisoboti (Handoff Report) — Explorer 1

**Loyiha:** `bot_post_using` (`/home/fayzillo/Desktop/Loyihalar/bot_post_using`)  
**Tadqiqotchi:** Explorer 1 (Codebase & Database Architecture Investigator)  
**Sana:** 2026-09-06  
**Status:** Muvaffaqiyatli yakunlandi  

---

## 1. Observation (To'g'ridan-to'g'ri Kuzatuvlar va Dalillar)

### 1.1 Loyiha Strukturasi va Atrof-muhit
Loyiha NestJS 11 frameworki asosida qurilgan modulli backend va Telegram bot ilovasi hisoblanadi:
- **Asosiy papka strukturasi:**
  - `src/main.ts`: Ilovaning kirish nuqtasi (`bootstrap`).
  - `src/core/`: Global infratuzilma servislari (`prisma.service.ts`, `redis.service.ts`, `state.service.ts`, `message_queue.service.ts`, `bot_connector.service.ts`, `post_formatter.service.ts`, `voice_transcriber.service.ts`, MongoDB sxemalari).
  - `src/global/`: Xavfsizlik va monitoring (`user_filter.guard.ts`, `all-exceptions.filter.ts`, `logger.service.ts`).
  - `src/common/`: Konfiguratsiyalar (`configuration.ts`), turlar (`types/index.ts`), yordamchilar (`_cb_functions/index.ts`, `_message_generator/index.ts`, `date_parser.ts`).
  - `src/modules/`: Biznes domenlari (`admin/`, `channels/`, `groups/`, `posts/`, `users/`).
  - `prisma/`: Prisma sxemasi (`schema.prisma`).

### 1.2 `package.json` va Asosiy Bog'liqliklar (`package.json:22-39, 57`)
Loyiha quyidagi texnologiyalar stekidan foydalanadi:
```json
"dependencies": {
  "@nestjs/bullmq": "^12.0.0",
  "@nestjs/common": "^11.0.1",
  "@nestjs/config": "^12.0.0",
  "@nestjs/core": "^11.0.1",
  "@nestjs/mongoose": "^12.0.0",
  "@nestjs/platform-express": "^11.0.1",
  "@prisma/client": "^6.4.1",
  "bullmq": "^6.3.4",
  "ioredis": "^6.0.0",
  "mongoose": "^9.9.5",
  "nestjs-telegraf": "^2.9.1",
  "reflect-metadata": "^0.2.2",
  "rxjs": "^7.8.1",
  "telegraf": "^4.16.3"
},
"devDependencies": {
  "prisma": "^6.4.1",
  "typescript": "^5.7.3"
}
```

### 1.3 TypeScript Konfiguratsiyasi va Kirish Nuqtasi
- **`tsconfig.json`:**
  - `target: "ES2023"`, `module: "commonjs"`, `strictNullChecks: true`, `emitDecoratorMetadata: true`, `experimentalDecorators: true`.
- **`src/main.ts:5-15`:**
  ```typescript
  async function bootstrap() {
    const app = await NestFactory.create(AppModule, { bufferLogs: true });
    await initializeApp(app);
    const port = process.env.PORT || 3000;
    await app.listen(port);
  }
  ```
- **`src/core/initialition.ts:5-28`:**
  `AllExceptionsFilter`, `ValidationPipe` (whitelist, transform) va CORS sozlamalarini ulaydi.

### 1.4 Prisma Sxemasi va Baza Modellari (`prisma/schema.prisma:1-105`)
- **Datasource:** PostgreSQL (`provider = "postgresql"`, `url = env("DATABASE_URL")`).
- **Generator:** `prisma-client-js`.
- **Modellar va Maydonlar:**
  1. **`User` (`@@map("users")`)**:
     - `id String @id @default(uuid())`: Ichki birlamchi kalit (UUID v4).
     - `telegramId BigInt @unique @map("telegram_id")`: Telegram foydalanuvchi ID raqami.
     - `firstName String?`, `lastName String?`, `username String?`, `isAllowed Boolean @default(false)`.
     - `posts Post[]`: 1-ga-ko'p bog'liqlik.
  2. **`Channel` (`@@map("channels")`)**:
     - `id String @id @default(uuid())`: Ichki UUID.
     - `chatId BigInt @unique @map("chat_id")`: Telegram kanal chat ID raqami.
     - `title String`, `username String?`, `type TargetType @default(CHANNEL)`.
     - `hasAdmin Boolean @default(true)`, `canPost Boolean @default(true)`.
     - `postTargets PostTarget[]`.
  3. **`Group` (`@@map("groups")`)**:
     - `id String @id @default(uuid())`: Ichki UUID.
     - `chatId BigInt @unique @map("chat_id")`: Telegram guruh chat ID raqami.
     - `title String`, `username String?`, `type TargetType @default(GROUP)`.
     - `hasAdmin Boolean @default(true)`, `canPost Boolean @default(true)`.
     - `postTargets PostTarget[]`.
  4. **`Post` (`@@map("posts")`)**:
     - `id String @id @default(uuid())`: Post UUID.
     - `text String? @db.Text`: Post matni (HTML/Markdown teglari bilan).
     - `mediaType String?`, `mediaFileId String?`: Rasm, video yoki hujjat identifikatori.
     - `scheduledAt DateTime?`, `sentAt DateTime?`.
     - `status PostStatus @default(DRAFT)` (`DRAFT`, `SCHEDULED`, `SENT`, `FAILED`, `CANCELLED`).
     - `createdBy BigInt @map("created_by")`: Muallifning Telegram ID raqami.
     - `user User? @relation(fields: [createdBy], references: [telegramId])`.
     - `targets PostTarget[]`.
  5. **`PostTarget` (`@@map("post_targets")`)**:
     - `id String @id @default(uuid())`.
     - `postId String @map("post_id")`: Bog'langan post UUID si.
     - `targetType TargetType @map("target_type")`: `CHANNEL` yoki `GROUP`.
     - `channelId String? @map("channel_id")`, `groupId String? @map("group_id")`.
     - `status PostStatus @default(SCHEDULED)`.
     - `errorMessage String?`, `messageId Int? @map("message_id")`.
     - `post Post @relation(fields: [postId], references: [id], onDelete: Cascade)`.
     - `channel Channel? @relation(fields: [channelId], references: [id], onDelete: SetNull)`.
     - `group Group? @relation(fields: [groupId], references: [id], onDelete: SetNull)`.
- **Migratsiyalar:** `prisma/migrations` papkasi mavjud emas. Tarixiy yozuv (`history/task_001_2026-09-06_.md:29`) tasdiqlaydi: sxema PostgreSQL bazasiga `npx prisma db push` orqali to'g'ridan-to'g'ri sinxronlashtirilgan.

### 1.5 ID Turlarining Amaldagi Holati (Kuzatuv Matritsasi)

| Ob'ekt | Maydon | Prisma Tipi | PostgreSQL Tipi | TypeScript Tipi | Telegram API Tipi |
|---|---|---|---|---|---|
| **User** | `id` | `String` | `uuid / varchar` | `string` | — (Ichki UUID) |
| **User** | `telegramId` | `BigInt` | `int8 (BIGINT)` | `bigint` | 64-bit integer |
| **Channel** | `chatId` | `BigInt` | `int8 (BIGINT)` | `bigint` | Manfiy 64-bit integer (`-100...`) |
| **Group** | `chatId` | `BigInt` | `int8 (BIGINT)` | `bigint` | Manfiy 64-bit integer (`-...`) |
| **Post** | `createdBy` | `BigInt` | `int8 (BIGINT)` | `bigint` | 64-bit integer |
| **PostTarget** | `messageId` | `Int?` | `int4 (INTEGER)` | `number \| null` | 32-bit sequential int |

### 1.6 Codebase Bo'ylab BigInt Keltirib Chiqargan Qiyinchiliklar va Sun'iy O'zgartirishlar

Koddagi bevosita dalillar:
1. **`src/core/state.service.ts:76-80`**: Redis va `JSON.stringify` BigInt ni serialize qila olmagani sababli qo'lda o'zgartirish:
   ```typescript
   // 2. Redis keshga yozish (24 soat TTL)
   const serializableState = {
     ...state,
     userId: state.userId.toString(),
   };
   await this.redisService.set(`session:${userKey}`, JSON.stringify(serializableState), 86400);
   ```
   Va `src/core/state.service.ts:31-32` keshdan o'qilganda qayta tiklash:
   ```typescript
   const parsed = JSON.parse(redisData) as UserSessionState;
   parsed.userId = BigInt(parsed.userId);
   ```
2. **MongoDB Schemas (`src/core/schemas/state-backup.schema.ts:9` va `post-backup.schema.ts:27`)**:
   MongoDB (Mongoose) ga yozishda BigInt ishlatilmagan, balki majburiy ravishda `string` deb e'lon qilingan:
   ```typescript
   // StateBackup:
   @Prop({ required: true, unique: true, index: true })
   userId: string;
   // PostBackup:
   @Prop({ required: true, index: true })
   createdBy: string;
   ```
3. **`src/modules/users/users.service.ts:78-85, 108-111, 126-134`**:
   REST API orqali javob qaytarilganda, Prisma qaytargan obyekt to'g'ridan-to'g'ri Express `res.json()` ga berilsa `TypeError: Do not know how to serialize a BigInt` otiladi. Shu sababli har bir metodda `.map()` qilinib, `telegramId: u.telegramId.toString()` ga aylantirilgan:
   ```typescript
   const formatted = dbUsers.map((u) => ({
     id: u.id,
     telegramId: u.telegramId.toString(),
     firstName: u.firstName,
     ...
   }));
   ```
4. **`src/core/message_queue.service.ts:163`**:
   BullMQ navbatiga job yuklanganda `createdBy` stringga o'girilgan:
   ```typescript
   await this.queue.add(
     'send_post',
     { postId: post.id, createdBy: post.createdBy.toString() },
     ...
   );
   ```
5. **`src/core/bot_connector.service.ts:79-152`**:
   Barcha Telegraf jo'natish metodlarida `chatId: string | number | bigint` qabul qilinib, darhol `chatId.toString()` chaqirilgan:
   ```typescript
   await this.bot.telegram.sendMessage(chatId.toString(), text, ...);
   ```

### 1.7 Baza Aloqalari va Polimorfizm
- **`User` -> `Post`**: 1-ga-ko'p. `Post.createdBy` maydoni `User.telegramId` maydoniga `@relation(fields: [createdBy], references: [telegramId])` orqali bog'langan (diqqat: `User.id` ga emas, `@unique` bo'lgan `telegramId` ga bog'langan).
- **`Post` -> `PostTarget`**: 1-ga-ko'p, `@relation(fields: [postId], references: [id], onDelete: Cascade)`. Post o'chirilganda uning barcha targetlari bazadan avtomatik kaskadli o'chiriladi.
- **`PostTarget` -> `Channel` & `Group`**: Polimorf n-ga-1. `targetType: TargetType` enumi orqali ajratiladi. Har bir target uchun `channelId` yoki `groupId` maydoni to'ldiriladi (`onDelete: SetNull`).

### 1.8 Tugmalar, Sozlamalar va State Boshqaruvi
- **Tugmalar DB ga yozilmaydi:** Inline va Reply tugmalar relatsion bazada saqlanmaydi, balki `CallbackKeyboardBuilder` (`src/common/utils/_cb_functions/index.ts`) orqali har bir so'rovda dinamik generatsiya qilinadi.
- **3-Pog'onali State:**
  1. In-Memory `Map<string, UserSessionState>` (sub-millisekundlik tezlik).
  2. Redis (`session:<userId>`, 24 soat TTL) (server qayta yuklanganda saqlanish).
  3. MongoDB (`state_backups`, 3 kunlik TTL index) (uzoq muddatli zaxira).
- **Xavfsizlik Sozlamalari:**
  - `User.isAllowed`: Foydalanuvchiga post yaratish ruxsati.
  - `Channel.hasAdmin` / `canPost`, `Group.hasAdmin` / `canPost`: Botning chatdagi post yuborish imkoniyatlari.

---

## 2. Logic Chain (Mantiqiy Tahlil va Asoslash Zanjiri)

### 1-qadam: Telegram ID larining tabiatini anglash
- *Kuzatuv:* Telegram foydalanuvchi ID lari hozirda 6-8 milliarddan oshgan, guruh va kanal ID lari esa `-100` prefiksi bilan boshlanadigan 13-14 xonali manfiy sonlardir (masalan, `-1002234567890`).
- *Mantiqiy xulosa:* Ushbu sonlar 32-bitli integer chegarasidan (`2^31 - 1 = 2,147,483,647`) ancha katta. Shuning uchun bazada ularni `Int` (int4) sifatida saqlash imkonsiz.

### 2-qadam: JavaScript `MAX_SAFE_INTEGER` chegarasi va xavfi
- *Kuzatuv:* JavaScript tili barcha oddiy sonlarni IEEE 754 ikki karra aniqlikdagi suzuvchi nuqtali (Double Precision Float) formatda saqlaydi.
- *Mantiq:* `Number.MAX_SAFE_INTEGER = 2^53 - 1 = 9,007,199,254,740,991` (16 xona). Agar son ushbu chegaradan oshsa, JavaScript eng oxirgi xonalarni yaxlitlab tashlaydi (masalan, `9007199254740993 === 9007199254740992` bo'lib qoladi). Agar Telegram ID lar son sifatida JSON orqali parse qilinsa yoki frontendga uzatilsa, ID ning oxirgi raqamlari buziladi va xabarlar mutlaqo boshqa foydalanuvchi/chatga yuborilishi yoki topilmasligi xavfi yuzaga keladi.

### 3-qadam: Prisma va Node.js da `BigInt` ning seriyalashtirish fojeasi
- *Kuzatuv:* Prisma sxemasida `BigInt` ishlatilganda, Prisma Client ma'lumotni JavaScript `bigint` (masalan, `123456789n`) ko'rinishida qaytaradi.
- *Mantiq:* ECMAScript spetsifikatsiyasiga ko'ra, `JSON.stringify()` standart holatda `BigInt` turini qabul qilmaydi va to'g'ridan-to'g'ri `TypeError: Do not know how to serialize a BigInt` istisnosini otadi.
- *Oqibat:*
  - Express kontrollerlari (`res.json()`) orqali `User` modelini to'g'ridan-to'g'ri qaytarib bo'lmaydi (HTTP 500 beradi).
  - Redis ga kesh yozishda `JSON.stringify(state)` xato beradi.
  - BullMQ orqali Redis navbatiga job yuklashda xato beradi.
  - Dasturchi butun loyiha bo'ylab o'nlab joyda `.toString()` va `BigInt(...)` bilan qo'lda konvertatsiya qilishga majbur bo'lgan (`state.service.ts:78`, `users.service.ts:80`, `message_queue.service.ts:163`). Agar biror yangi dasturchi bitta joyda `.toString()` ni esdan chiqarsa, butun bot yoki API krash bo'ladi.

### 4-qadam: Semantik to'g'rilik (Domain-Driven Design)
- *Kuzatuv:* Telegram User ID yoki Chat ID ustida HECH QACHON arifmetik amallar bajarilmaydi (ularni qo'shish, ayirish, o'rtachasini topish mantiqqa zid).
- *Mantiq:* Telegram ID lar miqdor (quantity) emas, balki **shaxsiyat tokeni (opaque identifier / token)** hisoblanadi. Shuning uchun ularni son emas, matn (`String`) sifatida saqlash DDD (Domain-Driven Design) tamoyillariga 100% mos keladi.

### 5-qadam: PostgreSQL `int8` (BIGINT) va `VARCHAR` / `TEXT` taqqoslovi
- *Kuzatuv:* PostgreSQL da `VARCHAR(64)` yoki `TEXT` ustiga `UNIQUE INDEX` qo'yilganda, qidiruv B-tree indeksi orqali O(log N) murakkablikda amalga oshiriladi.
- *Mantiq:* Disk maydoni bo'yicha farq minimal (8 bayt vs ~16 bayt). Biroq `VARCHAR(64)`/`String` ishlatilganda:
  1. Node.js, Express, NestJS, Redis, MongoDB va BullMQ o'rtasida 100% tip uyg'unligi (type consistency) ta'minlanadi.
  2. Barcha `JSON.stringify` va `JSON.parse` operatsiyalari xatosiz, tabiiy ishlaydi.
  3. DTO va kontrollerlarda ortiqcha manual transformerlar (`.toString()`, `BigInt()`) talab etilmaydi.
  4. Web/Frontend dashboard integratsiyasida JavaScript bit-truncation muammosi butunlay yo'qoladi.

---

## 3. Caveats (Cheklovlar va Hisobga Olingan Holatlar)

1. **Joriy Prisma sxemasining holati:** `bot_post_using` loyihasida hozirgi paytda `telegramId` va `chatId` maydonlari `BigInt` qilib qo'yilgan. Dasturchi ushbu arxitekturaviy og'riqni his qilib, servislar qatlamida sun'iy ravishda `.toString()` orqali yamoqlar (workarounds) qo'llagan. Raqamli Miya (`~/Downloads/brains/`) bazasiga ushbu tajriba "Nega String majburiy" darsi sifatida kiritilishi lozim.
2. **PostTarget MessageId:** Telegram xabar ID si (`messageId`) bitta chat doirasida 32-bitli butun son bo'lgani uchun `Int?` sifatida qoldirilishi xavfsiz (u hech qachon 2 milliarddan oshmaydi).
3. **Migratsiya fayllari:** Loyihada `prisma/migrations/` mavjud emasligi sababli, ishlab chiqarishga (production) o'tishda `prisma migrate dev` orqali toza migratsiya fayllarini yaratish tavsiya etiladi.

---

## 4. Conclusion (Xulosa va Tavsiyalar)

1. **Arxitekturaviy xulosa:** Telegram botlari va tarmoq ilovalarida har qanday tashqi tizim identifikatorlari (Telegram User ID, Chat ID, Channel ID, Discord ID, Twitter ID) ma'lumotlar bazasida qat'iy **`String` (`VARCHAR`)** sifatida saqlanishi shart.
2. **Keltirgan asoratlari:** `bot_post_using` loyihasida `BigInt` tanlanishi oqibatida:
   - Redis va BullMQ ga ma'lumot yozishda `JSON.stringify` nosozliklari yuzaga kelgan.
   - MongoDB zaxira modellarida majburan `String` ishlatilib, oraliq konvertorlar yozilgan.
   - REST API da har bir foydalanuvchini DTO ga xaritalashda `.toString()` yozishga majbur bo'lingan.
3. **Raqamli Miyaga kiritish tavsiyasi:**
   - Ushbu topilmalar `~/Downloads/brains/grouped-md/05-id-string-db-majburiy` va `23-prisma-id-string-va` klasterlariga arxitekturaviy qoida sifatida kiritilishi kerak.

---

## 5. Verification Method (Mustaqil Tekshirish Usullari)

Quyidagi buyruqlar va fayllar orqali hisobotdagi dalillarni tekshirish mumkin:

1. **Prisma sxemasidagi tiplarni tekshirish:**
   ```bash
   grep -n "BigInt" /home/fayzillo/Desktop/Loyihalar/bot_post_using/prisma/schema.prisma
   ```
   *Kutilgan natija:* 25, 40, 56, 78-qatorlarda `telegramId BigInt`, `chatId BigInt`, `createdBy BigInt`.

2. **StateService dagi BigInt serialization yechimini ko'rish:**
   ```bash
   sed -n '75,82p' /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/core/state.service.ts
   ```
   *Kutilgan natija:* `userId: state.userId.toString()` va `JSON.stringify(serializableState)`.

3. **UsersService dagi manual `.toString()` konvertatsiyasini ko'rish:**
   ```bash
   sed -n '126,134p' /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/users/users.service.ts
   ```
   *Kutilgan natija:* `telegramId: u.telegramId.toString()`.

4. **MongoDB modellarida string ishlatilganini ko'rish:**
   ```bash
   grep -n "userId:" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/core/schemas/state-backup.schema.ts
   grep -n "createdBy:" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/core/schemas/post-backup.schema.ts
   ```
   *Kutilgan natija:* Ikkala faylda ham `userId: string` va `createdBy: string`.

5. **Invalitsiya sharti:**
   Agar PostgreSQL da `chatId` ustida matematik hisob-kitoblar zarur bo'lsa yoki Node.js `JSON.stringify` standart ravishda `BigInt` ni qabul qilsa, bu xulosa qayta ko'rib chiqilishi mumkin. Biroq ECMAScript spetsifikatsiyasi va Telegram Bot API arxitekturasi buni inkor etadi.
