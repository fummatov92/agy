# 📋 Handoff Report: UI/State Management, Pagination, Dinamik Konfiguratsiya va Raqamli Miya (Brains) Arxitekturasi

- **Tadqiqotchi:** Explorer 3 (UI/State Management & Brains Target Format Investigator)
- **Sana:** 2026-09-06T22:31:00+05:00
- **Loyiha 1:** `bot_post_using` (`/home/fayzillo/Desktop/Loyihalar/bot_post_using`)
- **Loyiha 2:** `brains` (`/home/fayzillo/Downloads/brains`)
- **Holati:** To'liq yakunlandi (Comprehensive Read-Only Investigation)

---

## 1. Observation (Bevosita Kuzatuvlar va Aniq Dalillar)

Tadqiqot davomida har ikkala repozitoriya (`bot_post_using` va `brains`) qatorlar va kod darajasida tekshirilib, quyidagi bevosita faktlar aniqlandi:

### 1.1 `bot_post_using`: Inline Tahrirlash va Holat Boshqaruvi (Inline Editing & State Management)

#### A. Draft Post Yaratish va Multi-step Wizard Oqimi
- `src/common/types/index.ts:1-28`: Wizard bosqichlari enum va sessiya interfeysi:
  ```typescript
  export enum BotWizardStep {
    IDLE = 'IDLE',
    WAITING_FOR_CONTENT = 'WAITING_FOR_CONTENT',
    REVIEWING_AI_FORMAT = 'REVIEWING_AI_FORMAT',
    SELECTING_TARGETS = 'SELECTING_TARGETS',
    CHOOSING_SCHEDULE_TYPE = 'CHOOSING_SCHEDULE_TYPE',
    WAITING_FOR_DATE = 'WAITING_FOR_DATE',
    CONFIRMING = 'CONFIRMING',
    ADDING_CHANNEL = 'ADDING_CHANNEL',
    ADDING_GROUP = 'ADDING_GROUP',
    EDITING_EXISTING_POST = 'EDITING_EXISTING_POST',
  }
  ```
- `src/modules/admin/admin.update.ts:274-336, 507-562`:
  - Yangi post `/new_post` orqali boshlanadi (`BotWizardStep.WAITING_FOR_CONTENT`).
  - Matn yoki media (photo/video/document/voice) qabul qilinganda `PostFormatterService.beautifyPost` orqali formatlanadi.
  - Matn qabul qilingach foydalanuvchi `BotWizardStep.REVIEWING_AI_FORMAT` holatiga o'tadi va unga ko'rib chiqish klaviaturasi beriladi.

#### B. Inline Tahrirlash Mexanizmi (`SwitchInlineQueryCurrentChat` va Tap-to-Copy)
- `src/common/utils/_cb_functions/index.ts:12-27`:
  ```typescript
  static aiFormatReviewKeyboard(textToEdit: string = '') {
    const cleanText = textToEdit.replace(/<[^>]*>?/gm, '');

    return Markup.inlineKeyboard([
      [Markup.button.callback('✨ AI formatini qabul qilish', 'accept_ai_format')],
      [Markup.button.switchToCurrentChat('✏️ Matnni tahrirlash', cleanText)],
      [
        Markup.button.callback('📝 Asl matnni qoldirish', 'keep_raw_format'),
        Markup.button.callback('❌ Bekor qilish', 'cancel_action'),
      ],
    ]);
  }
  ```
- **Kuzatuv:** Telegram Bot API dagi `switch_inline_query_current_chat` imkoniyati foydalanuvchining pastki kiritish maydoniga (input box) formatlangan matnni avtomatik to'ldirib beradi. Foydalanuvchi matnga o'zgartirish kiritib jo'natganda, `AdminUpdate.onText` (`REVIEWING_AI_FORMAT` holatida) yangi matnni qabul qilib, bot username prefiksini tozalaydi:
  `src/modules/admin/admin.update.ts:319`: `editedText = editedText.replace(/^@\w+\s*/, '').trim();`.

