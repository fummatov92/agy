# 📊 Handoff Report: Telegram Bot Arxitekturasi, Telegraf Regex Kolliziyalari va Huquqlarni Tekshirish

- **Tadqiqotchi:** Explorer 2 (Telegram Bot Architecture & Edge Cases Investigator)
- **Sana:** 2026-09-06T22:30:00+05:00
- **Loyiha manzili:** `/home/fayzillo/Desktop/Loyihalar/bot_post_using`
- **Tadqiqot holati:** To'liq yakunlandi (Comprehensive Read-Only Investigation)

---

## 1. Observation (Bevosita Kuzatuvlar va Dalillar)

Loyihaning kod bazasi (`/home/fayzillo/Desktop/Loyihalar/bot_post_using`) va rivojlanish tarixi (`history/task_001_...` dan `history/task_021_...` gacha, hamda `git log` diff'lari) tahlil qilinganda quyidagi aniq faktlar va kod bloklari kuzatildi:

### 1.1. Bot Arxitekturasi va Telegraf Instansiyasi
- **Entry point va Modul integratsiyasi:**
  - `src/main.ts:6-15`: NestFactory orqali ilova ishga tushadi, `initializeApp(app)` chaqiriladi.
  - `src/app.module.ts:9-18`: `CoreModule`, `AdminModule`, `ChannelsModule`, `GroupsModule`, `PostsModule`, `UsersModule` ulanadi.
  - `src/core/core.module.ts:37-43`: `TelegrafModule.forRootAsync` orqali bot token `ConfigService` dan olinadi. Biroq Telegraf standart `session()` middleware'i yoki Telegraf `WizardScene` ulanmagan.
  - `src/core/bot_connector.service.ts:12-42`: `BotConnectorService` singleton provayder bo'lib, `onModuleInit` bosqichida `this.bot.telegram.getMe()` orqali bot ID, username va nomini olib, `BotMetadata` statik o'zgaruvchisiga saqlaydi (`BotConnectorService.getBotName()`, `BotConnectorService.getBotUsername()`).

### 1.2. Sessiya va State Arxitekturasi (3-Tier State Machine)
- `src/core/state.service.ts:8-108`: Telegrafning xotiradagi omonat `session()` o'rniga maxsus **3 bosqichli State Machine** yaratilgan:
  1. **Tier 1 (In-Memory Map):** `this.memoryState = new Map<string, UserSessionState>()` — foydalanuvchi qadamma-qadam wizardda harakatlanayotganda nol kechikish (zero-latency).
  2. **Tier 2 (Redis Cache):** `session:${userKey}` (TTL: 86400s / 24 soat) — jarayonlararo kesh va tezkor qayta yuklash.
  3. **Tier 3 (MongoDB Persistent Backup):** `this.stateBackupModel.findOneAndUpdate({ userId }, ..., { upsert: true })` — to'liq server restart, deploy yoki avariya holatida ham foydalanuvchining loyihasi (draftPost) va qadami (step) yo'qolmasligi uchun MongoDB zaxira bazasi.
- **BigInt JSON Serialization himoyasi:**
  - `src/core/state.service.ts:21, 70, 78`: `userId` kaliti doim `userId.toString()` shaklida saqlanadi. Aks holda Node.js da `JSON.stringify` chaqirilganda `TypeError: Do not know how to serialize a BigInt` xatosi chiqib, bot qulashi kuzatiladi.

### 1.3. UserFilterGuard va Xavfsizlik
- `src/global/user_filter/user_filter.guard.ts:8-42`:
  - `TelegrafExecutionContext.create(context)` orqali Telegram Context olinadi.
  - `src/global/user_filter/user_filter.guard.ts:23-26`:
    ```typescript
    const update = ctx.update as any;
    if (update && update.my_chat_member) {
      return true;
    }
    ```
    Bu tekshiruv bot kanal yoki guruhga qo'shilganda (`my_chat_member` event) guard tomonidan bloklanib qolmasdan, to'g'ridan-to'g'ri `AdminUpdate.onMyChatMember` handleriga o'tishini ta'minlaydi.
  - `src/global/user_filter/user_filter.guard.ts:28-35`: `UsersService.isUserAllowed(userId)` tekshiriladi (avval `.env`, so'ng Redis `allowed_user:${id}`, so'ng PostgreSQL `prisma.user`). Ruxsatsiz bo'lsa:
    ```typescript
    ctx.reply(MessageGenerator.accessDeniedMessage(), { parse_mode: 'HTML' }).catch(() => {});
    return false;
    ```
    `.catch(() => {})` bloklangan userlar uchun 403 xatosini xavfsiz yutadi.

### 1.4. Telegraf Regex Kolliziyalari (Collision) va Ularning Yechimi
- `src/modules/admin/admin.update.ts`:
  - Dastlabki commitlarda (`git log -S"Action(" -p`) quyidagi action listenerlar bo'lgan:
    - `@Action('back_to_posts')` — statik string bo'lgan.
    - `@Action(/switch_posts:(.+)/)` — `^` anchorsiz bo'lgan.
    - `@Action(/view_post:(.+)/)` — `^` anchorsiz bo'lgan.
    - `@Action(/send_now:(.+)/)` — `^` anchorsiz bo'lgan.
    - `@Action(/delete_post:(.+)/)` — `^` anchorsiz bo'lgan.
    - `@Action(/delete_channel:(.+)/)` — `^` anchorsiz bo'lgan.
    - `@Action(/delete_group:(.+)/)` — `^` anchorsiz bo'lgan.
  - **Kolliziya 1: Substring to'qnashuvlari (Unanchored RegExp Collision):**
    RegExp boshlang'ich `^` anchorisiz ishlatilganda, masalan `/delete_post:(.+)/`, Telegraf uning substringini qidiradi. Natijada `cancel_delete_post:123` yoki `confirm_delete_post:123` kabi callbacklar ham adashib `delete_post` handleriga tushgan.
  - **Kolliziya 2: Statik string va parametrli callback to'qnashuvi (`back_to_posts` muammosi):**
    Task 008 (`history/task_008_2026-09-06_.md`) va commit `9ddf82b` da e'lonlarni kutilayotgan (`SCHEDULED`) va arxiv (`SENT`) toifalariga ajratib, orqaga qaytishda aynan o'sha toifaga qaytish talabi qo'yilgan (`back_to_posts:SCHEDULED` va `back_to_posts:SENT`).
    Agar handler `@Action('back_to_posts')` sifatida qolsa, Telegraf faqat to'liq tenglikni tekshirgani sababli parametrli `back_to_posts:SENT` ishlamay qolgan.
    Agar `@Action(/back_to_posts:(.+)/)` qilinsa, parametrsiz eski `back_to_posts` chaqiruvlari qulagan.
    **Yechim:**
    `src/modules/admin/admin.update.ts:1523`:
    ```typescript
    @Action(/^back_to_posts(?::(.+))?/)
    async onBackToPosts(@Ctx() ctx: Context) {
      const match = (ctx as any).match;
      const category: 'SCHEDULED' | 'SENT' = (match && match[1] === 'SENT') ? 'SENT' : 'SCHEDULED';
      ...
    }
    ```
    `^` langari bilan boshlanishi ta'minlangan, `(?::(.+))?` ixtiyoriy capture group orqali ham parametrsiz (`back_to_posts`), ham parametrli (`back_to_posts:SENT`) callbacklar bitta xavfsiz regex orqali ushlangan.
  - **Kolliziya 3: To'liq Regex Langarlari (`^` Anchor Refactoring):**
    Hozirgi `src/modules/admin/admin.update.ts` faylidagi barcha 11 ta dinamik action qat'iy boshlang'ich `^` belgisi bilan himoyalangan:
    - Qator 915: `@Action(/^toggle_target:(.+)/)`
    - Qator 1072: `@Action(/^switch_posts:(.+)/)`
    - Qator 1104: `@Action(/^page_posts:(SCHEDULED|SENT):(\d+)/)`
    - Qator 1143: `@Action(/^view_post:(.+)/)`
    - Qator 1195: `@Action(/^ai_reformat:(.+)/)`
    - Qator 1242: `@Action(/^apply_ai_reformat:(.+)/)`
    - Qator 1310: `@Action(/^cancel_ai_reformat:(.+)/)`
    - Qator 1356: `@Action(/^send_now:(.+)/)`
    - Qator 1371: `@Action(/^delete_post:(.+)/)`
    - Qator 1444: `@Action(/^delete_channel:(.+)/)`
    - Qator 1486: `@Action(/^delete_group:(.+)/)`
    - Qator 1523: `@Action(/^back_to_posts(?::(.+))?/)`
  - **Kolliziya 4: Paginatsiya va Delimiter konvensiyasi:**
    `@Action(/^page_posts:(SCHEDULED|SENT):(\d+)/)` — greedy `.+` o'rniga aniq enum `(SCHEDULED|SENT)` va raqam `(\d+)` belgilangan. Bu boshqa post amallari bilan chalkashishning oldini oladi.

### 1.5. Guruh va Kanal Huquqlarini Tekshirish & 403 Forbidden
- **Kanallar huquqlarini tekshirish (`src/modules/channels/channels.service.ts:42-87`):**
  - Havolani tozalash: `t.me/` olib tashlanib `@` formatiga keltiriladi.
  - `chat = await telegram.getChat(cleanInput)`: Chat topilmasa yoki bot a'zo bo'lmasa Telegram xatosi granular `try/catch` da ushlanadi.
  - Chat turi tekshiruvi: `if (chat.type !== 'channel')`.
  - Adminlik va xabar yozish tekshiruvi:
    ```typescript
    chatMember = await telegram.getChatMember(chat.id, botInfo.id);
    const isCreator = chatMember.status === 'creator';
    const isAdmin = chatMember.status === 'administrator' || isCreator;
    const canPost = Boolean(isCreator || chatMember.can_post_messages);
    ```
  - Aniq xatolik differensiatsiyasi:
    1. Agar `!isAdmin` bo'lsa: `⚠️ Bot "${chat.title}" kanalida administrator emas.`
    2. Agar `isAdmin` lekin `!canPost` bo'lsa: `⚠️ Bot "${chat.title}" kanalida administrator, lekin unda "Post yuborish (Post Messages)" huquqi yo'q!`
- **Guruhlar huquqlarini tekshirish (`src/modules/groups/groups.service.ts:41-88`):**
  - Chat turi tekshiruvi: `chat.type !== 'group' && chat.type !== 'supergroup'`.
  - Haydalgan yoki chiqqan holat:
    `if (chatMember.status === 'left' || chatMember.status === 'kicked')` -> `⚠️ Bot "${chat.title}" guruhiga a'zo emas (yoki chiqarib yuborilgan).`
  - Huquqi cheklangan holat:
    ```typescript
    const isRestricted = chatMember.status === 'restricted';
    const canSendMessages = isRestricted ? chatMember.can_send_messages !== false : true;
    if (isRestricted && !canSendMessages) { ... }
    ```
- **Xabar tarqatishda 403/Telegram API xatolarini lokallashtirish (Exception Containment):**
  - `src/modules/posts/posts.service.ts:150-217`:
    Post bir nechta kanallar va guruhlarga tarqatilayotganda `for (const target of post.targets)` sikli ichida har bir jo'natish alohida `try/catch` bilan o'ralgan.
    Agar bitta kanalda bot adminlikdan olingan bo'lsa (403 Forbidden) yoki guruh o'chirilgan bo'lsa:
    1. Sikl to'xtamaydi (`continue` orqali keyingi chatlarga jo'natish davom etadi).
    2. Ushbu target uchun PostgreSQL da `status: 'FAILED', errorMessage: err.message` yoziladi.
    3. MongoDB `executionLogs` massiviga xatolik vaqti va xabari push qilinadi.
    4. Postning umumiy statusi `successCount > 0 ? 'SENT' : 'FAILED'` qilib belgilanadi.
