# Telegraf Bot Arxitekturasi, Callback Regex Kolliziyalari va Clean Telegram UX Qoidalari

**Loyiha manbasi:** `bot_post_using`  
**Muallif / Ekspert tahlili:** Worker 1 & Brains Architecture Team  
**Mavzu doirasi:** Telegraf.js / NestJS-Telegraf, RegExp kolliziyalari va `^` langarlari, Telegram ruxsatlarini tekshirish (Channels & Groups), 403 Forbidden Exception Containment, `my_chat_member` himoyasi, Clean UX (miltillashsiz switchlar, inline tahrirlash, paginatsiya, breadcrumbs va HTML fallback).

---

## 1. Kirish: Telegraf.js Asosidagi Botlarda Arxitekturaviy Qiyinchiliklar

Telegraf.js — Node.js ekotizimida Telegram Bot API bilan ishlash uchun eng ommabop va qulay freymvorklardan biri hisoblanadi. NestJS bilan birgalikda (`nestjs-telegraf`) u deklarativ dekoratorlar (`@Update()`, `@Action()`, `@Command()`) orqali juda chiroyli kod tuzilishini ta'minlaydi.

Biroq, bot kattalashib, o'nlab inline tugmalar, ko'p bosqichli wizardlar, kanallarga xabar tarqatish va admin boshqaruvi qo'shilgach, dasturchilar quyidagi jiddiy muammolarga duch kelishadi:
1. **RegExp Kolliziyalari:** Kutilmagan handlerlarning ishlab ketishi yoki parametrli tugmalarning e'tibordan chetda qolishi.
2. **Kanal va Guruhlardagi Ruxsat Nomutanosibligi:** Bot admin emasligi yoki xabar yozish huquqi yo'qligi sababli botning xatolik bilan to'xtab qolishi.
3. **Ommaviy Xabar Tarqatishda 403 Falokati:** Bitta chatda bot bloklangani sababli butun siklning uzilishi va boshqa kanallarga xabar yetib bormasligi.
4. **Chatning "Axlatxona"ga Aylanishi (Dirty UX):** Har bir bosishda yangi xabarlar yuborilishi, ekranning miltillashi (flicker) va foydalanuvchining qayerda turganini yo'qotib qo'yishi.

Ushbu maqolada `bot_post_using` loyihasida yuzaga kelgan real keyslar va ularning mukammal arxitekturaviy yechimlari tizimlashtirilgan qoidalar ko'rinishida taqdim etiladi.

---

## 2. Telegraf RegExp Kolliziyalari (Collision) va Langarlar (`^` Anchor) Qoidasi

### 2.1 Unanchored RegExp (Langar Qo'yilmagan Regex) Tuzog'i
Telegrafning `@Action(regex)` dekoratori kelayotgan `callback_query.data` matniga nisbatan regexni `RegExp.prototype.test()` orqali tekshiradi.

Agar regex boshiga satr boshi langari (`^`) qo'yilmasa, regex matnning istalgan joyidan substring qidiradi!

**Haqiqiy falokatli misol:**
```typescript
// Yomon amaliyot (Unanchored RegExp):
@Action(/delete_post:(.+)/)
async onDeletePost(ctx: Context) { ... }

@Action(/cancel_delete_post:(.+)/)
async onCancelDelete(ctx: Context) { ... }
```
Foydalanuvchi "O'chirishni bekor qilish" (`cancel_delete_post:123`) tugmasini bosganda, Telegraf listenerlar ro'yxatida birinchi bo'lib `/delete_post:(.+)/` ga duch keladi. `cancel_delete_post:123` satri ichida `delete_post:123` mavjud bo'lgani sababli, regex match beradi va post bekor bo'lish o'rniga **bazadan o'chib ketadi!**

### 2.2 Strict `^` Anchoring Qoidasi
Har bir dinamik action listener qat'iy ravishda satr boshi langari (`^`) bilan boshlanishi shart:

```typescript
// ✅ To'g'ri amaliyot (Strictly Anchored):
@Action(/^delete_post:(.+)/)
async onDeletePost(@Ctx() ctx: Context) { ... }

@Action(/^cancel_delete_post:(.+)/)
async onCancelDelete(@Ctx() ctx: Context) { ... }
```

