# AI Agent va Tizim Xatti-harakatlari Yo'riqnomasi (System Rules & Skills)


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/restart-timing/use_cases.md`

# Use Cases — Restart timing

## UC-1: Bitta katta fayl o'qilgani uchun vaqtinchalik sakrash

Messages ulushi bir checkpoint'da keskin oshdi, lekin sabab bitta katta
faylni o'qish edi (masalan loyiha tahlili). Keyingi checkpoint'da ulush
pasayishi mumkin. → Darhol restart shart emas, trendni kuzating.

## UC-2: Doimiy o'sish trendi

3 ketma-ket checkpoint: 15% → 20% → 27%. → Bu "kech qolinayotgan" signal,
keyingi tabiiy to'xtash nuqtasida (masalan joriy sub_task tugaganda)
restart tavsiya qilinadi.

## UC-3 (taxminiy): Kichik, tez tugaydigan loyiha

Loyiha kichik bo'lsa (bir necha soatlik ish), restart chegarasi yuqoriroq
qo'yilishi mumkin — chunki checkpoint/restart overhead'i nisbatan
qimmatroq bo'lib qoladi.

## UC-4 (taxminiy): Uzoq muddatli, ko'p sessiyali loyiha

Loyiha haftalar davom etsa, past chegara (masalan 15-20%) qo'yish
mantiqiy — chunki uzoq context'da sifat pasayishi xavfi yuqoriroq.


## Manba: `zdes_archive_docs/raw_history/orcestor/steps/05-integration.md`

# 5-bosqich: Integration (Kodbazaga integratsiya)

**Maqsad:** Claude Code qaytarilgan ishni kodbaza bilan solishtirib tekshiradi va uni yakuniy integratsiya qiladi.

**Mas'ul:** Claude Code (Orchestrator, yakuniy vakolat)

**Kirish (Input):**
- Fayzillo tomonidan loyihaga kiritilgan AGY natijasi

**Jarayon:**
1. Kod sifat, konventsiya va vazifa talablariga mosligi tekshiriladi
2. Mos bo'lsa — integratsiya qilinadi (merge/finalize); mos bo'lmasa — tuzatish so'raladi (qayta dispatch)
3. `orcestor/status/` ga natija bo'yicha log yoziladi
4. Vazifa fayli `task_pending/` dan `task_compliete/` ga ko'chiriladi

**Chiqish (Output):**
- Yangilangan `orcestor/status/` yozuvi
- Vazifa fayli `orcestor/task_compliete/` da

**Done when:**
Kod kodbazaga integratsiya qilingan, status yangilangan, vazifa fayli `task_compliete/` ga ko'chirilgan.


## Manba: `my_digital_brain/90_System/orcestor/project_status/overview.md`

# Project Status — my_digital_brain

**Oxirgi yangilanish:** 2026-08-20 (bootstrap paytida yaratildi)
**Yangilanish rejimi:** on_demand

## Loyiha tuzilmasi
- **`ai-chat-history/`** — ChatGPT, Claude, Gemini, Grok suhbat arxivlari (bir nechta email akkaunt)
- **`repo_analiz/`** — Repozitoriyalarni tahlil qilish loyihasi (FULLDEEP-01..11 + SYNTHESIS — hammasi ✅ yakunlangan, 2026-08-04)
- **`reports_agy/`** — 28 ta tahlil hisoboti (deep_*, fulldeep_*, principles.md)
- **`tasks/`** — Roadmap va sintez fayllar (00..07_step_*.md)
- **`orcestor/`** — Orcestor-skill workspace (hozir qurildi)

## Oxirgi bajarilgan ishlar
- Barcha repo tahlil tasklari (FULLDEEP-01..11) yakunlangan (2026-08-04)
- Orcestor-skill bootstrap qilindi (2026-08-20)

## Ma'lum muammolar
(yo'q)


## Manba: `zdes_archive_docs/raw_history/orcestor/tasklist.md`

# Tasklist — `zdes/orcestor/` (backend↔frontend API ulash)

2 fazali oqim (`requirements.MD` 0-bo'lim, `README.MD`):
- **Faza 1 — Tahlil (`B-A-<MODUL>`):** shu sessiya boshqaradi. AGY
  `zdes_backend`ni o'qiydi, `backend_crud_review/<modul>.md`ga yozadi
  (`prompt_analysis.md`), Claude Code (bu sessiya) qator-qator manba bilan
  solishtirib tasdiqlaydi.
- **Faza 2 — Integratsiya (`B-I-<MODUL>`):** **alohida, parallel sessiya**
  boshqaradi (`orcestor/front_integration_tasks/`,
  `../front_agent.md`) — u faqat mening ACCEPTED tahlillarimni
  o'qiydi, backendni qayta tekshirmaydi (`requirements.MD`ga aloqasi yo'q,
  bu boshqa jarayon).

Backend modul ↔ frontend feature xaritasi — **FAZA 1 TO'LIQ TUGADI
(2026-07-25)**, barcha 17/17 ACCEPTED:

| # | Backend modul | Frontend feature | B-A- (tahlil) | B-I- (integratsiya, boshqa sessiya) |
|---|---|---|---|---|
| 1 | `auth` (+`refresh-token`) | `auth` | **ACCEPTED** | yozilgan (`front_agent.md`) |
| 2 | `company` | `company` | **ACCEPTED** | yozilgan |
| 3 | `branch` | `branches` | **ACCEPTED** (patch bilan) | yozilgan |
| 4 | `department` | `departments` | **ACCEPTED** | yozilgan |
| 5 | `position` | `positions` | **ACCEPTED** | yozilgan |
| 6 | `user` | `employees` | **ACCEPTED** | yozilgan |
| 7 | `attendance` (+`raw-attendance-log`) | `attendance` | **ACCEPTED** | backlog (boshqa sessiyada) |
| 8 | `work-schedule` | `work-schedules` | **ACCEPTED** | backlog |
| 9 | `terminal` | `terminals` | **ACCEPTED** | backlog |
| 10 | `employee-leave` | `leaves` | **ACCEPTED** (patch bilan — `/api/v1` prefiksi) | backlog |
| 11 | `holiday` | `holidays` | **ACCEPTED** | backlog |
| 12 | `advance` | `advances` | **ACCEPTED** | backlog |
| 13 | `salary-adjustment` | `salary-adjustments` | **ACCEPTED** | backlog |
| 14 | `payroll` | `payroll` | **ACCEPTED** | backlog |
| 15 | `notification` | `notifications` | **ACCEPTED** | backlog |
| 16 | `setting` | `settings` | **ACCEPTED** | backlog |
| 17 | — (agregat, backendda alohida modul YO'Q) | `dashboard` | **ACCEPTED** (topilma: backend endpoint yo'q, `dashboard.md`da tavsiya yozilgan) | backlog |

**Hozircha tashqarida** (frontendda to'g'ridan-to'g'ri feature yo'q,
kerak bo'lsagina qo'shiladi): `app-version`, `push-token`, `turnstile`.

Holat qiymatlari: `backlog` → `draft` → `pending` → `complete` →
`ACCEPTED` / `REJECTED` / `NEEDS_REVISION` (`status/`da).

---

## Joriy holat (2026-07-25) — Faza 1 yakunlandi

**17/17 modul ACCEPTED.** Har birining tafsiloti: `orcestor/status/B-A-*.log`.
Ikkita patch talab qilindi (branch — kiruvchi relations to'liq emas edi;
employee-leave — `/api/v1` prefiksi butunlay tushib qolgan edi, shundan
keyin shablon (`prompt_analysis.md`) ikkalasi uchun ham mustahkamlandi).

**Keyingi qadam — Fayzillodan kutilmoqda:** Faza 1 tugagani haqida xabar
berish, keyingi buyruqni kutish (yangi modul kerakmi, yoki Faza
2/integratsiya tomonga o'tish kerakmi — bu allaqachon parallel sessiyada
ketmoqda).


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ovovo******utvata@gmail.com/lokal_fayl_tahlili.md`

# Lokal fayl tahlili

### 👤 Foydalanuvchi:

admin:///home/fayzillo/Desktop/testing/claude_tasks/new_fixing_orcestration_system.zipadmin:///home/fayzillo/Desktop/testing/claude_tasks/README.md

### 🤖 ChatGPT:

Ko'rinishidan siz lokal fayl yo'lini yuborgansiz:

- `admin:///home/fayzillo/Desktop/testing/claude_tasks/new_fixing_orcestration_system.zip`
- `admin:///home/fayzillo/Desktop/testing/claude_tasks/README.md`

Men kompyuteringizdagi fayllarga bevosita kira olmayman. Ularni tahlil qilishim uchun quyidagilardan birini qiling:

1. **ZIP faylni** chatga yuklang.
2. Yoki **README.md** faylini chatga tashlang.
3. Yoki ikkalasini ham yuklang.

Shundan keyin men:
- ZIP ichidagi barcha papka va fayllarni tahlil qilaman.
- Arxitekturasini tushuntiraman.
- Orchestrator logikasini tekshiraman.
- Muammolarini topaman.
- Kerak bo'lsa refaktor bo'yicha aniq tavsiyalar beraman.

Oldingi safargidek faqat README emas, butun ZIP'ni ham ochib, ichidagi kodlarni ko'rib chiqaman.

---

### 🤖 ChatGPT:

ZIP ochildi va o'qildi. README ham ko'rildi. fileciteturn0file0L6-L17

Birinchi taassurotim: bu **kod emas**, balki yaxshi o'ylangan **architecture decision record (ADR)** to'plami. Hujjatlar tartibli va bir-birini to'ldirib boradi.

### Tuzilishi

```
new_fixing_orcestration_system/
├── README.md
├── 01-muammo-va-kelib-chiqishi.md
├── 02-metaforalar.md
├── 03-arxitektura-eskiz.md
├── 04-taxminlar-va-tekshirish.md
├── 05-use-caselar.md
└── 06-xulosa-va-keyingi-qadamlar.md
```

### Kuchli tomonlari

Menga ayniqsa quyidagilar yoqdi:

- Muammo → Metafora → Arxitektura → Taxmin → Use Case → Xulosa ketma-ketligi.
- Taxminlarni o'chirmaslik (`✅`/`❌`) g'oyasi. Bu keyinchalik nima sinab ko'rilganini unutmaslikka yordam beradi.
- Session memory va permanent memory ni alohida qatlamlarga ajratish.
- Token sarfini asosiy muammo sifatida ko'rganing.

Bu hujjatlarni o'qiganda g'oya nima uchun paydo bo'lgani tushunarli bo'ladi.

---

## Lekin men ko'rayotgan eng katta muammo

Hozirgi reja **AI qanday ishlaydi** ni juda yaxshi tushuntiradi.

Ammo **DB qanday ishlaydi** deyarli yo'q.

Masalan:

- task lifecycle
- state machine
- lock
- queue
- retry
- worker
- parallel session
- conflict resolution

bular haqida deyarli yozilmagan.

Natijada implementatsiya boshlansa juda ko'p qarorlar yana joyida qabul qilinadi.

---

## Ikkinchi muammo

Session checkpoint yoziladi deyilgan.

Lekin:

```
qachon yoziladi?
```

Masalan

- har promptdan keyinmi?
- 5 promptdan keyinmi?
- tool ishlagandan keyinmi?
- file edit bo'lgandan keyinmi?
- manualmi?

Bular hali specification darajasiga chiqmagan.

---

## Uchinchi muammo

Standing rules juda muhim.

Ammo versioning yo'q.

Masalan

```
Rule v1
Rule v2
Rule merged
Rule deprecated
```

yoki

```
created_by
updated_by
source_session
confidence
```

kabi metadata kerak bo'lishi mumkin.

---

## To'rtinchi muammo

Task modeli hali yo'q.

Masalan men kutgan edim:

```
Task

id
project
title
goal
status

NEW
READY
RUNNING
WAITING
FAILED
DONE

priority

parent_task

checkpoint_id

summary

created_at
updated_at
```

Shunaqa model hali yozilmagan.

---

## Beshinchi muammo

Orchestrator ichidagi agentlar hali concept darajasida.

Masalan

```
Planner

↓

Architect

↓

Coder

↓

Reviewer

↓

Tester

↓

Committer
```

yoki

```
Claude
↓

AGY

↓

DB

↓

Task Queue
```

interaction diagram hali yo'q.

---

## Men qo'shishni tavsiya qiladigan hujjatlar

Men bo'lsam yana quyidagilarni yozardim:

```
07-database-schema.md

08-task-lifecycle.md

09-agent-protocol.md

10-api.md

11-conflict-resolution.md

12-performance.md

13-failure-recovery.md

14-versioning.md
```

Shunda bu hujjatlar bevosita implementatsiya uchun specification bo'lib qoladi.

---

## Umumiy baho

Agar bu hujjatni:

- oddiy README sifatida baholasam:

**10/10**

Agar uni:

- implementatsiyaga tayyor specification sifatida baholasam:

**7.5/10**

G'oya juda yaxshi shakllangan, lekin implementatsiya uchun hali texnik tafsilotlar yetishmaydi. Eng katta bo'shliq — **DB modeli, task lifecycle va agentlar o'rtasidagi protokol**. Shu uchta qism yozilsa, bu hujjat real tizimni qurish uchun ancha to'liq spetsifikatsiyaga aylanadi.

---

### 👤 Foydalanuvchi:

Hozirgina yozilgan bular README.MD da bazi tafsilotlar holos asosiy qisim zip fayilidagi md larda ularni o'qib chiqmasang vaziyatga tushunmaysan kegin menga aqillik qilmasdan qisqacha nimani tushunganingni ayt.

### 🤖 ChatGPT:

Ha, endi to'liq o'qib chiqdim.

Qisqacha men tushungan narsa:

- Bu **yangi orchestrator yozish loyihasi emas**. Asosiy maqsad — hozir turli loyihalarda tarqab ketgan `orcestor` g'oyasini yagona tizimga keltirish.
- Sen aniqlagan asosiy muammo **AI kod yozishi emas**, balki har sessiyada eski context qayta-qayta yuklanishi sabab tokenlarning 80% behuda ketayotgani.
- Shu sabab sen fayl-asosli (`status.md`, `requirements.md`, `prompt.md`) ishlashdan asta-sekin **DB-asosli knowledge storage** ga o'tmoqchisan.
- Sen xotirani ikki turga ajratgansan:
  - **Session checkpoint** — qisqa muddatli, sprint yakunidagi holat.
  - **Standing rules** — uzoq muddatli, sessiyadan mustaqil qoidalar.
- **AGY** ni kotib sifatida ishlatmoqchisan: u checkpoint va qoidalarni yozadi. **Claude** esa qimmat resurs bo'lgani uchun faqat o'qiydi, tekshiradi va tasdiqlaydi.
- `/clear` endi "hammasini unutish" emas, balki sprint tugashi bo'ladi. Keyingi sessiya faqat oxirgi checkpoint va kerakli standing rule'larni yuklaydi.
- Hujjatlarda ataylab ko'p narsani "taxmin" deb qoldirgansan. Ya'ni bu yakuniy dizayn emas, pilot orqali tekshiriladigan reja.
- Birinchi haqiqiy sinov sifatida ham aynan **4 ta `orcestor` nusxasini birlashtirish** tanlangan. Agar shu ishlasa, qolgan loyihalarga ham tarqatiladi.

Menga yana bitta narsa yoqdi: sen DB'ni "tokenni tejaydigan sehrli vosita" deb qaramabsan. Aksincha, tejash **compact checkpoint** va **selective loading** dan kelishini alohida ta'kidlagansan. Bu hujjatdagi eng muhim g'oyalardan biri deb tushundim.

---

### 👤 Foydalanuvchi:

Aslida boshida shunchaki ckat kjabi ishladim clida  birinchi kuni va status.md g'oyasi keldi  ekgingi kuni vazifani tasklarga bo'lish loyihani hujjatlashtirish kegin history usuliga o'tdim yani ikkinchi kuni orcetor g'oyasi kegin esa dbda tasklarni boshqarish endi smal context backup usuliga o'tmoqchiman clean session single task multi agent free token :xd.  Kelajactda db ga yozishni aftomatlashtirmoqchiman. yani o'zim API chiuqaraman NestJs server u serverda agy --print bilaqn birmarttalik amalni bajarib natijani qaytaradi. tekin Apilar bitta pro obuna va bir nechta tekin agentlar.

### 🤖 ChatGPT:

Endi ancha tushunarli bo'ldi. Menga ko'rinishicha, g'oya bir necha bosqichda tabiiy evolyutsiya qilgan:

1. **Status.md** — "Claude keyingi sessiyada nima bo'lganini eslasin."
2. **Tasklarga bo'lish** — katta vazifani mayda vazifalarga ajratish.
3. **History** — nima qilindi, nima uchun qilindi, nima rad etildi.
4. **Orchestrator** — bularni tartib bilan boshqaradigan qatlam.
5. **DB** — fayllar o'rniga strukturali saqlash.
6. **Small context backup** — faqat kerakli minimum kontekstni yuklash.

Menga eng qiziq tuyulgan joy oxirgisi.

Bu endi oddiy "AI task manager" emas. Bu ko'proq **AI uchun operatsion tizim** g'oyasiga o'xshayapti:

- Session = vaqtinchalik RAM.
- DB = disk.
- Checkpoint = save state.
- Standing rules = konfiguratsiya.
- Task = process.
- Agent = worker.

Kelajakdagi rejang ham mantiqli ketma-ketlikda:

```
NestJS API
        │
        ▼
Task Queue
        │
        ▼
AGY --print
        │
        ▼
Natija
        │
        ▼
DB ga avtomatik yozish
```

Shunda Claude yoki boshqa model to'g'ridan-to'g'ri SQL yozmaydi. Hammasi API orqali boshqariladi.

Yana bir narsa e'tiborimni tortdi:

> tekin Apilar bitta pro obuna va bir nechta tekin agentlar.

Bu aslida **heterogeneous multi-agent** arxitekturasi. Ya'ni har agentning vazifasi boshqacha:

- qimmat model — murakkab reasoning;
- tekin model — hujjat yozish;
- yana biri — summary;
- yana biri — classification;
- AGY esa orchestration.

Shunda eng qimmat tokenlar faqat haqiqatan kerak bo'lgan joyda ishlatiladi.