- **Ruxsatsiz bot qo'shilishidan himoya (`my_chat_member`):**
  - `src/modules/admin/admin.update.ts:63-125`:
    Agar bot kanal yoki guruhga qo'shilsa, `my_chat_member.from.id` tekshiriladi.
    Agar u `isUserAllowed` dan o'tmasa, bot ogohlantirish berib, `await ctx.telegram.leaveChat(chat.id)` orqali chatdan darhol chiqib ketadi.

### 1.6. Xatoliklarni Ushlash va Xavfsiz Reply/Edit Strategiyalari
- **HTML Parsing Fallback:**
  - `src/modules/admin/admin.update.ts:34-54`:
    `safeReply` va `safeEditMessageText` yordamchi metodlari:
    Agar Telegram `parse_mode: 'HTML'` bilan yuborilgan xabarda noto'g'ri teglarni ko'rib `Bad Request: can't parse entities` xatosini bersa, metod avtomatik ravishda `text.replace(/<[^>]*>?/gm, '')` orqali HTML teglarni tozalab, oddiy matn rejimida qayta jo'natadi.
- **Clean UX & Chat Tozaligi:**
  - Bekor qilish bosilganda `ctx.deleteMessage()` orqali ortiqcha xabarlar o'chiriladi.
  - Yangi xabarlar yuborish o'rniga mavjud xabar `safeEditMessageText` orqali yangilanadi (Task 014 va Task 019).
- **BullMQ Navbat va Rate Limiting:**
  - `src/core/message_queue.service.ts:27-190`:
    Postlarni rejalashtirilgan vaqtda yuborish Redis asosidagi BullMQ orqali amalga oshiriladi.
    Job ID deterministik qilib berilgan (`jobId: 'post_${postId}'`), bu takroriy jo'natishni oldini oladi va foydalanuvchi "Darhol yuborish" yoki "O'chirish" ni bosganda `job.remove()` orqali navbatdan O(1) vaqtda bekor qilinadi.
    Server restart bo'lganda `rehydratePendingJobs()` orqali PostgreSQL dagi barcha kutilayotgan postlar navbatga avtomatik qayta tiklanadi.

---

## 2. Logic Chain (Mantiqiy Zanjir va Tahlil)

1. **Bot Framework & Initsializatsiya tanlovi:**
   - *Kuzatuv:* NestJS ekotizimi `nestjs-telegraf` deklarativ dekoratorlaridan foydalanadi, lekin Telegrafning standart sessiya mexanizmlari ishlatilmagan (`core.module.ts`).
   - *Mantiqiy tahlil:* Telegram botlarida buyruqlar va xabarlar oqimida foydalanuvchi holati (state) server restart bo'lganda yoki ko'p instansiyali deployda yo'qolib ketmasligi kerak. Telegrafning standart xotiradagi `session()`i server qayta yuklanganda nobud bo'ladi. Shu sababli ishlab chiquvchilar NestJS servisi sifatida In-Memory Map + Redis + MongoDB uch bosqichli holat mashinasini qurgan.
   - *Xulosa:* Bot arxitekturasi tashqi infratuzilma buzilishlariga chidamli (fault-tolerant) qilib loyihalashtirilgan.

2. **Regex Kolliziyasining Kelib Chiqishi va Mexanikasi:**
   - *Kuzatuv:* Callback datalari `action:payload` (masalan, `delete_post:clx...`, `view_post:clx...`) ko'rinishida tuzilgan. Dastlabki kodda `@Action(/pattern/)` ishlatilgan bo'lsa, keyinchalik barchasi `@Action(/^pattern/)` ga o'zgartirilgan.
   - *Mantiqiy tahlil:* Telegrafning action trigger tekshiruvchisi callback_data matniga nisbatan berilgan regexni `RegExp.prototype.test()` yoki `exec()` orqali tekshiradi. Agar regex boshiga `^` qo'yilmasa, `delete_post` regexi `cancel_delete_post` yoki `confirm_delete_post` so'zlarini ham o'z ichiga olib, noto'g'ri handlerni ishga tushiradi. Bundan tashqari, `back_to_posts` kabi navigatsion tugmalar statik bo'lganidan so'ng parametrli (`back_to_posts:SENT`) ko'rinishga o'tkazilganda, qat'iy string match buzilgan.
   - *Xulosa:* Barcha action regexlariga `^` qo'yish, parametrli qismlarni `(?::(.+))?` ko'rinishida ixtiyoriy qilish va aniq ajratuvchi sifatida `:` (colon) dan foydalanish Telegrafdagi regex kolliziyalarini to'liq bartaraf etgan.

3. **Huquqlarni Tekshirishdagi Edge Caselar:**
   - *Kuzatuv:* `ChannelsService` va `GroupsService` alohida ajratilgan bo'lib, kanallarda `can_post_messages` va `isAdmin`, guruhlarda esa `restricted` va `can_send_messages !== false` tekshiriladi.
   - *Mantiqiy tahlil:* Telegram Bot API kanallar va guruhlar uchun ruxsatnomalarni turlicha modelda taqdim etadi. Kanallarda bot faqat `administrator` yoki `creator` bo'lsagina post qo'ya oladi, oddiy a'zo bo'la olmaydi. Guruhlarga esa bot oddiy a'zo bo'lib ham kirishi mumkin, lekin guruh adminlari unga `can_send_messages: false` cheklovini qo'ygan bo'lishi mumkin. Agar bu farq hisobga olinmasa, bot post yuborishda `403 Forbidden: bot is not a member of the channel` yoki `400 Bad Request: have no rights to send a message` xatolariga duch keladi.
   - *Xulosa:* Kanal va guruhlar uchun alohida ruxsatnomalar matritsasi tuzilgani va ular bazada `hasAdmin` hamda `canPost` boolean bayroqlari sifatida keshlanishi optimal arxitekturaviy yechimdir.

4. **Exception Containment va Tarqatish Ishonchliligi:**
   - *Kuzatuv:* `PostsService.sendPostNow` ichidagi targetlar bo'yicha aylanishda har bir jo'natish alohida `try/catch` qilingan.
   - *Mantiqiy tahlil:* Agar post 10 ta kanalga yuborilayotgan bo'lsa va 3-kanalda bot adminlikdan olingan bo'lsa (403 Forbidden), unhandled exception butun funksiyani to'xtatib qo'yishi va qolgan 7 ta kanalga xabar bormay qolishi mumkin edi. Granular `try/catch` xatolikni bitta target doirasida izolyatsiya qiladi va PostgreSQL hamda MongoDB da qaysi chatda qanday xatolik yuz berganini batafsil qayd etadi.

---

## 3. Caveats (Cheklovlar va Shartlar)

1. **Tadqiqot doirasi:** Ushbu tahlil faqat `/home/fayzillo/Desktop/Loyihalar/bot_post_using` loyihasi kodlari va `git` tarixi bo'yicha o'tkazildi. Kodga hech qanday o'zgartirish kiritilmadi (Read-Only).
2. **Kesh muddati:** `UsersService` dagi ruxsat berilgan adminlar keshlanishi (Redis TTL: 3600s) sababli, agar bazada to'g'ridan-to'g'ri SQL orqali user o'zgartirilsa, kesh 1 soatgacha eski holatda qolishi mumkin (garchi `UsersService.addAllowedUser` va `removeAllowedUser` orqali o'zgartirilsa kesh darhol yangilanadi).
3. **Telegram Rate Limiting:** Loyihada BullMQ worker mavjud bo'lsa-da, Telegramning global sekundi/daqiqasiga xabar yuborish limiti (30 msgs/second) uchun maxsus `bottleneck` yoki `limiter` kutubxonasi ulanmagan; ko'p targetli ommaviy yuborishda (yuzlab kanallar bo'lsa) Telegram `429 Too Many Requests: retry after X` xatosi chiqishi ehtimoli bor.

---

## 4. Conclusion (Xulosa va Tavsiyalar)

"Bot Post Using" loyihasi Telegraf va NestJS asosida qurilgan juda sifatli va tajribali ishlab chiqilgan Telegram bot hisoblanadi. Undagi quyidagi arxitekturaviy yechimlar Raqamli Miya (`~/Downloads/brains/`) va RAG tizimiga distillatsiya qilish uchun yuqori qiymatga ega:

1. **Telegraf Regex Kolliziyalarini Oldini Olish Qoidalari:**
   - Doimo boshlang'ich `^` langaridan foydalanish (`@Action(/^verb:(.+)/)`).
   - Ixtiyoriy parametrlar uchun `(?::(.+))?` sintaksisini qo'llash (orqaga qaytish va ko'p bosqichli navigatsiya uchun).
   - Murakkab holatlarda greedy `.+` o'rniga aniq regex turlarini berish (`(SCHEDULED|SENT):(\d+)`).
   - Callback data chegarasini (64 bayt) doim nazorat qilish.
2. **3-Bosqichli Holat Mashinasi (3-Tier State Machine):**
   - Standart Telegraf session o'rniga: In-Memory (tezlik) + Redis (taqsimlangan kesh) + MongoDB (falokatdan tiklanish).
   - `BigInt` ID larni serializatsiya qilishda `userId.toString()` amaliyoti.
3. **Telegram API Huquqlarini Tekshirish va 403 Xatoliklarini Yutish:**
   - Kanal va guruhlarni farqlash (`getChat` + `getChatMember`).
   - `can_post_messages` (kanallar) va `can_send_messages` (guruhlar) tekshiruvlari.
   - `my_chat_member` orqali ruxsatsiz chatlardan avtomatik chiqib ketish (`leaveChat`).
   - Ko'p targetli jo'natishda xatoliklarni izolyatsiya qilish (Exception Containment).
4. **HTML Parsing Xatoliklariga Chidamlilik:**
   - `safeReply` va `safeEditMessageText` orqali noto'g'ri HTML teglardan plain text fallback mexanizmi.

---

## 5. Verification Method (Mustaqil Tekshirish Usuli)

Tadqiqot natijalarini mustaqil tekshirish uchun quyidagi qadamlar va buyruqlarni bajarish mumkin:

1. **Regex Langarlarini Tekshirish:**
   ```bash
   grep -n "@Action" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/admin/admin.update.ts
   ```
   *Kutilgan natija:* Barcha dinamik actionlar `^` bilan boshlangan regexlarga ega.

2. **Guruh va Kanal Huquqlarini Tekshirish:**
   ```bash
   grep -n "getChatMember" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/channels/channels.service.ts /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/groups/groups.service.ts
   ```
   *Kutilgan natija:* 62 va 60-qatorlarda `getChatMember` chaqirilib, `can_post_messages` va `can_send_messages` tekshirilgan.

3. **Exception Containment va 403 Xatolarini Izolyatsiya Qilish:**
   ```bash
   sed -n '150,217p' /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/posts/posts.service.ts
   ```
   *Kutilgan natija:* Targetlar bo'yicha tsikl ichida har bir chat uchun alohida `try/catch` va `postTarget.status = 'FAILED'` qayd etilgan.

4. **Loyiha Kompilyatsiyasini Tekshirish:**
   ```bash
   cd /home/fayzillo/Desktop/Loyihalar/bot_post_using && npm run build
   ```
   *Kutilgan natija:* Barcha TypeScript fayllari hech qanday xatosiz muvaffaqiyatli kompile bo'ladi (`nest build` exit code 0).