`bot_post_using` loyihasida ushbu qoidaga muvofiq barcha dinamik actionlar to'liq refaktoring qilingan:
- `@Action(/^toggle_target:(.+)/)` — chat tanlash tugmalari;
- `@Action(/^switch_posts:(.+)/)` — arxiv va kutilayotgan toifani almashtirish;
- `@Action(/^page_posts:(SCHEDULED|SENT):(\d+)/)` — aniq turlar bilan sahifalash;
- `@Action(/^view_post:(.+)/)` — postni ochish;
- `@Action(/^ai_reformat:(.+)/)` — postni AI bilan tahlil qilish;
- `@Action(/^apply_ai_reformat:(.+)/)` va `@Action(/^cancel_ai_reformat:(.+)/)` — in-place tasdiqlash;
- `@Action(/^send_now:(.+)/)` va `@Action(/^delete_post:(.+)/)` — post operatsiyalari;
- `@Action(/^delete_channel:(.+)/)` va `@Action(/^delete_group:(.+)/)` — chatlarni o'chirish.

### 2.3 Statik va Parametrli Callbacklar To'qnashuvi (`back_to_posts` Keysi)
Loyihada postlar ro'yxatidan post ichiga kirilganda, ortga qaytish tugmasi (`back_to_posts`) mavjud edi. Keyinchalik ro'yxat 2 ta toifaga ajratildi: `SCHEDULED` (kutilayotgan) va `SENT` (arxiv). Endi ortga qaytishda aynan qaysi toifaga qaytish kerakligini bilish uchun callback parametrli bo'ldi (`back_to_posts:SENT` yoki `back_to_posts:SCHEDULED`).

Biroq, agar handler `@Action('back_to_posts')` sifatida qolsa, u parametrli chaqiruvlarni qabul qilmaydi. Agar faqat `@Action(/^back_to_posts:(.+)/)` qilinsa, parametrsiz eski tugmalar ishlamay qoladi.

**Mukammal Yechim — Ixtiyoriy Capture Group:**
```typescript
// src/modules/admin/admin.update.ts:1523
@Action(/^back_to_posts(?::(.+))?/)
async onBackToPosts(@Ctx() ctx: Context) {
  const match = (ctx as any).match;
  // Agar parametr berilgan bo'lsa uni olamiz, aks holda default SCHEDULED
  const category: 'SCHEDULED' | 'SENT' = (match && match[1] === 'SENT') ? 'SENT' : 'SCHEDULED';
  
  await this.stateService.clearState(userId);
  await this.renderPostsList(ctx, category, 1);
  await ctx.answerCbQuery();
}
```
`(?::(.+))?` konstruktsiyasi:
- `:` va unga ergashgan parametrni guruhlaydi;
- `?` belgisi ushbu guruh ixtiyoriy (optional) ekanligini bildiradi;
- Ham `back_to_posts`, ham `back_to_posts:SENT` bir xil darajada mukammal ishlaydi.

### 2.4 Callback Data Hajm Cheklovi (64 Bayt)
Telegram Bot API da `callback_data` maydoni maksimal **64 bayt** bo'lishi mumkin!
- Agar siz callback ga uzun parametr qo'ymoqchi bo'lsangiz (masalan, `view_post:very-long-custom-id-with-many-words-and-timestamp`), 64 baytdan oshib ketib, Telegram `BUTTON_DATA_INVALID` xatosini otadi.
- **Qoida:** Callback verb qisqa bo'lishi kerak (`v_p:` yoki `view_post:`), parametr esa qat'iy ixcham UUID yoki qisqa kod bo'lishi lozim.

---

## 3. Guruh va Kanallarda Ruxsatlarni Tekshirish (Permissions Matrix)

Telegramda kanal (Channel) va guruh (Group/Supergroup) tushunchalari texnik jihatdan tubdan farq qiladi. Bot har ikkala joyda xabar yozishi uchun ularning huquqlarini alohida tekshirish shart.