#### C. Dinamik Tugmalar va Ko'p Tanlovli Switchlar (Toggle Switches)
- `src/common/utils/_cb_functions/index.ts:38-64` (`selectTargetsKeyboard`):
  Har bir kanal yoki guruh uchun alohida qatorda inline button yaratiladi.
  ```typescript
  const isSelected = selectedIds.includes(target.id);
  const mark = isSelected ? '✅' : '❌';
  const typeIcon = target.type === 'CHANNEL' ? '📢' : '👥';
  Markup.button.callback(`${mark} ${typeIcon} ${target.title}`, `toggle_target:${target.id}`);
  ```
- `src/modules/admin/admin.update.ts:915-945` (`onToggleTarget`):
  Foydalanuvchi chat tugmasini bosganda:
  ```typescript
  let selected = state.draftPost?.selectedTargets || [];
  if (selected.includes(targetId)) {
    selected = selected.filter((id) => id !== targetId);
  } else {
    selected.push(targetId);
  }
  state.draftPost.selectedTargets = selected;
  await this.stateService.setState(state);
  await ctx.editMessageReplyMarkup(
    CallbackKeyboardBuilder.selectTargetsKeyboard(targets, selected).reply_markup,
  );
  await ctx.answerCbQuery();
  ```
  **Kuzatuv:** Matn qayta chizilmaydi (`safeEditMessageText` chaqirilmaydi), faqat `editMessageReplyMarkup` orqali tugmalarning `✅`/`❌` holati joyida o'zgartiriladi (zero flicker, Clean UX).
  Tugmalar boshqaruvi: Kamida bitta chat tanlangandagina `Davom etish ➡️` tugmasi dinamik ravishda paydo bo'ladi (`selectedIds.length > 0`).

#### D. In-Place AI Reformatting Tasdiqlash Oqimi
- `src/modules/admin/admin.update.ts:1195-1355` va `history/task_019` - `task_021`:
  - Post tafsilotlarida `✨ AI bilan qayta formatlash` (`ai_reformat:${postId}`) bosilganda yangi xabar yuborilmaydi, mavjud xabar joyida `⏳ Post matni AI yordamida qayta formatlanmoqda...` ga aylanadi.
  - Yangi matn taklif qilingach, `apply_ai_reformat:${postId}` va `cancel_ai_reformat:${postId}` tugmalari chiqadi.
  - `apply_ai_reformat` bosilganda: bazadagi post yangilanadi, agar post `SENT` bo'lsa barcha kanallardagi jonli xabarlar Telegram API orqali tahrirlanadi, alert beriladi va o'sha postning yangilangan batafsil ko'rinishiga (`postPreviewMessage` + `postDetailKeyboard`) qaytiladi.
  - `cancel_ai_reformat` bosilganda: postning dastlabki ko'rinishiga xavfsiz qaytadi.

---

### 1.2 `bot_post_using`: Pagination va Breadcrumb Navigatsiyasi

#### A. Sahifalash Mexanizmi (Pagination)
- `src/modules/posts/posts.service.ts:246-285` (`listPosts`):
  ```typescript
  const skip = (page - 1) * limit;
  const [posts, totalCount] = await Promise.all([
    this.prisma.post.findMany({
      where: { status: category },
      orderBy: { createdAt: 'desc' },
      skip,
      take: limit,
    }),
    this.prisma.post.count({ where: { status: category } }),
  ]);
  const totalPages = Math.ceil(totalCount / limit) || 1;
  ```