Menimcha, sening asosiy maqsading "yana bitta AI agent" qilish emas. Sen AI'ni **stateless chat**dan chiqarib, **stateful development environment**ga aylantirishga harakat qilyapsan. Shu nuqtani tushunganimdan keyin hujjatlardagi ko'p qarorlar o'z o'rniga tushdi.

---

### 👤 Foydalanuvchi:

Endi bu rejamni qisqa qilib yozib ber men uni claude cliga beraman u yuqoridagi zipdagi fayillarni yozayotgan agent . Unga APPI haqida aytmagandim.

### 🤖 ChatGPT:

Qisqacha va Claude CLI uchun:

:::writing{variant="document" id="48371"}
Bu g'oya bir kunda paydo bo'lmagan, balki amaliy ishlash davomida bosqichma-bosqich shakllangan.

Evolyutsiya quyidagicha bo'lgan:

1. Dastlab har sessiyadan keyin holatni saqlash uchun `status.md` g'oyasi paydo bo'ldi.
2. Keyin katta vazifalarni kichik tasklarga ajratish va loyiha hujjatlarini tartibga solish qo'shildi.
3. So'ng history yondashuvi qo'shildi — nima qilindi, nima uchun qilindi va qaysi gipotezalar rad etilgani saqlanadigan bo'ldi.
4. Shu jarayondan `orcestor` konsepsiyasi tug'ildi.
5. Keyinchalik fayllar o'rniga DB orqali task va holatlarni boshqarish g'oyasi paydo bo'ldi.
6. Hozirgi asosiy maqsad esa **small context backup**: har yangi sessiyada butun tarixni emas, faqat kerakli minimal checkpoint va standing rule'larni yuklash.

Uzoq muddatli maqsad — bu jarayonni to'liq avtomatlashtirish.

Buning uchun alohida NestJS API server yaratiladi. Agentlar (masalan, AGY) ish yakunida bitta buyruq orqali natijani API'ga yuboradi, API esa checkpoint, history, standing rule va task holatini avtomatik ravishda DB'ga yozadi. Shunday qilib AI modellar faqat reasoning bilan shug'ullanadi, holatni saqlash va boshqarish esa markaziy servis zimmasida bo'ladi.

Yakuniy maqsad — **clean session + single task + multi agent + minimal context** tamoyiliga asoslangan, tokenni tejaydigan va istalgan AI model bilan ishlay oladigan orchestration tizimini yaratish.
:::

---

### 👤 Foydalanuvchi:

E axmoq men senga holatni tushuntirdim yani ishlab turgan cli sessiyaga yozaman. u sessiyda yuqoridagi hujjatlarni shakiillantirganman. Shundan kelib chiqib promt yoz desam sen toliq shu chatdagi Contextni promt qilib berding

### 🤖 ChatGPT:

Tushundim. Sen **Claude CLI ichida davom etayotgan sessiyaga bitta qo'shimcha topshiriq** bermoqchisan. U oldingi hujjatlarni allaqachon biladi. Shuning uchun unga faqat **yangi g'oyani** aytish kerak.

Mana shunday prompt yetarli:

:::writing{variant="document" id="63428"}
Yangi g'oya paydo bo'ldi. Uni mavjud hujjatlarni buzmasdan, kerakli joylarga qo'sh yoki yangila.

Asosiy evolyutsiya endi quyidagicha davom etadi:

`status.md` → task management → history → orcestor → DB-based task management → small context backup.

Hozirgi asosiy maqsad endi **small context backup** konsepsiyasi bo'ladi. Ya'ni har yangi sessiyada butun history yoki barcha hujjatlar emas, faqat ayni task uchun kerakli minimal checkpoint va standing rule'lar yuklanadi. Maqsad — clean session, minimal context va token sarfini keskin kamaytirish.

Shuningdek, kelajakdagi roadmap sifatida quyidagi g'oyani ham hujjatlarga mos joyda qayd et:

Kelajakda barcha checkpoint, history, standing rule va task holatini saqlash qo'lda emas, avtomatik ishlaydi. Buning uchun alohida NestJS API server yaratiladi. Agentlar (masalan AGY) ish yakunida natijani API'ga yuboradi, API esa barcha kerakli yozuvlarni DB'ga avtomatik saqlaydi. Bu hozirgi implementatsiya emas, balki uzoq muddatli roadmap sifatida qayd etilsin.

Mavjud hujjatlar bilan zid joylar bo'lsa, ularni moslashtir, ammo umumiy konsepsiyani o'zgartirma.
:::

---


## Manba: `zdes_archive_docs/raw_history/orcestor/front-tasklist.md`

# orcestor/tasklist.md — Umumiy task progress jadvali (ARXIV, 2026-07-25gacha)

> **2026-07-26dan boshlab bu fayl endi qo'lda yangilanmaydi** — status/
> holat manbai PostgreSQL (`zdes_orcestor` bazasi, `tasks` jadvali) ga
> ko'chdi. Batafsil: [`README.MD`](./README.MD) 7-bo'lim (ulanish,
> sxema). Joriy holatni ko'rish uchun:
> ```sql
> SELECT task_id, status, verdict, module FROM tasks ORDER BY task_id;
> ```
> Pastdagi jadval — 2026-07-25 kungacha bo'lgan holatning muzlatilgan
> nusxasi, tarixiy ma'lumot sifatida qoladi.

**Oxirgi yangilanish (fayl sifatida, muzlatilgan):** 2026-07-25

## 1. Asosiy modullar (10 modul)

| Task | Sarlavha | Holat |
|---|---|---|
| T-001 | agency-agents repodan skill/tool fayllarni `agents/skills/`ga olib kelish (meta) | ✅ Tugagan |
| T-002 | `orcestor/dispatch.py` — vazifa hayot siklini boshqaruvchi skript (meta) | ✅ Tugagan |
| T-003 | [Modul 1/10] Core infratuzilma — Routing, Environment, HTTP servisi | ✅ Tugagan |
| T-004 | [Modul 2/10] Auth — login, guard'lar, interceptor'lar | ✅ Tugagan |
| T-005 | [Modul 3/10] Shared UI Kit — DataTable, ConfirmDialog, ImageUpload, CameraCapture, Header, Sidebar, Pipe'lar | ✅ Tugagan |
| T-006 | [Modul 4/10] Dashboard | ✅ Tugagan |
| T-007 | [Modul 5/10] Tashkiliy tuzilma — Company/Branches/Departments/Positions | ✅ Tugagan |
| T-008 | [Modul 6/10] Xodimlar — CRUD + Face Register | ✅ Tugagan |
| T-009 | [Modul 7/10] Vaqt va Davomat — Attendance/Work Schedules/Terminals/Scanner | ✅ Tugagan |
| T-010 | [Modul 8/10] Ta'til va G'oyiblik — Leaves/Holidays/Advances | ✅ Tugagan |
| T-011 | [Modul 9/10] Ish haqi — Payroll/Salary Adjustments | ✅ Tugagan |
| T-012 | [Modul 10/10] Admin — Settings/Notifications | ✅ Tugagan |

## 2. Sifat auditi seriyasi (T-013..T-019)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-013 | Dark/Light rejim moslik tahlili (faqat tahlil) | — | ✅ Tugagan |
| T-014 | Performance holati tahlili (faqat tahlil) | — | ✅ Tugagan |
| T-015 | API baseUrl globallashtirish auditi (tahlil + tuzatish) | — | ✅ Tugagan (tuzatish kerak topilmadi) |
| T-016 | Tailwind CSS tahlili (faqat tahlil) | — | ✅ Tugagan |
| T-017 | Dark/Light rejimni amalga oshirish | T-013 natijasiga asoslanadi | ✅ Tugagan |
| T-018 | Dublikat/orphaned fayllar auditi va tozalash | — | ✅ Tugagan (0 dublikat topildi) |
| T-019 | Performance tuzatishlari — OnPush + RxJS `takeUntilDestroyed` | T-014 topilmalariga asoslanadi | ✅ Tugagan |

## 3. API/State hujjatlashtirish seriyasi (T-020..T-022)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-020 | [Docs 1/3] Core/Auth/Dashboard/Tashkiliy tuzilma — API + state hujjati | — | ✅ Tugagan |
| T-021 | [Docs 2/3] Xodimlar/Davomat/Ta'til guruhi — API + state hujjati | — | ✅ Tugagan |
| T-022 | [Docs 3/3] Payroll/Admin + yakuniy indeks (`project_docs/api/README.md`) | T-020, T-021 tugagandan keyin | ✅ Tugagan |

## 4. Error handling + Axios seriyasi (T-023..T-025)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-023 | Error handling darajasi auditi (faqat tahlil) | — | ✅ Tugagan |
| T-024 | Axios'ga o'tish — imkoniyat tahlili (faqat tahlil) | — | ✅ Tugagan (Variant A — kam-ta'sirli tavsiya qilindi) |
| T-025 | Axios'ni amalga oshirish | T-024 tugagandan keyin, uning rejasiga rioya qiladi | ✅ Tugagan (Claude Code to'g'ridan-to'g'ri yozdi, AGY'siz — kritik infra) |

## 5. Performance/UX seriyasi (T-026..T-031)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-026 | [Perf 1/6] Skeleton/bubble loading — shared komponent | — | ✅ Tugagan |
| T-027 | [Perf 2/6] DataTable — qidiruv/filter | T-026dan keyin (bir xil faylga tegadi) | ✅ Tugagan (+ Claude Code hardcoded rang/dead CSS tuzatishi) |
| T-028 | [Perf 3/6] DataTable — DOM virtualization (`@angular/cdk`) | T-027 tugagandan keyin | 📝 Draft (`tasks/`) |
| T-029 | [Perf 4/6] Lazy loading — `@defer` + rasm lazy-load | Mustaqil | 📝 Draft (`tasks/`) |
| T-030 | [Perf 5/6] HTTP javob keshlash (caching) | Mustaqil (axios/HttpClient'dan qat'i nazar) | 📝 Draft (`tasks/`) |
| T-031 | [Perf 6/6] Server-side pagination — faqat API sirtini tayyorlash | T-027, T-028 tugagandan keyin | 📝 Draft (`tasks/`) |

## 6. Auth UX — alohida so'rov (T-032)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-032 | `/auth/login` → `/sign` + bitta sahifada Login/Register animatsiyali switch-form | Mustaqil (Fayzillo to'g'ridan-to'g'ri so'ragan, 2026-07-25) | 📝 Draft (`tasks/`) |

## 9. Responsive/Dark-mode audit (T-033)

| Task | Sarlavha | Bog'liqlik | Holat |
|---|---|---|---|
| T-033 | Responsive + Dark/Light mode + Forma UX auditi (shallow) | Mustaqil (Fayzillo so'ragan, 2026-07-25) | ✅ Tugagan (Claude Code to'g'ridan-to'g'ri, AGY'siz) — natija: [`analysis/T-033-...md`](./analysis/T-033-responsive-darkmode-forms-audit.md) |