### 3.1 Kanallarda Ruxsat Tekshirish Algoritmi (`ChannelsService`)
Kanallarda oddiy "a'zo" (member) bo'lish degan tushuncha botlar uchun mavjud emas. Bot kanalda faqat **Administrator** bo'lishi shart!

```typescript
// 1. Kanal ma'lumotlarini olish
const cleanInput = input.replace(/^https?:\/\/t\.me\//, '').replace(/^@/, '');
const chat = await telegram.getChat(`@${cleanInput}`);

if (chat.type !== 'channel') {
  throw new BadRequestException('Kiritilgan havola kanalga tegishli emas!');
}

// 2. Botning kanaldagi a'zoligini tekshirish
const botInfo = await telegram.getMe();
const chatMember = await telegram.getChatMember(chat.id, botInfo.id);

const isCreator = chatMember.status === 'creator';
const isAdmin = chatMember.status === 'administrator' || isCreator;
const canPost = Boolean(isCreator || (chatMember as any).can_post_messages);

if (!isAdmin) {
  return { success: false, message: `⚠️ Bot "${chat.title}" kanalida administrator emas. Iltimos, avval admin qiling.` };
}

if (!canPost) {
  return { success: false, message: `⚠️ Bot "${chat.title}" kanalida admin, ammo "Post yuborish (Post Messages)" huquqi yo'q!` };
}
```

### 3.2 Guruhlarda Ruxsat Tekshirish Algoritmi (`GroupsService`)
Guruhlarda bot admin bo'lmasa ham oddiy a'zo sifatida post yozishi mumkin, ammo guruh sozlamalarida yoki adminlar tomonidan bot huquqlari cheklangan (`restricted`) bo'lishi mumkin:

```typescript
const chat = await telegram.getChat(cleanInput);
if (chat.type !== 'group' && chat.type !== 'supergroup') {
  throw new BadRequestException('Bu chat guruh yoki superguruh emas!');
}

const chatMember = await telegram.getChatMember(chat.id, botInfo.id);

// Bot chiqarib yuborilgan holat
if (chatMember.status === 'left' || chatMember.status === 'kicked') {
  return { success: false, message: `⚠️ Bot "${chat.title}" guruhiga a'zo emas (chiqarib yuborilgan).` };
}

// Bot huquqlari cheklangan holat (Mute qilingan)
const isRestricted = chatMember.status === 'restricted';
const canSendMessages = isRestricted ? (chatMember as any).can_send_messages !== false : true;

if (isRestricted && !canSendMessages) {
  return { success: false, message: `⚠️ Bot "${chat.title}" guruhida mavjud, ammo xabar yozish huquqi cheklangan (Restricted)!` };
}
```

---

## 4. Ommaviy Yuborishda 403 Forbidden Exception Containment

### 4.1 Muammo: Yagona Xato Butun Tarqatishni To'xtatishi
Tasavvur qiling, rejalashtirilgan post 15 ta kanalga yuborilishi kerak. Sikl ishlayotganda 3-kanalda kanal egasi botni administratorlikdan chiqarib yuborgan. Telegram API darhol `403 Forbidden: bot is not a member of the channel` qaytaradi.
Agar bu chaqiruv umumiy funksiya doirasida ushlanmasa, butun funksiya qulaydi va qolgan 12 ta kanalga xabar umuman yetib bormaydi!

### 4.2 Yechim: Target Darajasidagi Izolyatsiya (Exception Containment)
`bot_post_using` loyihasidagi `PostsService.sendPostNow` arxitekturasi:

```typescript
let successCount = 0;
let failCount = 0;