- `src/common/utils/_cb_functions/index.ts:85-132` (`postsListKeyboard`):
  - Har bir post qatori: `Markup.button.callback("📌 " + previewTitle, "view_post:" + post.id)`
  - Sahifalar soni > 1 bo'lsa:
    - Oldingi: `⬅️ Oldingi` -> `page_posts:${category}:${page - 1}` (faqat `page > 1` bo'lsa)
    - Ko'rsatkich: `📄 ${page}/${totalPages}` -> `noop` (hech qanday amal bajarmaydi, faqat info)
    - Keyingi: `Keyingi ➡️` -> `page_posts:${category}:${page + 1}` (faqat `page < totalPages` bo'lsa)
  - Toifani almashtirish (Category Switcher):
    `➡️ Arxiv postlar` (`switch_posts:SENT`) yoki `➡️ Kutilayotgan postlar` (`switch_posts:SCHEDULED`).
- `src/modules/admin/admin.update.ts:1104-1134`:
  `@Action(/^page_posts:(SCHEDULED|SENT):(\d+)/)`
  Aniq regex parametrlari orqali toifa va sahifa soni olinadi, postlar bazadan yuklanib, xabar in-place yangilanadi.

#### B. Breadcrumb (Non qatlamlari) Navigatsiyasi
- `src/common/utils/_message_generator/index.ts:5-8`:
  ```typescript
  static breadcrumb(...steps: string[]): string {
    if (!steps || steps.length === 0) return '';
    return `📍 <i>${steps.filter(Boolean).join(' ❯ ')}</i>\n\n`;
  }
  ```
- **Kuzatilgan qatlamlar:**
  1. Post yaratishda:
     - 1-qadam: `📍 Bosh menyu ❯ 📝 Yangi E'lon ❯ 1️⃣ Matn / Media`
     - 2-qadam: `📍 Bosh menyu ❯ 📝 Yangi E'lon ❯ 2️⃣ Chatlarni tanlash`
     - 3-qadam: `📍 Bosh menyu ❯ 📝 Yangi E'lon ❯ 3️⃣ Vaqtni belgilash`
     - 4-qadam: `📍 Bosh menyu ❯ 📝 Yangi E'lon ❯ 4️⃣ Tasdiqlash`
  2. Ro'yxatlarda:
     - `📍 Bosh menyu ❯ 📋 E'lonlar ❯ ⏰ Kutilayotgan (1-sahifa)`
     - `📍 Bosh menyu ❯ 📋 E'lonlar ❯ 📁 Arxiv (2-sahifa)`
  3. Post ko'rishda:
     - `📍 Bosh menyu ❯ 📋 E'lonlar ❯ 📁 Arxiv ❯ 🔍 Postni ko'rish`
- **Orqaga qaytish (Back navigation):**
  - `src/modules/admin/admin.update.ts:1523-1563`: `@Action(/^back_to_posts(?::(.+))?/)`
  - Post kutilayotgan (`SCHEDULED`) yoki arxiv (`SENT`) bo'lishiga qarab orqaga qaytish tugmasi `back_to_posts:SCHEDULED` yoki `back_to_posts:SENT` parametrini yuboradi.
  - Handlerda foydalanuvchi sessiyasi (`stateService.clearState(userId)`) tozalanadi va to'g'ri toifadagi ro'yxatga qaytariladi.

---

### 1.3 `bot_post_using`: Dinamik Konfiguratsiya va Sozlamalar Boshqaruvi

- `src/common/config/configuration.ts:1-24`:
  - Muhit o'zgaruvchilari (`process.env`): `PORT`, `NODE_ENV`, `BOT_TOKEN`, `ALLOWED_USER_IDS`, `DATABASE_URL`, `MONGODB_URI`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`.
  - `bot.allowedUserIds`: vergul bilan ajratilgan IDlar `BigInt` massiviga aylantiriladi.
- `src/modules/users/users.service.ts:1-155`:
  - **Uch bosqichli ruxsat tekshiruvi (`isUserAllowed`):**
    1. `.env` dagi boshlang'ich adminlar (`this.envAllowedIds.some(id => id === telegramId)`).
    2. Redis kesh (`allowed_user:${telegramId}`, TTL: 3600s / 1 soat).
    3. PostgreSQL `users` jadvali (`isAllowed: true`).
  - **Dinamik boshqaruv REST API:**
    - `POST /users/allowed` -> `addAllowedUser`: botni qayta ishga tushirmasdan yangi foydalanuvchiga ruxsat beradi va Redis keshini bir zumda yangilaydi (`set(..., '1')`).
    - `DELETE /users/allowed/:telegramId` -> `removeAllowedUser`: ruxsatni bekor qiladi va keshni yangilaydi (`set(..., '0')`).
    - `GET /users/allowed` -> `listAllowedUsers`: barcha ruxsat berilganlar ro'yxatini qaytaradi.
- `src/global/user_filter/user_filter.guard.ts:22-26`:
  `my_chat_member` hodisasi guard orqali ruxsat etiladi, lekin `AdminUpdate.onMyChatMember` da botni chatga qo'shgan shaxs tekshiriladi; agar u ruxsatsiz bo'lsa, ogohlantirish berilib, bot chatni tark etadi (`ctx.telegram.leaveChat(chat.id)`).

---

### 1.4 `brains` Repozitoriyasi Arxitekturasi va Standartlari

#### A. Mavjud Klasterlar Strukturasi (`grouped-md/`)
Biz tekshirgan klasterlar:
1. `05-id-string-db-majburiy/`:
   - Hajmi: 707 KB, 18,466 qator, 37 ta manba hujjati.
   - Mavzu: API Sozlamalari, Xabarnomalar va Prisma Tizim Arxitekturasi (API & DB Settings).
2. `23-prisma-id-string-va/`:
   - Hajmi: 843 KB, 26,009 qator, 16 ta manba hujjati.
   - Mavzu: NestJS CRM va Prisma ORM Sxemalari (NestJS & Prisma Schemas).
3. `04-md-va-bo-bu/`:
   - Hajmi: 113 KB, 2,390 qator, 37 ta manba hujjati.
   - Mavzu: AI Agent va Tizim Xatti-harakatlari Yo'riqnomasi (System Rules & Skills).

**Klaster fayllari ichki formati (`consolidated.md`):**
- Har bir klaster ichida faqat bitta `consolidated.md` mavjud.
- Bosh sarlavha: `# <Klaster Nomi (O'zbekcha / Inglizcha)>`
- Har bir hujjat bo'limi aniq ajratuvchi bilan boshlanadi:
  `## Manba: <nisbiy_yo'l/fayl_nomi.md>`
- Undan so'ng texnik tahlil, API pointlar (`POST /api/v1/...`), DTO xususiyatlari, Guardlar, Service mantiq qadamlari, Response JSON, Error caselar, DB strukturalari va cURL misollari to'liq keltiriladi.
- Ohang: qat'iy texnik, aniq, me'moriy va professional o'zbek tilida.

#### B. `00-INDEX.md` Mundarija Standarti
- Fayl: `/home/fayzillo/Downloads/brains/00-INDEX.md` (36 qator).
- Standart qator sintaksisi:
  `- **<Klaster Nomi (Uzbek / English)>** (\`<klaster-papka-nomi>\`) — <soni> ta hujjat ([MD](grouped-md/<klaster-papka-nomi>/consolidated.md), [RAG chunks](rag-ready/<klaster-papka-nomi>/chunks.jsonl))`
- Masalan:
  `- **API Sozlamalari, Xabarnomalar va Prisma Tizim Arxitekturasi (API & DB Settings)** (\`05-id-string-db-majburiy\`) — 37 ta hujjat ([MD](grouped-md/05-id-string-db-majburiy/consolidated.md), [RAG chunks](rag-ready/05-id-string-db-majburiy/chunks.jsonl))`
  `- **NestJS CRM va Prisma ORM Sxemalari (NestJS & Prisma Schemas)** (\`23-prisma-id-string-va\`) — 16 ta hujjat ([MD](grouped-md/23-prisma-id-string-va/consolidated.md), [RAG chunks](rag-ready/23-prisma-id-string-va/chunks.jsonl))`

#### C. `rag-ready/` JSONL Chunks Standarti
- Har bir klaster papkasida faqat bitta `chunks.jsonl` fayli joylashgan.
- JSON qator formati va kalitlari (aniq 4 ta kalit):
  ```json
  {"id": "<klaster_papka>__<slug20>__<chunk_index>", "source": "<manba_fayl_yo'li>", "topic": "<mavzu_slug>", "text": "<matn_bo'lagi>"}
  ```
- **Kuzatilgan parametrlar:**
  - `id`: `<cluster_dir>__<source_alphanumeric_first_20_lower>__<index>`
    Misol: `05-id-string-db-majburiy__zdesarchivedocsrawhi__0`
  - `source`: Manba faylning nisbiy yo'li (masalan `zdes_archive_docs/.../setting.md` yoki `bot_post_using/docs/...`).
  - `topic`: Klaster papkasi nomining raqamsiz qismi (masalan `05-id-string-db-majburiy` uchun `id-string-db-majburiy`).
  - `text`: Chunk matni.
    - Maksimal uzunlik: aniq **1000 belgi**.
    - Overlap (ustma-ust tushish): **150 belgi**.
    - Step (siljish qadami): **850 belgi**.
    - Min uzunlik: oxirgi qoldiq bo'lak (35-492 belgi).

---

## 2. Logic Chain (Kuzatuvlardan Xulosalarga Mantiqiy Zanjir)

1. **Inline Tahrirlash va Holat Boshqaruvi:**
   - *Kuzatuv:* Telegram Bot API da matn kiritish maydoniga tashqi dasturdan to'g'ridan-to'g'ri matn yozib bo'lmaydi.
   - *Mantiq:* Loyihada `Markup.button.switchToCurrentChat` orqali matn inline so'rov sifatida foydalanuvchining o'z chatiga yuboriladi. Foydalanuvchi matnni tahrirlab jo'natganda, `AdminUpdate.onText` (`REVIEWING_AI_FORMAT` va `EDITING_EXISTING_POST`) uni qabul qilib, regex orqali bot prefiksini qirqadi.
   - *Xulosa:* Bu yechim Telegram cheklovini yengib, to'liq inline tahrirlash (Clean In-Place UX) imkonini beradi.

2. **Dinamik Tanlov (Toggle Switches) va Miltillashsiz UI:**
   - *Kuzatuv:* Chatlar tanlanayotganda `ctx.safeEditMessageText` emas, `ctx.editMessageReplyMarkup` chaqiriladi (`src/modules/admin/admin.update.ts:938`).
   - *Mantiq:* Xabar matnini tahrirlash butun xabarning qayta yuklanishiga va ekranda miltillashga (flicker) olib keladi. Faqat `reply_markup` ni almashtirish orqali faqat tugmalardagi `✅` va `❌` belgilari silliq yangilanadi.
   - *Xulosa:* Bu Telegram botlarida professional darajadagi foydalanuvchi tajribasini (UX) ta'minlaydi.

3. **Sahifalash va Breadcrumb Integratsiyasi:**
   - *Kuzatuv:* Callback datada toifa va sahifa raqami aniq ajratilgan: `page_posts:(SCHEDULED|SENT):(\d+)` va `back_to_posts:(SCHEDULED|SENT)`.
   - *Mantiq:* Sahifalashda umumiy postlar soni va sahifa hajmi asosida `skip = (page - 1) * limit` va `totalPages = ceil(total / limit)` hisoblanadi. Breadcrumb esa har bir bosqichda joriy holatni foydalanuvchiga ko'rsatib turadi (`MessageGenerator.breadcrumb`).
   - *Xulosa:* Foydalanuvchi post ichiga kirib ketganda ham, `⬅️ Orqaga` bosilganda u aynan o'sha toifadagi ro'yxatga qaytadi va state chalkashmaydi.

4. **Dinamik Ruxsatlar:**
   - *Kuzatuv:* Ruxsatlar 3 bosqichda tekshiriladi (`.env` -> Redis -> PostgreSQL).
   - *Mantiq:* Har bir bot so'rovida PostgreSQL ga borish bazaga ortiqcha yuklama beradi. Shuning uchun Redis 1 soatlik kesh bilan oraga qo'yilgan. REST API orqali ruxsat berilganda yoki olinganda kesh darhol sinxronlashtiriladi.
   - *Xulosa:* Tizim yuqori tezlik (sub-millisecond) va dinamik boshqaruv imkoniyatiga ega.

5. **Brains Bazasi va RAG-Ready Standartlariga Muvofiqlik:**
   - *Kuzatuv:* `grouped-md/` fayllarida `## Manba: ...` sarlavhasi ostida modulli hujjatlar jamlangan. `rag-ready/` dagi `chunks.jsonl` fayllarida esa aniq 4 ta kalit (`id`, `source`, `topic`, `text`) mavjud bo'lib, chunk uzunligi 1000 belgidan oshmaydi.
   - *Mantiq:* Yangi bilimlarni (Telegram Bot arxitekturasi, state management, regex kolliziyalari, 403 himoyasi) integratsiya qilish uchun ularni `05-id-string-db-majburiy` (API va DB arxitekturasi), `23-prisma-id-string-va` (Prisma va modellar) hamda `04-md-va-bo-bu` (Agent xatti-harakatlari va tizim qoidalari) klasterlariga moslashtirish, `00-INDEX.md` mundarijasidagi hujjatlar sonini yangilash va `chunks.jsonl` ga standart parametrlar bo'yicha qo'shish talab etiladi.
   - *Xulosa:* M1 tadqiqot natijalari M2 (MD integratsiyasi) va M3 (RAG JSONL sinxronlash) bosqichlariga to'liq tayyor.

---

## 3. Caveats (Cheklovlar va E'tiborga Olinishi Kerak Bo'lgan Holatlar)

1. **Tadqiqot Rejimi:** Ushbu bosqich qat'iy **Read-Only** bo'lgani sababli, `bot_post_using` va `brains` repozitoriyalaridagi hech bir manba fayli o'zgartirilmadi yoki yangi modullar yozilmadi.
2. **`chunks.jsonl` Generatsiya Skripti:** `brains` repozitoriyasida tayyor chunklash skripti (masalan `chunker.py`) topilmadi; bu jarayon tashqi pipeline yoki avvalgi agentlar tomonidan bajarilgan. Biroq biz chunklash algoritmini (1000 belgi o'lcham, 150 belgi overlap, slug formati) matematik va empirik tarzda to'liq aniqladik.
3. **`00-INDEX.md` Sinxronlash:** Klasterlarga yangi hujjatlar qo'shilganda `00-INDEX.md` dagi `X ta hujjat` soni qo'shilgan manbalar soniga mutanosib ravishda oshirilishi zarur.

---

## 4. Conclusion (Yakuniy Xulosa va Tavsiyalar)

`bot_post_using` loyihasi Telegram bot yaratishda eng murakkab bo'lgan quyidagi UI/UX va me'moriy muammolarni mukammal hal etgan:
1. **Clean UX & In-Place Editing:** `switchToCurrentChat` orqali inline tahrirlash, `editMessageReplyMarkup` orqali miltillashsiz switchlar, `ai_reformat` orqali joyida yuklanish va tasdiqlash.
2. **Pagination & Breadcrumbs:** Aniq parametrli callbacklar (`page_posts:<CATEGORY>:<PAGE>`), dinamik sahifalash matematikasi va 4 bosqichli non qatlamlari.
3. **Dinamik Ruxsatlar:** REST API + Redis + PostgreSQL + UserFilterGuard orqali to'liq avtomatlashtirilgan xavfsizlik.

Raqamli Miya (`brains`) bazasiga integratsiya uchun barcha xaritalar va formatlar tayyorlandi:
- Klaster 05 (`05-id-string-db-majburiy`): API, State Service, Redis/Mongo kesh va dinamik ruxsatlar bo'yicha texnik hujjatlar.
- Klaster 23 (`23-prisma-id-string-va`): Prisma sxemasi, UUID String ID, BigInt Telegram ID, PostTarget relatsiyalari.
- Klaster 04 (`04-md-va-bo-bu`): Telegram bot regex kolliziyalari, 403 Forbidden handling va Clean UX qoidalari.
- `rag-ready/`: 1000 belgi / 150 overlap bo'yicha `.jsonl` chunklar.

---

## 5. Verification Method (Mustaqil Tekshirish Usuli)

Quyidagi buyruqlar va fayl tekshiruvlari orqali keltirilgan barcha xulosalarni mustaqil tekshirish mumkin:

1. **State va Klaviaturani Tekshirish:**
   ```bash
   cat /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/core/state.service.ts
   cat /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/common/utils/_cb_functions/index.ts
   ```
2. **Pagination va In-place Actionlarni Tekshirish:**
   ```bash
   grep -n "page_posts" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/admin/admin.update.ts
   grep -n "ai_reformat" /home/fayzillo/Desktop/Loyihalar/bot_post_using/src/modules/admin/admin.update.ts
   ```
3. **Brains Klasterlari va JSONL Formatini Tekshirish:**
   ```bash
   head -n 20 /home/fayzillo/Downloads/brains/grouped-md/05-id-string-db-majburiy/consolidated.md
   head -n 2 /home/fayzillo/Downloads/brains/rag-ready/05-id-string-db-majburiy/chunks.jsonl
   ```
4. **Chunk Statistikasini Tekshirish:**
   ```bash
   python3 -c "import json; f=open('/home/fayzillo/Downloads/brains/rag-ready/05-id-string-db-majburiy/chunks.jsonl'); ls=[len(json.loads(l)['text']) for l in f]; print('Max:', max(ls), 'Avg:', sum(ls)/len(ls))"
   ```