**MUHIM (2026-07-25):** shu sanadan boshlab bu T-0XX tizimini backend
tahlili qilgan sessiya boshqaradi (`zdes/orcestor/` endi alohida,
paralel API-integratsiya sessiyasining hududi — konflikt bo'lmasin
uchun ikkiga bo'lingan).

## 7. Umumiy holat

- **Jami:** 33 ta task.
- **Tugagan:** 28 ta (T-001..T-027, T-033).
- **Draft, hali dispatch qilinmagan:** 5 ta (T-028..T-032).
- **API/state docs seriyasi (T-020..T-022) TO'LIQ TUGADI** —
  `project_docs/api/README.md` 17 modulga havola beruvchi indeks. Bundan
  buyon yangilab borish qoidasi: `orcestor/requirements.MD` 7-bo'lim.
- **`task_pending/`da (jarayonda):** hozircha yo'q.

## 8. Muhim ochiq savollar (keyingi tasklarga bog'liq)

- T-016 (Tailwind) tavsiyasi hali amalga oshirilmagan (agar "o'tish kerak" desa, alohida implementatsiya taski kerak bo'ladi — bu jadvalda yo'q, kelajakda qo'shiladi).
- T-024 (axios) qaysi variantni (kam-ta'sirli/katta-ta'sirli) tavsiya qilishi T-025 va T-030 ning bajarilish tartibiga ta'sir qiladi.
- T-031 ataylab to'liq server-side pagination migratsiyasi EMAS — backend real bo'lganda yangi task kerak bo'ladi.
- T-032 Register uchun backend `/auth/register` endpoint kontrakti hali tasdiqlanmagan — frontend taxmin asosida yoziladi, real backend kelganda moslashtirish kerak bo'lishi mumkin.


## Manba: `zdes_archive_docs/raw_history/orcestor/steps/01-intake.md`

# 1-bosqich: Intake (Vazifani aniqlash)

**Maqsad:** Claude Code kodda bajarilishi kerak bo'lgan ishni aniqlaydi va uni aniq chegaralangan (scoped) vazifaga aylantiradi.

**Mas'ul:** Claude Code (Orchestrator)

**Kirish (Input):**
- Loyihadagi holat, foydalanuvchi so'rovi yoki mavjud backlog
- Kodbaza konteksti (`zdes-frontend`)

**Chiqish (Output):**
- Yangi vazifa fayli `orcestor/tasks/` papkasida (masalan, `TASK-001-nomi.md`)
- Vazifa faylida: maqsad, qamrov (scope), qabul mezonlari, tegishli fayllar/modullar

**Done when:**
Vazifa fayli `orcestor/tasks/` ichida yaratilgan, aniq va bitta izchil ishni tasvirlaydi, keyingi bosqich (dispatch) uchun tayyor.


## Manba: `my_digital_brain/90_System/claude_tasks/Claude_Tasks_MOC.md`

# 🌿 Claude Tasks va System hujjatlari

### 📁 Qism Papkalar:
- [[agy-align_MOC]]
- [[agy-ui-analizer_MOC]]
- [[agy_agents_MOC]]
- [[new_fixing_orcestration_system_MOC]]

### 📄 Fayllar:
- [[Orchestration_Synthesis_Report]]


## Manba: `zdes_archive_docs/raw_history/orcestor/errors/README.md`

# orcestor/errors/ — muammolarni doimiy (persistent) qayd etish

Bu papka `front_integration_tasks/` → `tasks/` → `task_pending/` →
`task_compliete/` → `status/` pipeline'ida yuzaga kelgan **har qanday
muammoni** darhol faylga yozib qo'yish uchun. Sabab (Fayzillo, 2026-07-25):
holat **suhbat konteksti/sessiyaga bog'liq bo'lmasligi** kerak — tarmoq
uzilishi, sessiya kompaktlanishi/tugashi, token limiti yoki `agy` kvotasi
tugashi holat izini yo'qotmasligi kerak. Fayl har doim disk ustida qoladi;
keyingi sessiya (yoki shu sessiyaning davomi) shu papkani o'qib, aynan
qayerda to'xtaganini va nima qilish kerakligini bilib oladi.

## Qachon yoziladi

Quyidagi holatlardan BIRI yuz bersa, `errors/B-I-<MODULE>.md` (yoki
`errors/B-A-<MODULE>.md`, agar kerak bo'lsa) darhol yoziladi/yangilanadi:

- `agy` chaqiruvi vaqt tugashi (`--print-timeout`) yoki tarmoq xatosi bilan tugasa.
- `agy models`da "individual quota reached" yoki shunga o'xshash xato chiqsa.
- AGY javobi keldi, lekin `npm run build` xato bersa (`NEEDS_REVISION`).
- AGY javobi keldi, lekin `backend_crud_review/<module>.md` bilan solishtirganda
  nomuvofiqlik/qamrovdan tashqari o'zgarish topilsa.
- AGY hech narsa yozmagan (bo'sh diff) — "muvaffaqiyatsiz dispatch" pattern.
- Har qanday kutilmagan holat — jarayon davom etishidan oldin qayd etiladi.

## Fayl formati

```markdown
## Task ID: B-I-<MODULE>
### Holat: FAILED_DISPATCH | BUILD_FAILED | NEEDS_REVISION | STRAY_FILES | UNKNOWN
### Vaqt: <ISO timestamp>

**Nima bo'ldi:**
[Aniq tavsif — xato xabari, qaysi bosqichda]

**Hozirgi fayl holati:**
- `orcestor/tasks/B-I-<MODULE>.md`: [bor/yo'q]
- `orcestor/task_pending/B-I-<MODULE>.md` / `-response.md`: [bor/yo'q]
- `test-zdes-front` git status (agar tekshirilgan bo'lsa): [xulosa]

**Keyingi qadam (retry qilinganda nima qilish kerak):**
[Aniq ko'rsatma — masalan "qayta dispatch qiling", "qo'lda tuzating",
"Fayzilloga eskalatsiya"]

**Hal qilindi (keyinroq to'ldiriladi):** [sana + qanday hal bo'ldi]
```

## Qoida

- Bu fayllar **hech qachon jimgina o'chirilmaydi** — muammo hal bo'lgach
  ham, "Hal qilindi" bandi to'ldirilib, faylda qoldiriladi (audit trail).
- Har bir yangi sessiya/davomida ishni boshlashdan oldin bu papkani
  (`ls orcestor/errors/`) tekshirish kerak — hal qilinmagan muammo bo'lsa,
  o'sha modulni davom ettirishdan oldin shuni hal qilish birinchi navbatda turadi.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/blocker-va-subtask/use_cases.md`

# Use Cases — Blocker/sub_task

## UC-1: Yetishmayotgan dependency (bog'liq, ketma-ket)

Asosiy task boshqa modulni chaqiradi, lekin o'sha modul hali yozilmagan.
→ Sub_task: modulni yaratish. Ketma-ket, chunki asosiy task shu natijaga
muhtoj.

## UC-2: Ikkita mustaqil kichik xato bir vaqtda topildi (mustaqil,
parallel)

Asosiy task davomida ikkita boshqa-boshqa, bir-biriga bog'liq bo'lmagan
kichik xato aniqlandi (masalan bittasi lint xatosi, ikkinchisi eskirgan
kommentariya). → Ikkalasi ham parallel sub_task sifatida ochilishi
mumkin, chunki bir-biriga bog'liq emas.

## UC-3: Context hali keng — bir xil sessiyada davom etish

Sub_task (masalan kichik utility funksiya yozish) tugadi, `/context`
tekshiruvida Messages ulushi hali past. → Checkpoint yozmasdan, xuddi
shu sessiyada asosiy taskka qaytiladi.

## UC-4: Context torlashgan — checkpoint + restart

Bir nechta sub_task ketma-ket ochilib, context sezilarli to'lgan. →
SKILL.md standart protokoli: `simple_context.md` yangilanadi, token
hisob-kitobi yoziladi, Supervisor_User qaroriga ko'ra restart qilinadi.

## UC-5 (taxminiy): Frontend loyihada blocker

Dizayn-token yoki komponent-kutubxona hali aniqlanmagan bo'lsa, UI
task'i boshlanishidan oldin bu **ketma-ket sub_task** sifatida hal
qilinishi mantiqiy — chunki keyingi barcha UI ishlari shunga bog'liq.

## UC-6 (taxminiy): Backend loyihada blocker

API kontrakti yoki DB sxemasi hali kelishilmagan bo'lsa — bu ham odatda
**ketma-ket** (boshqa endpointlar shunga tayanadi). Lekin agar bir nechta
mustaqil endpoint ustida parallel ishlansa, har biri o'z sub_task'i
sifatida **parallel** ochilishi mumkin.

## UC-7 (taxminiy): Bir xil blocker takrorlanishi

Agar xuddi shu turdagi blocker (masalan "eslatma: testlar hali
yozilmagan") bir necha marta chiqsa — bu holatni maxsus standing rule
sifatida yozib qo'yish, har safar sub_task ochishdan ko'ra samaraliroq
bo'lishi mumkin.


## Manba: `zdes_archive_docs/raw_history/orcestor/message.md`

# Xabar — Backend-tahlil/T-0XX sessiyasidan (2026-07-26)

Salom. Bu xabarni `test-zdes-front/orcestor/` (T-0XX tizimi) ustida
ishlayotgan sessiya qoldirdi — Fayzillo ikkalamiz o'rtasida shared
resurs haqida xabar berishni so'radi.

## Nima o'zgardi

Fayzillo qarori bilan orkestratsiya **status/holat/tarixi** endi fayl
emas, PostgreSQL'da saqlanadi (T-0XX tizimida allaqachon amalda —
`task_compliete/`/`status/` fayllari DB tasdiqlangandan keyin
o'chirilmoqda). Fayzillo buni **sizning B-A-*/B-I-* tizimingizga ham
taklif qildi** — foydalanish ixtiyoriy, lekin tavsiya etiladi (fayl
konfliktidan farqli, Postgres concurrent yozuvni xavfsiz boshqaradi).

## Ulanish

```
Host:     localhost
Port:     5432
Database: zdes_orcestor
User:     fayzullo
Password: 12345678
```

`DATABASE_URL`:
```
postgresql://fayzullo:12345678@localhost:5432/zdes_orcestor
```

Parolsiz ulanish uchun `~/.pgpass`ga shu qatorni qo'shish mumkin:
```
localhost:5432:zdes_orcestor:fayzullo:12345678
```
(keyin oddiy `psql -h localhost -U fayzullo -d zdes_orcestor` yetarli).

**Muhim:** bu DB `zdes_backend`ning production/dev bazalariga
(`test_zdes`, `zdes_db` — Prisma) HECH QANDAY aloqasi yo'q, butunlay
alohida, faqat orkestratsiya holatini kuzatish uchun.

## Sxema (qisqacha — to'liq DDL: `../test-zdes-front/orcestor/db/schema.sql`)

- **`tasks`** — har bir task uchun bitta qator: `task_id` (UNIQUE,
  masalan `B-A-COMPANY`, `B-I-USER`), `title`, `system`, `phase`,
  `module`, `status` (`draft`/`pending`/`complete`/`accepted`/
  `rejected`/`needs_revision`), `goal`, `constraints_txt`,
  `definition_of_done`, `files_in_scope` (`TEXT[]`), `dispatched_at`,
  `completed_at`, `reviewed_at`, `verdict`, `reviewer_notes`.
- **`task_events`** — voqealar tarixi: `task_id`, `event_type`
  (`created`/`dispatched`/`response_received`/`accepted`/`rejected`/
  `needs_revision`/`patched`/`note`), `note`, `created_at`.
- **`changed_files`** — "O'zgargan fayllar" jadvali: `task_id`,
  `file_path`, `change_type` (`yangi`/`o'zgartirilgan`/`o'chirilgan`),
  `reason`.

## Konflikt bo'lmasligi uchun

- **`system` ustunini har doim to'ldiring**: sizning tasklaringiz uchun
  `'zdes-integration'` (yoki `'zdes-backend-analysis'` — bu ikkovi
  allaqachon band, farqlash uchun). Men `test-zdes-front` ishlataman.
- **`task_id` nomlanish hech qachon to'qnashmaydi**: sizniki `B-A-*`/
  `B-I-*`, meniki `T-0XX` — shuning uchun bitta jadvalni baham ko'rish
  xavfsiz (Postgres UNIQUE constraint + tranzaksiyalar himoya qiladi).
- O'z tasklaringizni yozish namunasi:
  ```sql
  INSERT INTO tasks (task_id, title, system, phase, module, status)
  VALUES ('B-I-COMPANY', 'Company modul API integratsiyasi',
          'zdes-integration', 'integration', 'company', 'pending')
  ON CONFLICT (task_id) DO UPDATE SET status = EXCLUDED.status;
  ```
- Joriy holatni ko'rish:
  ```sql
  SELECT task_id, status, verdict FROM tasks
  WHERE system = 'zdes-integration' ORDER BY task_id;
  ```

## Eslatma

Bu sizning `front_integration_tasks/`/`front_agent.md` ish oqimingizni
almashtirmaydi — ular AGY'ga topshiriq matnini yuborish uchun baribir
kerak (DB matn emas, prompt kutadi). DB faqat **status/tarix** uchun
qo'shimcha, ixtiyoriy qatlam.

Savol bo'lsa — `test-zdes-front/orcestor/README.MD` 7-bo'limida
batafsilroq yozilgan.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/blocker-va-subtask/qoida.md`

# Qoida (heuristika) — Blocker/sub_task qaror daraxti

Bu **majburiy qoida emas** — har loyihada moslashtirish uchun boshlang'ich
qolip.

## 1-qadam: To'siq chiqqanda — mustaqilmi yoki bog'liqmi?

- **Mustaqil** (asosiy taskka bevosita ta'sir qilmaydi, alohida hal
  qilinishi mumkin) → **parallel** sub_task sifatida ochish mumkin.
- **Bog'liq** (asosiy task natijasi shu sub_task yechimiga muhtoj) →
  **ketma-ket**: avval sub_task, keyin asosiy taskka qaytish.

## 2-qadam: Sub_task tugagach — davom etish yo'li

Context/token holatini tekshiring (masalan Claude Code'da `/context`):

- **Context hali keng** (masalan Messages ulushi past, restart
  chegarasidan uzoq) → asosiy task **xuddi shu sessiyada** davom etadi,
  qo'shimcha checkpoint/restart shart emas.
- **Context torlashgan** → SKILL.md'dagi standart restart protokoliga
  o'ting: `simple_context.md` (yoki `checkpoint add`) yangilang, keyin
  Supervisor_User qarori bilan restart qiling.

## 3-qadam: Loyihaga xos formatni belgilash

Loyiha turi (frontend/backend/boshqa) uchun sub_task fayl/qator formati
qanday bo'lishini birinchi marta blocker chiqqanda Supervisor_User bilan
muhokama qiling, natijani `orcestor/memory/sub_task_policy.md` (yoki
o'xshash nomdagi faylga) yozing — sabab-mulohaza bilan. Keyingi safar bu
loyihada xuddi shu qoida avtomatik qo'llaniladi.

## Qачон bu qoidani qayta ko'rib chiqish kerak

- Agar bir xil turdagi blocker bir loyihada 3+ marta takrorlansa —
  bu holni maxsus qoidaga aylantirib, `standing_rules.json`ga (bir
  qatorlik, qisqa shaklda) qo'shish mantiqiy.


## Manba: `my_digital_brain/00_Bosh_Sahifa.md`

---
tags: [dashboard, bosh, markaz]
cssclasses: [dashboard]
---

# 🧠 Bosh Sahifa (Dashboard)

Xush kelibsiz! Bu sizning raqamli miyangizning markaziy boshqaruv paneli. Quyida barcha bilimlar xaritasiga to'g'ridan-to'g'ri bog'lanishlar (MOC - Map of Content) keltirilgan.

## 📥 Qabulxona (Inbox)
- 📝 **Yangi Qaydlar:** [[Obsidian_Boglanishlar_Darsi]] (O'quv darsi)

## 🚀 Loyihalar va Tahlillar (Projects & Areas)
- 📊 **Hisobotlar va Tahlillar:** [[Reports_MOC]] (Repozitoriya tahlillari)
- 📝 **Vazifalar (Roadmap):** [[Tasks_MOC]] (Kunlik tasklar va jarayonlar)

## 📚 Bilimlar Bazasi (Resources)
- 🤖 **AI Suhbatlar Arxivi:** [[AI_Chat_History_MOC]] (Claude, Grok, ChatGPT, Gemini arxivlari - Daraxt)
- 🎓 **O'quv va Konspektlar:** [[Learning_MOC]] (Angular, Docker darslari - Daraxt)
- 🛠️ **Avtomatlashtirish:** [[Scripting_MOC]] (Skriptlar va sozlamalar - Daraxt)

## ⚙️ Tizim va Orkestratsiya (System)
- 🧠 **Orkestratsiya Qoidalari:** [[Orcestor_MOC]] (Agentlar qoidalari va konfiguratsiyasi)
- 📂 **ADR va Loyihalashtirish:** [[Claude_Tasks_MOC]] (Tizim hujjatlari - Daraxt)

---
**Eslatma:** Har bir havolaga kirsangiz, ichida chiroyli 📁 (papka) va 📄 (fayl) lardan iborat ierarxiya sizni kutmoqda. Obsidian orqali bemalol ularni bitta "Graph View" ga birlashtirishingiz mumkin.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/restart-timing/qoida.md`

# Qoida (heuristika) — Restart timing

Bu **majburiy qoida emas** — SKILL.md'dagi mavjud `/context` o'lchov
mexanizmini qanday interpretatsiya qilishga oid amaliy qo'llanma.

## Chegara sifatida qanday foydalanish mumkin

- Har checkpoint'da "Messages" ulushini yozib boring (SKILL.md talabi).
- Bitta yuqori qiymatga emas, **ketma-ket 2-3 checkpoint'dagi trendga**
  qarang — agar ulush doimiy o'sib borsa (masalan 15% → 20% → 27%),
  bu "kech qolinayotgan" signal.
- Loyiha/task hajmiga qarab shaxsiy chegara belgilang (masalan "25%dan
  oshsa, keyingi tabiiy to'xtash nuqtasida restart taklif qilaman") va
  buni `orcestor/memory/*.md`ga yozib qo'ying — keyingi safar avtomatik
  qo'llaniladi.

## Qachon "erta" restart ham zarar keltiradi

- Agar restart juda erta (masalan Messages ulushi past bo'lsa ham)
  qilinsa, checkpoint yozish/o'qish overhead'i foyda keltirmaydi —
  bu SKILL.md'dagi "context hali keng bo'lsa davom etish mumkin" qoidasi
  bilan bog'liq (qarang: `blocker-va-subtask/qoida.md`, 2-qadam).

## Xulosa

Threshold — yagona son emas, balki **trend + task tabiiy to'xtash
nuqtasi** kombinatsiyasi orqali belgilanadi.


## Manba: `zdes_archive_docs/raw_history/orcestor/steps/06-logging.md`

# 6-bosqich: Logging (Yozib qo'yish)

**Maqsad:** Yakunlangan vazifadagi asosiy qarorlar va natijalar tarixiy jurnalga qayd etiladi.

**Mas'ul:** Claude Code (Orchestrator)

**Kirish (Input):**
- `orcestor/status/` dagi yakuniy natija
- `orcestor/task_compliete/` dagi yakunlangan vazifa

**Chiqish (Output):**
- Qisqa xulosa `orcestor/history/` ichida (operatsion jurnal)
- Muhim/keng ta'sirli o'zgarishlar bo'lsa — loyiha darajasidagi `session/` va `history/` papkalariga ham yoziladi

**Done when:**
Vazifa bo'yicha xulosa `orcestor/history/` da mavjud, va agar ahamiyatli bo'lsa, loyiha darajasidagi jurnalga ham qayd etilgan.


## Manba: `my_digital_brain/90_System/orcestor/status.md`

# ORCESTOR STATUS & TASK MANAGEMENT

**Loyiha:** Repozitoriyalarni Chuqurva Noodatiy Yechimlar Kesimida Tahlil Qilish  
**Tizim:** File-Based Orchestration (`orcestor/`)  
**Maqsad:** `/home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/repos/` ichidagi barcha loyihalardan Fayzillo yozgan **noodatiy yechimlar, custom algoritmlar, murakkab biznes mantiqlari va o'ziga xos arxitektura yondashuvlarini** to'liq o'rganish va hujjatlashtirish.

---

## 🎯 JORIY HOLAT VA REJA

| Task ID | Loyiha / Mavzu | Qiyinchilik / Diqqat Markazi | Status | Natija Fayli |
|---|---|---|---|---|
| `TASK-01` | `Admin-panel` | Private fields (`#`), RegEx validation, custom LocalStorage state | ✅ Bajarildi | `reports_agy/deep_01_admin_panel.md` |
| `TASK-02` | `StudentSYStemMenegment` | Custom Query filter logic, Express Layered Architecture | ✅ Bajarildi | `reports_agy/deep_02_student_sys.md` |
| `TASK-03` | `mini-erp` | ERP domen mantiqlari, File upload va Custom Response handlers | ✅ Bajarildi | `reports_agy/deep_03_mini_erp.md` |
| `TASK-04` | `online-courses` | Domain-Driven Design (DDD), Course Rating, Last Activity tracking | ✅ Bajarildi | `reports_agy/deep_04_online_courses.md` |
| `TASK-05` | `6_oy_imtihon` | C tilida HTML Web Template System, Custom C logic | ✅ Bajarildi | `reports_agy/deep_05_c_web_template.md` |
| `TASK-06` | `e-commerce-backend` | E-Commerce Custom Property-Media, BuildType, Favorites logic | ✅ Bajarildi | `reports_agy/deep_06_ecommerce.md` |
| `TASK-07` | `crm_backend` | Attendance tracking, Staff roles, Group-Student assignment logic | ✅ Bajarildi | `reports_agy/deep_07_crm.md` |
| `TASK-08` | `telegram_app_backend` | Real-time WebSockets Socket.io, Group/Channel Subscription logic | ✅ Bajarildi | `reports_agy/deep_08_telegram_app.md` |

---

## 📝 ORKESTRATSIYA LOGI
- [x] **[2026-08-03 23:15]** `orcestor/` papkasi va file-based task management tizimi yaratildi.
- [x] **[2026-08-03 23:16]** `TASK-01` (`Admin-panel`), `TASK-02` (`StudentSYStemMenegment`), `TASK-03` (`mini-erp`), `TASK-04` (`online-courses`) tahlil qilindi va chuqur hisobotlar saqlandi.
- [x] **[2026-08-03 23:17]** `TASK-06` (`e-commerce`), `TASK-07` (`crm`), `TASK-08` (`telegram_app`) tahlil qilindi va barcha orkestratsiya topshiriqlari yakunlandi.
- [x] **[2026-08-03 23:27]** `FULLDEEP-01` (`Admin-panel`) fulldeep tahlil qilindi, 7 ta noodatiy yechim topildi.
- [x] **[2026-08-03 23:32]** `FULLDEEP-02` (`StudentSYStemMenegment`) fulldeep tahlil qilindi, 8 ta noodatiy yechim topildi.
- [x] **[2026-08-03 23:38]** `FULLDEEP-03` (`6_oy_imtihon`) birinchi urinishda repo klon buzilgan (barcha fayllar 0 bayt) ekani aniqlandi, natija bekor qilindi — shablonga klon-tekshiruv qadami qo'shilib qayta ishga tushirilmoqda.
- [x] **[2026-08-03 23:45]** `FULLDEEP-03` (`6_oy_imtihon`) fulldeep tahlil qilindi, 5 ta noodatiy yechim topildi.
- [x] **[2026-08-03 23:58]** `FULLDEEP-04` (`mini-erp`) fulldeep tahlil qilindi, 9 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:11]** `FULLDEEP-05` (`e-commerce`) fulldeep tahlil qilindi, 12 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:11]** `FULLDEEP-06` (`e-commerce-backend`) fulldeep tahlil qilindi, 9 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:14]** `FULLDEEP-07` (`crm_frontend`) fulldeep tahlil qilindi, 12 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:16]** `FULLDEEP-08` (`crm_backend`) fulldeep tahlil qilindi, 10 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:19]** `FULLDEEP-09` (`telegram_app_front_end`) fulldeep tahlil qilindi, 9 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:22]** `FULLDEEP-10` (`telegram_app_backend`) fulldeep tahlil qilindi, 10 ta noodatiy yechim topildi.
- [x] **[2026-08-03 00:25]** `FULLDEEP-11` (`online-courses`) fulldeep tahlil qilindi, 10 ta noodatiy yechim topildi.
- [x] **[2026-08-04 00:25]** `SYNTHESIS` bosqichi yakunlandi, 9 ta takrorlanuvchi va 15 ta noyob yechim aniqlandi.

---

## 🔬 2-BOSQICH: FULLDEEP TAHLIL (2026-08-03, Claude tomonidan boshlandi)

**Sabab:** Fayzillo yuqoridagi `TASK-01..08` hisobotlarini tekshirib chiqib, ularni **yetarli chuqur emas** deb topdi — har bir loyihada faqat 1 ta fayl ko'rilgan, faqat umumiy/takrorlanuvchi patternlar (`initGlobalApp` va h.k., bular allaqachon `principles.md`da bor) qayd etilgan. Aslida har loyihada 100+ noodatiy, o'ziga xos yechim bor deb baholanmoqda — bular hali hujjatlashtirilmagan.