for (const target of post.targets) {
  const chatId = target.channel ? target.channel.chatId : target.group?.chatId;
  if (!chatId) continue;

  try {
    // Har bir chatga yuborish alohida izolyatsiyalangan try/catch ichida
    let sentMsg: any;
    if (post.mediaType === 'PHOTO' && post.mediaFileId) {
      sentMsg = await this.bot.telegram.sendPhoto(chatId.toString(), post.mediaFileId, {
        caption: post.text || undefined,
        parse_mode: 'HTML',
      });
    } else {
      sentMsg = await this.bot.telegram.sendMessage(chatId.toString(), post.text!, {
        parse_mode: 'HTML',
      });
    }

    // Muvaffaqiyatli yuborildi
    await this.prisma.postTarget.update({
      where: { id: target.id },
      data: { status: 'SENT', messageId: sentMsg.message_id, errorMessage: null },
    });
    successCount++;
  } catch (err: any) {
    // 403 Forbidden yoki boshqa Telegram xatosi faqat shu target uchun yoziladi
    failCount++;
    await this.prisma.postTarget.update({
      where: { id: target.id },
      data: { status: 'FAILED', errorMessage: err.message || 'Noma\'lum xatolik' },
    });

    // MongoDB audit logiga qayd etish
    await this.logToMongo(post.id, target.id, err.message);

    // SIKL TO'XTATILMAYDI! Keyingi kanalga o'tish:
    continue;
  }
}