**Yangi metodologiya:** Har loyihaning **barcha** source fayllari (node_modules/.git/dist chiqarib tashlab) fayl-fayl o'qiladi, faqat **noodatiy/custom** mantiqlar (oddiy CRUD/boilerplate emas) FACT→OBSERVATION→NEGA-ODATIY-EMAS formatida yoziladi. Ijrochi: `agy --print` (tez/arzon), Claude — tekshiruvchi/tasdiqlovchi (orcestor rolida).

**Roli taqsimoti (`new_fixing_orcestration_system/03-arxitektura-eskiz.md`ga muvofiq):** AGY — yozuvchi (fayl o'qiydi, hisobot yozadi, shu jadvalni yangilaydi). Claude — o'quvchi/tasdiqlovchi (har hisobotni sifat bo'yicha tekshiradi, keyingi taskni ishga tushiradi).

| Task ID | Loyiha | Fayl soni | Status | Natija Fayli |
|---|---|---|---|---|
| `FULLDEEP-01` | `Admin-panel` | 8 | ✅ Bajarildi | `reports_agy/fulldeep_01_admin_panel.md` |
| `FULLDEEP-02` | `StudentSYStemMenegment` | 9 | ✅ Bajarildi | `reports_agy/fulldeep_02_student_sys.md` |
| `FULLDEEP-03` | `6_oy_imtihon` | 13 | ✅ Bajarildi | `reports_agy/fulldeep_03_c_web_template.md` |
| `FULLDEEP-04` | `mini-erp` | 37 | ✅ Bajarildi | `reports_agy/fulldeep_04_mini_erp.md` |
| `FULLDEEP-05` | `e-commerce` (frontend) | 52 | ✅ Bajarildi | `reports_agy/fulldeep_05_ecommerce_frontend.md` |
| `FULLDEEP-06` | `e-commerce-backend` | 105 | ✅ Bajarildi | `reports_agy/fulldeep_06_ecommerce_backend.md` |
| `FULLDEEP-07` | `crm_frontend` | 73 | ✅ Bajarildi | `reports_agy/fulldeep_07_crm_frontend.md` |
| `FULLDEEP-08` | `crm_backend` | 123 | ✅ Bajarildi | `reports_agy/fulldeep_08_crm_backend.md` |
| `FULLDEEP-09` | `telegram_app_front_end` | 86 | ✅ Bajarildi | `reports_agy/fulldeep_09_telegram_frontend.md` |
| `FULLDEEP-10` | `telegram_app_backend` | 123 | ✅ Bajarildi | `reports_agy/fulldeep_10_telegram_backend.md` |
| `FULLDEEP-11` | `online-courses` | 154 | ✅ Bajarildi | `reports_agy/fulldeep_11_online_courses.md` |
| `SYNTHESIS` | Barcha 11 hisobot yakuniy sintezi | — | ✅ Bajarildi | `tasks/07_step_unusual_solutions_synthesis.md` |


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/restart-timing/examples.md`

# Examples — Restart timing

## Misol 1 (SKILL.md'dagi real o'lchov)

- **Kontekst**: SKILL.md o'z ichida real loyiha (`zdes_frontend`,
  2026-08-07) misolida "Messages ~27%" holatini keltiradi.
- **Izoh**: Bu qiymat mustaqil o'lchamda emas, balki SKILL.md matni
  o'zi buni "bu ko'rsatkich past bo'lishi kerak edi" degan ma'noda
  keltirgan — ya'ni 27% allaqachon "kech" chegarasiga yaqin misol
  sifatida qaraladi.

## Misol 2 (gipotetik)

- **Faraz**: Yangi checkpoint'da Messages ulushi 10% ko'rsatilgan, joriy
  sub_task hali tugallanmagan.
- **Kutilgan qaror**: Restart shart emas — sub_task tugagach yoki
  keyingi tabiiy to'xtash nuqtasida qayta baholanadi.


## Manba: `my_digital_brain/90_System/orcestor/resumer.md`

# RESUMER — Small Context Checkpoint

**O'qish tartibi:** Bu faylni o'qiganingdan keyin boshqa hech qanday eski suhbat tarixini so'rama — shu fayl + pastda ko'rsatilgan fayllar yetarli.

## Vazifa qisqacha
`repo_analiz/repos/` ichidagi loyihalarni **agy --print** orqali fayl-fayl chuqur tahlil qilib, Fayzillo yozgan **noodatiy/custom** yechimlarni (umumiy framework patternlari emas — ular `reports_agy/principles.md`da bor) topib, `reports_agy/fulldeep_NN_*.md` fayllariga yozish. Metodologiya: FACT → OBSERVATION → NEGA ODATIY EMAS, aniq fayl:qator bilan.

## Joriy holat
To'liq holat jadvali: **`orcestor/status.md`** ("🔬 2-BOSQICH: FULLDEEP TAHLIL" bo'limi) — u yerda qaysi `FULLDEEP-XX` tasklar ✅ Bajarildi, qaysilari ⏳ Navbatda ekani bor. Shuni o'qi va birinchi ⏳ Navbatda qatorni top.

**LOYIHA TO'LIQ YAKUNLANDI (2026-08-04).** Barcha `FULLDEEP-01`..`FULLDEEP-11` (11 ta loyiha, 101 ta noodatiy yechim) va `SYNTHESIS` bosqichi (`tasks/07_step_unusual_solutions_synthesis.md` — 9 ta takrorlanuvchi + 15 ta noyob yechim, statistika bilan) ✅ Bajarildi. `status.md`da barcha qatorlar tasdiqlangan. Keyingi safar bu faylni ochsang, qo'shimcha ish yo'q — faqat natijalarni ko'rib chiqish yoki yangi bosqich (masalan yana bir repo qo'shish) kerak bo'lsa davom ettiriladi.

**Yangi ish rejimi (Fayzillo tasdiqlagan, 2026-08-04):** agy'da 1 yillik Pro obuna (sovg'a, marjinal narxsiz) bor, shuning uchun tasklar navbat bilan emas — **doim 2 tasi parallel fon rejimida (`run_in_background:true`)** ishlaydi. Bittasi tugab, hisoboti sifat bo'yicha tasdiqlangach, navbatdagi bitta task darhol fonga tashlanadi (juftlik kutilmaydi) — shu tariqa 2 slot doim to'liq turadi. `status.md`ga concurrent yozish xavfi bor (ikkita agy jarayoni bir vaqtda faylni tahrirlashi mumkin) — shuning uchun har safar tugagan taskdan keyin `status.md` qo'lda tekshiriladi, mos yozuv yo'q bo'lsa qo'lda tuzatiladi.

**Muhim texnik tuzatish:** Original skriptdagi outer `timeout 300` (5 daqiqa) hardcoded edi — bu 40+ fayllik tasklar uchun (8-12 daqiqa kerak) muddatidan oldin o'ldirib qo'yardi. Endi outer timeout har task uchun dinamik hisoblanadi: TIMEOUT (agy --print-timeout) + ~2 daqiqa buffer, sekundlarda (`<40 fayl→240s/300s outer`, `40-100→480s/600s outer`, `100+→720s/840s outer`).

Sifat nazorati: FULLDEEP-01..10 barchasida matn tozalandi — takrorlanuvchi xato turi: agy ba'zan "to'g'ridan-to'g'ri" so'zi o'rniga uydirma so'z qo'shib yuboradi (masalan "to'g'ridan-to mezon", "to'g'ridan-to'g me'yorida", "bo'laklarga bo mezon", "bo me'yorida" — FULLDEEP-03,05,08,10'da uchradi). Har hisobotni o'qib, shunga o'xshash nuqsonlarga ko'z yugurtir va qo'lda tuzat.

**MUHIM — klon xatosi topildi va tuzatildi (2026-08-03):** `FULLDEEP-03` birinchi urinishda `repos/6_oy_imtihon/` papkasi butunlay 0 baytli (909 ta bo'sh fayl, buzilgan `.git`) ekanini aniqladi — bu chala/uzilib qolgan klon edi. Shundan keyin `fulldeep_prompt_template.txt` ga **0-QADAM** qo'shildi: endi agy har taskda avval loyihaning klon holatini tekshiradi, buzilgan bo'lsa avtomatik ravishda `.git/config`dagi URL orqali qayta klon qiladi (eski papkani `*.broken_<vaqt>` deb saqlab, o'chirmasdan). Bu allaqachon shablon ichida — keyingi tasklarda alohida eslatishga hojat yo'q. Eski buzilgan nusxa `repos/6_oy_imtihon.broken_20260803_2344/` da saqlanmoqda (18MB) — kerak bo'lmasa keyinroq o'chirish mumkin, hozircha tegilmadi.

**Model fallback qo'shildi:** Ijro buyrug'i endi bir nechta modelni (default → `claude-sonnet-4-6` → `claude-opus-4-6-thinking` → `gemini-3.1-pro-high` → `gemini-3.6-flash-high`) navbat bilan sinaydi — agar chiqishda `quota`/`rate limit`/`429`/`resource exhausted` so'zlari uchrasa, avtomatik keyingi modelga o'tadi.

## Keyingi qadam — aynan shu buyruqni bajar

**Muhim eslatma (har safar):** Shablon (`fulldeep_prompt_template.txt`) ichida endi 0-QADAM bor — agy tahlildan oldin loyihaning git klon holatini (0 baytli/buzilgan fayllar) tekshiradi va kerak bo'lsa o'zi qayta klon qiladi. Buyruq alohida "ogohlantirish" qo'shishga hojat yo'q, shablon o'zi buni qamrab oladi — faqat shablonni o'zgartirmasdan ishlat.

**Model fallback (quota tugasa):** Quyidagi ro'yxatdagi modellarni navbat bilan sinab ko'r. Agar chiqishda `quota`, `rate limit`, `429`, `resource exhausted` kabi so'zlar (case-insensitive) uchrasa — o'sha model kvotasi tugagan, keyingi modelga o't va shu vazifani qayta boshidan ishga tushir.

```bash
cd /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz
TPL=orcestor/fulldeep_prompt_template.txt
# status.md dagi keyingi ⏳ Navbatda qatordan PROJECT / REPORT_FILE / TASK_ID ni ol:
PROMPT=$(sed -e "s/__PROJECT__/<PROJECT_NOMI>/g" -e "s/__REPORT_FILE__/<REPORT_FAYL_NOMI>/g" -e "s/__TASK_ID__/<TASK_ID>/g" "$TPL")
# Fayl soniga qarab timeout tanla: <40 fayl -> 4m0s, 40-100 -> 8m0s, 100+ -> 12m0s
TIMEOUT=4m0s
MODELS=("" "claude-sonnet-4-6" "claude-opus-4-6-thinking" "gemini-3.1-pro-high" "gemini-3.6-flash-high")
for M in "${MODELS[@]}"; do
  if [ -z "$M" ]; then
    OUT=$(timeout 300 agy --print "$PROMPT" --print-timeout "$TIMEOUT" --dangerously-skip-permissions 2>&1)
  else
    echo ">>> Model: $M bilan sinalmoqda"
    OUT=$(timeout 300 agy --print "$PROMPT" --model "$M" --print-timeout "$TIMEOUT" --dangerously-skip-permissions 2>&1)
  fi
  echo "$OUT" | tail -80
  if echo "$OUT" | grep -qiE "quota|rate.?limit|429|resource.?exhausted"; then
    echo ">>> Kvota tugadi, keyingi modelga o'tilmoqda..."
    continue
  fi
  break
done
```

Bajargandan keyin:
1. Yozilgan `reports_agy/fulldeep_NN_*.md` faylini o'qi, sifatini tekshir (haqiqiy fayl:qator bor-yo'qligi, mazmunsiz so'z yo'qligi, klon-xatosi ogohlantirishi yo'qligi).
2. Agar hisobotda "OGOHLANTIRISH: ... klon xatosi tuzatilmadi" bo'lsa — bu taskni ⏳ holida qoldir (keyinroq qo'lda hal qilish kerak), keyingi navbatdagi taskka o'tma, foydalanuvchiga xabar ber.
3. `orcestor/status.md` avtomatik yangilangan bo'lishi kerak (agy o'zi yozadi) — tekshir, yangilanmagan bo'lsa qo'lda yangila.
4. Shu `resumer.md` faylini yangi holatga mos yangila (bajarilgan task ID'ni qo'shib, keyingi navbatdagi taskni ko'rsatib) — foydalanuvchi yana `/clear` qilib davom ettirishi mumkin.

## Navbat tartibi (status.md bilan bir xil, mos kelishi kerak)
FULLDEEP-03 `6_oy_imtihon` → FULLDEEP-04 `mini-erp` → FULLDEEP-05 `e-commerce` (frontend) → FULLDEEP-06 `e-commerce-backend` → FULLDEEP-07 `crm_frontend` → FULLDEEP-08 `crm_backend` → FULLDEEP-09 `telegram_app_front_end` → FULLDEEP-10 `telegram_app_backend` → FULLDEEP-11 `online-courses` → **SYNTHESIS**.

## SYNTHESIS bosqichi (barcha 11 ta FULLDEEP tugagach)
Barcha `reports_agy/fulldeep_*.md` fayllarni o'qib, `tasks/07_step_unusual_solutions_synthesis.md` yoz — `principles.md`dagi umumiy patternlarni takrorlamasdan, loyihalar kesimida qaytarilgan yoki eng noyob noodatiy yechimlarni sintez qil (mavjud `tasks/0X_step_*.md` fayllar formatiga mos, o'zbek tilida).

## Standing rules (qisqa eslatma — to'liqi Claude memory'da bor)
Fayzillo bilan: o'zbek tilida, lo'nda/tizimli javob, taxmin qilmasdan fayl o'qib ish qil, git status tekshirmasdan fayl o'chirma, RAM ~5.7GB cheklovini hisobga ol.


## Manba: `my_digital_brain/90_System/claude_tasks/new_fixing_orcestration_system/05-use-caselar.md`

# 5. Use case'lar

Reja mavhum qolmasligi uchun — hozir mavjud, real vaziyatlarga bog'langan
qo'llanish holatlari.

## UC1 — Orcestor'ning 4 nusxasini birlashtirish

Tizimning **birinchi haqiqiy sinov maydoni** shu bo'ladi: `zdes-backend`,
`zdes-frontend`, `zdes-frontend/Gpt_task`, `zdes/orcestor` — to'rttasidagi
`requirements.MD`/`prompt.md` farqlarini solishtirib, standing-rules
jadvaliga bitta `topic="orcestor-standard"` sifatida kiritish. Muvaffaqiyat
mezoni: to'rtta nusxa o'rniga bitta schema, boshqa loyihalar shundan meros
oladi.

## UC2 — zdes Faza 2 davomida sessiya uzilishi

`zdes/orcestor/README.MD`da yozilganidek, Faza 2 (frontend integratsiya)
hozir alohida, parallel sessiya sifatida davom etmoqda. Agar bu sessiya
o'rtada uzilib qolsa (yoki 5-prompt chegarasiga yetib `/clear` bo'lsa),
keyingi sessiya to'liq `tasklist.md` + `backend_crud_review/*.md`ni qayta
o'qimasdan, faqat oxirgi checkpoint + tegishli standing rule'lar bilan
davom etishi kerak.

## UC3 — Uzun status.md fayllarini checkpoint formatiga siqish

`github-backup/status.md` yonida 3 ta `.err*` fayl bor — bu aslida
muvaffaqiyatsiz urinishlarning xom logi, hech qachon tozalanmagan. Yangi
tizimda bunday xom loglar DB'ga kirmaydi — faqat AGY/Claude tomonidan
**xulosalangan** checkpoint kiradi (xom log fayl darajasida qolishi mumkin,
lekin context-reload'ga tushmaydi).

## UC4 — Yangi loyiha ochilganda qoidalarni avtomatik yuklash

Hozir har yangi sessiyada `backup-plan/overview.md`dagi "Muhim qoidalar"
bo'limini (masalan git account qoidalari, qaysi papkalarga tegilmasligi)
qo'lda o'qish kerak. Standing-rules jadvali bo'lsa, `project="backup-plan"`
bo'yicha bitta so'rov shu qoidalarni to'liq, qisqa holda qaytaradi —
bir necha yuz qatorlik faylni to'liq o'qish shart bo'lmaydi.

## UC5 — Token sarfi taqsimotini keyingi haftada qayta o'lchash

Joriy holat (1.3-bo'lim): 80% context-load. Tizim qurilgach, xuddi shu
o'lchov (session boshiga sarflangan token, foizga bo'lib) qayta olinadi —
bu rejaning **muvaffaqiyat mezoni**: agar context-load ulushi sezilarli
pasaymasa, arxitektura noto'g'ri deb topiladi va 4-fayldagi taxminlar
qayta ko'riladi.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/blocker-va-subtask/examples.md`

# Examples — Blocker/sub_task

## Misol 1 (foydalanuvchi tavsifi asosida)

- **Kontekst**: "Orcestoration ishga tushganda oldin holat o'rganib
  chiqilib, keyin tasklar shakllantiriladi. Bitta majburiy qoida: agar
  asosiy tasklarni bajarish jarayonida biror to'siq chiqsa, sub_tasks/
  tasklar ochiladi — vaziyatga qarab parallel yoki avval sub_task, keyin
  asosiy tasklar."
- **Izoh**: Bu — real amaliyotda qo'llanilayotgan qoida, lekin hozircha
  SKILL.md matnida yozilmagan (faqat `sub_tasks/` papka boshqa maqsadda —
  audit jurnali sifatida — tilga olingan). Bu paket shu bo'shliqni
  to'ldirish uchun tuzilgan.

## Misol 2 (foydalanuvchi tavsifi asosida — davom etish qarori)

- **Kontekst**: "Holatga qarab, contextda hali limit ko'p bo'lsa asosiy
  task bajarish mumkin."
- **Izoh**: Bu qoida-daraxtining 2-qadamiga (Sub_task tugagach — davom
  etish yo'li) to'g'ridan-to'g'ri asos bo'ldi. SKILL.md'dagi mavjud
  restart-o'lchov mexanizmi (`/context`, Messages ulushi) shu qarorni
  amalga oshirish uchun tayyor vosita sifatida ishlatilishi mumkin.

## Misol 3 (gipotetik)

- **Faraz**: Backend loyihada bitta asosiy task davomida uchta mustaqil
  kichik xato topildi — birortasi boshqasiga bog'liq emas.
- **Kutilgan qo'llanish**: Uchalasi ham parallel sub_task sifatida
  ochiladi, har biri alohida yakunlanadi, keyin asosiy task ularning
  natijasidan mustaqil ravishda davom etadi (chunki ular asosiy taskka
  kirish sifatida kerak emas edi, faqat yon-effekt sifatida topilgan).


## Manba: `my_digital_brain/10_Projects/orcestor-skill/templates/task_template.md`

# Task Shablon

## Sarlavha: [Task Nomi]
- **Status**: TODO | PENDING | COMPLETED
- **Yaratilgan sana**: YYYY-MM-DD
- **Tegishli modul / loyiha**: [Modul nomi]

### Tavsif
[Vazifa bo'yicha qisqacha ma'lumot va kutilayotgan natija]

### Qabul Qilish Mezonlari (Acceptance Criteria)
- [ ] Mezon 1
- [ ] Mezon 2
- [ ] Mezon 3

### Sinab Ko'rilgan va Rad Etilgan Gipotezalar (agar bo'lsa)
- ❌ [Gipoteza 1]: [Nega ishlamaganligi sababi]


## Manba: `zdes_archive_docs/raw_history/orcestor/prompt_analysis.md`

# AGY uchun Backend Tahlil Topshiriq Shabloni (Analysis Prompt Template)

`zdes/orcestor/` tizimining **1-fazasi**: `zdes_backend`ni modul-modul
tahlil qilib, `backend_crud_review/<modul>.md` fayllariga yozib borish.
Bu fayllar keyinchalik 2-faza (frontend API ulash, `prompt.md`) uchun
**yagona ishonchli manba** bo'ladi — shuning uchun bu shablon boshqasidan
qattiqroq, aniqroq va tekshiriladigan qilib yozilgan.

**Nega alohida shablon:** bu fazada AGY'ga `zdes_backend`ni **o'qish**
uchun workspace ruxsati beriladi (`--add-dir zdes_backend --add-dir
backend_crud_review`) — bu yagona holat, qachonki AGY backend papkasini
ko'radi. AGY hech qachon bu fazada `test-zdes-front`ni ko'rmaydi va
`zdes_backend` ichiga bironta baytni ham yozmaydi (faqat o'qiydi).

---

## 0. Muhim tamoyil — gallyutsinatsiyaga qarshi qat'iy qoida

Fayzillo (2026-07-25): **"AGY ko'p xato qiladi — promt mukammal
bo'lishi kerak."** Shu sababli har bir analysis-task quyidagi qoidalarga
**so'zma-so'z** rioya qiladi (task matnida ham aynan shu jumlalar
takrorlanadi):

1. Har bir maydon/tip/dekorator **haqiqiy fayldan aynan ko'chiriladi**
   (nusxa ko'chirish, taxmin qilish emas). Fayl nomini o'zgartirmang,
   qisqartirmang.
2. Agar biror bo'lim mavjud bo'lmasa (masalan endpoint `@Public()` bo'lib,
   Guard yo'q), shu holat **aniq va ochiq yoziladi** ("Guard: yo'q — @Public()
   endpoint"), bo'sh qoldirilmaydi va o'ylab topilmaydi.
3. Controller'dagi **HAR BIR** endpoint (route handler metodi) tahlil
   qilinishi shart — birortasi ham o'tkazib yuborilmaydi. Task matnida
   endpointlar soni oldindan aniq ko'rsatiladi (masalan "4 ta endpoint:
   login, refresh, logout, me") — chiqish fayli aynan shuncha bo'lim
   o'z ichiga olishi shart.
4. Faqat **o'qish** — `zdes_backend` ichida birorta ham fayl
   yaratilmaydi/o'zgartirilmaydi/o'chirilmaydi. Chiqish FAQAT
   `backend_crud_review/<modul>.md`ga yoziladi.
5. **Global API prefiks doim `/api/v1` — HECH QACHON tashlab
   ketilmasin.** `zdes_backend/src/main.ts`da `app.setGlobalPrefix('api/v1')`
   o'rnatilgan — bu `@Controller('...')` dekoratoridagi yo'lga QO'SHIMCHA,
   controller faylida ko'rinmaydi. Har bir "Point" yo'li shu prefiks bilan
   boshlanishi SHART (masalan `@Controller('employee-leaves')` +
   `@Post()` → yo'l `/api/v1/employee-leaves`, `/employee-leaves` EMAS).
   Bu qoida bir marta buzilgan (employee-leave modulida prefiks butunlay
   tashlab ketilgan) — shuning uchun endi bu yerda aynan yozilgan.

---

## 1. Shablon (nusxa ko'chirish uchun)

```markdown
## Task ID: {{TASK_ID}} (Analysis — Faza 1)
### Sarlavha: {{MODULE_NAME}} modulini backend tahlili

**Maqsad (Goal):**
`zdes_backend/src/modules/{{MODULE_PATH}}` controller'idagi
**{{ENDPOINT_COUNT}} ta endpoint**ning har birini quyidagi 8 bo'limli
strukturada tahlil qilib, `backend_crud_review/{{MODULE_FILE}}.md`
fayliga yozish.

**O'qiladigan fayllar (read-only, faqat shular o'qiladi):**
{{SOURCE_FILES}}

**Cheklovlar (Constraints):**
- FAQAT o'qing. `zdes_backend/` ichida hech qanday fayl
  yaratmang/o'zgartirmang/o'chirmang — buzilsa task avtomatik
  REJECTED bo'ladi.
- Chiqish FAQAT bitta fayl: `backend_crud_review/{{MODULE_FILE}}.md`.
  Boshqa hech qanday fayl (skript, json, vaqtinchalik fayl) yaratmang.
- Har bir maydonni haqiqiy fayldan ko'chiring — taxmin qilmang,
  "odatda shunday bo'ladi" deb yozmang.
- {{ENDPOINT_COUNT}} ta endpointning barchasi tahlil qilinishi shart —
  birortasi ham tashlab ketilmasin.

**Har bir endpoint uchun MAJBURIY 8 bo'lim (aynan shu tartibda,
aynan shu sarlavhalar bilan):**

~~~
### Endpoint: <HTTP_METHOD> /api/v1/<to'liq yo'l>
**Controller:** <fayl yo'li>:<metod nomi>

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l (masalan `POST /api/v1/auth/login`)
- Controller class + method nomi

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- DTO maydonlaridagi `@ApiProperty({ example: ... })` /
  `@ApiPropertyOptional({ example: ... })` (yoki controller darajasidagi
  `@ApiBody(...)`) qiymatlarini **aynan shu ko'rinishda** ko'chiring —
  har bir maydon uchun alohida qator: `maydon: misol qiymat`.
- Agar biror maydonda `example` ko'rsatilmagan bo'lsa, "misol yo'q" deb
  aniq yozing — o'zingiz misol o'ylab topmang.
- Agar endpoint umuman body qabul qilmasa (masalan `GET`), "Body yo'q"
  deb yozing.
- **Nega kerak:** bu qiymatlar Faza 2da frontend forma
  `placeholder`/namuna matni sifatida ishlatiladi — shuning uchun
  aniqlik juda muhim.

**3. Guard:**
- Qo'llangan guard'lar (`@UseGuards(...)`, class-darajasidagi va
  metod-darajasidagi) yoki `@Public()` bo'lsa shu aniq yozilsin
- `@Roles(...)` bo'lsa — qaysi rollar ruxsat etilgan

**4. DTO:**
- Request DTO class nomi + fayl yo'li
- Har bir maydon: nomi, tipi, validation dekoratorlari
  (`@IsString()`, `@IsOptional()`, va h.k.) — aynan fayldagidek

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li
- 1-2 gapli mantiq tavsifi (nima qiladi, qaysi jadvallarga
  yozadi/o'qiydi, qanday side-effect bor — masalan token yaratish,
  notification yuborish)

**6. Response:**
- Qaytariladigan javob shakli — aniq maydon nomlari + tiplar
- Agar paginatsiya bo'lsa (`{items, meta}` yoki shunga o'xshash) —
  aniq ko'rsatilsin, oddiy massiv bilan aralashtirilmasin

**7. Error case:**
- Qaysi exception'lar tashlanishi mumkin (`NotFoundException`,
  `ForbiddenException`, `ConflictException`, `BadRequestException`
  va h.k.) + qaysi shart bajarilmasa shu xato chiqadi + HTTP status

**8. DB struktura:**
- Tegishli Prisma model(lar) nomi (`prisma/schema.prisma`dan).
- Shu endpoint o'qiydigan/yozadigan **har bir maydon uchun to'liq
  ustun ta'rifi**, aynan `schema.prisma`dagidek — quyidagilarning
  BARCHASI ko'rsatilishi shart, birortasi ham tashlab ketilmasin:
  - Prisma tipi (`String`, `Int`, `Boolean`, `DateTime`, `Decimal`, enum
    nomi va h.k.)
  - Majburiy/ixtiyoriy (`?` bor-yo'qligi)
  - `@default(...)` qiymati (bo'lsa)
  - `@unique` yoki `@@unique([...])` ichida ishtirok etishi (bo'lsa)
  - `@db.*` annotatsiyasi (masalan `@db.VarChar(255)`, `@db.Uuid`) —
    bo'lsa aynan ko'chiring
- **Relations / references (eng muhim, tashlab ketilmasin) — IKKALA
  YO'NALISH ham kerak:**
  1. **Chiquvchi (bu model → boshqa model):** har bir `@relation(...)`
     uchun alohida qator — bog'langan model nomi, FK maydon nomi
     (`fields: [...]`), qaysi maydonga bog'lanadi (`references: [...]`),
     va `onDelete` xatti-harakati. Masalan:
     `RefreshToken.userId -> User.id (onDelete: Cascade)`.
  2. **Kiruvchi (boshqa modellar → bu model) — ayniqsa DELETE
     endpoint uchun MAJBURIY:** `schema.prisma` bo'yicha shu modelga
     ishora qiluvchi BOSHQA barcha modellarni toping (masalan
     `grep -n "<model>Id"` uslubida qidiring) va har birini alohida
     qator qilib yozing — bu o'chirilganda nima bo'lishini (cascade
     o'chadimi, yoki faqat FK NULL bo'ladimi) ko'rsatadi. Masalan
     `Company` o'chirilsa: `Branch.companyId -> Company.id (onDelete:
     Cascade)`, ..., `User.companyId -> Company.id (onDelete:
     SetNull)`. Bitta ham qoldirmang — bu ro'yxat to'liqsiz bo'lsa,
     Faza 2da noto'g'ri "xavfsiz o'chirish" taxmin qilinishi mumkin.
- Tegishli `@@index([...])`/`@@unique([...])` (model darajasidagi,
  agar shu endpoint mantig'iga aloqador bo'lsa — masalan qidiruv/filter
  shu indeksga tayansa).
- **Nega bunchalik batafsil kerak:** bu ma'lumot Faza 2da frontend
  formalarni (majburiy/ixtiyoriy maydon, select-dropdown uchun qaysi
  boshqa modelga bog'liqligini) to'g'ri qurish uchun ishlatiladi —
  yuzaki ("bu yerda User modeli bor" kabi) yozuv YETARLI EMAS.
~~~

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `backend_crud_review/{{MODULE_FILE}}.md` yaratilgan, {{ENDPOINT_COUNT}}
  ta endpoint bo'limi bor (kam emas, ko'p emas).
- Har bir bo'lim yuqoridagi 8 qismning barchasini o'z ichiga oladi.
- "8. DB struktura" bo'limida har bir maydonning Prisma tipi +
  majburiy/ixtiyoriy holati ko'rsatilgan, VA agar model boshqa modelga
  `@relation` orqali bog'langan bo'lsa — bu bog'lanish (FK maydon,
  qaysi modelga, `onDelete`) alohida aniq yozilgan (yuzaki "tegishli
  model — User" kabi yozuv YETARLI EMAS, NEEDS_REVISION sabab bo'ladi).
- `zdes_backend/` ichida `git status` bo'yicha HECH QANDAY o'zgarish yo'q
  (Claude Code bu narsani dispatch tugagach alohida tekshiradi).

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven (read-heavy, lekin faqat bitta yozish maqsadi bor).

**Natijani qayerga yozish kerak (Report back):**
- Jarayonni `orcestor/task_pending/{{TASK_ID}}-response.md`ga yozib
  boring (qaysi fayllarni o'qidingiz, qanday qarorlar qabul qildingiz).
- Tugagach, yakuniy xulosa + "Tahlil qilingan endpointlar" ro'yxatini
  qo'shing (nechta endpoint, ularning yo'llari).
- **Fayllarni o'zingiz ko'chirmang.** `{{TASK_ID}}.md` va
  `{{TASK_ID}}-response.md` `task_pending/`da qoladi — Claude Code
  tahlilni tekshirib bo'lgach, o'zi `task_compliete/`ga ko'chiradi
  (`dispatch.py complete`). Sizning vazifangiz faqat response.md yozish
  bilan tugaydi.
```

---

## 2. Dispatch qanday bajariladi (Claude Code uchun eslatma)

```
agy --print "<task matni>" \
    --add-dir /home/fayzillo/Desktop/zdes/zdes_backend \
    --add-dir /home/fayzillo/Desktop/zdes/backend_crud_review \
    --add-dir /home/fayzillo/Desktop/zdes/orcestor \
    --mode accept-edits --dangerously-skip-permissions \
    --model gemini-3.1-pro-low --print-timeout 15m
```

`orcestor/` qo'shiladi FAQAT `task_pending/{{TASK_ID}}-response.md`
yozishi uchun (report-back majburiyati). `test-zdes-front` bu fazada
`--add-dir`ga HECH QACHON qo'shilmaydi.

**Dispatchdan keyin Claude Code MAJBURIY tekshiradi:**
1. `cd zdes_backend && git status --porcelain` — bo'sh bo'lishi shart.
   Bo'sh bo'lmasa: darhol `git checkout -- <fayl>` bilan qaytariladi,
   task `NEEDS_REVISION` deb belgilanadi, sabab status logga yoziladi.
2. `backend_crud_review/<modul>.md` ochilib, kamida 2-3 ta endpoint
   bo'limi tasodifiy tanlanib, haqiqiy controller/DTO/service fayli bilan
   qator-qator solishtiriladi (`requirements.MD` 7-bo'lim — API-bog'liq
   ishlarda qat'iy tekshirish).
3. Endpoint soni controller'dagi haqiqiy route handler soniga mos
   kelishi tekshiriladi (`grep -E "@(Get|Post|Patch|Put|Delete)\("`).

---

## 3. Maydonlar tavsifi

| Maydon | Tavsif |
|---|---|
| `{{TASK_ID}}` | `B-A-<MODUL>` (masalan `B-A-AUTH`) |
| `{{MODULE_NAME}}` | Inson o'qiydigan nom (masalan "Auth") |
| `{{MODULE_PATH}}` | `zdes_backend/src/modules/` ostidagi papka nomi (masalan `auth`) |
| `{{MODULE_FILE}}` | Chiqish fayl nomi, kengaytmasiz (masalan `auth`) |
| `{{ENDPOINT_COUNT}}` | Oldindan `grep` bilan sanalgan aniq raqam |
| `{{SOURCE_FILES}}` | Controller/service/dto/interfeys fayllarining to'liq ro'yxati (aniq yo'llar) |


## Manba: `my_digital_brain/10_Projects/tasks/Tasks_MOC.md`

# 📋 Roadmap va Tasklar (MOC)
Barcha amaliy vazifalar va sintez fayllari:
- [[06_step_foundation_lessons_topics]]
- [[00_rules_and_roadmap]]
- [[07_step_unusual_solutions_synthesis]]
- [[03_step_data_and_state_logic]]
- [[01_step_code_architecture]]
- [[04_step_chronological_growth_summary]]
- [[02_step_custom_business_logic]]
- [[05_step_curriculum_topics_list]]
- [[obsidian_boglanishlarni_organish]]


## Manba: `zdes_archive_docs/raw_history/orcestor/steps/README.md`

# Orkestratsiya oqimi bosqichlari

Bu papka vazifaning boshidan oxirigacha (Claude Code → AGY → Claude Code) qanday harakatlanishini tavsiflaydi.

1. [01-intake.md](./01-intake.md) — Claude Code ishni aniqlaydi va vazifa faylini `tasks/` ga yaratadi.
2. [02-dispatch.md](./02-dispatch.md) — Claude Code promptni to'ldirib, vazifani `task_pending/` ga jo'natadi.
3. [03-execution.md](./03-execution.md) — Fayzillo promptni Antigravity'ga joylashtiradi, AGY vazifani bajaradi.
4. [04-review.md](./04-review.md) — Fayzillo AGY natijasini tekshiradi va loyihaga kiritadi.
5. [05-integration.md](./05-integration.md) — Claude Code natijani kodbazaga integratsiya qilib, statusni yangilaydi.
6. [06-logging.md](./06-logging.md) — Asosiy natijalar `history/` (va zarur bo'lsa loyiha darajasidagi jurnalga) yoziladi.


## Manba: `zdes_archive_docs/raw_history/orcestor/steps/02-dispatch.md`

# 2-bosqich: Dispatch (Vazifani jo'natishga tayyorlash)

**Maqsad:** Claude Code tanlangan vazifani AGY uchun ijro etiladigan promptga aylantiradi va uni navbatga qo'yadi.

**Mas'ul:** Claude Code (Orchestrator)

**Kirish (Input):**
- `orcestor/tasks/` dagi vazifa fayli
- `orcestor/prompt.md` shabloni

**Chiqish (Output):**
- To'ldirilgan prompt (vazifa tafsilotlari bilan)
- Vazifa fayli `orcestor/task_pending/` papkasiga ko'chirilgan/nusxalangan
- Fayzillo'ga xabar: prompt tayyor, Antigravity'ga relay qilish kerak

**Done when:**
Vazifa `orcestor/task_pending/` da joylashgan, to'ldirilgan prompt Fayzillo'ga uzatishga tayyor holda taqdim etilgan.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/blocker-va-subtask/vaziyat.md`

# Vaziyat — Nega blocker/sub_task uchun yagona qoida yo'q

## Muammo

Asosiy task davomida to'siq chiqqanda, ikkita savol bir vaqtda hal
qilinishi kerak:

1. **Sub_task qanday tuzilsin** — parallel (bir nechta mustaqil sub_task
   bir vaqtda) yoki ketma-ket (avval sub_task, keyin asosiy task)?
2. **Sub_task tugagach nima bo'ladi** — asosiy task xuddi shu sessiyada
   davom etadimi, yoki checkpoint yozib restart kerakmi?

## Nega bitta qattiq qoida ishlamaydi

- **Loyiha turi farq qiladi**: frontend loyihada blocker ko'pincha UI
  komponent bog'liqligi (masalan avval dizayn-token aniqlanishi kerak),
  backend loyihada esa ko'pincha ma'lumotlar sxemasi yoki API kontrakti.
  Bu ikki holat butunlay boshqa sub_task formatini talab qiladi.
- **Bog'liqlik xarakteri farq qiladi**: ba'zi to'siqlar mustaqil (bir
  nechtasi bir vaqtda hal qilinishi mumkin — parallel), ba'zilari esa
  ketma-ket (sub_task natijasi asosiy taskka kirish sifatida kerak).
- **Resurs holati farq qiladi**: context/token limiti hali keng bo'lsa,
  sub_task tugagach asosiy taskka bir xil sessiyada qaytish mumkin;
  limit torlashgan bo'lsa, checkpoint + restart kerak bo'ladi.

Shuning uchun bu qaror **SKILL.md darajasida qattiq qoida emas**, balki
har loyihada Supervisor_User + Orcestor_Agent muhokamasi orqali
(`orcestor/memory/*.md` yoki `standing_rules.json`ga yozilgan holda)
shakllanadi.


## Manba: `my_digital_brain/90_System/orcestor/fulldeep_prompt_template.txt`

Sen repo_analiz loyihasida ishlayapsan. Ish papkasi: /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/

0-QADAM (MAJBURIY, tahlildan oldin — klon xatosini tekshirish):
Ba'zi `repos/*` loyihalari GitHub'dan klonlanganda chala/buzilgan holda qolgan — fayl-papka tuzilmasi bor, lekin fayllar 0 baytli (bo'sh). Tahlilni boshlashdan oldin buni tekshir:
1. `repos/__PROJECT__/` ichidagi asosiy source fayllardan bir nechtasini (masalan eng katta fayl yoki `src/` ichidagilar) ko'r — agar ular 0 baytli bo'lsa, bu klon xatosi belgisi.
2. Buni tasdiqlash uchun `cd repos/__PROJECT__ && git log --oneline -5` va `git log -1 --stat` ishlat — agar "bad object" yoki "unknown revision"/HEAD topilmasa yoki fayllar statda 0 bayt ko'rsatilsa, klon buzilgan.
3. Klon buzilgan bo'lsa: `repos/__PROJECT__/.git/config`dagi `url = ...`ni o'qi, keyin loyiha papkasini `repos/__PROJECT__.broken_<vaqt>` nomiga ko'chir (o'chirma!) va o'sha URL'dan `git clone <url> repos/__PROJECT__` orqali qayta klon qil.
4. Qayta klondan keyin fayllar haqiqatan mazmunli (0 baytdan katta) ekanini tekshir va shundan keyingina pastdagi tahlilni boshla.
5. Agar qayta klon ham muvaffaqiyatsiz bo'lsa (tarmoq yo'q, repo topilmadi va h.k.), tahlilni to'xtat va natija faylida faqat shuni yoz: "## OGOHLANTIRISH: `__PROJECT__` repo klon xatosi tuzatilmadi — tahlil bajarilmadi. Sabab: <aniq xato>." — bunday holda status.md dagi __TASK_ID__ qatorini "✅ Bajarildi" emas, "⚠️ Klon xatosi" deb belgila va pastdagi 3-11 qadamlarni bajarma.

VAZIFA: /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/repos/__PROJECT__/ papkasidagi loyihani TO'LIQ, fayl-fayl bo'yicha chuqur tahlil qil.

MUHIM CHEKLOV: Bu ishni avvalgi (shu loyihada allaqachon mavjud) tahlildan FARQLI qil. Avvalgi tahlil har loyihada faqat 1 ta faylni ko'rib, umumiy/takrorlanuvchi framework patternlarini (masalan initGlobalApp, standart middleware ulash, oddiy CRUD) qayd etgan edi — bular allaqachon /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/principles.md faylida hujjatlashtirilgan. SEN ULARNI QAYTARMA.

Sen faqat dasturchi (Fayzillo)ning NOODATIY, CUSTOM, standart bo'lmagan yechimlarini, algoritmlarini va o'ziga xos biznes mantiqlarini qidirasan — ya'ni boshqa o'quvchi/frameworkning odatiy yo'lidan (boilerplate, andozaviy CRUD, kutubxonaning standart usuli) chetga chiqqan joylarni.

QOIDALAR:
1. node_modules, .git, dist, build, vendor, package-lock.json, va rasm/font fayllarni o'tkazib yubor.
2. Loyihadagi BARCHA qolgan source fayllarni (controller, service, model/schema, util, middleware, config, custom script, HTML/CSS/JS/C/frontend komponent - qaysi til bo'lishidan qat'iy nazar) birma-bir o'q.
3. Har bir topilgan noodatiy yechim uchun quyidagi formatda yoz:
   #### FACT
   - Fayl: `nisbiy/yo'l/fayl.ext` (qator raqami bilan)
   - Kod parchasi (qisqa, faqat muhim qismi)
   #### OBSERVATION
   - Bu yerda nima qilinayotgani (mexanizm)
   #### NEGA ODATIY EMAS
   - Bu nima uchun standart/boilerplate yechim emas — muqobil (odatiy) yondashuv nima bo'lardi va bu nimasi bilan farq qiladi.
4. Agar biror fayl to'liq boilerplate/andozaviy bo'lsa (masalan bo'sh CRUD, standart routing), uni ATLAB O'T — faqat DIQQATGA SAZOVOR narsalarni yoz. Miqdor emas, sifat va haqiqiylik muhim.
5. Hech qanday narsani o'ylab topma (no hallucination) — faqat haqiqatda o'qigan kodingga asoslan, aniq fayl va qator ko'rsat.
6. Hujjatni yozib bo'lgach, uni oxirigacha qayta o'qib chiq va matnda mazmunsiz/tasodifiy so'z yoki uzilib qolgan jumlalar (masalan noto'g'ri joyga tushib qolgan so'z) bor-yo'qligini tekshir, topilsa darhol tuzat. Grammatik va mazmuniy aniqlik muhim.

NATIJA:
- Natijani /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/__REPORT_FILE__ fayliga yoz (o'zbek tilida, markdown, yuqoridagi format asosida).
- Hujjat boshida sarlavha + sana (2026-08-03) + qamrab olingan fayllar soni yoz.
- Hujjat oxirida qisqa xulosa yoz: nechta noodatiy yechim topilgani, va eng diqqatga sazovor 3 tasi qaysi ekani.
- Hujjatni yozib bo'lgach, /home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/orcestor/status.md faylini o'qi va undagi "__TASK_ID__" qatoridagi "⏳ Navbatda" holatini "✅ Bajarildi" ga o'zgartir (Edit orqali, boshqa hech narsani o'zgartirmasdan). Shu faylning "ORKESTRATSIYA LOGI" bo'limiga bitta yangi qator qo'sh: "- [x] **[2026-08-03 <hozirgi_vaqt>]** `__TASK_ID__` (`__PROJECT__`) fulldeep tahlil qilindi, N ta noodatiy yechim topildi."

Faqat shu ikkita faylni yoz/o'zgartir (report fayli + status.md). Boshqa hech qanday faylga tegma, hech narsani o'chirma.


## Manba: `zdes_archive_docs/raw_history/orcestor/tasks/tasklist.md`

# orcestor/tasks/tasklist.md — Draft tasklar qisqa xulosasi

> **Maqsad:** `tasks/` papkasidagi HAR BIR `.md` faylni to'liq ochib
> o'qimasdan, qaysi task nima qilishini, nimaga bog'liqligini va qaysi
> fayllarga tegishini bir qarashda bilish — kontekst/token tejash uchun.
> Bu yerdagi ma'lumot QISQARTIRILGAN xulosa, dispatch qilishdan oldin
> baribir asl `T-0XX.md` faylining o'zini oching (Cheklovlar, to'liq DoD,
> Report back qismlari bu yerda yo'q).
>
> Umumiy progress (tugagan tasklar bilan birga) uchun:
> [`../tasklist.md`](../tasklist.md).

**Oxirgi yangilanish:** 2026-07-25 — hozircha barcha quyidagilar `tasks/`da (draft, dispatch qilinmagan).

---

### T-020 — ✅ TUGAGAN — [Docs 1/3] API+state hujjati: Core/Auth/Dashboard/Tashkiliy tuzilma
`project_docs/api/{auth,dashboard,company,branches,departments,positions}.md` yaratildi, `orcestor/task_compliete/`ga ko'chirildi.

### T-021 — ✅ TUGAGAN — [Docs 2/3] API+state hujjati: Xodimlar/Davomat/Ta'til guruhi
`project_docs/api/{employees,attendance,work-schedules,terminals,leaves,holidays,advances}.md` yaratildi, `orcestor/task_compliete/`ga ko'chirildi.

### T-022 — ✅ TUGAGAN — [Docs 3/3] API+state hujjati: Payroll/Admin + yakuniy indeks
`project_docs/api/{payroll,salary-adjustments,settings,notifications,README}.md` yaratildi, `orcestor/task_compliete/`ga ko'chirildi. Docs seriyasi (T-020..T-022) to'liq tugadi.

### T-023 — Error handling darajasi auditi
**Bog'liqlik:** yo'q. **Fayllar:** `orcestor/analysis/T-023-error-handling-analysis.md` (yangi). O'qiydi: `core/interceptors/**`, barcha `features/**/services|pages`. Global (`error-interceptor.ts`) va component-darajasidagi xato handling qay darajada ekanini tahlil qiladi, aniq tavsiya yozadi. Kod o'zgarmaydi.

### T-024 — Axios'ga o'tish: imkoniyat tahlili
**Bog'liqlik:** yo'q. **Fayllar:** `orcestor/analysis/T-024-axios-analysis.md` (yangi). `core/services/http.ts` yagona choke-point ekanini hisobga olib, kam-ta'sirli (faqat `Http` ichida) vs katta-ta'sirli (butun loyiha) variantni solishtiradi, ANIQ birini tavsiya qiladi + T-025 uchun reja. Kod o'zgarmaydi, npm o'rnatilmaydi.

### T-025 — Axios'ni amalga oshirish
**Bog'liqlik:** T-024 tugagandan keyin, uning rejasiga qat'iy rioya qiladi. **Fayllar:** `package.json`, `core/services/http.ts`, `core/interceptors/{auth,error}-interceptor.ts`, `app.config.ts` (+ agar katta-ta'sirli tanlansa: `features/*/services/*.ts`). `axios` qo'shiladi, interceptor mantig'i ko'chiriladi.

### T-026 — [Perf 1/6] Skeleton/bubble loading shared komponenti
**Bog'liqlik:** yo'q (birinchi bo'lib ishlaydi, keyingilar shunga tayanishi mumkin). **Fayllar:** `shared/components/ui/skeleton-loader/` (yangi), `data-table.{ts,html,css}` (loading holati). Yangi dependency yo'q.

### T-027 — [Perf 2/6] DataTable qidiruv/filter
**Bog'liqlik:** T-026dan keyin (bir xil faylga tegadi). **Fayllar:** `data-table.{ts,html,css}`. `processData()` oqimini filter→sort→paginate tartibiga qat'iylashtiradi — bu keyingi T-028/T-031 uchun asos.

### T-028 — [Perf 3/6] DataTable DOM virtualization
**Bog'liqlik:** T-027 tugagandan keyin. **Fayllar:** `package.json` (**`@angular/cdk` qo'shiladi — istisno, ruxsat berilgan**), `data-table.{ts,html,css}`. Opt-in `virtualScroll` input, default xatti-harakat o'zgarmaydi.

### T-029 — [Perf 4/6] Lazy loading (`@defer` + rasm)
**Bog'liqlik:** yo'q, mustaqil. **Fayllar:** `attendance/pages/scanner/*`, `employees/components/face-register/*`, `image-upload.html`. `CameraCapture`ni `@defer (on interaction)` bilan o'raydi, `<img loading="lazy">` qo'shadi.

### T-030 — [Perf 5/6] HTTP javob keshlash
**Bog'liqlik:** yo'q — `Http.get()` public interfeysiga qarab ishlaydi, T-024/T-025 tartibidan mustaqil. **Fayllar:** `core/services/http.ts`, + 5 ta "kam o'zgaradigan" service (`company`, `branch`, `department`, `position`, `holiday`). Opt-in TTL kesh, default o'chirilgan.

### T-031 — [Perf 6/6] Server-side pagination — FAQAT API kontrakt
**Bog'liqlik:** T-027 VA T-028 tugagandan keyin. **Fayllar:** `data-table.{ts,html}`, (ixtiyoriy) `project_docs/api/README.md`. **Hech qanday feature service o'zgarmaydi** — backend yo'qligi sababli faqat Input/Output kontrakt qo'shiladi, haqiqiy ulash keyingi (hali yozilmagan) taskka qoladi.

### T-032 — Auth: `/auth/login` → `/sign`, bitta sahifada Login/Register switch-form
**Bog'liqlik:** yo'q, mustaqil (Fayzillo to'g'ridan-to'g'ri so'ragan, 2026-07-25). **Fayllar:** `app.routes.ts`, `features/auth/auth-routing-module.ts`, `features/auth/pages/login/` → yangi birlashtirilgan `sign` sahifasi, `core/services/auth.ts` (`register()`), `core/models/user.ts` (Register DTO'lar), `core/guards/{auth,role}-guard.ts` (redirect `/sign`). URL `/auth/login`dan `/sign`ga o'zgaradi, bitta komponentda animatsiyali login/register switch, Register uchun backend kontrakti taxmin sifatida yoziladi (hali tasdiqlanmagan).

---

## Tavsiya etilgan dispatch tartibi

```
T-020 → T-021 → T-022                              (docs, mustaqil ketma-ketlik)
T-023                                                (mustaqil, istalgan vaqt)
T-024 → T-025                                        (axios, ketma-ket)
T-026 → T-027 → T-028 → T-031                        (DataTable, qat'iy ketma-ket)
T-029                                                (mustaqil)
T-030                                                (mustaqil)
```


## Manba: `my_digital_brain/90_System/claude_tasks/new_fixing_orcestration_system/06-xulosa-va-keyingi-qadamlar.md`

# 6. Umumiy xulosa va keyingi qadamlar

## Xulosa

- Muammo ikkita: (1) `orcestor` g'oyasi 4 loyihada tarqoq va sinxronsiz
  rivojlangan, (2) token sarfining 80%i sessiya-context yuklanishidan
  ketmoqda — kod/tahlil ishi emas.
- Markaziy konsepsiya (2026-07-30 aniqlandi): **small context backup** —
  har sessiyada butun tarix emas, faqat minimal checkpoint + tegishli
  standing rule yuklanadi ([`01-muammo-va-kelib-chiqishi.md#15`](./01-muammo-va-kelib-chiqishi.md#15-evolyutsiya-zanjiri-va-markaziy-konsepsiya-2026-07-30-qoshildi),
  [`03-arxitektura-eskiz.md#30`](./03-arxitektura-eskiz.md#30-markaziy-konsepsiya-small-context-backup-2026-07-30)).
- Yechim yo'nalishi (Faza A, yaqin muddatli): yagona DB-asosli tizim, ikki
  qatlamli xotira (`session_checkpoints` — tez eskiruvchi, `standing_rules`
  — doimiy), yozuvni tez/arzon AGY bajaradi, Claude faqat
  tekshiradi/tasdiqlaydi, har sessiya 5 promptdan keyin `/clear` + qisqa
  checkpoint bilan davom.
- Yechim yo'nalishi (Faza B, uzoq muddatli roadmap): saqlash to'liq
  avtomatlashadi — alohida NestJS API server, agentlar natijani API'ga
  yuboradi, DB serverda turadi, holat GitHub'ga sinxronlanadi. Tafsilot:
  [`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md).
  **Bu hali qurilmagan, faqat yo'nalish sifatida qayd etilgan.**
- Bu — **reja**, kod emas. Barcha arxitektura tafsilotlari
  ([`03-arxitektura-eskiz.md`](./03-arxitektura-eskiz.md)) va taxminlar
  ([`04-taxminlar-va-tekshirish.md`](./04-taxminlar-va-tekshirish.md))
  hali tekshirilmagan — qurish paytida o'zgarishi kutilmoqda.

## Keyingi qadamlar (vaqt topilganda)

**Faza A — yaqin muddatli:**

1. Schema'ni aniq loyihalash (jadval nomlari, ustunlar) — shu papkada
   yangi fayl sifatida.
2. Local SQLite bilan kichik prototip — [4.4-bandidagi](./04-taxminlar-va-tekshirish.md#44-db-qayerda-turadi) savolni yopish.
3. Pilot: [UC1](./05-use-caselar.md#uc1--orcestorning-4-nusxasini-birlashtirish)
   — orcestor'ning 4 nusxasini shu tizim yordamida birlashtirish, shu
   bilan birga tizimning o'zini sinash.
4. Pilot natijasidan keyin: [UC5](./05-use-caselar.md#uc5--token-sarfi-taqsimotini-keyingi-haftada-qayta-olchash)
   bo'yicha token taqsimotini qayta o'lchash, natijaga qarab boshqa
   loyihalarga (`secvault`, `pass_manager_bot`, ...) tarqatish yoki
   arxitekturani qayta ko'rib chiqish.

**Faza B — uzoq muddatli (roadmap, Faza A pilot muvaffaqiyatidan keyin):**

5. [`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md)dagi
   ochiq savollarni (xarajat, xavfsizlik, sinxronizatsiya) aniqlashtirish,
   keyin NestJS API server qurishni boshlash.

## Status izohi

Bu papka **statik emas** — qurish boshlangach yoki yangi taxmin/muammo
chiqqach, mavjud fayllarga qo'shimcha qilinadi (rad etilganlar
"❌ RAD ETILDI" deb belgilanadi, o'chirilmaydi — `claude_tasks`
konvensiyasiga mos).


## Manba: `my_digital_brain/20_Areas/reports_agy/principles.md`

# Fayzillo — Noodatiy Logikalar, Custom Algoritmlar va Loyiha Qurish Metodologiyasi

> Ushbu hujjat Fayzillo Ummatovning `repos/` ichidagi barcha real manba kodlaridan ajratib olingan **noodatiy yechimlar (Custom Logic), unikal algoritmlar, arxitektura tamoyillari va signature patternlar** bazasidir.

---

## 1. Tahlil va Orkestratsiya Metodologiyasi

- **Orkestratsiya Tizimi:** `/home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/orcestor/` (File-based Task Management).
- **Manba Kodlar:** `/home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/repos/` (`Admin-panel`, `StudentSYStemMenegment`, `mini-erp`, `online-courses`, `e-commerce-backend`, `crm_backend`, `telegram_app_backend`).
- **Noodatiy Yechimlar Tahlili:** Oddiy nazariya va umumiy ta'riflar chetga surilib, faqat dasturchining o'zi yozgan maxsus algoritmlar, custom schemas, regex generatorlar va call chainlar o'rganildi.

---

## 2. FAYZILLO YOZGAN NOODATIY LOGIKALAR VA CUSTOM ALGORITMLAR

### 2.1. Dynamic Mock User Generator Algorithm (`setDefaultUsers`)
* **Repo / Fayl:** `Admin-panel` (`appdata/getclass.js` L270-L287)
* **Noodatiy Yechim:**
  Dasturchi 100 ta foydalanuvchi ma'lumotlarini o'z qo'li bilan yozib o'tirmasdan, matematik formulalar va `Array.from` generatori orqali dinamik generatsiya qilgan:
  ```javascript
  ...Array.from({ length: 90 }, (_, i) => {
      const id = i + 11;
      return new User(
        id, `User ${id}`, `user_${id}`, `user${id}@example.com`, `password${id}`,
        id % 2 === 0, `Role ${id}`,
        { posts: id % 3 === 0, newsletter: id % 4 === 0, personalOffer: id % 5 === 0 },
        this.getNewDate(`2024-01-${(id % 28 + 1).toString().padStart(2, '0')}`)
      );
  })
  ```
* **Nima uchun qilingan:** Test muhiti va LocalStorage state-ni soniyalar ichida realistic mock ma'lumotlar bilan to'ldirish uchun.

---

### 2.2. Schema-Driven Input Validation Engine (`isvalid`)
* **Repo / Fayl:** `StudentSYStemMenegment` (`src/servise/servise.js` L8-L25)
* **Noodatiy Yechim:**
  Tashqi validation kutubxonalari (Joi, Validator) ishlatmasdan, oddiy JS obyekti (`sxema`) shabloni asosida kiruvchi JSON request body kalitlarini va tiplarini dinamik tekshirgan:
  ```javascript
  let sxema = { id: 1, firstName: "Ali", lastName: "Valiyev", course: 2, faculty: "IT" };

  function isvalid(data) {
      let keys = [...Object.keys(sxema)];
      for(let key in data) {
          if(!keys.includes(key)) return false;
          if(key == 'course' && (isNaN(+data[key]) || +data[key] > 4 || +data[key] < 1)) return false;
          if((key == 'firstName' || key == 'lastName') && (!/^[a-zA-Z]+$/.test(data[key].trim()) || data[key].length < 3)) return false;
      }
      return true;
  }
  ```
* **Nima uchun qilingan:** Tashqi bog'liqliklar (dependencies) siz toza va tejamkor JSON validation mexanizmini yaratish uchun.

---

### 2.3. Dynamic Granular Action-Based Permission Model (`model Permission`)
* **Repo / Fayl:** `online-courses` (`prisma/schema.prisma` L17-23, L77-89)
* **Noodatiy Yechim:**
  Oddiy role-based auth (RBAC) o'rniga, har bir foydalanuvchi va model uchun dinamik HTTP Action (`GET`, `POST`, `PUT`, `DELETE`) huquqlarini beruvchi schema modellash:
  ```prisma
  enum Action { GET POST PUT PATCH DELETE }

  model Permission {
    id      String   @id @default(auto()) @map("_id") @db.ObjectId
    model   String
    actions Action[]
    userId  String   @db.ObjectId
    user    User     @relation(fields: [userId], references: [id])
  }
  ```

---

### 2.4. Multi-Device Session Connections & Real-Time Typing Engine
* **Repo / Fayl:** `telegram_app_backend` (`src/soket/soket.gateway.ts` L18-38)
* **Noodatiy Yechim:**
  ```typescript
  handleConnection(client: Socket) {
      const userId = client.handshake.query.userId as string;
      const deviceId = client.handshake.query.deviceId as string;
      this.socketService.addConnection(userId, deviceId, client);

      client.on("typing", (data) => {
          this.socketService.onTypingByUserIdUser(userId, data);
      });
  }
  ```
* **Nima uchun qilingan:** Bitta foydalanuvchining bir nechta qurilmalaridan (Multi-Device) WebSockets ulanishini `handshake.query` orqali dinamik ajratib olish va real vaqtda instant chat holatini efirga uzatish uchun.

---

### 2.5. Synchronous Disk File Cleanup Scheme (`removeImg`)
* **Repo / Fayl:** `mini-erp` (`src/services/user.service.js` L26-38)
* **Noodatiy Yechim:**
  Ma'lumotlar bazasidan foydalanuvchi o'chirilganda, unga tegishli faylni diska chirib yetim qolmasligi uchun `fs.existsSync` va `fs.unlinkSync` orqali sinxron tozalash kodi.

---

## 3. UNIKAL SIGNATURE PATTERNLAR

### 3.1. Centralized Global Initialization (`initGlobalApp` / `setterAppConfigurations`)
- **Fakt:** `e-commerce-backend`, `crm_backend`, `telegram_app_backend`, `online-courses` loyihalarining barchasida `main.ts` fayli atigi 10-14 qatordan iborat.
- **Mexanizm:** `main.ts` `initGlobalApp(app)` (yoki `setterAppConfigurations(app)`) chaqiradi va u `src/core/use_initilation.ts` ichida `GlobalPrefix`, `ValidationPipe`, `cookieParser`, `SwaggerModule` (Dark Theme `SwaggerThemeNameEnum.ONE_DARK`), `DeviceMiddleware` va `GlobalFilters` larni bitta joyda biriktiradi.

---

### 3.2. Ephemeral Container Storage + External Platform-ID File Reference Pattern
- **Tamoyil:** Fayllar (rasm, video va h.k.) hech qachon asosiy loyiha bazasida (DB) bayt-massiv sifatida, hech qachon konteynerning doimiy diskida ham saqlanmaydi — faqat **nomi yoki ID'si** saqlanadi.
- **Mexanizm:** Fayllar uchun alohida, mustaqil server (microservice) ko'tariladi. Bu server kelgan faylni tashqi cloud platformaga yuklaydi va qaytgan `id`ni asosiy loyihaga beradi. Asosiy loyiha bazasida faqat shu `id` saqlanadi. `GET /image` so'ralganda, saqlangan ID asosida `cloudUrl/imageId` ko'rinishidagi to'liq URL dinamik shakllantirilib qaytariladi.
- **Nima uchun qilingan:** Konteynerga (Docker) fayl saqlash har redeploy'da fayllarning o'chib ketishiga olib keladi (ephemeral filesystem muammosi). Fayzillo buni bootcamp/imtihon loyihalari uchun qabul qilinadigan trade-off deb hisoblaydi — maqsad asosiy talablarni bajarish, production darajadagi doimiy saqlashni ta'minlash emas. Bu qaror mantiqan `tasks/07_step_unusual_solutions_synthesis.md`dagi "In-Memory Map-Based Anti-Spam Rate-Limited Expiring Cache Engine" patterniga (Redis o'rniga in-memory `JS Map` bilan kesh yasash) o'xshaydi: murakkab infratuzilma (S3, persistent volume) o'rniga minimal, lekin talabni qondiradigan "yetarli darajada yaxshi" (good-enough) yechim tanlanadi.

---

## 4. CHUQUR TAHLIL HUJJATLARI XARITASI

| Task ID | Loyiha Nomi | Noodatiy Yechim / Diqqat Markazi | Chuqur Hisobot Fayli |
|---|---|---|---|
| `TASK-01` | `Admin-panel` | Dynamic Mock Generator, Client-Side Pagination & Slicing | [`reports_agy/deep_01_admin_panel.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_01_admin_panel.md) |
| `TASK-02` | `StudentSYStemMenegment` | Schema-Driven Custom Input Validation, Auto-Increment PK | [`reports_agy/deep_02_student_sys.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_02_student_sys.md) |
| `TASK-03` | `mini-erp` | Custom Error Hierarchy, Synchronous Disk File Cleanup | [`reports_agy/deep_03_mini_erp.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_03_mini_erp.md) |
| `TASK-04` | `online-courses` | Granular Action-Based Permission Model, Enum Models | [`reports_agy/deep_04_online_courses.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_04_online_courses.md) |
| `TASK-06` | `e-commerce-backend` | Hybrid Dynamic Schema (Relational + JSON BSON features) | [`reports_agy/deep_06_ecommerce.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_06_ecommerce.md) |
| `TASK-07` | `crm_backend` | Course Schedule WeekDays Array `[1,3,5]`, Room Capacity | [`reports_agy/deep_07_crm.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_07_crm.md) |
| `TASK-08` | `telegram_app_backend` | Multi-Device Handshake Extraction & WebSockets Typing | [`reports_agy/deep_08_telegram_app.md`](file:///home/fayzillo/Desktop/testing/claude_tasks/repo_analiz/reports_agy/deep_08_telegram_app.md) |

---

## 5. YAKUN
Fayzillo'ning koding uslubi faqat standart freymvork qoliplaridan iborat emas, balki har bir loyihada u muammoni hal qilish uchun **xususiy algoritmlar, dinamik validation mexanizmlari, gibrid schema modellari hamda resurslarni tejaydigan yechimlar**ni izchil qo'llagan.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/blocker-va-subtask/shart.md`

# Shart — Blocker/sub_task qachon dolzarb bo'ladi

Bu use-case quyidagi holatda yuzaga keladi:

- Orchestration `orcestor/tasks/` → `task_pending/` → `task_compliete/`
  (yoki DB `tasks` jadvali) orqali rasmiy lifecycle bilan ishlaydi.
- Asosiy task (masalan "X funksiyani qo'sh") bajarilish jarayonida
  kutilmagan to'siqqa duch keladi — masalan yetishmayotgan dependency,
  boshqa modulda avval hal qilinishi kerak bo'lgan xato, yoki
  aniqlashtirish talab qiluvchi kichik-noaniqlik.
- Bu to'siqni hal qilish asosiy task doirasidan tashqariga chiqadi —
  ya'ni uni alohida, kichikroq ish sifatida ajratish mantiqiy bo'ladi.

**Muhim**: SKILL.md'dagi `orcestor/sub_tasks/` papkasi bu use-case bilan
bir xil emas — u rasmiy lifecycle **tashqarisida** qilingan ishlar
(qo'lda refaktoring, audit) jurnali sifatida ta'riflangan. Bu hujjatdagi
"blocker → sub_task" mantig'i SKILL.md'da hozircha yozilmagan, loyiha
turiga qarab moslashuvchan shakllanadi (front/backend/boshqa loyihalarda
farqli bo'lishi mumkin).


## Manba: `my_digital_brain/90_System/orcestor/simple_context.md`

# Simple Context — joriy holat (har doim QISQA saqlanadi)

**Oxirgi yangilanish:** 2026-08-20

## Joriy holat
Bootstrap yakunlandi. `my_digital_brain` loyihasida orcestor-skill o'rnatildi (file-based, BATCH_SIZE=1). Loyiha — shaxsiy arxiv/hujjat tizimi: AI suhbat tarixi (`ai-chat-history/`) + repo tahlil natijalari (`reports_agy/`, `tasks/`). Eski orcestor fayllari (`resumer.md`, `status.md`, `fulldeep_prompt_template.txt`) saqlanib qolindi — ular oldingi repo tahlil loyihasiga tegishli, o'chirilmadi.

## Ko'rilgan muammolar
(yo'q)

## Keyingi qadam
Bootstrap yakunlandi, birinchi task kutilmoqda.

## Restart paytidagi token hisob-kitobi
(bo'sh — birinchi restartda to'ldiriladi)


## Manba: `mini_brain/ai_controlling_style/ai_controlling_style.md`

- **Yagona Orkestratsiya tizimi**: `orcestor` asosida "File-based Task Management" tizimidan foydalaniladi.
- **Markaziy Konsepsiya ("Small context backup")**: Token sarfini qisqartirish uchun har yangi sessiyada butun tarix yoki barcha hujjatlar emas, faqat ayni task uchun kerakli bo'lgan minimal checkpoint va unga tegishli qoidalar (standing rules) yuklanadi.
- **Ikki Qatlamli Xotira Modeli**:
  1. `session_checkpoints`: Sessiyaga bog'langan, tez eskiruvchi, oxirgi holatni ko'rsatuvchi majburiy qisqa xulosa.
  2. `standing_rules`: Sessiyalardan tashqari (cross-session), sekin o'zgaruvchi muhim loyiha qoidalari. Bular `topic` bo'yicha unikalligi tekshirilib (UPSERT qilinib) yangilanadi.
- **5-Promptli Sprint Sikli**: [Prompt 1..5] → ish bajarish → AGY oxirgi checkpointni yozadi → `/clear` qilinadi → Yangi prompt faqat bitta oxirgi checkpoint va kerakli filtrlangan qoidalar bilan yuklanadi.
- **Rollar Taqsimoti**:
  - **Claude (Orchestrator / Bosh muhandis)**: Qimmatroq va chuqur fikrlaydigan rolda o'qiydi, yakuniy qaror qabul qiladi va tasdiqlaydi.
  - **AGY (Executor / Kotib)**: Arzon, tezkor rolda ijro etadi hamda checkpoint va qoidalarni to'g'ridan-to'g'ri yozadi.
- **Fayllar Statusi (Rad etish qoidasi)**: Noto'g'ri chiqqan yoki rad etilgan g'oyalar hamda fayllar o'chirilmaydi, balki "❌ RAD ETILDI" deb belgilanadi (`claude_tasks` konvensiyasiga mos tarzda).


## Manba: `my_digital_brain/90_System/claude_tasks/new_fixing_orcestration_system/03-arxitektura-eskiz.md`

# 3. Arxitektura eskizi (bog'lovchi emas — boshlang'ich taxmin)

## 3.0 Markaziy konsepsiya: small context backup (2026-07-30)

Evolyutsiya zanjirining ([`01-muammo-va-kelib-chiqishi.md#15`](./01-muammo-va-kelib-chiqishi.md#15-evolyutsiya-zanjiri-va-markaziy-konsepsiya-2026-07-30-qoshildi))
oxirgi va hozirgi markaziy bosqichi — **small context backup**. Ta'rif:

> Har yangi sessiyada butun history yoki barcha hujjatlar emas, balki
> **faqat ayni task uchun kerakli minimal checkpoint va standing rule'lar**
> yuklanadi.

Bu bo'limdagi qolgan hamma narsa (3.1–3.5) — shu konsepsiyaning texnik
ifodasi: ikki qatlamli model (3.1) checkpoint'ni "minimal" saqlashning
mexanizmi, 5-promptli sikl (3.3) esa "ayni task uchun kerakli"ni amalda
ta'minlash usuli. Faza B (uzoq muddatli, [`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md))
xuddi shu konsepsiyani saqlaydi, faqat saqlash/yozish mexanizmini
o'zgartiradi (qo'lda/AGY to'g'ridan-to'g'ri DB emas, API orqali avtomatik).

## 3.1 Ikki qatlamli model

**a) `session_checkpoints` — session-scoped, tez eskiruvchi**

| Ustun | Mazmun |
|---|---|
| `session_id` | sessiya identifikatori |
| `project` | qaysi loyiha (zdes, secvault, ...) |
| `boshlangan_vaqt` | — |
| `oxirgi_holat` | ~200–400 tokenlik qisqa xulosa — "qayerga kelindi" |
| `korilgan_muammolar` | qisqa ro'yxat (nima sinab ko'rildi, nima rad etildi) |
| `keyingi_qadam` | — |

Bu — hozirgi `status.md`ning DB ekvivalenti, lekin **majburan qisqa** (fayl
kabi cheksiz uzayib ketmaydi, chunki har checkpoint eskisini almashtiradi,
qo'shilmaydi).

**b) `standing_rules` — cross-session, sekin o'zgaruvchi**

| Ustun | Mazmun |
|---|---|
| `topic` | masalan `"zdes-orcestor-scope"`, `"github-accounts"` |
| `qoida` | qisqa matn |
| `manba` | qaysi sessiya/sana kiritgan |

`session_id`ga bog'lanmaydi, `topic` bo'yicha **unique + UPSERT** — xuddi
shu topic bo'yicha yangi ma'lumot kelsa, yangi qator qo'shilmaydi, mavjudi
yangilanadi. Bu qatlam `orcestor/requirements.MD` va
`backup-plan/overview.md`dagi "Muhim qoidalar" bo'limlarining DB'dagi
muqobili.

## 3.2 Yozuvchi va o'quvchi rollari

- **AGY** — yozuvchi. Checkpoint va (tasdiqlangandan keyin) standing rule
  yozuvlarini DB'ga kiritadi. Tez va arzon (340+ tok/s) — Claude bu mexanik
  ishga o'z (qimmatroq) tokenini sarflamaydi.
- **Claude** — o'quvchi + tasdiqlovchi. Yangi standing rule DB'ga tushishidan
  oldin tekshiradi (orcestor'dagi "Orchestrator — yakuniy texnik qaror"
  roliga mos).

**Faza izohi:** yuqoridagi taqsimot — **Faza A** (yaqin muddatli, shu reja):
AGY DB'ga to'g'ridan-to'g'ri yozadi, lokal. Uzoq muddatli **Faza B**da
([`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md))
AGY DB'ga emas, **API'ga** natija yuboradi, DB'ga yozishni API'ning o'zi
avtomatik bajaradi — rollar taqsimoti (Claude tasdiqlovchi, AGY ijrochi)
o'zgarmaydi, faqat yozish yo'li o'zgaradi.

## 3.3 Sikl (5-promptli sprint)

```
[Prompt 1..5] → ish → AGY oxirgi checkpointni yozadi
      ↓
   /clear
      ↓
[Yangi prompt] → faqat quyidagilar yuklanadi:
   - session_checkpoints: oxirgi qator (bitta)
   - standing_rules: faqat shu loyiha/topic bo'yicha filtrlangan qatorlar
   - yangi prompt
   (to'liq tarix YO'Q)
```

## 3.4 Muhim ogohlantirish — DB o'zi token tejamaydi

DB ishlatish o'zi hech narsani tejamaydi — agar `SELECT *` bilan hamma
checkpointlar yoki hamma qoidalar tashib kelinsa, fayldan farqi yo'q.
Tejash ikki narsadan keladi: (1) reload hajmi doim **bitta compact
checkpoint** bo'lishi (to'liq tarix emas), (2) standing rules **faqat
kerakli topic bo'yicha** filtrlanib olinishi. DB'ning haqiqiy afzalligi —
shu selektiv so'rovni tuzilgan (structured) tarzda qilish qulayligi, fayl
bilan ham grep orqali qisman erishish mumkin bo'lgan narsa, lekin DB'da
tabiiyroq.

## 3.5 Infratuzilma savoli (hal qilinmagan)

Local SQLite (bitta noutbuk, RAM 5.7GB) yetarlimi, yoki alohida servis
kerakmi — bu [`04-taxminlar-va-tekshirish.md`](./04-taxminlar-va-tekshirish.md)da
ochiq savol sifatida qoldirilgan.


## Manba: `my_digital_brain/30_Resources/ai-chat-history/claude/ovovo******utvata@gmail.com/gemini_flash_va_pro_modellarining_farqi.md`

# Gemini Flash va Pro modellarining farqi

### 🤖 Claude:

Ran a command, viewed a file

Ran a command, viewed a file

Ha, ko'rdim. Restart qoidasi hujjatda aniq va qattiq belgilangan — asosiy nuqtalar:

1. Restart faqat Supervisor_User buyrug'i bilan — qattiq prompt/token limiti yo'q, ya'ni tizim o'zi avtomatik restart qilmaydi, qaror doim inson tomonidan qabul qilinadi.

2. Restart'dan OLDIN majburiy qadam:

file rejimida — simple_context.md yangilanishi shart
db rejimida — checkpoint add chaqirilishi shart (--session-id, --summary majburiy)

3. Checkpoint qat'iy qisqa (200-400 so'z) — faqat 4 element:

Joriy holat
Blockers/issues
Keyingi qadamlar
Token hisob-kitobi

4. O'lchov intizomi (eng qiziq qism) — restart oldidan /context orqali "Messages" ulushini tekshirib, simple_context.mdga bitta qatorda yozib qo'yish (masalan "Messages ~27%"). Bu — restartning o'zi samarali ishlayotganini vaqt o'tishi bilan kuzatish uchun. Agar bu ko'rsatkich doim yuqori bo'lsa, demak restartlar juda kech qilinyapti degani — SKILL.md buni aniq ogohlantirish sifatida talab qiladi.

Bu — sen aytgan "asosiy task davomida context hali keng bo'lsa davom etiladi" mantig'ining aksincha tomoni: bu yerda qachon restart qilish kerakligini o'lchash mexanizmi bor, lekin "qachon sub_task blocker context'ni band qilib qo'yganda asosiy taskka qaytish" qarori — bu, oldin aytganimdek, hujjatda yo'q, sen uni amalda moslashuvchan qaror sifatida qo'llaysan.

---

### 👤 Foydalanuvchi:

Qiziq men oʻzim bu skilldan foydalanish vaqtida yaxshi boshqara olishim mumkin lekin open sourcega yuqoridagi bilimlar bilan chiqarish kerak shekili.

### 🤖 Claude:

Ha, aynan shu farq muhim — sen hozir implicit tacit knowledge bilan ishlayapsan (blocker/sub_task qarori, restart timing sezgisi), lekin bu bilim faqat sening boshingda, hujjatda emas. Bu shaxsiy foydalanish uchun yetarli, chunki sen har safar planning mode orqali qaror qabul qilasan.

Open source qilib chiqarganingda esa boshqa foydalanuvchi bu "sezgi"ga ega bo'lmaydi — ular xuddi shu vaziyatga tushganda:

Qachon sub_task ochish, qachon asosiy taskni davom ettirish kerakligini bilmaydi
Restart qachon "kech" bo'lib qolganini tushunmaydi (sendagi 27% empirik benchmark ularda yo'q)
Loyiha turiga (front/backend) qarab qoidani qanday moslashtirish kerakligi haqida yo'l-yo'riq topolmaydi

Amaliy variant: hammasini qattiq qoidaga aylantirish shart emas — bu sening o'zing tanlagan moslashuvchanlik falsafasiga zid bo'lardi. Buning o'rniga SKILL.md'ga "decision guidance" yoki misol qatlamini qo'shish mumkin:

Blocker chiqqanda qanday savol berish kerak ("bu blocker asosiy taskka bog'liqmi yoki mustaqilmi?") — qoida emas, balki qaror daraxti (decision heuristic)
Restart timing uchun aniq signal ("agar Messages ulushi 25%+ bo'lsa va joriy task hali tugallanmagan bo'lsa, Supervisor_User'ga restart tavsiya qiling")
1-2 real misol (zdes_frontend tajribasidan) — front vs backend loyihada sub_task formati qanday farq qilgani

Bu — qoidalarni majburiy qilmasdan, foydalanuvchiga sening tajribangdan kelib chiqqan yo'l-yo'riq berish usuli. Xohlasang, shu qismni SKILL.md formatiga moslab birga yozib chiqishimiz mumkin.

---

### 👤 Foydalanuvchi:

Unda bunday qilamiz sen yuqoridagi use case lar haqida hulosalaringni hujjatlashtirib chiqasan. skill_sub_menagament_planning_information_docs / shart ,vaziyat, qoida , use_cases , exampels md larni shakillantirib zip qilib men oʻzim skill ga joriy qilaman

### 🤖 Claude:

Ran a command

Ran a command

Bir nechta narsani aniqlashtirib olay, keyin to'g'ridan-to'g'ri yozishga o'taman:

---

### 🤖 Claude:

Check SKILL.md structure conventions for formatting consistency

Check SKILL.md structure conventions for formatting consistency

Yaxshi, formatni tushundim. Endi papka strukturasini yarataman — har use-case o'z papkasida shart/qoida/misol bilan.

Created 13 files, ran a command · 3 notes

Created 13 files, ran a command · 3 notes

---


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ovovo******utvata@gmail.com/iso_faylni_ochish.md`

# ISO faylni ochish

### 👤 Foydalanuvchi:

fayzillo@Jarvis:/$ ls
bin                home               mnt   sbin.usr-is-merged  usr
bin.usr-is-merged  lib                opt   snap                var
boot               lib64              proc  srv
cdrom              lib.usr-is-merged  root  swap.img
dev                lost+found         run   sys
etc                media              sbin  tmp


men fleshkani kompga uladim uning ichida ISO fayil bo'lgani uchun File Managerda ocholmayabman Qanday ochishim mumkin

### 🤖 ChatGPT:

Ha, tushundim. Sizning fleshkada ISO fayl bor va uni File Manager orqali to‘g‘ridan-to‘g‘ri ocholmaysiz, chunki ISO — bu virtual disk tasviri (disk image). Uni ochish yoki ichidagi fayllarga kirishning bir necha usullari bor. Linuxda eng qulay usullar:  

---

### 1️⃣ ISO faylni **mount qilish** (virtual disk sifatida ulash)
1. Avvalo, fleshkada ISO faylning to‘liq yo‘lini aniqlang, masalan:  
   ```bash
   /media/fayzillo/FLESH/filename.iso
   ```
2. Keyin yangi katalog yarating, bu katalog ISO faylni ulash uchun ishlatiladi:  
   ```bash
   sudo mkdir /mnt/iso
   ```
3. ISO faylni ushbu katalogga ulash:  
   ```bash
   sudo mount -o loop /media/fayzillo/FLESH/filename.iso /mnt/iso
   ```
4. Endi siz ISO ichidagi fayllarni ko‘rishingiz mumkin:  
   ```bash
   ls /mnt/iso
   ```

⚠️ Foydalangandan so‘ng, ISO faylni ulashni yechish:  
```bash
sudo umount /mnt/iso
```

---

### 2️⃣ GUI orqali (Graphical File Manager)
Agar siz Ubuntu yoki boshqa GNOME/KDE asosli tizim ishlatayotgan bo‘lsangiz:  
- ISO fayl ustiga **o‘ng tugma → Open With → Disk Image Mounter** ni tanlash mumkin.  
- Shu bilan ISO yangi virtual disk sifatida ochiladi va File Manager’da ko‘rinadi.

---

### 3️⃣ ISO faylni arxiv sifatida ochish
Ba’zi Linux arxiv menejerlari (File Roller, Ark) ISO faylini `.zip` yoki `.tar.gz` kabi ochishga imkon beradi:  
- ISO ustiga o‘ng tugma → “Extract Here” yoki “Open with Archive Manager”.

---

Agar xohlasang, men senga **komanda orqali tez va xavfsiz mount qilish va fayllarni ko‘rish uchun tayyor buyruqlarni** yozib bera olaman. Shu qilaylikmi?

---

### 👤 Foydalanuvchi:

ayzillo@Jarvis:/$ cd media/
fayzillo@Jarvis:/media$ ls
fayzillo
fayzillo@Jarvis:/media$ cd fayzillo
fayzillo@Jarvis:/media/fayzillo$ ls
fayzillo@Jarvis:/media/fayzillo$ 

### 🤖 ChatGPT:

Ko‘rinyapti, sizning fleshkangiz `/media/fayzillo/` ostida mont qilingan, lekin `ls` bo‘sh chiqyapti. Bu bir necha narsani anglatishi mumkin:  

1. Fleshka **to‘g‘ri o‘rnatilmagan** yoki mount qilinmagan.  
2. Siz noto‘g‘ri katalogga kirgansiz (fleshka boshqa katalogda mount qilingan bo‘lishi mumkin).  
3. Tizim ISO faylni virtual disk sifatida ko‘rsatgan, shuning uchun uni to‘g‘ridan-to‘g‘ri ko‘rolmaysiz.  

---

### Tekshirish usuli
Fleshka qayerga mont qilinganini aniqlash uchun terminalga yozing:  
```bash
lsblk
```
yoki  
```bash
df -h
```

Bu buyruqlar sizga barcha disk va mount qilingan joylarni ko‘rsatadi. Fleshkada ISO fayl ko‘rinishi va uning mount nuqtasi ko‘rinadi.

---

Agar xohlasang, men senga **Linuxda ISO faylni xavfsiz mount qilish va ichidagi fayllarni ko‘rish bo‘yicha aniq buyruqlar** yozib bera olaman. Shu qilaylikmi?

---

### 👤 Foydalanuvchi:

sda           8:0    1  29.3G  0 disk 
└─sda1        8:1    1  29.3G  0 part 

### 🤖 ChatGPT:

Ko‘rinyapti, tizim faqat `sda1` bo‘linmani ko‘rmoqda (sizning fleshka 29.3 GB), lekin hozircha u mount qilinmagan. Shu sababli `/media/fayzillo` bo‘sh chiqyapti.  

Fleshkani mount qilish uchun buyruqlar:  

1. Mount nuqtasi yaratish:  
```bash
sudo mkdir /mnt/fleshka
```

2. Fleshkani mount qilish:  
```bash
sudo mount /dev/sda1 /mnt/fleshka
```

3. Endi fayllarni ko‘rish:  
```bash
ls /mnt/fleshka
```

---

Agar fleshka ichida **faqat ISO fayl bo‘lsa**, uni ham virtual disk sifatida mount qilish kerak bo‘ladi:  

```bash
sudo mkdir /mnt/iso
sudo mount -o loop /mnt/fleshka/filename.iso /mnt/iso
ls /mnt/iso
```

Shu orqali ISO ichidagi fayllarni ko‘rishingiz mumkin.  

Agar xohlasang, men senga **bir buyruq ketma-ketligida fleshka va ISO ni bir vaqtning o‘zida ko‘rish** usulini yozib bera olaman. Shu qilaylikmi?

---


## Manba: `zdes_archive_docs/raw_history/orcestor/prompt.md`

# AGY uchun Standart Topshiriq Shabloni (Prompt Template)

`zdes/orcestor/` tizimining bir qismi. Claude Code shablonni to'ldiradi,
`agy` CLI orqali (yoki Fayzillo qo'lda Antigravity'ga) dispatch qiladi.
AGY **faqat `test-zdes-front` ichida** ishlaydi (`--add-dir` shu repога
ko'rsatiladi) — `zdes_backend` faqat task matni ichida **kontekst/manba**
sifatida ko'rsatiladi (fayl yo'llari, DTO/schema parchalari), AGY'ga
o'zgartirish uchun berilmaydi.

> Qamrov eslatmasi: bu tizim faqat response/request tiplar, servislar va
> CRUD-oqim uchun — stil/CSS/layoutga hech qachon tegilmaydi (`requirements.MD`,
> 0-bo'lim).

---

## 1. Shablon (nusxa ko'chirish uchun)

```markdown
## Task ID: {{TASK_ID}}
### Sarlavha: {{TASK_TITLE}}

**Maqsad (Goal):**
{{GOAL}}
<!-- Bitta aniq, o'lchanadigan gap: qaysi modul, backendga qanday moslanadi. -->

**Backend manba (Backend Source — read-only kontekst):**
{{BACKEND_SOURCE}}
<!-- zdes_backend/src/modules/<x>/... fayl yo'llari + kerakli DTO/Prisma
     model parchasi (qisqa, faqat zarur qism). AGY bu fayllarga YOZMAYDI,
     faqat o'qib moslashtiradi. -->

**Kontekst (Context):**
{{CONTEXT}}
<!-- test-zdes-front kod bazasining qaysi qismi: model, servis. Faqat yo'l. -->

**Cheklovlar (Constraints):**
{{CONSTRAINTS}}
<!-- Doim: "tip/servis va komponent .ts render/data-binding mantig'ida
     ishlang, lekin CSS/SCSS/HTML dizayn-layoutga tegmang",
     "zdes_backend'ga yozmang (Fayzillo aniq istisno bermasa)",
     "boshqa modullarga tegmang". -->

**Ish doirasidagi fayllar (Files in scope):**
{{FILES_IN_SCOPE}}
<!-- Faqat test-zdes-front ichidagi aniq fayl yo'llari. -->

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
{{DEFINITION_OF_DONE}}
<!-- Tip backend bilan mos, npm run build xatosiz, project_docs/api/*.md
     yangilangan (agar tegishli bo'lsa). -->

**Tavsiya etilgan Antigravity rejimi (Mode):**
{{MODE}}

**Natijani qayerga yozish kerak (Report back):**
- **`orcestor/` ga HECH QANDAY fayl yozmang/ko'chirmang** — bu papka
  `--add-dir` orqali sizga berilgan hudud (`test-zdes-front`)dan
  TASHQARIDA, sizda unga yozish huquqi yo'q (agar urinsangiz,
  `test-zdes-front` ichida noto'g'ri, tasodifiy `orcestor/` papkasi
  qayta yaratiladi — buni qilmang).
- Buning o'rniga: **yakuniy xulosani to'g'ridan-to'g'ri o'zingizning
  so'nggi javobingiz (final message) matnida qaytaring** — bosqichlar,
  yakuniy xulosa, va "O'zgargan fayllar" jadvali:

  ### O'zgargan fayllar
  | Fayl | Turi | Qisqa sabab |
  |---|---|---|

  Turi ustuni faqat: `yangi` / `o'zgartirilgan` / `o'chirilgan`.
- Orchestrator (Claude Code) sizning shu javobingizni o'qib,
  `orcestor/task_compliete/`ga o'zi yozadi — bu qadam sizning
  vazifangiz emas.
```

---

## 2. Maydonlar tavsifi

| Maydon | Tavsif |
|---|---|
| `{{TASK_ID}}` | Masalan `B-001` (Backend-moslashuv seriyasi, `test-zdes-front/orcestor/`dagi `T-0XX` bilan aralashmasin) |
| `{{BACKEND_SOURCE}}` | `zdes_backend` ichidagi aniq fayl yo'li(lar) + zarur DTO/schema parchasi — **faqat kontekst, yozilmaydi** |
| `{{CONTEXT}}` | `test-zdes-front` ichidagi tegishli qism |
| `{{CONSTRAINTS}}` | Qamrov chegarasi har doim shu yerda takrorlanadi |
| `{{FILES_IN_SCOPE}}` | Faqat `test-zdes-front/...` yo'llari |
| `{{DEFINITION_OF_DONE}}` | Backendga mosligi + build + docs |
| `{{MODE}}` | Agent-driven / Review-driven / Agent-assisted |

---

## 3. Eslatma

`agy` chaqiruvida (`agy --print "..." --add-dir <yo'l-test-zdes-front>
--mode accept-edits --dangerously-skip-permissions --model
gemini-3.1-pro-low`) **`--add-dir` FAQAT `test-zdes-front`ga ko'rsatiladi**
— `zdes_backend` hech qachon `--add-dir`ga qo'shilmaydi (yozish huquqi
berilmasligi uchun). Backend kontekst kerak bo'lsa, tegishli qism task
matni ichiga (yoki `orcestor/analysis/`dagi faylga havola sifatida)
kiritiladi.

Granularlik: `requirements.MD` 7-bo'limiga ko'ra ~1 servis/2-4 fayl bir
dispatchda — kattaroq topshiriqlar bo'lib yuboriladi.

---

## Manba: bot_post_using/docs/telegraf-bot-architecture-and-ux-rules.md

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