// Yakuniy post holati
const finalStatus = successCount > 0 ? 'SENT' : 'FAILED';
await this.prisma.post.update({ where: { id: post.id }, data: { status: finalStatus, sentAt: new Date() } });
```

---

## 5. Ruxsatsiz Qo'shilishlardan Himoya: `my_chat_member` va Auto-Leave

Ko'plab ochiq botlarni begona foydalanuvchilar o'zlarining shaxsiy kanallariga yoki noqonuniy guruhlariga admin qilib qo'shishadi. Agar bot bunga cheklov qo'ymasa, bot nomidan spamlash yoki ruxsatsiz kontentlar tarqatish xavfi tug'iladi.

### Yechim: `my_chat_member` Handleri va Avtomatik Chiqib Ketish
`src/modules/admin/admin.update.ts:63-125`:

```typescript
@Update()
export class AdminUpdate {
  @On('my_chat_member')
  async onMyChatMember(@Ctx() ctx: Context) {
    const update = (ctx.update as any).my_chat_member;
    if (!update) return;

    const chat = update.chat;
    const fromUser = update.from;
    const newStatus = update.new_chat_member?.status;

    // Faqat bot administrator yoki a'zo qilib qo'shilganda tekshiramiz
    if (newStatus === 'administrator' || newStatus === 'member') {
      const isAllowed = await this.usersService.isUserAllowed(fromUser.id);

      if (!isAllowed) {
        // Ruxsatsiz shaxs qo'shgan bo'lsa ogohlantirish beramiz
        await ctx.telegram.sendMessage(
          chat.id,
          `⛔️ <b>Xavfsizlik ogohlantirishi:</b> Ushbu bot faqat vakolatli administratorlar tomonidan boshqariladi. Bot chatni tark etmoqda.`,
          { parse_mode: 'HTML' }
        ).catch(() => {});

        // Bot zudlik bilan chatdan chiqib ketadi
        await ctx.telegram.leaveChat(chat.id);
        return;
      }
    }
  }
}
```

---

## 6. Telegramda Clean UX: Miltillashsiz UI, Inline Tahrirlash va Breadcrumb

### 6.1 Miltillashsiz Toggle Switchlar (`editMessageReplyMarkup`)
Foydalanuvchi post yuboriladigan kanallarni tanlayotganda (masalan, 5 ta kanal ro'yxatida `✅` va `❌` bosilganda), ko'pchilik dasturchilar xabarni `editMessageText` orqali matni bilan birga qayta jo'natadi.
Bu xatodir! Chunki xabar matni qayta chizilganda Telegram ekrani butunlay o'chib-yonadi (miltillaydi / flicker).

**Clean UX Usuli:**
Xabar matniga tegmang, faqat tugmalar klaviaturasini almashtiring:
```typescript
// src/modules/admin/admin.update.ts:938
await ctx.editMessageReplyMarkup(
  CallbackKeyboardBuilder.selectTargetsKeyboard(targets, selectedIds).reply_markup,
);
await ctx.answerCbQuery(); // Loading spinnerni to'xtatish
```
Natijada matn o'z joyida qimir etmay turadi, faqat bosilgan tugmadagi `❌` belgisi bir zumda va silliq tarzda `✅` ga aylanadi.

### 6.2 In-Place Inline Tahrirlash (`switchToCurrentChat`)
Telegram Bot API da foydalanuvchining klaviaturasiga matnni tashqi tomondan to'ldirib berish imkonsiz. Ammo `Markup.button.switchToCurrentChat` orqali bu cheklovni aylanib o'tish mumkin!

```typescript
// Klaviaturada:
Markup.button.switchToCurrentChat('✏️ Matnni tahrirlash', cleanText);
```
Foydalanuvchi bu tugmani bosganda, Telegram uning pastki kiritish maydoniga (input field) avtomatik ravishda `@bot_username <mavjud_matn>` ni yozib beradi. Foydalanuvchi matnga o'zgartirish kiritib jo'natgach, bot handleri username prefiksini qirqib oladi:
```typescript
let editedText = ctx.message.text.replace(/^@\w+\s*/, '').trim();
```
Bu foydalanuvchiga matnni noldan qayta yozmasdan, o'z joyida qulay tahrirlash imkoniyatini beradi.

### 6.3 Paginatsiya Matematikasi va Aniq Callback Regex
Ro'yxatlarni sahifalashda standart matematika va aniq regex qo'llaniladi:
- `skip = (page - 1) * limit`
- `totalPages = Math.ceil(totalCount / limit) || 1`
- Callback data: `page_posts:${category}:${page}` (Masalan: `page_posts:SCHEDULED:2`)
- Handler: `@Action(/^page_posts:(SCHEDULED|SENT):(\d+)/)`

O'rtadagi `📄 2/5` tugmasi `noop` amali bilan bosilganda hech qanday ortiqcha yuklama bermaydi, faqat indikator vazifasini bajaradi.

### 6.4 Breadcrumb (Non Qatlamlari) Navigatsiyasi
Foydalanuvchi doimo qaysi bo'limda turganini tushunishi uchun xabarlarning yuqori qismida doimiy breadcrumb satri aks ettiriladi:
```typescript
static breadcrumb(...steps: string[]): string {
  if (!steps || steps.length === 0) return '';
  return `📍 <i>${steps.filter(Boolean).join(' ❯ ')}</i>\n\n`;
}
```
Misol: `📍 Bosh menyu ❯ 📋 E'lonlar ❯ ⏰ Kutilayotgan (1-sahifa) ❯ 🔍 Postni ko'rish`.

### 6.5 Noto'g'ri HTML Xatoliklariga Chidamli Fallback (`safeReply`)
Agar post matnida yopilmagan `<b>` yoki noto'g'ri `<tag>` bo'lsa, Telegram API `Bad Request: can't parse entities` xatosini beradi.
`safeReply` va `safeEditMessageText` bu xatoni avtomatik ushlab, teglarni tozalaydi va oddiy matn rejimida qayta jo'natadi:
```typescript
async safeReply(ctx: Context, text: string, extra: any = {}) {
  try {
    return await ctx.reply(text, extra);
  } catch (err: any) {
    if (err.description?.includes("can't parse entities")) {
      const stripped = text.replace(/<[^>]*>?/gm, '');
      const fallbackExtra = { ...extra };
      delete fallbackExtra.parse_mode;
      return await ctx.reply(stripped, fallbackExtra);
    }
    throw err;
  }
}
```

---

## 7. Xulosa

Telegraf botlarida yuqori sifatli arxitektura va professional foydalanuvchi tajribasiga erishish uchun:
1. Doimo har bir action regexini `^` bilan boshlang.
2. Callback parametrlarida 64 baytlik cheklovni unutmang.
3. Kanallar va guruhlar huquqlarini alohida tekshiring.
4. Ommaviy yuborishda har bir chatni alohida `try/catch` qilib, 403 xatolarini izolyatsiya qiling.
5. `my_chat_member` orqali ruxsatsiz chatlardan darhol chiqib keting.
6. Miltillashsiz UI uchun `editMessageReplyMarkup`, qulay inline tahrirlash uchun `switchToCurrentChat` va aniq yo'naltirish uchun Breadcrumbs qo'llang.
