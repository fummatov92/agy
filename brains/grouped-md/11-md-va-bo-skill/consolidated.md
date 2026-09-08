# O'quv va O'rganish Strategiyalari hamda Texnik Roadmaplar (Learning & Roadmaps)


## Manba: `misc/Learning_Parking_Lot_Strategy.pdf`

Learning Parking Lot Strategy
Maqsad
Learning vaqtida chuqur o'rganish istagini yo'qotmasdan, ish va vazifalarni vaqtida
tugatish.
Asosiy qoida
1. Avval taskni bajar.
2. Qiziq mavzu chiqsa darhol chuqur ketma.
3. Uni Parking Lot ro'yxatiga yoz.
4. Task tugagach Learning Mode ni yoq.
Workflow
Task -> Parking Lot -> Task Finished -> Learning Mode -> Deep Dive
Parking Lot formati
- JWT HS256 vs RS256
- Passport source code
- Node crypto.sign()
- Redis persistence
ROI qoidasi
Savol: "Buni keyingi 30 kun ichida ishlatamanmi?"
Ha -> Hozir o'rgan.
Yo'q -> Parking Lot'da qoldir.
3 ta 'Nega?' qoidasi
Mavzuni ketma-ket faqat 3 ta chuqur 'nega?' bilan o'rgan. Undan keyingi savollar
Parking Lot'ga yoziladi.
Haftalik tartib
Haftasiga Parking Lot'dan faqat 1 ta mavzu tanlab chuqur o'rgan.
Eslatma
Learning Mode maqsadi - tushunish.
Work Mode maqsadi - natijani vaqtida yetkazish.
Ikki rejimni aralashtirma.


## Manba: `zdes_archive_docs/raw_history/orcestor/front-legacy/starter.md`

# starter.md — Sessiya tiklash uchun tezkor holat fayli

> Agar joriy Claude Code sessiyasi kontekst to'lishi/limit tugashi
> sababli uzilsa, yoki yangi sessiya shu loyihada ishni davom ettirsa —
> **shu fayldan boshlang.**

**Oxirgi yangilanish:** 2026-07-26, ~01:35 (limit 95% bo'lgani uchun
shoshilinch yozilgan) — Claude Code (bu sessiya) `test-zdes-front/
orcestor/` (T-0XX tizimi) ustida ishlaydi, forma responsive/dark-mode
ishi tugagan, endi eski perf/auth backlog (T-028-032) ustida.

---

## 1. ENG MUHIM — arxitektura endi BUTUNLAY BOSHQACHA (2026-07-25/26)

**Ikkita alohida, parallel Claude Code sessiyasi bor, ikkalasi ham
`~/Desktop/zdes/` ostida, lekin har biri o'z hududida:**

1. **Bu sessiya (backend-tahlil → frontend UI/responsive/perf):**
   ishchi papka **`test-zdes-front/orcestor/`** (T-0XX tizimi, ESKI,
   original tizim). Backend tahlilini (`B-A-*`, 17/17 modul) yakunlab,
   endi shu yerda ishlaydi.
2. **Boshqa sessiya (API integratsiya):** ishchi papka
   **`~/Desktop/zdes/orcestor/`** (yangi, `B-I-*` seriya,
   `front_integration_tasks/`, `front_agent.md`). **BU YERGA
   TEGMANG** — konflikt xavfi.

**Status/tarix endi FAYLDA EMAS — PostgreSQL'da:**
```
Host: localhost, Port: 5432, DB: zdes_orcestor, User: fayzullo, Pass: 12345678
DATABASE_URL: postgresql://fayzullo:12345678@localhost:5432/zdes_orcestor
```
Parolsiz ulanish: `~/.pgpass` allaqachon sozlangan, shunchaki
`psql -h localhost -U fayzullo -d zdes_orcestor` yetarli.

To'liq sxema/qoida: [`orcestor/README.MD`](./orcestor/README.MD)
7-bo'lim. Qisqacha: `tasks` (har task — status/goal/DoD/verdikt),
`task_events` (tarix), `changed_files`. **Bajarilgan task faylini
o'chirishdan OLDIN DBga to'liq matn yozilishi SHART** (bir marta bu
qadam o'tkazib yuborilib, T-001-027 matni yo'qolgan edi — keyin
`~/Desktop/zdes-frontend/orcestor/` zaxiradan tiklandi, endi to'liq).

Joriy holatni ko'rish: `SELECT task_id,status,verdict FROM tasks ORDER BY task_id;`

---

## 2. Joriy holat — nima tugagan, nima qolgan

**Forma responsive/dark-mode ishi (T-033-T-039) — TO'LIQ TUGAGAN.**
Barcha 11 forma responsive, deyarli barchasi dark-mode tozalangan.

**Eski perf/auth backlog (T-028-032) — HALI DISPATCH QILINMAGAN
(hozir ishlanyapti):**
- **T-028** (DataTable DOM virtualization, `@angular/cdk`) — DBda
  to'liq matn bor (`draft`), hali AGYga jo'natilmagan.
- **T-029** (Lazy loading `@defer`+rasm) — hali DBga to'liq
  yozilmagan, matn faylida (`orcestor/tasks/T-029.md`), backend
  bog'liqligi yo'q, xavfsiz.
- **T-030** (HTTP caching) — matn faylida. **MUHIM: `department`
  xizmatini shu paytda QAMROVDAN CHIQARING** — integrator
  (`zdes/orcestor/task_pending/B-I-DEPARTMENT.md`) shu ustida faol
  ishlagan edi (tekshiring, balki hozir tugagan). Faqat
  company/branch/position/holiday + `http.ts` bilan boshlang.
- **T-031** (Server-side pagination — faqat API kontrakt) — matn
  faylida. **YANGILANGAN topilma:** asl matn "backend hali yo'q" deb
  yozgan, bu ENDI NOTO'G'RI — backend real va HAR BIR list endpoint
  (`backend_crud_review/*.md`) `{items,total,page,limit,totalPages}`
  qaytaradi. Shunga qaramay, ATAYLAB scope kengaytirilmadi (real ulash
  = integrator hududi bilan katta konflikt xavfi) — faqat DataTable
  kontraktini qo'shish rejasi saqlanadi, matnni shunchaki
  "backend hali yo'q" dan "backend real, lekin ulash alohida/kelajak
  ishi" ga yangilash kifoya.
- **T-032** (Auth `/sign`) — **QAYTA YOZILDI**
  (`orcestor/tasks/T-032.md`): Fayzillo tasdiqladi — Register
  funksiyasi BUTUNLAY OLIB TASHLANDI (backendda `/auth/register` yo'q,
  `backend_crud_review/auth.md` tasdiqladi). Endi faqat
  `/auth/login` → `/sign` marshrut o'zgarishi, hech qanday yangi
  funksiya yo'q. DBda `title`/`goal`/`constraints`/`DoD` to'liq
  yozilgan, `status='draft'` (hali dispatch qilinmagan).

**Dispatch tartibi tavsiyasi:** T-028 → T-029 → T-031 → T-030
(department chiqarib) → T-032. Har birida: integrator navbatini
(`ls ~/Desktop/zdes/orcestor/task_pending/`) tekshirib, keyin
`orcestor/dispatch.py send T-0XX` + `agy --print ...`.

---

## 3. Konflikt oldini olish protokoli (Fayzillo qat'iy talab qilgan)

Har bir dispatchdan OLDIN:
1. `ls ~/Desktop/zdes/orcestor/task_pending/` — integrator hozir band
   bo'lgan modulni ko'ring, o'sha modul fayliga shu payt tegmang.
2. Agar `.ts` o'zgarish "shubhali" (kutilmagan) ko'rinsa —
   **avval integratorning `~/Desktop/zdes/orcestor/task_compliete/
   B-I-<MODUL>-response.md` faylini tekshiring** — ehtimol bu ULARNING
   ishi, sizniki emas (bir marta shu sabab bilan noto'g'ri ayblab, DBga
   yolg'on yozib, keyin tuzatishga to'g'ri kelgan — `T-039` DB
   yozuvidagi "TUZATISH" eventini ko'ring, saboq sifatida).
3. Shubha bo'lmasa — hech narsa qilmang, faqat shubhali holatda tekshiring.

## 4. Model/kvota

`agy --model <nom>` bilan tanlanadi: `gemini-3.1-pro-low` (asosiy),
`claude-sonnet-4-6` (Fayzillo alohida so'raganda — **soatlik limit OK,
lekin HAFTALIK limit kam qolgan, tejab ishlating**), `gpt-oss-120b-medium`.

## 5. Havolalar

- [`orcestor/README.MD`](./orcestor/README.MD) — to'liq tizim, DB sxemasi
- [`orcestor/requirements.MD`](./orcestor/requirements.MD) — qoidalar
- [`orcestor/prompt.md`](./orcestor/prompt.md) — task shabloni (AGY endi
  DBga o'zi yozadi — `status='complete'`gacha, tasdiq Claude Code'da)
- `~/Desktop/zdes/orcestor/message.md` — integratorga yozilgan xabar
  (DB ulash ma'lumotlari, ular ham foydalanishi mumkin)
- `~/Desktop/zdes-frontend/` — ESKI to'liq nusxa/zaxira (T-001-027 matni
  shu yerdan tiklangan edi)


## Manba: `my_digital_brain/10_Projects/orcestor-skill/README.md`

# Orcestor Start Skill (`orcestor-start`)

Ushbu skill loyihalarda AI-agentlar orkestratsiyasini (Orchestrator, Executor hamda Supervisor rollari bilan) oson va portativ ravishda ishga tushirish va boshqarish imkonini beradi.

> ### AI agentlarga to'g'ridan-to'g'ri ko'rsatma
> Agar sen AI agentsan (Claude Code, Codex, yoki boshqa) va foydalanuvchi
> seni shu faylni o'qishga yo'naltirgan bo'lsa (masalan "README.md'ni o'qi",
> "shu skillni ishga tushir" kabi so'rov bilan) — bu YETARLI TRIGGER, rasmiy
> Skill-chaqiruv mexanizmini kutib o'tirma. LEKIN Bootstrap savol-javobini
> DARHOL BOSHLAMA — avval quyidagini bajar:
> 1. Ushbu fayl (README.md) va `SKILL.md` mazmunini o'qi.
> 2. Foydalanuvchiga **qisqa** qilib tushuntir: bu skill nima qiladi (rollar,
>    lifecycle, asosiy imkoniyatlar — 3-5 gapda, batafsil emas).
> 3. Shundan keyin ANIQ SO'RA: "Bootstrap'ni (sozlash savol-javobini) hozir
>    boshlaymizmi?" — faqat foydalanuvchi tasdiqlagach (ha/boshla/davom et
>    kabi javobdan keyin), `SKILL.md`dagi Bootstrap/Resume jarayonini
>    0-qadamdan (til tanlash) boshla.
> Boshqacha aytganda: **"README.md'ni o'qi" = "nima ekanini tushuntir, keyin
> ruxsat so'rab, orkestratsiyani boshla"** — bootstrapga bevosita sakrash
> emas.

## Tezkor boshlash (foydalanuvchi uchun, qadam-baqadam)

1. **Talablar:** `agy` (Antigravity CLI) PATH'da bo'lishi kerak. Docker esa FAQAT DB rejimida Postgres/MySQL tanlansa kerak.
2. **O'rnatish** — pastdagi "O'rnatish" bo'limidan birini tanlab, paketni nusxalang.
3. **Yangi sessiya oching** (skilllar ro'yxati sessiya boshida yuklanadi — o'rnatgandan keyin ochiq turgan sessiyada ko'rinmaydi).
4. Loyiha papkasida agentga shuni yozing: **"orkestratsiya boshla"** yoki **"README.md'ni o'qi"** (ikkalasi ham ishlaydi — yuqoridagi ko'rsatmaga qarang).
5. Agent avval **qisqa tushuntiradi** (bu skill nima qilishi) va **"Bootstrap'ni hozir boshlaymizmi?"** deb so'raydi — darhol savol-javobga sakramaydi.
6. Tasdiqlagach — **Bootstrap** suhbati boshlanadi: til tanlash → (eski loyihada) tezkor tahlil → bir nechta sozlash savoli → `orcestor/` avtomatik yaratiladi → oxirida `/clear` tavsiyasi beriladi (tanlov sizniki).
7. **Keyingi safarlar** — shu loyihada shunchaki qayta "orkestratsiya boshla" deyish kifoya: tushuntirish/ruxsat-savoli qayta berilmaydi (bu faqat birinchi, README orqali kirishga xos), oxirgi holatdan (**Resume**) avtomatik davom etadi.

Tafsilotlar (rollar, lifecycle, konflikt-himoya mexanizmlari) — `SKILL.md`da.

## Xususiyatlari
- **Portativlik**: Loyihaga moslashuvchan, shaxsiy papka yo'llari yoki ismlarga bog'lanmagan.
- **Minimal Context Backup**: Har sessiyada faqat eng kerakli checkpoint (`simple_context.md`) o'qiladi, ortiqcha token sarfi oldi olinadi.
- **Bir nechta Tracking Mode**: Ish jarayonini fayllar bilan (`file-based`) yoki DB bilan (`db-based`: sqlite / postgres / mysql, tanlov sizniki) kuzatish mumkin.
- **Eski loyihalar uchun `project_status`**: mavjud kod bazasiga tezkor/tejamkor tahlil qilib, struktura/qoidalar/tarix/muammolarni doimiy saqlab boradi.

## Talablar
- **`agy` (Antigravity CLI)** — `Executer_Agent` rolida kod yozish va buyruqlarni bajarish uchun tizim `PATH`ida o'rnatilgan bo'lishi kerak.
- **Python 3** — `TRACKING_MODE=db` tanlansa, `scripts/orcestor.py` uchun (stdlib only, qo'shimcha paket kerak emas).
- **Docker + Docker Compose** — FAQAT `DB_ENGINE=postgres` yoki `DB_ENGINE=mysql` tanlansa kerak (konteyner ichidagi user/password asosiy ilova bazasiga hech qanday ta'sir qilmaydi — izolyatsiya shu orqali ta'minlanadi). `DB_ENGINE=sqlite` yoki `TRACKING_MODE=file` uchun Docker shart emas.

## O'rnatish — Global yoki Loyiha-darajasida? (tanlov sizniki)

O'rnatishdan oldin shu ikkisidan birini tanlang. Agar skillni siz uchun kimdir
(masalan AI agent) o'rnatayotgan bo'lsa, u ushbu farqni tushuntirib, aynan
shu savolni SIZDAN so'rashi kerak — avtomatik hal qilmasligi lozim.

| | **Global** (`~/.claude/skills/`) | **Loyiha-darajasida** (`<loyiha>/.claude/skills/`) |
|---|---|---|
| Qamrov | Kompyuteringizdagi **BARCHA** loyihalarda ishlaydi | Faqat **shu bitta** loyihada ishlaydi |
| Ulashish | Faqat sizning mashinangizda, boshqalarga avtomatik ko'chmaydi | Loyiha bilan birga git'ga tushsa — jamoa a'zolari ham oladi |
| Mos holat | Siz orkestratsiyani odatiy ish uslubi sifatida ko'p loyihada qo'llasangiz | Faqat bitta muayyan loyiha/jamoa uchun standartlashtirmoqchi bo'lsangiz |

**1. Global o'rnatish:**
```bash
cp -r orcestor-skill ~/.claude/skills/orcestor-start
```

**2. Loyiha-darajasida o'rnatish:**
```bash
cp -r orcestor-skill <loyiha-papkasi>/.claude/skills/orcestor-start
```

## Foydalanish

Claude Code yoki mos keluvchi agent interfeysida quyidagi kabi so'rovlarni yozing:
- `"orkestratsiya boshla"`
- `"orcestor ishga tush"`
- `"start orchestration"`

Birinchi marta ishga tushirilganda **Bootstrap** rejimi ishga tushadi va bir nechta savol orqali loyiha sozlanadi (tafsilot: `SKILL.md`). Keyingi safar ishga tushirilganda esa oxirgi checkpoint'dan **Resume** rejimi davom etadi.

**Muhim — bootstrap tugagach:** Bootstrap/sozlash suhbati o'zi ham token
sarflaydi. Shu sabab, sozlash tugagach, asosiy ish (task'larni bajarish)
boshlanishidan oldin context'ni tozalash (`/clear` yoki mos buyruq) tavsiya
etiladi — bu shart emas, tanlov Supervisor_User'niki, lekin tejamkorlik
uchun tavsiya qilinadi.


## Manba: `my_digital_brain/90_System/claude_tasks/new_fixing_orcestration_system/README.md`

# new_fixing_orcestration_system — yagona orkestratsiya + memory + task-db rejasi

**Holat: REJA bosqichida (2026-07-30 boshlangan) — hali qurilmagan.**

Bu papka kod emas, **g'oyalarni yo'qotmaslik uchun yozilgan reja hujjatlari**.
Fayzillo vaqt topganda shu asosda haqiqiy tizim quradi. Maqsad: hozir bir
nechta loyihada tarqoq va turlicha shakllangan `orcestor/` g'oyasini +
sessiya-context muammosini + task-db fikrini **bitta tezkor, tejamkor
tizimga** birlashtirish.

## Kelib chiqishi (qisqa)

`orcestor` orkestratsiya g'oyasi — Fayzillo'ning o'z ishlanmasi, bitta
o'tirishda emas, **~3 kunlik loyiha davomida duch kelingan muammolar orqali
bosqichma-bosqich shakllangan**. Natijada hozir bir nechta loyihada
(`zdes-backend`, `zdes-frontend`, `zdes-frontend/Gpt_task`, `zdes`) bir xil
g'oyaning **turlicha nusxalari** mavjud — konsolidatsiya qilinmagan. Bu
rejaning bir maqsadi — shu tarqoqlikni ham yagona standartga keltirish.

Parallel ravishda, o'tgan haftalik token sarfini kuzatib, asosiy isrofning
**sessiya context yuklanishida** ekani aniqlandi (tafsilot: [`01-muammo-va-kelib-chiqishi.md`](./01-muammo-va-kelib-chiqishi.md)).

## G'oyaning evolyutsiya zanjiri (2026-07-30 yangilandi)

```
status.md → task management → history → orcestor → DB-based task management → small context backup
```

Zanjirning oxirgi bo'g'ini — **small context backup** — endi bu rejaning
**markaziy konsepsiyasi** deb belgilandi: har yangi sessiyada butun tarix
yoki barcha hujjatlar emas, faqat ayni task uchun kerakli **minimal
checkpoint + tegishli standing rule'lar** yuklanadi. Maqsad — clean session,
minimal context, token sarfini keskin kamaytirish (tafsilot: [`01-muammo-va-kelib-chiqishi.md#15`](./01-muammo-va-kelib-chiqishi.md), konsepsiyaning texnik ta'rifi: [`03-arxitektura-eskiz.md#30`](./03-arxitektura-eskiz.md)).

Uzoq muddatli roadmap (hozirgi implementatsiya emas — kelajak yo'nalishi):
[`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md).

## O'qish tartibi

1. [`01-muammo-va-kelib-chiqishi.md`](./01-muammo-va-kelib-chiqishi.md) — nima uchun kerak, hozirgi holat, raqamlar, evolyutsiya zanjiri
2. [`02-metaforalar.md`](./02-metaforalar.md) — g'oyani tushuntiruvchi metaforalar
3. [`03-arxitektura-eskiz.md`](./03-arxitektura-eskiz.md) — bog'lovchi emas, boshlang'ich eskiz (markaziy konsepsiya: small context backup)
4. [`04-taxminlar-va-tekshirish.md`](./04-taxminlar-va-tekshirish.md) — tekshirilmagan taxminlar, ochiq savollar
5. [`05-use-caselar.md`](./05-use-caselar.md) — real qo'llanish holatlari
6. [`06-xulosa-va-keyingi-qadamlar.md`](./06-xulosa-va-keyingi-qadamlar.md) — umumiy xulosa, keyingi qadam (Faza A)
7. [`07-roadmap-nestjs-api-server.md`](./07-roadmap-nestjs-api-server.md) — uzoq muddatli roadmap (Faza B): NestJS API server, avtomatik saqlash, GitHub sync

**Qoida (`claude_tasks` konvensiyasiga mos):** noto'g'ri chiqqan yoki rad
etilgan g'oyalar bu papkadan o'chirilmaydi, "❌ RAD ETILDI" deb belgilanadi.


## Manba: `zdes_archive_docs/raw_history/orcestor/README.MD`

# orcestor/ — `zdes` orkestratsiya tizimi (backend↔frontend tip/CRUD moslashuvi)

## 0. Konsolidatsiya eslatmasi (2026-07-26)

Ilgari `test-zdes-front/orcestor/` ostida alohida yashagan ikkinchi bir
tizim bor edi — **`T-0XX` seriyasi**, frontend UI/responsive/dark-mode/
performance ishlari uchun (bu `orcestor/`dagi `B-` seriyasidan — backend
tip moslashuvi — butunlay boshqa qamrov). Ikkalasi ham bir xil DB'da
(`zdes_orcestor`, `tasks` jadvali) yashagani va bir xil naqshga ega
bo'lgani sababli, MVP-tozalash doirasida **shu joyga birlashtirildi**:

- Kolliziyasiz papkalar (`analysis/`, `db/`, `steps/`, `task_compliete/`,
  `tasks/`) — tarkibi to'g'ridan-to'g'ri qo'shildi (T- va B- prefikslar
  hech qachon to'qnashmaydi).
- Nomi to'qnashgan top-level hujjatlar — `front-` prefiksi bilan tarixiy
  ma'lumot sifatida saqlandi: [`front-README.MD`](./front-README.MD),
  [`front-prompt.md`](./front-prompt.md),
  [`front-requirements.MD`](./front-requirements.MD),
  [`front-tasklist.md`](./front-tasklist.md),
  [`front-module-plan.md`](./front-module-plan.md),
  [`front-dispatch.py`](./front-dispatch.py) (bu tizimning o'z
  `dispatch.py`si bilan deyarli bir xil, faqat CLI buyruqlari
  T-0XX'ga moslashtirilgan edi).
- Eskirgan kirish-nuqta hujjatlar (`ROOT.MD`, `starter.md`) —
  [`front-legacy/`](./front-legacy/) papkasida arxivlangan.

**Shu kundan boshlab yangi barcha tasklar (shu jumladan `M-` seriyasi —
MVP-tozalash) shu `orcestor/` ichida yoziladi**, `test-zdes-front`
ichida alohida orkestratsiya papkasi endi yo'q.

## 1. Maqsad va qamrov (Scope)

Bu tizim `~/Desktop/zdes/` ostidagi ikkita **alohida git repo**ni bog'laydi:

- **`zdes_backend/`** — NestJS + Prisma backend. Bu tizim uchun **faqat
  o'qish uchun manba (read-only reference)** — bu yerga hech qanday
  o'zgartirish kiritilmaydi (agar Fayzillo alohida, aniq buyruq bermasa).
- **`test-zdes-front/`** — Angular frontend. Maqsad: frontendni haqiqiy
  backend API'ga ulash va shundan chiqadigan render xatolarini tuzatish.
  O'zgarishlar shu repoga tushadi, lekin **faqat quyidagi qamrovda**:
  - `core/models/*.ts` va feature'lar ichidagi response/request tiplar
  - Servislar (`features/*/services/*.ts`) — endpoint yo'li, HTTP metod,
    request/response shakli backendga mos qilib to'g'irlash
  - Komponent `.ts` fayllaridagi render/data-binding mantig'i (masalan
    backend paginatsiyali javob qaytarsa-yu komponent oddiy massiv kutsa)
  - `project_docs/api/*.md` — backend bilan solishtirib yangilash
  - **CSS/HTML dizayn/layout — QAMROVGA KIRMAYDI** ("nima ko'rinadi" emas,
    "qanday ma'lumot bilan ishlaydi" — shu chegara).

**Bu tizimning qamroviga KIRMAYDI** (tegilmaydi, hatto oson tuzatish
ko'ringan taqdirda ham):
- Stil/CSS/dizayn/layout — Fayzillo shu ustida **hozir ham qo'lda**
  ishlayapti (`test-zdes-front` ichida commit qilinmagan o'zgarishlar bor).
- `zdes/review/` papkasi — alohida, bu tizimga aloqasi yo'q ish maydoni.
- `zdes_backend/` ichidagi haqiqiy kod o'zgarishi (faqat tahlil/o'qish).

Sabab (Fayzillo, 2026-07-25): frontend'da parallel ravishda stil ishi
davom etayotgani sababli, bu orkestratsiya tizimi faqat **backend tahlili
asosida response/CRUD tiplarni to'g'irlash**ga qat'iy cheklangan — bir xil
fayllarga ikki tomonlama (stil + tip) tegilib, to'qnashuv chiqmasligi
uchun.

## 2. Rollar

`test-zdes-front/orcestor/`dagi tizim bilan bir xil 3 rollik model
qo'llaniladi:

| Rol | Kim | Vazifasi |
|---|---|---|
| **Orchestrator** | Claude Code | `zdes_backend`ni tahlil qiladi, task yozadi, AGY natijasini tekshiradi (backend manbaga solishtirib), `test-zdes-front`ga integratsiya qiladi. Yakuniy texnik qaror. |
| **Sub-agent / Executor** | AGY (`agy` CLI, Antigravity/Gemini) | Faqat bitta-yo'nalishli (fire-and-forget) chaqiruv orqali ishlaydi — `--add-dir test-zdes-front` bilan, faqat o'sha repo ichida yozadi. |
| **Supervisor** | Fayzillo | Vazifalarni beradi, xavfli/noaniq holatlarda yakuniy qaror, ruxsat beradi. |

## 3. Ishchi zanjir — 2 faza

**Faza 1 — Tahlil (`B-A-<MODUL>`):**
```
zdes_backend/ (read-only, AGY --add-dir bilan o'qiydi)
   → AGY yozadi →  ../backend_crud_review/<modul>.md
   → Claude Code tekshiradi (zdes_backend git-toza + qator-qator solishtirish)
```
Shablon: [`prompt_analysis.md`](./prompt_analysis.md). Tartib va modul
ro'yxati: [`tasklist.md`](./tasklist.md) (auth'dan boshlab, 16 modul +
dashboard).

**Faza 2 — Integratsiya (`B-I-<MODUL>`):**
```
../backend_crud_review/<modul>.md (tasdiqlangan tahlil, yagona manba)
   → AGY o'qiydi → ../test-zdes-front/ ichida tip/servis/render mantig'ini yozadi
   → Claude Code tekshiradi (npm run build + backendga solishtirish)
```
Shablon: [`prompt.md`](./prompt.md). Faza 2 faqat tegishli modulning
Faza 1 tahlili `ACCEPTED` bo'lgandan keyin boshlanadi.

Ikkala fazada ham: `tasks/ → task_pending/ → task_compliete/ → status/`
umumiy lifecycle (qarang: [`requirements.MD`](./requirements.MD) 3-bo'lim).

- **`../backend_crud_review/`** (top-level, `orcestor/` yonida) — Faza 1
  natijalari, modul nomi bilan fayllangan (`auth.md`, `company.md`, ...).
  Faza 2 uchun yagona ishonchli manba.
- **`../skills/`** (top-level) — AGY fon rejimida yuklagan texnik
  ko'nikma/pattern hujjatlari (NestJS API contracts, Angular typed HTTP
  servis, JWT guard oqimi, DTO validation, error handling) — task
  yozishda uslub/kontekst sifatida ishlatiladi.
- **`analysis/`** — bo'sh, zaxira (agar `backend_crud_review/` yetarli
  bo'lmasa qo'shimcha ichki eslatmalar uchun).
- **`history/`** — yakunlangan sikllarning qisqartirilgan arxivi.

## 4. Holat (2026-07-25) — Faza 1 TUGADI, papka egasi almashdi

**Faza 1 (backend tahlili) 17/17 modul ACCEPTED** — to'liq jadval:
[`tasklist.md`](./tasklist.md), har birining tafsiloti `status/B-A-*.log`.

**MUHIM (2026-07-25, Fayzillo buyrug'i — konfliktning oldini olish
uchun):** Faza 1 tugagach, bu `zdes/orcestor/` papkasi (va
`../front_integration_tasks/`, `../front_agent.md`) endi **API
integratsiya (Faza 2) bilan shug'ullanuvchi parallel sessiyaning to'liq,
mustaqil hududi** hisoblanadi. Backend-tahlil sessiyasi (shu hujjatni
yozgan sessiya) bu yerdan **`test-zdes-front/orcestor/`ga ko'chdi** —
u yerda mavjud T-0XX tizimi orqali frontend responsive/dark-mode/forma
ishlarini olib boradi (backend tahliliga aloqasi yo'q, sof frontend-dev
ish). Ikkala sessiya endi bir-birining fayllariga tegmaydi — bu shu
ko'chish orqali ta'minlanadi.

## 5. Havolalar

- [`./requirements.MD`](./requirements.MD) — qoidalar, rollar, AGY
  ishonchlilik saboqlari (eski loyihadan meros, muhim)
- [`./prompt.md`](./prompt.md) — AGY task-dispatch shabloni
- [`./dispatch.py`](./dispatch.py) — task lifecycle CLI (`new`/`send`/`complete`/`status`/`check`)
- Andoza olingan manba: `../test-zdes-front/orcestor/` (o'sha loyihaning
  o'zi uchun alohida, hali ham amal qiladigan tizim — bu yerdagisi bilan
  ARALASHTIRILMAYDI, ikkalasi mustaqil)


## Manba: `my_digital_brain/30_Resources/learning/ai_orchestration/ai_orchestration_best_practices.md`

# AI Orchestration va Multi-Agent Tizimlari: Amaliyot va Qoidalar

**Sana:** 2026-yil, 23-avgust
**Kontekst:** `zdes_employee_panel` loyihasini noldan to'liq orkestratsiya yordamida qurish tajribasidan olingan xulosalar va arxitektura namunalari.

Ushbu hujjat AI agentlari bilan parallel ishlash, vazifalarni taqsimlash (task management), to'siqlarni yechish (blockers) va to'qnashuvlarni oldini olish (collision avoidance) kabi real amaliyotda uchragan bilimlarni kelajak uchun saqlaydi.

---

## 1. Planlash va Tasklarni Maydalash (Granular Tasks)

Eng muhim kashfiyotlardan biri: Bitta agentga juda katta qamrovli vazifa berish (masalan: bitta faylda 5 ta sahifani va state managementni qilish) qat'iy xatodir. Bu kontekstni to'ldirib yuboradi va "Quota limit" yoki mantiqiy chalkashliklarga olib keladi.

### Optimal yechim (Pipeline):
1. **Planner Agent:** Umumiy arxitektura va hujjatlarni o'qib `master_plan.md` tuzadi.
2. **Step Writer Agent:** Rejani qadamlarga ajratadi (`steps.md`).
3. **Task Splitter Agent (Maydalovchi):** Qadamlarni **faqat bitta logik maqsadga** qaratilgan o'nlab mayda .task.md fayllariga bo'ladi (Masalan: `T-004_layout_auth.task.md`, `T-009_dashboard.task.md`).
4. **Task Reviewer Agent:** Barcha tasklarni sifat nazoratidan o'tkazadi va referenslarni tekshiradi.

---

## 2. To'siqlarni yechish (Blocker and Sub-task Protocol)

Agent biror taskni bajarayotganda kutilmagan muammoga duch kelsa, asosiy taskni buzib qo'ymasligi yoki to'xtab qolmasligi uchun tizimli yondashuv o'ylab topildi.

Har bir task faylining oxiriga quyidagi qoida majburiy qo'shiladi:
> ⚠️ **Diqqat:** Agar ushbu taskni bajarish davomida biror blocker (to'siq) yoki muammo chiqsa, uni hal qilish yuzasidan yo'riqnoma va sub-task ochish qoidalari uchun ushbu hujjatlarni reference qiling: `skill_sub_management_planning_information_docs/blocker-va-subtask/qoida.md`.

**Qoida qanday ishlaydi:**
- Muammo asosiy taskdan mustaqil bo'lsa -> parallel sub-task ochiladi (`orcestor/sub_tasks/` da).
- Muammo asosiy taskka bog'liq bo'lsa -> ketma-ket sub-task ochilib, avval o'sha yechiladi.

---

## 3. Loyiha qoidalari (Standing Rules)

`orcestor/standing_rules.json` fayli tizimning "konstitutsiyasi" hisoblanadi. Undagi eng muhim qoidalar:

### A) Global State & Backend
- Barcha global state faqat **Zustand** orqali. Lokal state uchun `useState`.
- Backend papkasi faqat o'qish uchun, unga teginish taqiqlanadi.

### B) Sifat nazorati (Monitoring & Fix)
- Har bir coding task tugagach, avtomatik ravishda **Monitoring_Fix_Agent** ishga tushadi. 
- U sahifalarning SSR (Server-Side Rendering), Skeleton animatsiyalari va umumiy Next.js talablariga javob berishini tekshiradi. Xato bo'lsa `sub_tasks/` da fix ochadi.

### C) Multi-Agent To'qnashuvining oldini olish (Collision Avoidance) 🚀
Bu qoida parallel agentlar ishlaganda Git conflict yoki kod buzilishini yechadi:
> **Qoida:** "Monitoring_Fix_Agent fayllarni o'zgartirishdan oldin `orcestor/task_pending/` papkasida hozirda ishlayotgan boshqa agentlar vazifalarini ko'rib chiqishi va ularga daxldor bo'lgan fayllarga tegmasligi shart."
- Agent atrofidagi boshqa agentlar qaysi fayllar bilan "band" ekanini (Context Awareness) his etadi. Band fayllarni o'tkazib yuboradi.

---

## Xulosa
Multi-agent orkestratsiyasida muvaffaqiyat garovi qattiq va intizomli infrastruktura hisoblanadi. Vazifalarning mantiqiy maydalanishi (1 task = 1 aniq maqsad), xatolarni sub-task orqali hal etilishi va agentlarning bir-biriga halal bermasligi (Collision avoidance) ushbu tajribadagi eng yirik yutuqlardir.

## 4. Real loyiha natijasi: Muvaffaqiyat ko'rsatkichi (23-Avgust kuzatuvi)
Orkestratsiya davomida 18 ta vazifadan 12 tasi (Infratuzilma, Layoutlar, Auth va asosoiy Panel sahifalari) to'liq yakunlandi va `task_compliete` papkasiga o'tdi. Eng e'tiborli jihati — **`sub_tasks` papkasi hanuzgacha bo'sh**.

**Xulosa:** Tasklarning qamrovi kichraytirilgani (Granular splitting) hamda har bir sahifaning oldindan hujjatlashtirilgani (Page Specs) tufayli agentlar orasida mantiqiy chalkashliklar, API ulanishidagi xatolar yoki "blocker" holatlari umuman yuzaga kelmadi. Sifat nazorati va to'g'ri rejalashtirish to'g'ridan-to'g'ri loyiha tezligini (0% to'xtalish) ta'minladi.


## Manba: `zdes_archive_docs/raw_history/orcestor/front-requirements.MD`

# Talablar: Qoidalar va Rollar (Requirements)

Ushbu hujjat `orcestor/` papkasi orqali ishlaydigan fayl-asosli multi-agent
orkestratsiya tizimining **majburiy qoidalari va rollarini** belgilaydi.
Loyihaning barcha ishtirokchilari (Claude Code, AGY, Fayzillo) shu qoidalarga
rioya qiladi. Qoidaga zid harakat — xato hisoblanadi, hatto natija "ishlagan"
bo'lsa ham.

---

## 1. Rollar jadvali

| Rol | Kim / Nima | Mas'uliyat | Vakolat darajasi | Nima qila oladi | Nima qila OLMAYDI |
|---|---|---|---|---|---|
| **Claude Code** | Orkestrator (AI) | Vazifalarni bo'laklarga bo'lish, task fayllarini yozish, AGY natijasini tekshirish, kodni `src/`ga integratsiya qilish, arxitektura va sifat nazorati | **Yakuniy texnik vakolat** (final technical authority) | Task yaratish/tahrirlash, kodni review qilish, `src/`ga merge qilish, arxitekturaviy qaror qabul qilish, AGY natijasini rad etish | Ishlab chiqarish muhitiga (production) to'g'ridan-to'g'ri deploy qilish; Fayzilloning roziligisiz risky/keng qamrovli o'zgarishlarni yakunlash |
| **AGY** | Google Antigravity IDE (Gemini-asosli) sub-agent / ijrochi | `task_pending/`dagi vazifalarni bajarish — real kod yozish, ishga tushirish, test qilish | **Ijrochi vakolat** — faqat topshirilgan task doirasida | Kod yozish, mavjud kodni o'zgartirish (task doirasida), natijani `task_compliete/`ga topshirish | Claude Code bilan to'g'ridan-to'g'ri bog'lanish (API yo'q); main/production branchga bevosita push qilish; task doirasidan tashqari qaror qabul qilish; o'z ishini o'zi "tasdiqlangan" deb belgilash |
| **Fayzillo** | Inson — supervisor / ko'prik (bridge) | Claude Code va AGY o'rtasida qo'lda ma'lumot tashish (task va natijalarni copy-paste qilish), xavfli holatlarda yakuniy qaror | **Eng yuqori — inson nazorati** (final say on risky items) | Har qanday vazifani to'xtatish, bekor qilish, qayta yo'naltirish; xavfli/norouten holatlarda yakuniy "ha/yo'q" qarorini berish | Kodni Claude Code review qilmasdan to'g'ridan-to'g'ri mainga kiritish (favqulodda holatlar bundan mustasno va alohida qayd etiladi) |

**Muhim:** AGY va Claude Code o'rtasida to'g'ridan-to'g'ri API aloqasi yo'q —
har bir uzatish Fayzillo orqali qo'lda amalga oshiriladi. Shu sababli har bir
task fayli **o'z-o'zidan tushunarli (self-contained)** bo'lishi shart.

---

## 2. Qattiq qoidalar (Hard Rules)

1. **Production/main himoyasi.** AGY hech qachon `main` yoki production
   branchga bevosita tegmaydi yoki push qilmaydi. Barcha o'zgarishlar avval
   Claude Code tomonidan review qilinadi, so'ng Fayzillo orqali integratsiya
   qilinadi.
2. **"Bajarildi" deb hisoblash faqat statusdan keyin.** Claude Code hech
   qachon biror task "tugadi" deb faraz qilmaydi — bu faqat tegishli
   `status/` yozuvi mavjud va tasdiqlangan bo'lsa haqiqiy hisoblanadi. AGY
   xabari yoki Fayzilloning og'zaki tasdig'i yetarli emas — status fayli
   yozilishi shart.
3. **Review majburiy.** Har qanday kod o'zgarishi `src/`ga qo'shilishidan
   oldin Claude Code tomonidan ko'rib chiqilishi (review) shart. Review
   o'tmagan kod integratsiya qilinmaydi.
4. **Maxfiy ma'lumotlar taqiqlanadi.** API kalitlar, parollar, tokenlar,
   `.env` qiymatlari va boshqa sirlar hech qachon task fayllariga, status
   yozuvlariga yoki session loglariga yozilmaydi — bu fayllar oddiy matn
   (plain text) bo'lib, tarixda doimiy saqlanadi va istalgan vaqt qayta
   o'qilishi mumkin.
5. **Har bir o'zgarish izlanadigan (traceable) bo'lishi kerak.** Qaysi task
   qaysi commit/faylga olib kelganini keyinchalik aniqlash imkoni bo'lishi
   shart — shuning uchun task ID va status yozuvlari izchil yuritiladi.
6. **Papka nomlarini o'zgartirmaslik.** `task_compliete/` nomidagi xatoni
   ("complete" emas, "compliete") ataylab tuzatmaslik — mavjud struktura
   bilan mosligini saqlash uchun aynan shu nom ishlatiladi.

---

## 3. Vazifa hayot sikli (Task Lifecycle)

Har bir task quyidagi bosqichlar orqali harakatlanadi:

```
tasks/  →  task_pending/  →  task_compliete/  →  status/
```

| Bosqich | Papka | Kim yaratadi / ko'chiradi | Tavsif |
|---|---|---|---|
| 1. Backlog | `tasks/` | **Claude Code** | Yangi task yoziladi: aniq maqsad, qamrov (scope), kerakli fayllar/pointerlar. Hali hech kimga topshirilmagan. |
| 2. Dispatch | `task_pending/` | **Claude Code** yozadi → **Fayzillo** AGYga uzatadi | Task bajarish uchun tayyor deb belgilanadi va Fayzillo uni Antigravitydagi AGY agentiga qo'lda kiritadi. |
| 3. Bajarildi | `task_compliete/` | **Fayzillo** (AGY natijasini qo'lda ko'chiradi) | AGY natijasini (kod, diff, izoh) shu yerga qo'yadi. Bu hali "tasdiqlangan" degani emas — faqat "ijrochi tugatdi" degani. |
| 4. Tekshiruv va yopish | `status/` | **Claude Code** | `task_compliete/`dagi natijani review qiladi, qaror yozadi: `ACCEPTED`, `REJECTED`, yoki `NEEDS_REVISION`. Faqat shu yozuvdan keyin task "yopiq" hisoblanadi. |

**Qo'shimcha qoida:** agar task `NEEDS_REVISION` bo'lsa, u qayta `tasks/`ga
(yoki to'g'ridan-to'g'ri `task_pending/`ga, aniq tuzatish izohi bilan)
qaytariladi — status faylida sabab aniq yozilishi shart.

---

## 4. Eskalatsiya qoidasi (Escalation Rule)

Agar AGY:
- vazifani bajara olmasa (stuck),
- noaniq/qarama-qarshi natija chiqarsa,
- yoki **xavfli** o'zgarish taklif qilsa (masalan: ma'lumotlar bazasi
  migratsiyasi, auth logikasi, katta refactor, `package.json`/dependency
  o'zgarishi, production konfiguratsiyasi),

— bunday holatlar **avtomatik qayta urinilmaydi (no blind auto-retry)**.
Buning o'rniga:

1. Holat **Fayzilloga** yetkaziladi (u AGY ekranida buni ko'radi).
2. Fayzillo natijani **Claude Code**ga qaytaradi (masalan `task_compliete/`
   ga xato/qisman natija bilan yoki alohida izoh bilan).
3. Claude Code holatni tahlil qiladi va yo: (a) taskni aniqroq qilib qayta
   yozadi, (b) taskni kichikroq qismlarga bo'ladi, yoki (c) Fayzilloga
   inson qarori kerakligini bildiradi.
4. Faqat shundan keyin task qayta `task_pending/`ga qaytariladi.

Xavfli deb topilgan har qanday natija **hech qachon** Fayzillo yoki Claude
Code tasdig'isiz `src/`ga kiritilmaydi.

---

## 5. Token / xarajat intizomi (Token & Cost Discipline)

Fayl-asosli tizim odam tomonidan qo'lda ko'chiriladi va AI kontekst
oynasidan foydalanadi — shuning uchun:

1. **Task tavsiflari qisqa va aniq qamrovli bo'lishi kerak.** Har bir task
   bitta aniq maqsadga ega bo'lsin — "hamma narsani tuzat" kabi noaniq
   topshiriqlar taqiqlanadi.
2. **To'liq fayllarni tashlamaslik.** Agar fayl allaqachon mavjud bo'lsa,
   uning **yo'li (path)** va o'zgartirilishi kerak bo'lgan **aniq
   qism/qator** ko'rsatiladi — butun fayl matni task ichiga
   ko'chirilmaydi, faqat zarur bo'lgan diff yoki qisqa parcha keltiriladi.
3. **Pointer > Copy.** Kontekst uchun fayl nusxasi o'rniga fayl yo'liga
   (`src/app/...`) havola berish afzal — bu ham token, ham inson vaqtini
   tejaydi.
4. **Ortiqcha tarixni qaytarmaslik.** Yangi task yozishda avvalgi
   sessiyalarning to'liq loglari emas, faqat `history/`dagi **xulosalangan
   (distilled)** ma'lumot ishlatiladi.
5. **Status yozuvlari ham qisqa bo'ladi.** `status/`ga natijani tavsiflovchi
   qisqa, struktura holatini (`ACCEPTED`/`REJECTED`/`NEEDS_REVISION`) va
   sababini yozish yetarli — uzun muhokama emas.

---

## 6. AGY kvota nazorati va model-switch qoidasi (2026-07-25)

`agy` CLI orqali fire-and-forget dispatch qilinganda, AGY'ning kvotasi
(odatda default Gemini Flash tier) sessiya davomida tugab qolishi mumkin —
xato aniq ko'rinishda qaytadi: `Error: Individual quota reached... Resets
in <vaqt>`.

**Muhim: `/usage` orqali oldindan tekshirib bo'lmaydi.** `agy --print
"/usage"` sinab ko'rilgan — bu real kvota ma'lumotini qaytarmaydi (model
shunchaki umumiy javob "hallutsinatsiya" qiladi, chunki headless `--print`
rejimida hisob balansiga haqiqiy tool-access yo'q). Demak kvotani oldindan
bilishning ishonchli usuli yo'q — buning o'rniga quyidagi reaktiv qoida
qo'llaniladi:

1. Har bir `agy --print` chaqiruvida **aniq model ko'rsatilsin**
   (`--model gemini-3.1-pro-low`) — sukut bo'yicha Flash tier ishlatiladi,
   u tezroq tugaydi.
2. Agar chaqiruv "Individual quota reached" xatosi bilan qaytsa:
   - Avval keyingi model darajasiga o'ting (masalan
     `gemini-3.1-pro-low` → `gemini-3.1-pro-high`, keyin zarurat bo'lsa
     Gemini bo'lmagan variantlar: `claude-sonnet-4-6`,
     `gpt-oss-120b-medium`).
   - Agar barcha modellar ham kvota xatosi bersa, xatoda ko'rsatilgan
     "Resets in Xh Ym" vaqtigacha **hech qanday qayta urinish qilinmaydi**
     — AGY-bog'liq barcha ishlar to'xtatiladi, faqat Claude Code o'zi
     bajaradigan (AGY'siz) task'lar davom ettiriladi.
3. `agy models` buyrug'i orqali mavjud modellar ro'yxati olinadi —
   ro'yxat vaqti-vaqti bilan o'zgarishi mumkin, shuning uchun qattiq
   kodlanmagan, har safar tekshirilsin.

Batafsil topilmalar va real misollar: Claude Code xotirasidagi
`agy-cli-dispatch-reliability` yozuvi.

---

## 7. `project_docs/api/` — hujjatlarni doimiy yangilab borish qoidasi (2026-07-25)

T-020/T-021/T-022 orqali `project_docs/api/` ichida har bir modul uchun
API endpoint + tip + state hujjati yaratildi (`README.md` — yakuniy
indeks). Bu hujjat **bir martalik snapshot emas** — loyiha davom etar
ekan, quyidagi holatlarda **shu hujjatlar ham majburiy yangilanadi**:

1. **Yangi endpoint qo'shilsa yoki mavjudi o'zgarsa** (metod, yo'l, so'rov/
   javob tipi) — tegishli `project_docs/api/<modul>.md` faylidagi
   "Endpoint'lar" jadvali darhol yangilanadi.
2. **Yangi model/tip qo'shilsa yoki mavjudi o'zgarsa**
   (`src/app/core/models/*.ts` yoki feature ichidagi tiplar) — "Tiplar"
   bo'limi shu bilan sinxron tutiladi.
3. **Sahifa/komponentning state boshqaruvi o'zgarsa** (masalan oddiy
   propertydan `signal()`ga o'tilsa, yoki yangi state o'zgaruvchi
   qo'shilsa) — "State" jadvali yangilanadi.
4. **Butunlay yangi modul/feature qo'shilsa** (masalan T-032 — Auth
   `/sign` sahifasi) — o'sha modul uchun **yangi** `project_docs/api/
   <modul>.md` yozilishi va `project_docs/api/README.md` indeksiga
   qo'shilishi shart.
5. **Kim yangilaydi:** hujjat yangilanishi tegishli task/AGY-dispatchning
   **Definition of Done** qismiga aniq band sifatida kiritiladi — ya'ni
   kod o'zgarishini bajaruvchi task (masalan T-025 Axios, T-032 Auth
   `/sign`) o'z DoD'ida "tegishli `project_docs/api/*.md` fayli(lari) ham
   yangilangan" shartini o'z ichiga oladi. Claude Code yangi task
   yozayotganda buni unutmasligi kerak.
6. **Review paytida tekshiriladi:** Claude Code kod o'zgarishini
   `task_compliete/`ga yopishdan oldin, agar o'zgarish API/tip/state'ga
   tegsa, mos `project_docs/api/*.md` fayli ham yangilanganini
   tasdiqlaydi — aks holda task `NEEDS_REVISION` deb qaytariladi (4-bo'lim,
   Eskalatsiya qoidasi ruhida).

Maqsad: `project_docs/api/` doim kodning **haqiqiy joriy holatini**
aks ettirsin — vaqt o'tishi bilan eskirib, chalg'ituvchi hujjatga
aylanmasin.

---

*Ushbu hujjat `orcestor/` tizimining barcha ishtirokchilari uchun
majburiydir. O'zgartirish faqat Claude Code tomonidan, Fayzillo bilan
kelishilgan holda amalga oshiriladi.*


## Manba: `my_digital_brain/10_Projects/orcestor-skill/status.md`

# orcestor-skill — ish jurnali

**Holat: ✅ birinchi versiya tayyor, funksional sinovdan o'tgan.**
Manba: shu papka. O'rnatilgan (global): `~/.claude/skills/orcestor-start/`.

## Nima bu

Portativ Claude Code Skill (`orcestor-start`) — loyihada ko'p agentli
orkestratsiyani (Orchestrator/Executor/Supervisor rollari bilan) bitta
komanda ("orkestratsiya boshla" yoki "README.md'ni o'qi") orqali ishga
tushiradi yoki mavjud sessiyani davom ettiradi. `new_fixing_orcestration_system/`
rejasidagi "small context backup" konsepsiyasi va `zdes/orcestor` (eski,
ishlab turgan tizim) tahlili asosida qurilgan — batafsil kelib chiqishi
o'sha papkada, bu yerda faqat yakuniy artefakt va qurish jarayonidagi
topilmalar.

## Asosiy arxitektura qarorlari

- **Rol-token konvensiyasi**: `Supervisor_User` / `Orcestor_Agent` /
  `Executer_Agent` — haqiqiy ism FAQAT bitta faylda (`orcestor.config.env`,
  `.env` uslubi). Boshqa hech bir hujjatda shaxsiy ism yo'q (tekshirilgan,
  toza).
- **`Executer_Agent` doim `agy`** (Antigravity CLI), `Orcestor_Agent` esa
  ixtiyoriy (Claude Code, Codex, va h.k.).
- **Ikki tracking rejimi**: `file` (papka-lifecycle, zdes uslubi) va `db`
  (3 dvigatel: `sqlite` / `postgres` / `mysql` — tanlov foydalanuvchiniki,
  skill faqat tavsiya beradi).
- **`simple_context.md`** — majburiy, qisqa (200-400 so'z) checkpoint;
  restart faqat Supervisor_User so'raganda (qattiq prompt-limit yo'q).
- **`project_status/overview.md`** — ESKI loyihalar uchun, doimiy
  to'planadigan bilim (struktura/qoidalar/tarix/muammolar), Executer_Agent
  orqali tezkor/tejamkor tahlil qilinadi.
- **Til tanlash** — bootstrap'ning ENG BIRINCHI qadami, ikki tilda so'raladi.
- **README.md o'zi trigger** — AI agent shu faylni o'qisa, avval qisqa
  tushuntiradi, keyin "boshlaymizmi?" deb so'raydi (darhol savol-javobga
  sakramaydi).

## Konflikt-himoya (eng ko'p vaqt shu yerga ketdi)

- **DB rejimi**: `task claim` — atomik (Postgres: `FOR UPDATE SKIP LOCKED`;
  MySQL: bitta tranzaksiyada SELECT+UPDATE; SQLite: bitta connection ichida
  UPDATE+rowcount). Barcha 5 jadvalga (`tasks`, `task_events`,
  `changed_files`, `standing_rules`, `session_checkpoints`) `workspace_path`
  ustuni qo'shildi — bitta DB bir nechta loyiha orasida ulashilsa ham,
  har bir so'rov shu ustun bilan filtrlanadi (real testda tasdiqlangan: SQLite
  va Postgres'da begona workspace_path'li qatorlar ko'rinmaydi/tegilmaydi).
- **Konteyner qayta ishlatish**: bootstrap'da mavjud `orcestor-db*`
  konteynerlarni tekshirib, foydalanuvchidan qayta ishlatish yoki yangi
  yaratishni so'raydi. Qayta ishlatilsa — `POSTGRES_DB`/`MYSQL_DATABASE`
  albatta loyihaga xos (masalan `orcestor_<loyiha-nomi>`). Baza mavjud
  bo'lmasa avtomatik yaratiladi (real testda tasdiqlangan: bitta konteyner,
  ikkita loyiha, ikkita baza — aralashmadi).
- **File rejimi**: claim — fayl `tasks/`→`task_pending/`ga ATOMIK ko'chirish
  (mv/rename) orqali; "topilmadi" xatosi normal (boshqa sessiya oldi).
  Workspace-aro himoya: `WORKSPACE_PATH` (mutlaq yo'l) bootstrap'da
  yoziladi, Resume'da solishtiriladi — mos kelmasa (papka ko'chirilgan
  bo'lsa) ogohlantirish beriladi.

## Topilgan va tuzatilgan real xatolar (AGY gallyutsinatsiyasi — qo'lda tekshirib topilgan)

Bular — `04-taxminlar-va-tekshirish.md` 4.2-banddagi "AGY ishonchlilik
pattern"ining amaliy tasdig'i, shu skillni qurish jarayonida:

1. DB yo'li nomuvofiqligi (`.orcestor` vs `orcestor/db`) — birinchi
   qoralamada.
2. `scripts/orcestor.py`ning sxemasi `templates/db-schema.sql`dan
   butunlay farq qilardi (3 vs 5 jadval) — yagona sxema-manbaga
   birlashtirildi.
3. `standing_rules.example.json`da eski "5 promptdan keyin /clear"
   qoidasi — yangi kelishuvga (foydalanuvchi nazorati) zid edi.
4. **Jiddiy**: `MySQLAdapter.claim_task()` ikkita ALOHIDA `docker exec`
   chaqiruvida ishlagani uchun tranzaksiya/lock ikkinchisigacha
   saqlanmasdi — "atomik claim" aslida atomik emas edi. Bitta chaqiruvga
   birlashtirib tuzatildi.
5. **Jiddiy, faqat live-testda topildi**: `psql`da `-q` bayrog'i yo'qligi
   sababli, RETURNING natijasidan keyingi "UPDATE N" xizmatchi qatori
   soxta "ma'lumot qatori" sifatida parse qilinardi — 0 mos qator bo'lganda
   ham soxta "claimed" natija chiqarardi. `-q` qo'shib tuzatildi, qayta
   test qilindi.

**Xulosa**: agy natijasini hech qachon ko'r-ko'rona qabul qilmaslik kerak —
kamida asosiy oqim (happy path + zero-result holat) qo'lda/real muhitda
sinab ko'rilishi shart, chunki xatolar ko'pincha faqat chekka holatlarda
(zero rows, ikki alohida chaqiruv orasidagi tranzaksiya) ko'rinadi.

6. **Foydalanuvchi real sinovda topdi (2026-08-04, `GoogleAiStudio` test
   papkasida)**: `agy`ni Executer_Agent qilib skill sinalganda, boshida
   yaxshi ishladi, keyin agy o'zicha `src/` papka ochib, so'ralmagan
   Angular loyihasi yoza boshladi.
   - **Birinchi gipoteza (RAD ETILDI):** agy'da loyihalar-aro "xotira"
     bor deb o'ylandim, `conversation_summaries.db`dagi `workspace_uris`
     ustunini asos qilib. Bu YETARLI ISBOT emas edi — keyingi tekshiruv
     (foydalanuvchi tomonidan, boshqa terminalda) buni rad etdi.
   - **Aniq, tasdiqlangan sabab:** `task-18.log`da `file://` havolalar
     orqali isbotlandi — bu gallyutsinatsiya/xotira EMAS, mexanik bug:
     Orcestor rolida ham `agy` ishlatilgan edi (foydalanuvchining "agy->agy"
     variantida), va SKILL.md ko'rsatmasi bo'yicha ICHKI/NESTED `agy -p
     "..." --dangerously-skip-permissions` chaqirilganda **hech qanday
     aniq path argumenti berilmagan edi**. Natijada ichki chaqiruv ambient
     `cwd`ga tayandi, bu esa joriy (GoogleAiStudio) emas, balki BOSHQA,
     oldin faol bo'lgan real Angular loyihaga (`.../test-zdes-front`)
     ishora qilardi. Executer_Agent o'sha (noto'g'ri, lekin haqiqiy)
     loyihani 100% aniq tahlil qildi, lekin natijani "joriy loyihaga
     tegishli" deb qaytardi — tashqi Orcestor (agy) buni tekshirmasdan
     qabul qilib, Angular tasklar yarata boshladi.
   - **Tuzatish (`SKILL.md` 1.1-band, to'g'rilangan sabab bilan qayta
     yozildi):** endi eski "scope-lock/--new-project" gipotezasi o'rniga
     ANIQ, mexanik talab: har `agy -p` chaqiruvi MAJBURIY `cd
     "<WORKSPACE_PATH>" && agy -p ...` shaklida, hech qachon argumentsiz/
     ambient-cwd'ga tayanmasdan. Orcestor_Agent uchun ham KONKRET
     tekshirish protsedurasi qo'shildi (o'zi `ls`/`find` bilan 1-2 faktni
     qo'lda solishtirishi shart, shunchaki "tekshirdim" deyish yetarli
     emas).
   - **Sinalmagan** — bu tuzatish hali qayta shu stsenariyda (ichki
     agy->agy chaqiruv, noto'g'ri cwd) tekshirilmagan.

## Sinovdan o'tgan (tasdiqlangan)

- SQLite: to'liq CRUD + claim + rule upsert + workspace izolyatsiyasi.
- Postgres: xuddi shu, ikki marta (bir marta xato bilan, bir marta
  tuzatilgandan keyin) + konteyner-qayta-ishlatish stsenariysi.

## Sinalmagan (ochiq qoldi)

- MySQL yo'li — faqat kod darajasida ko'rib chiqilgan, live-test
  qilinmagan (Docker bilan haqiqiy MySQL konteynerda sinash kerak).
- Fayl-rejimidagi atomik claim (mv/rename) — mantiqan to'g'ri, lekin
  amalda ikkita parallel jarayon bilan sinalmagan.


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ovovo******utvata@gmail.com/claude_usage_tahlili.md`

# Claude usage tahlili

### 👤 Foydalanuvchi:

Usage
Session (5hr)
0%
Weekly (7 day)
79%
Resets in 2d
Manage usage on claude.ai
What’s contributing to your limits usage?
Day
Week
Approximate, based on local sessions on this machine — does not include other devices or claude.ai
Last 7d · these are independent characteristics of your usage, not a breakdown
82% of your usage was at >150k context
Longer sessions are more expensive even when cached. /compact mid-task, /clear when switching to new tasks.
20% of your usage came from subagent-heavy sessions
Each subagent runs its own requests. Be deliberate about spawning them — and consider configuring a cheaper model for simpler subagents.
18% of your usage came from sessions active for 8+ hours
These are often background/loop sessions. Continuous usage can add up quickly so make sure it is intentional.
Skills
% of usage
/update-config
2%
Subagents
% of usage
fork

bu claude /usage dan qaytgan data

### 🤖 ChatGPT:

Bu hisobotdan ko'rinib turibdiki, sening limitingni asosan **token/context** yeyapti, so'rovlar soni emas.

Tahlil:

- **Session (5hr): 0%**
  - Hozirgi 5 soatlik sessiyada deyarli limit ishlatilmagan.

- **Weekly (7 day): 79%**
  - Haftalik limitning 79% ishlatilgan.
  - 2 kundan keyin reset bo'ladi.

Asosiy sabablar:

### 1. 82% usage was at >150k context ⭐⭐⭐⭐⭐
Bu eng katta muammo.

150k+ context degani Claude har safar:
- eski chatlarni ham o'qiydi,
- yangi promptni ham qo'shadi,
- javob yozadi.

Chat qancha uzunlashsa, har bir yangi xabar shuncha qimmatlashadi.

Shuning uchun ular tavsiya qilmoqda:
- `/compact` — eski conversationni qisqartirib memory qiladi.
- `/clear` — yangi task boshlaganda historyni tozalaydi.

---

### 2. 20% usage came from subagent-heavy sessions

Sen ko'p ishlatayotgan narsa:

```
Task(...)
```

yoki

```
fork
```

Har bir subagent alohida Claude request qiladi.

Masalan:

```
Main agent
 ├── Backend agent
 ├── Frontend agent
 ├── DB agent
 └── Security agent
```

Bu 4-5 ta alohida request hisoblanadi.

---

### 3. 18% usage came from sessions active for 8+ hours

Claude Code 8-10 soat terminalda ochiq qolgan.

Masalan:

```
claude
```

ochib qo'yasan.

Keyin:

```
npm run dev
```

```
git status
```

```
Task(...)
```

```
continue
```

hammasi bitta sessionda ketadi.

Bu ham contextni ulkan qiladi.

---

### Skills

```
/update-config
2%
```

Bu deyarli ta'sir qilmagan.

---

### Subagents

```
fork
```

Demak asosan `fork` subagent ishlatilgan.

---

## Xulosa

Sening limitingning taxminan:

- **82%** — juda katta context (150k+ token).
- **20%** — subagent (`Task`, `fork`) ishlatilishi.
- **18%** — 8+ soat davom etgan uzun sessiyalar.

Shuning uchun limitni ancha tejash uchun:

1. Har bir yangi loyiha yoki mavzuda `/clear` ishlat.
2. Chat juda kattalashsa `/compact` qil.
3. Kerak bo'lmaganda `Task`/`fork` subagentlarini ishga tushirma.
4. Claude Code'ni kunlab bitta sessiyada ishlatish o'rniga, ish tugagach chiqib, keyin yangi sessiya och.

Shu hisobotdan ko'rinib turibdiki, eng katta foyda beradigan optimizatsiya aynan **context hajmini kamaytirish** bo'ladi; qolgan omillar undan ancha kichik ta'sir ko'rsatmoqda.

---

### 🤖 ChatGPT:

Siz faqat ZIP yubordingiz, lekin nima qilishimni yozmadingiz. ZIP ichini ocha oldim — unda `orcestor/` papkasi va taxminan **64 ta fayl** bor.

Nima qilishimni ayting, masalan:

- Strukturani tahlil qilish.
- README va arxitekturani tekshirish.
- Kodni review qilish.
- Xatolarni topish.
- Responsive yoki frontendni tekshirish.
- Claude usage'ga bog'liq nimadirni tekshirish.
- Yoki boshqa aniq vazifa.

Qaysi biri kerak?

---

### 👤 Foydalanuvchi:

BU orcetratsiya file base tizimi papkasi

### 🤖 ChatGPT:

Tushunarli. Demak bu **orchestratsiya file-based tizimi** uchun papka ekan.

Oldingi suhbatlardan eslayman, sening g'oyang quyidagicha edi:

- Fayllarda faqat **prompt**, **qoida**, **reference** va task tavsifi saqlanadi.
- Holat (status), tarix, queue va orchestration ma'lumotlari esa **SQLite/PostgreSQL** bazasida bo'ladi.
- Orchestrator kerakli taskni `WHERE status = ... LIMIT ...` bilan olib ishlaydi.
- Bu yondashuv millionlab tasklarga ham mos keladi.

Agar bu ZIP o'sha tizimning joriy versiyasi bo'lsa, men quyidagilarni tekshirib bera olaman:

1. **Arxitektura** — papkalar va fayllar mantiqan to'g'ri ajratilganmi.
2. **Scalability** — minglab yoki millionlab tasklarda qanday ishlaydi.
3. **Kamchiliklar** — keyinchalik muammo beradigan joylar.
4. **Soddalashtirish** — qayerlarni ixchamlashtirish mumkin.
5. **AI agent workflow** — Claude/GPT agentlari bilan ishlash uchun qanchalik qulay.
6. **Production readiness** — real loyihada ishlatishga tayyormi.

Men uni oddiy kod review emas, balki **tizim dizayni (System Design)** nuqtai nazaridan tahlil qilaman va kuchli hamda zaif tomonlarini aytaman.

---

### 👤 Foydalanuvchi:

Token sarfiga tasirini aniqlashing uchun ichidagi md larni o'qib chiq

### 🤖 ChatGPT:

Ha, ko'rib chiqdim. Ichida **39 ta `.md` fayl** bor.

Taxminan:
- **~80 000 belgi**
- **~8 500 ta so'z**
- Bu LLM uchun taxminan **11–18 ming token** (til va Markdown tuzilishiga qarab).

### Token sarfiga ta'siri

Agar sen **har bir taskda butun `orcestor/` papkasini contextga bersang**:

- Faqat orkestratsiya hujjatlarining o'zi **10–20k token** yeydi.
- Ustiga kod, foydalanuvchi so'rovi va javob qo'shilsa, 30–100k token juda tez yig'iladi.
- Claude Usage'dagi **`82% of your usage was at >150k context`** holatiga aynan shunday yondashuv sabab bo'lishi mumkin.

### Lekin yaxshi tomoni ham bor

Men ko'rgan tuzilmada:
- `steps/01-intake.md`
- `steps/02-dispatch.md`
- `steps/03-execution.md`
- ...
- `prompt.md`
- task response fayllari

ularning aksariyati **mustaqil**. Ya'ni har bir task uchun hammasini o'qish shart emas.

Masalan:

- Intake bosqichida → faqat `01-intake.md`.
- Dispatchda → `02-dispatch.md` va `prompt.md`.
- Reviewda → `04-review.md`.
- Loggingda → `06-logging.md`.

Shunda har bosqichga **500–2000 token** atrofida qo'shiladi, 15–20 ming emas.

### Men tavsiya qiladigan optimizatsiya

Eng yaxshi variant:

- **Doimiy (static) qoidalar** → bitta ixcham `SYSTEM.md` (1–2k token).
- **Bosqichga oid qoida** → faqat kerakli `steps/*.md`.
- **Task fayli** → faqat joriy task.
- **Reference** → zarur bo'lsa.

Shunda har request taxminan:

- System: **1–2k token**
- Step: **0.5–2k token**
- Task: **0.5–2k token**
- Kod: keraklicha

Bu hozirgi holatga nisbatan **bir necha baravar kam context** ishlatadi.

### Xulosa

Arxitekturangning o'zi tokenni ko'p sarflamaydi. **Muammo uni qanday contextga qo'shishingda.**

Agar har safar butun `orcestor/` papkasini modelga bersang — bu qimmat.

Agar orchestrator **faqat kerakli `.md` fayllarni dinamik yuklasa**, token sarfi sezilarli kamayadi va Claude Usage'dagi katta context muammosi ham ancha bartaraf bo'ladi.

---

### 👤 Foydalanuvchi:

Claude serverlarida nimadir muammo bo'layabdi shekili browserdagi chatda sekin javob kelayabdi bazida kelmayham qolayabdi. internetdan qarachi.

### 🤖 ChatGPT:

Ha, bugun Anthropic tomonda haqiqatan ham muammolar bo'lgan.

Rasmiy status sahifasiga ko'ra, **27-iyul** kuni bir necha marta **Claude Opus 5** va keyin **Haiku 4.5** uchun **"Elevated errors"** (xatolar sonining oshishi) hodisalari qayd etilgan. Har safar muammo tekshirilgan va keyin "Resolved" deb yopilgan. citeturn0search10

Shu bilan birga, ayni paytda rasmiy status:
- **claude.ai — Operational**
- **Claude Code — Operational**
- **API — Operational** citeturn0search10turn0search9

Lekin amalda foydalanuvchilar quyidagilarni ham yozishmoqda:
- chatlarning juda sekin javob berishi;
- `529 Overloaded` va `500` xatolari;
- Projects yoki chat ro'yxati yuklanmasligi;
- ba'zan javob umuman kelmasligi. citeturn0reddit22turn0reddit21turn0reddit26

Bu sen aytayotgan holatga juda o'xshaydi:

> "browserdagi chatda sekin javob kelayabdi, ba'zida kelmay ham qolayabdi."

Ehtimoliy sabablar:
- serverlar hali ham bugungi nosozlikdan keyin to'liq barqarorlashmagan;
- Opus/Fable modellari yuklamasi yuqori;
- sening juda katta contextli (150k+ token) chatlaring javob vaqtini yana ham oshirayotgan bo'lishi mumkin.

Agar yangi chat ochib bitta oddiy "Hello" yuborsang ham sekin javob bersa, bu deyarli aniq server tomoni muammosi bo'ladi. Agar faqat bitta ulkan chat sekin bo'lsa, unda context hajmi ham sezilarli rol o'ynaydi.

Menimcha, bugun sening internetingdan ko'ra **Anthropic serverlari bilan bog'liq vaqtinchalik muammolar** bo'lish ehtimoli yuqori.

---

### 👤 Foydalanuvchi:

Umuman yangi chat ochib chromeda oddiy savol bersam ham javob kelmay qolayabdi

### 🤖 ChatGPT:

Ha, unda muammo deyarli aniq **Anthropic tomonda**.

Agar:
- ✅ yangi chat ochsang,
- ✅ atigi bitta oddiy savol bersang,
- ❌ javob uzoq kutsa yoki umuman kelmasa,

unda bu:
- interneting,
- browser cache,
- yoki 150k context

bilan bog'liq emas.

Bugun Anthropic statusida haqiqatan ham xatolar qayd etilgan va ular "Resolved" deb belgilangan bo'lsa ham, bunday holatlarda barcha regionlar darhol normal ishlay boshlamasligi mumkin.

Tekshirib ko'rish uchun:
1. `https://claude.ai`ni Incognito oynasida och.
2. Boshqa tarmoqdan (masalan, telefon hotspoti) sinab ko'r.
3. Agar Claude Code ishlatsa, terminaldan ham oddiy prompt yuborib ko'r.

Agar uchalasida ham sekin yoki javobsiz bo'lsa, bu server tomoni muammosi.

Aytgancha, bugun shunga o'xshash shikoyatlar boshqa foydalanuvchilarda ham bo'lgan:
- javoblar 1–5 daqiqa kechikishi;
- "Thinking..." holatida qolib ketishi;
- umuman javob bermasligi;
- 529 yoki 5xx xatolari.

**Bir savol:** sening holatingda nima bo'lyapti?
- `Thinking...` yozuvi cheksiz turadimi?
- yoki **"Failed to generate response"** chiqadimi?
- yoki boshqa xato (masalan, 5xx yoki 529) ko'rinyaptimi?

---

### 👤 Foydalanuvchi:

Thinking... uzoq turadi va network error 

### 🤖 ChatGPT:

Bu simptomlar odatda **server yoki WebSocket/API ulanishi** bilan bog'liq bo'ladi, ayniqsa:

- `Thinking...` juda uzoq turishi.
- Oxirida `Network error` chiqishi.
- Yangi chatlarda ham takrorlanishi.

Bu holatda muammo deyarli aniq sening prompting yoki contexting emas.

Yana bir necha narsani tekshir:

1. **Anthropic Status** sahifasida hozir ham yangi incident chiqyaptimi.
2. Browser DevTools (`F12 → Network`)da `chat` yoki `messages` requestlari `502`, `503`, `504` yoki `529` bilan tugayaptimi.
3. Agar VPN ishlatayotgan bo'lsang, o'chirib yoki boshqa server bilan sinab ko'r.
4. Boshqa browser (Firefox/Edge) yoki telefon orqali `claude.ai`ni ochib ko'r.

Agar:
- boshqa browserda ham,
- boshqa internetda ham,
- yangi chatda ham

`Thinking...` → `Network error` bo'lsa, bu deyarli 100% Anthropic infratuzilmasidagi vaqtinchalik nosozlik hisoblanadi.

Menda eng qiziq narsa — **`Network error` qachon chiqyapti?**
- 5–10 soniyadan keyinmi?
- 1–2 daqiqadan keyinmi?
- yoki javob yozishni boshlagandan keyin uzilib qolayaptimi?

Bu vaqt ham muammoning qaysi bosqichda yuz berayotganini aniqlashga yordam beradi.

---

### 👤 Foydalanuvchi:

shared-0-B6nQ_22V.js:1 [O11Y] [DatadogRUM] Initialized Object
shared-3-BiRzWlbq.js:2 Deprecated API for given entry type.
(anonymous) @ shared-3-BiRzWlbq.js:2
content.js:109 [SlashCommand] Manager started
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
/v1/toolbox/shttp/mcp/2dfdb9be-3a85-451d-9cb8-fd30d4fcb635:1  Failed to load resource: the server responded with a status of 405 ()
/v1/toolbox/shttp/mcp/78ebd772-3452-41b5-aa59-4e1988b7bb21:1  Failed to load resource: the server responded with a status of 405 ()
ad.doubleclick.net/ccm/s/collect?auid=1530325386.1784029863&gtm=45be67m1v9196940227za200zd9196940227xec&fmt=8:1  Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
shared-0-B6nQ_22V.js:1 [COMPLETION] Starting completion request (attempt 1, mode=legacy)
shared-0-B6nQ_22V.js:1 [COMPLETION] message_store_sync_blocked Object
warn @ shared-0-B6nQ_22V.js:1




shared-0-B6nQ_22V.js:1 [O11Y] [DatadogRUM] Initialized Object
shared-3-BiRzWlbq.js:2 Deprecated API for given entry type.
(anonymous) @ shared-3-BiRzWlbq.js:2
content.js:109 [SlashCommand] Manager started
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
/v1/toolbox/shttp/mcp/2dfdb9be-3a85-451d-9cb8-fd30d4fcb635:1  Failed to load resource: the server responded with a status of 405 ()
/v1/toolbox/shttp/mcp/78ebd772-3452-41b5-aa59-4e1988b7bb21:1  Failed to load resource: the server responded with a status of 405 ()
ad.doubleclick.net/ccm/s/collect?auid=1530325386.1784029863&gtm=45be67m1v9196940227za200zd9196940227xec&fmt=8:1  Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
content.js:109 [SlashCommand] Config loaded, enabled: true commands: 22
shared-0-B6nQ_22V.js:1 [COMPLETION] Starting completion request (attempt 1, mode=legacy)
shared-0-B6nQ_22V.js:1 [COMPLETION] message_store_sync_blocked Objectconversation_uuid: "3d3a8cac-37aa-441b-a7ae-5030010361c3"current_last_uuid: "new-assistant-message-uuid-019fa45b-57c9-730c-9940-4f17f71956f3"current_path_count: 2new_last_uuid: undefinednew_path_count: 0new_tree_count: 0prev_tree_count: 2reason: "tree_shrink"tree_lost_count: 2[[Prototype]]: Object
warn @ shared-0-B6nQ_22V.js:1





### 🤖 ChatGPT:

Loglarga qaraganda **asosiy xato bu emas**:

```
405 /v1/toolbox/shttp/mcp/...
```

Bu odatda MCP/toolbox endpointlari bilan bog'liq va chat ishlashiga sabab bo'lmaydi.

```
ERR_BLOCKED_BY_CLIENT
```

Bu esa AdBlock/uBlock/Brave Shield reklama so'rovini bloklaganini bildiradi. Ham normal.

---

### Meni qiziqtirgan qator:

```
[COMPLETION] Starting completion request
```

va darhol

```
message_store_sync_blocked
```

keyin esa

```
reason: "tree_shrink"
tree_lost_count: 2
```

Bu Claude frontendi conversation tree (xabarlar daraxti) bilan sinxronlasha olmayotganini ko'rsatadi. Bu ko'pincha:

- server javob bermaganda;
- websocket uzilganda;
- backend conversation state yo'qolganda

uchraydi.

---

## Network tabni tekshir

Console emas, **Network** kerak.

1. `F12`
2. **Network**
3. Filter:

```
messages
```

yoki

```
completion
```

yoki

```
chat
```

Keyin bitta prompt yubor.

Menga quyidagilar kerak:

- Request URL
- Status Code

masalan

```
POST /api/organizations/.../messages
```

```
200
```

yoki

```
502
```

```
503
```

```
504
```

```
529
```

yoki

```
failed
```

---

### Yana bir narsaga e'tibor berdim

Console'da:

```
content.js
SlashCommand
```

chiqyapti.

Bu **Claude'ning o'zi emas**.

Bu browser extension inject qilayotgan script.

Shuningdek:

```
/v1/toolbox/shttp/mcp/
```

ham extensionga o'xshayapti.

Shuning uchun bir marta sinab ko'r:

- Chrome'da **Incognito** och.
- Extensionlarni ishlatmasdan (`Allow in Incognito` o'chirilgan bo'lsa) `claude.ai`ga kir.
- Oddiy `Hello` yubor.

Agar Incognito'da ham aynan shu muammo bo'lsa, bu deyarli aniq Anthropic serveri bilan bog'liq.

Agar Incognito'da muammo yo'qolsa, unda aybdor browser extension (masalan, AI helper, Slash Command, MCP extension yoki shunga o'xshash) bo'lish ehtimoli yuqori.

**Menga Network tabdagi bitta screenshot yoki `messages` requestining status kodini yubor.** Shu bilan muammo server tomonidami yoki browser tomonidami, deyarli aniq aytish mumkin bo'ladi.

---


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/model-tanlash/qoida.md`

# Qoida (heuristika) — Model tanlash qaror daraxti

Bu **majburiy qoida emas** — tekshirish uchun savollar ro'yxati.
Supervisor_User yoki Orcestor_Agent har loyihada/task'da shu savollarni
o'zi javoblab, mos modelni tanlaydi.

## 1-savol: Vazifa oldindan spetsifikatsiya qilinganmi?

- **Ha** (aniq hujjat/shablon/qoida bor, planning-mode allaqachon
  o'tkazilgan) → arzon/tez model (Sonnet) odatda yetarli.
- **Yo'q** (vazifa hali "xom", noaniq, ko'p variant bor) → kuchliroq
  model (Opus/Fable) yoki avval planning-mode'ga qaytish.

## 2-savol: Xato narxi qanday?

- **Past** (oson qaytariladi, sinov-xato mumkin) → arzon model bilan
  boshlash xavfsiz.
- **Yuqori** (production migratsiya, xavfsizlik, geri qaytarib
  bo'lmaydigan o'zgarish) → kuchliroq model yoki qo'shimcha inson
  tekshiruvi (review) qatlami qo'shish.

## 3-savol: Rol nima — Orcestor (strategik) yoki Executer (ijrochi)?

- **Orcestor_Agent** — reja tuzish, ish-taqsimoti, standing rules/memory
  yozish. Agar bu qarorlar allaqachon oldindan yaxshi spetsifikatsiya
  qilingan bo'lsa (SKILL.md + memory fayllari aniq), Sonnet darajasi
  odatda yetarli.
- **Executer_Agent** (`agy` ichida) — ko'p va tez chaqiriladi, shuning
  uchun tezlik/narx muhimroq. Standart holatda arzonroq/tezroq model
  (Flash yoki Sonnet), faqat murakkab yakka vazifa uchun `/model` orqali
  vaqtincha kuchliroq modelga o'tish.

## 4-savol: Ko'p marta takrorlanadigan (iterativ) ishmi?

- Hujjat/skill yozish, formatga qat'iy amal qilish kabi ishlarda —
  tezroq model (Sonnet) ko'pincha amaliy ustunlik beradi, chunki
  yozish→ko'rib chiqish→tuzatish sikli tez-tez takrorlanadi.

## Qachon qayta baholash kerak

- Agar Orcestor_Agent'ga "noaniq muammoni o'zi tahlil qilib, yechim
  taklif qil" turidagi vazifa berila boshlasa (ya'ni planning-mode
  bosqichi qisqartirilsa yoki chetlab o'tilsa) — 1-savolga qaytib,
  modelni qayta baholang.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/README.md`

# Skill Sub-Management Planning Information Docs

Bu paket — `orcestor-skill` uchun **qo'shimcha guidance qatlami**. SKILL.md
skeletini (checkpoint / standing rules / memory, task lifecycle) o'zgartirmaydi,
balki amaliyotda tez-tez chiqadigan, ammo hozircha hujjatlashtirilmagan
qarorlar uchun **heuristika** (qattiq qoida emas) taqdim etadi.

## Nega bu alohida paket

`orcestor-skill`ning o'zi ataylab moslashuvchan qurilgan: loyiha turiga
(front/backend/boshqa) qarab ko'p qoida `orcestor/memory/*.md` yoki
`standing_rules.json` orqali **har loyihada alohida** shakllanadi. Bu paket
o'sha shakllanish jarayonida foydalanuvchiga (yoki Orcestor_Agent'ga) yo'l
ko'rsatish uchun mo'ljallangan — "nima haqida o'ylash kerak" ro'yxati, "har
doim shunday qil" degan buyruq emas.

## Tarkib

| Papka | Mavzu |
|---|---|
| `model-tanlash/` | Orcestor_Agent va Executer_Agent uchun qaysi model (Sonnet/Opus/Flash) tanlanadi |
| `blocker-va-subtask/` | Asosiy task davomida to'siq chiqqanda sub_task ochish, parallel vs ketma-ket qaror |
| `restart-timing/` | Context restart qachon "vaqtida", qachon "kech" hisoblanadi |
| `skill-vs-loyiha-qoidalari/` | Qaysi qoida SKILL.md darajasida, qaysi biri loyiha-darajasida (`memory/*.md`) yashashi kerak |

Har papka ichida bir xil struktura:

- `shart.md` — bu use-case qachon yuzaga keladi (old-shart, kontekst)
- `vaziyat.md` — muammoning o'zi, nega bir yechim yo'q
- `qoida.md` — heuristika / qaror daraxti (majburiy qoida emas)
- `use_cases.md` — tipik holatlar ro'yxati
- `examples.md` — konkret misollar (shu jumladan taxminiy/gipotetik holatlar)

## Qanday ishlatish

Bu paket **SKILL.md o'rniga emas**, uning yonida turadi. Orcestor_Agent
bootstrap/resume paytida bu fayllarni o'qish shart emas — ular ko'proq
**inson (Supervisor_User) uchun** yoki loyiha-darajasidagi `memory/*.md`
yozishda mos keladigan tayyor qolip sifatida mo'ljallangan.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/model-tanlash/use_cases.md`

# Use Cases — Model tanlash

## UC-1: Yangi loyihani boshlash (bootstrap)

Orcestor_Agent birinchi marta savollar beradi (BATCH_SIZE, TRACKING_MODE
va h.k.) — bu allaqachon SKILL.md'da qattiq skript sifatida yozilgan,
noaniqlik yo'q. **Sonnet darajasi yetarli.**

## UC-2: Hujjat/skill yozish (SKILL.md, README, shablon)

Aniq format, aniq maqsad, ko'p iteratsiya. **Sonnet afzal** — tez, format
talablariga qat'iy amal qiladi, ortiqcha "kreativlik" qo'shmaydi.

## UC-3: Arxitektura darajasidagi qaror (masalan yangi modul qanday
loyihalansin, DB sxemasi qanday bo'lsin)

Ko'p variant, kelajakka ta'siri katta, xato narxi yuqori. **Opus/Fable
ko'rib chiqish tavsiya etiladi** — yoki avval planning-mode orqali
noaniqlikni kamaytirib, keyin Sonnet'ga topshirish.

## UC-4: Executer_Agent orqali oddiy kod yozish (masalan bitta funksiya,
kichik refaktor)

Aniq task, tez-tez chaqiriladi. **Flash yoki Sonnet** (agy ichida
`/model` orqali standart qilib qo'yish mumkin).

## UC-5: Executer_Agent orqali murakkab, ko'p faylli o'zgarish

Bitta task ichida ko'p bog'liqlik bor. **Vaqtincha Sonnet/Opus'ga
`/model` orqali o'tish**, keyin oddiy tasklar uchun yana arzon modelga
qaytish.

## UC-6 (taxminiy/gipotetik): Ko'p tilli yoki noan'anaviy stack

Agar loyiha kam uchraydigan texnologiya stack'ida bo'lsa (model
training-data'da kam ko'rgan), kuchliroq model (Opus/Fable) dastlabki
tadqiqot bosqichida foydali bo'lishi mumkin — keyin aniqlashtirilgan
qoidalar bilan Sonnet'ga o'tish mantiqiy.

## UC-7 (taxminiy): Debugging — sabab noaniq xato

Xato xabari o'zi aniq bo'lmagan, sabab bir nechta joyda bo'lishi mumkin
bo'lgan holatlarda — bu "noaniq vazifa" toifasiga kiradi, kuchliroq model
yoki qo'shimcha diagnostika qadami (log yig'ish, keyin tahlil) foydali.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/skill-vs-loyiha-qoidalari/use_cases.md`

# Use Cases — Qoidani joylashtirish

## UC-1: Model tanlash heuristikasi (shu suhbatdagi mavzu)

Bu — ko'plab loyihalarga tegishli umumiy pattern, lekin hali faqat 1-2
loyihada sinalgan. → Hozircha alohida hujjat (`model-tanlash/`) sifatida
saqlanadi; bir necha loyihada tasdiqlansa, SKILL.md'ga qisqa reference
sifatida qo'shilishi mumkin.

## UC-2: Blocker/sub_task format (frontend loyihaga xos)

Faqat bitta loyiha stack'iga tegishli konkret format (masalan dizayn-
token bog'liqligi). → `orcestor/memory/sub_task_policy.md` (loyiha
darajasida).

## UC-3: "Restart chegarasi 25%" kabi son

Bu loyiha hajmiga bog'liq, universal emas. → standing_rules.json
(loyihaga xos, lekin barqaror qoida sifatida).

## UC-4 (taxminiy): Bir nechta loyihada bir xil qoida qayta-qayta chiqsa

Agar xuddi shu qoida 3+ turli loyihada mustaqil ravishda paydo bo'lsa —
bu SKILL.md darajasiga "ko'tarilish" uchun signal.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/model-tanlash/shart.md`

# Shart — Model tanlash qachon savol bo'lib qoladi

Bu use-case quyidagi old-shartlar bajarilganda dolzarb bo'ladi:

- Orchestration ikkita agent-rolga bo'lingan: **Orcestor_Agent** (reja
  tuzuvchi, nazorat qiluvchi) va **Executer_Agent** (`agy` — Antigravity
  CLI orqali kod yozuvchi).
- Orcestor_Agent uchun istalgan LLM ishlatilishi mumkin (Claude, Codex,
  GPT va h.k.) — SKILL.md bu tanlovni ataylab ochiq qoldirgan.
- Executer_Agent tomonida `agy` ichida `/model` orqali bir nechta model
  (Gemini Flash/Pro, Claude Sonnet/Opus, GPT-OSS) o'rtasida almashish
  imkoni bor.
- Loyiha **planning mode** orqali ishlaydi: noaniq muammo avval
  Supervisor_User va Orcestor_Agent orasida muhokama qilinib, keyin aniq
  task shakllantiriladi (ya'ni model "noaniqlikni o'zi hal qilish"
  vazifasini kam bajaradi).

Agar loyihada planning-mode bosqichi yo'q bo'lsa (ya'ni Orcestor_Agent'ga
to'g'ridan-to'g'ri noaniq, kam-spetsifikatsiyali topshiriq beriladi) — bu
hujjatdagi heuristika to'liq amal qilmaydi, chunki xulosalar aynan
"noaniqlik oldindan hal qilingan" holat uchun chiqarilgan.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/skill-vs-loyiha-qoidalari/shart.md`

# Shart — Qaysi qoida qayerda yashashi kerak

Bu use-case orcestor-skill'ning uch qatlamli modeliga tegishli:

- **SKILL.md** — barcha loyihalarga umumiy skelet (checkpoint format,
  task lifecycle, restart protokoli, til tanlash va h.k.).
- **standing_rules.json** — loyihaga xos, lekin barqaror qoidalar
  (masalan "har doim TypeScript strict mode ishlatiladi").
- **orcestor/memory/*.md** — loyihaga xos qarorlar, sabab-mulohaza bilan
  (masalan "nima uchun bu arxitektura tanlandi").

Savol shu joyda tug'iladi: yangi bir qoida/kuzatuv paydo bo'lganda (masalan
shu suhbatdagi model tanlash yoki blocker/sub_task heuristikasi), uni
qaysi qatlamga yozish kerak?


## Manba: `my_digital_brain/30_Resources/ai-chat-history/claude/apre*****siyat@gmail.com/cv_and_resume_differences.md`

# CV and resume differences

### 👤 Foydalanuvchi:

Salom Oʻzbek tilida javob ber CV bilan resume nima

### 🤖 Claude:

Salom! Albatta, tushuntirib beraman.

CV (Curriculum Vitae) va Resume ikkalasi ham ish izlashda foydalaniladigan hujjatlar, lekin ularning orasida farqlar bor:

CV (Curriculum Vitae)

Uzunligi: Odatda 2-3 sahifa yoki undan ko'proq
Mazmuni: Butun professional va akademik hayotingizni batafsil ko'rsatadi
Nima kiritiladi: Barcha ma'lumotingiz, ish tajribangiz, ta'lim, nashrlar, tadqiqotlar, mukofotlar, konferensiyalar, til bilimlari va boshqalar
Qachon ishlatiladi: Akademik lavozimlar, ilmiy tadqiqot, tibbiyot sohasida, Evropa mamlakatlari va xalqaro tashkilotlarda ko'proq qo'llaniladi
Xususiyati: Kamdan-kam yangilanadi, butun martabangizni aks ettiradi

Resume

Uzunligi: Odatda 1 sahifa (maksimum 2 sahifa)
Mazmuni: Muayyan ish o'rni uchun mos keladigan muhim ma'lumotlarni qisqacha ko'rsatadi
Nima kiritiladi: Asosiy ish tajribasi, tegishli ko'nikmalar, ta'lim va yutuqlar
Qachon ishlatiladi: Xususiy sektor, biznes kompaniyalari, AQSh va ko'pchilik mamlakatlarida
Xususiyati: Har bir ish uchun moslashtirib yoziladi

O'zbekistonda odatda CV so'zi ko'proq ishlatiladi va resume bilan deyarli bir xil ma'noda tushuniladi. Lekin xalqaro kompaniyalarga yoki chet elga ariza topshirganda bu farqni bilish muhimdir.

Yana savolaringiz bo'lsa, bemalol so'rang!

---


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/skill-vs-loyiha-qoidalari/vaziyat.md`

# Vaziyat — Noto'g'ri joyga yozishning narxi

- Agar **loyihaga xos** qoida SKILL.md'ga (umumiy skelet) yozilsa —
  boshqa loyihalarda mos kelmasligi mumkin, skill haddan tashqari
  qattiqlashadi, moslashuvchanlik yo'qoladi.
- Agar **umumiy** qoida faqat bitta loyihaning memory faylida qolib
  ketsa — boshqa loyihalarda xuddi shu muammo qaytadan "kashf qilinadi",
  vaqt/token behuda sarflanadi.
- Standing rules va memory orasidagi farq ham ba'zan noaniq: standing
  rule — "har doim shunday qil" turidagi qisqa buyruq, memory esa
  "nega bunday qaror qilindi" degan kontekst bilan birga keladi.


## Manba: `zdes_archive_docs/raw_history/session/2026-07-25-handoff-to-other-claude.md`

# Xabar: ikkinchi (permission) sessiyadan — orcestor/ tizimida qilingan o'zgarishlar

Bu fayl boshqa terminaldagi Claude Code sessiyasi uchun yozildi. Ikkala
sessiya o'rtasida to'g'ridan-to'g'ri bog'lanish yo'q, shuning uchun Fayzillo
buni qo'lda ko'rsatadi. Quyidagilarni bilib oling:

## 1. `orcestor/dispatch.py`ga yangi `check` subcommand qo'shildi (faqat maslahat, gate emas)

```
python3 orcestor/dispatch.py check T-XXX [--build]
```

Hech narsaga yozmaydi, status/ACCEPTED/REJECTED belgilamaydi — faqat 3 ta
signal chiqaradi:
1. Task scope'idagi fayllar haqiqatan o'zgarganmi (bo'sh bo'lsa — soxta
   "tayyor" hisobot xavfi, xuddi T-004'da bo'lgani kabi).
2. Scope'dan tashqari o'zgargan fayllar (eslatma sifatida, xato emas —
   umumiy working tree'da bir nechta task/sessiya parallel bo'lishi mumkin).
3. Response.md'da "O'zgargan fayllar" jadvali va Definition of Done
   eslatilganmi.

Review qilishdan oldin ishlatib ko'rish tavsiya etiladi, lekin yakuniy
ACCEPTED/REJECTED qarori va `status/` yozuvi baribir sizning zimmangizda
qoladi — bu skript review'ni almashtirmaydi, faqat tezlashtiradi.

## 2. `orcestor/prompt.md` shabloni yangilandi

Endi har bir yangi task uchun "Report back" bo'limida AGY'dan
**"O'zgargan fayllar" jadvali** talab qilinadi (fayl | turi | qisqa sabab).
Bu review'ni tezlashtirish uchun (to'liq faylni o'qimasdan, nuqtali
`git diff` qilish imkoni).

**T-005 va undan oldingi tasklar bu jadvalsiz** — bu normal, ular shablon
yangilanishidan oldin dispatch qilingan. T-007'dan boshlab yangi tasklarni
`orcestor/tasks/`ga yozganda (yoki `dispatch.py new` bilan) shu talab
avtomatik kiradi.

## 3. Kichik bug tuzatildi

`dispatch.py new T-XXX` oldin noto'g'ri blokni (section 3'dagi to'ldirilgan
T-021 namunasini, section 1'dagi bo'sh shablon o'rniga) chiqarayotgan edi
(regex xatosi — greedy `.*` oxirgi ```markdown blokni tanlab olayotgan edi).
Endi to'g'ri ishlaydi.

## 4. Permission eslatmasi

`.claude/settings.local.json`da Write ruxsati loyiha papkasi +
`~/.claude/**` + `/tmp/claude-*/**` bilan cheklangan, `rm` esa faqat
`orcestor/*` bilan. Agar shundan tashqarida biror amal uchun ruxsat
prompti chiqsa (bloklanmaydi, faqat so'raladi) — Fayzilloga yoki
ikkinchi (permission) sessiyaga ayting, kerak bo'lsa qo'shib qo'yiladi.

## 5. T-005 holati

Test paytida payqaldi: T-005 allaqachon `orcestor/task_compliete/`ga
ko'chirilgan, scope bo'yicha 26 ta fayl to'g'ri o'zgargan ko'rinadi. Agar
hali `status/T-005.log`ga ACCEPTED/REJECTED yozilmagan bo'lsa, shuni
navbatga qo'ying.


## Manba: `my_digital_brain/90_System/claude_tasks/new_fixing_orcestration_system/02-metaforalar.md`

# 2. Metaforalar

G'oyani aniqroq muhokama qilish uchun — texnik spec emas, tushuntirish
vositasi.

## 2.1 Bosh muhandis va kotib

**Claude — bosh muhandis** (qimmat, sekin, lekin chuqur fikrlaydi), **AGY —
kotib** (arzon, juda tez yozadi — 340+ token/soniya). Bosh muhandis har bir
kichik xulosani o'zi qog'ozga tushirsa, uning qimmat vaqti behuda ketadi.
To'g'ri taqsimot: muhandis qaror qabul qiladi va tekshiradi, kotib esa
qarorni tezkor va arzon tarzda qayd etadi (DB'ga yozadi). Bu taqsimot
hozircha `orcestor`da qisman bor (AGY — Executor), lekin checkpoint/memory
yozish vazifasi hali aniq ajratilmagan.

## 2.2 Sprint va retro

**Sessiya — bitta sprint** (maksimal 5 prompt). Sprint oxirida `/clear` —
**retro**: nima qilindi, nima chiqdi, keyingi qadam nima — bittagina qisqa
paragraf. Keyingi sprint shu paragrafdan boshlanadi, oldingi sprintning
har bir tafsiloti emas. Hozirgi `status.md` fayllari aslida qo'lda
yozilayotgan retro — lekin ular tez uzayib, o'zi ham "context" bo'lib
qolyapti (masalan `github-backup/status.md` yonida 3 ta `.err*` fayl bor).

## 2.3 Filiallar va bosh ofis

To'rtta `orcestor/` nusxasi — **bir xil kompaniyaning turli shahar
filiallari**, har biri o'z mahalliy tartibini ixtiro qilgan (bir xil
`requirements.MD` skeleti, lekin turlicha to'ldirilgan). Yagona tizim —
**bosh ofis**: bitta schema, bitta qoidalar to'plami, filiallar shundan
meros oladi, o'zidan qonun chiqarmaydi.

## 2.4 Kundalik daftar vs versiyalangan checkpoint

Fayl-asosli `status.md` — **qo'l bilan yozilgan kundalik daftar**: chiziqli,
qidirish qiyin, eskisi o'chirilmaydi (faqat "RAD ETILDI" deb belgilanadi),
vaqt o'tib qalinlashadi. DB-asosli checkpoint — **versiyalangan yozuv**:
har checkpoint bitta qator, oxirgisini so'rash — bitta so'rov (`WHERE
session=X ORDER BY vaqt DESC LIMIT 1`), butun daftarni o'qish shart emas.

## 2.5 Ikki xil xotira turi — qisqa muddatli va uzoq muddatli

**Session checkpoint — ishchi xotira** (bugungi kunga xos, tez eskiradi,
har sprintda yangilanadi). **Standing rules — uzoq muddatli xotira**
(masalan "CSS'ga tegilmaydi", "fayzillofn30-ai faqat gh token orqali push
qiladi") — bular sessiyaga bog'liq emas, har safar qayta yozilmasligi,
faqat **yangilanishi** kerak. Ikkalasini bitta jadvalga aralashtirish —
kundalik daftarga passport ma'lumotlarini har kuni qayta yozishga o'xshaydi:
ishlaydi, lekin behuda va xatoga moyil.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/model-tanlash/examples.md`

# Examples — Model tanlash

## Misol 1 (real tajriba asosida)

- **Kontekst**: Orcestor loyihasining rivojlanish tarixi — avval `agy`
  ichida Gemini modellarida sinov, so'ng Claude CLI Sonnet 5 →
  Orcestor rolida, Executer_Agent `agy` + `/model` orqali kerakli
  modelga o'tkazilgan.
- **Kuzatuv**: Sonnet Orcestor rolida yetarli sifat bergan, Opus'ga
  o'tishga ehtiyoj sezilmagan — chunki vazifalar (bootstrap savollari,
  checkpoint yozish, standing rules boshqarish) allaqachon SKILL.md
  darajasida aniq spetsifikatsiya qilingan.
- **Xulosa**: 1-savol ("oldindan spetsifikatsiya qilinganmi") javobi
  "ha" bo'lgani uchun arzon model yetarli bo'lgan — heuristikaga mos.

## Misol 2 (real tajriba asosida)

- **Kontekst**: SKILL.md va hujjatlarni yozish jarayoni.
- **Kuzatuv**: "Aniq tafsilotlar va hujjatlar bo'lsa, Sonnet mukammal
  natija berishini kuzatdim."
- **Izoh**: Bu UC-2'ga to'g'ri keladi — struktura va format oldindan
  aniq bo'lganda, model vazifasi "ijodiy qaror qabul qilish" emas,
  "berilgan mantiqni izchil ifodalash" bo'ladi.

## Misol 3 (gipotetik — planning-mode bo'lmasa)

- **Faraz**: Agar Supervisor_User Orcestor_Agent'ga to'g'ridan-to'g'ri
  "loyiha uchun eng yaxshi database sxemasini tanlab, sabab-mulohaza
  bilan asosla" desa (planning-mode'ni chetlab o'tib) — bu holatda
  noaniqlik model zimmasida qoladi.
- **Kutilayotgan farq**: bu holatda Opus/Fable Sonnet'dan sezilarli
  farqli (chuqurroq) natija berishi mumkin, chunki vazifa UC-3 toifasiga
  kiradi.

## Misol 4 (gipotetik — Executer_Agent xato qaytarsa)

- **Faraz**: `agy` orqali Flash modeli bir nechta urinishda ham to'g'ri
  natija bermasa (masalan murakkab refaktor).
- **Tavsiya**: `/model` orqali Sonnet yoki Opus'ga vaqtincha o'tish,
  vazifa tugagach yana arzon modelga qaytish — bu UC-5'ga mos.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/restart-timing/shart.md`

# Shart — Restart timing qachon dolzarb bo'ladi

Bu use-case SKILL.md'dagi mavjud, allaqachon hujjatlashtirilgan
mexanizmga **qo'shimcha izoh** beradi (yangi qoida kiritmaydi):

- SKILL.md 2.2-bo'limida: context restart FAQAT Supervisor_User
  so'raganda amalga oshadi (qattiq prompt limiti yo'q).
- SKILL.md 2.3-bo'limida: restart oldidan token taqsimotini (`/context`)
  tekshirish va "Messages" ulushini `simple_context.md`ga qayd etish
  talab qilinadi — bu ko'rsatkich vaqt o'tishi bilan pasayib borishi
  kerak (restart intizomi samarali ishlayotganining dalili sifatida).

Bu paket o'sha o'lchov ko'rsatkichini **qachon, qanday interpretatsiya
qilish** kerakligiga oid amaliy qo'llanma qo'shadi — SKILL.md matnini
o'zgartirmaydi.


## Manba: `mini_brain/coding_style/coding_style.md`

- **Umumiy yondashuv**: Standart freymvork qoliplaridan chekinib, xususiy algoritmlar, dinamik validation mexanizmlari, gibrid schema modellari va resurslarni tejaydigan yechimlar qo'llaniladi.
- **Dynamic Mock User Generator**: Test muhiti va local state-ni ma'lumotlar bilan to'ldirish uchun qo'lda kiritish o'rniga, matematik formulalar va `Array.from` orqali ma'lumotlar dinamik generatsiya qilinadi.
- **Schema-Driven Input Validation Engine**: Tashqi validatsiya kutubxonalarisiz (Joi, Validator), oddiy JS obyekti (shablon) orqali kiruvchi JSON request body kalitlari va tiplari dinamik tekshiriladi.
- **Dynamic Granular Action-Based Permission**: Oddiy RBAC o'rniga, har bir foydalanuvchi va model uchun dinamik HTTP Action (`GET`, `POST`, `PUT`, `DELETE`) darajasida huquqlar beriladi.
- **Multi-Device Session & Real-Time Typing**: Bitta foydalanuvchining bir nechta qurilmasidan ulanishini aniqlash (`handshake.query` orqali) va WebSockets orqali chat holatini efirga uzatish mexanizmi qo'llaniladi.
- **Synchronous Disk File Cleanup**: Baza bilan ishlashda yetim qolgan fayllarni `fs.existsSync` va `fs.unlinkSync` orqali sinxron tozalash qoidasi mavjud.
- **Centralized Global Initialization**: Loyihaning `main.ts` fayllari kichik hajmda (10-14 qator) saqlanadi. Barcha konfiguratsiya (`ValidationPipe`, `SwaggerModule` va h.k.) alohida fayldagi bitta global funksiya orqali biriktiriladi.
- **Ephemeral Container Storage + External ID Reference**: Fayllar bazada yoxud asosiy konteyner diskida emas, mustaqil cloud/microservice'da saqlanadi. Asosiy bazada faqat fayl ID'si saqlanib, URL dinamik yig'iladi. Murakkab infratuzilma o'rniga In-Memory va oddiy tejamkor yechimlarga ustunlik beriladi.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/skill-vs-loyiha-qoidalari/examples.md`

# Examples — Qoidani joylashtirish

## Misol 1 (shu suhbat asosida)

- **Kontekst**: Foydalanuvchi blocker/sub_task va model tanlash haqida
  kuzatuvlarini bevosita suhbatda bayon qildi, SKILL.md'da bular yo'q
  edi.
- **Qaror**: Bu paket (`skill_sub_management_planning_information_docs`)
  — bu kuzatuvlarni "hali SKILL.md emas, lekin suhbatdan yo'qolib
  ketmasin" darajasida saqlash usuli. Foydalanuvchi o'zi keyin skill'ga
  qanday joriy qilishni hal qiladi.

## Misol 2 (gipotetik)

- **Faraz**: Ikkita turli loyihada (biri frontend, biri backend)
  mustaqil ravishda "sub_task tugagach, agar context 20%dan kam bo'lsa
  davom et" degan xuddi shu qoida qo'llanilgan.
- **Kutilgan qadam**: Bu holatda qoida endi "loyihaga xos" emas,
  balki umumiy pattern — SKILL.md'ga qisqa qo'shimcha sifatida
  ko'chirish mantiqiy bo'ladi.


## Manba: `my_digital_brain/10_Projects/orcestor-skill/SKILL.md`

---
name: orcestor-start
description: Loyihada AI-agentlar orkestratsiyasini (Orchestrator/Executor/Supervisor rollari bilan) bitta komanda orqali ishga tushiradi yoki mavjud sessiyani davom ettiradi. "orkestratsiya boshla", "orcestor ishga tush", "start orchestration", "README.md'ni o'qi" (shu paket ichidagi), "read README" kabi so'rovlarda ishlatiladi.
---

# Orcestor Start Skill

**QAT'IY OGOHLANTIRISH:** Ushbu skill va butun Orkestratsiya tizimi hammaviy/umumiy foydalanish uchun EMAS. U faqatgina **Fayzillo Ummatov (Supervisor_User)** ning shaxsiy "Obsidian Digital Brain" tajribasi, Node.js/NestJS bilimlari hamda DRY/Design Pattern tamoyillari asosida maxsus moslashtirilgan. 

Ushbu skill loyihada ko'p agentli orkestratsiya tizimini ishga tushirish hamda boshqarish uchun ishlatiladi. Tizim uchta asosiy rolga tayanadi:
- **Supervisor_User**: Inson — Fayzillo (loyihani nazorat qiluvchi, qoidalar belgilovchi va qaror beruvchi).
- **Orcestor_Agent**: Orkestrator AI (Sizning uslubingizda o'ylaydigan, vazifalarni mantiqan to'g'ri taqsimlovchi va tekshiruvchi mutaxassis).
- **Executer_Agent**: Kod yozuvchi / ijrochi AI (`agy` - Antigravity CLI).

---

## 1. Ishga tushirish jarayoni va Lifecycle

### A) Tekshiruv (Check Phase)
Loyiha ildiz papkasida `orcestor/` papkasi va `orcestor/orcestor.config.env` fayli bor-yo'qligini tekshiring.

Shuningdek, loyiha **YANGI** (deyarli bo'sh, kod/git tarixi yo'q) yoki **ESKI** (mavjud kod bazasi, git tarixida bir nechta commit, yoki sezilarli miqdorda manba fayllar) ekanini aniqlang — bu B-bo'limdagi 0.5-qadamga ta'sir qiladi.

---

### B) Bootstrap Rejimi (Agar `orcestor/` papkasi yo'q bo'lsa)

0. **(ENG BIRINCHI qadam, hamma narsadan oldin) Til tanlash:**
   - Skill ishga tushirilgan ZAHOTI, boshqa hech narsadan oldin (loyiha eski/yangi tekshiruvidan ham oldin), Supervisor_User'dan so'rang: "Qaysi tilda suhbat qurishni xohlaysiz? (masalan: o'zbek, ingliz, rus — yoki boshqa til nomini yozing)"
   - Bu savolning O'ZI ham javob kutilayotgan tilda emas, **bir nechta tilda** (kamida o'zbek + ingliz) berilsin — masalan: "Qaysi tilda suhbat qurishni xohlaysiz? / Which language would you like to use?"
   - Javobni `LANGUAGE` sifatida `orcestor.config.env`ga saqlang (2-qadamga qarang). Shundan keyingi BARCHA savol/xabar/hisobot (shu jumladan quyidagi 0.5- va 1-qadamlar) tanlangan tilda beriladi.
   - Resume rejimida bu savol qayta berilmaydi — `LANGUAGE` config'dan o'qiladi (C-bo'lim).

0.5. **(FAQAT loyiha ESKI bo'lsa) Tezkor loyiha tahlili:**
   - Batafsil mexanizm va sabab uchun qarang: [4-bo'lim, "Mavjud (eski) loyihada ishga tushirish"](#4-mavjud-eski-loyihada-ishga-tushirish--project_status).
   - Qisqacha: tahlilni **Executer_Agent** (`agy -p "..."`) orqali bajaring — Orcestor_Agent xom loyiha fayllarini o'zi to'liq o'qib token sarflamasin, faqat Executer_Agent tayyorlagan qisqa xulosani ko'rib chiqsin/tasdiqlasin.
   - **MAJBURIY (1.1-bandga qarang):** buyruqda joriy loyiha yo'lini ANIQ, aniq qilib bering — hech qachon ambient/inherited cwd'ga ishonmang: `cd "<WORKSPACE_PATH>" && agy -p "Loyihani tahlil qil: ..." --dangerously-skip-permissions`.
   - Natijani `orcestor/project_status/overview.md` ga saqlang (`templates/project_status.md.template` asosida).

1. **Foydalanuvchidan (Supervisor_User) savollarni so'rang (bittalab, aniq):**
   - **1-savol:** "Bitta sprintda nechta Executer_Agent-task ishlatilsin?" (`BATCH_SIZE`, standart taklif: `5`)
   - **2-savol:** "Task kuzatuvi file-based (papka-lifecycle) yoki db-based bo'lsinmi?" (`TRACKING_MODE`: `file` | `db`)
   - **2.1-savol (faqat TRACKING_MODE=db bo'lsa):** "Qaysi DB dvigateli ishlatilsin — postgres, mysql yoki sqlite? Tavsiya: agar bu kompyuterda Docker o'rnatilgan bo'lsa va bir nechta loyiha/agent parallel ishlashi kutilsa — postgres (eng ishonchli, FOR UPDATE SKIP LOCKED bilan konflikt xavfsiz). Agar sodda, yengil, bitta foydalanuvchi uchun yetarli bo'lsa — sqlite (Docker shart emas). MySQL — Postgres bilan bir xil darajada ishonchli, agar loyihada allaqachon MySQL infratuzilmasi bo'lsa shu tanlanadi. Postgres/MySQL konteynerining user/password i FAQAT o'sha konteyner ichida amal qiladi — asosiy ilova bazasiga hech qanday ta'siri yo'q (xavfsizlik uchun ataylab shunday)."
   - **3-savol:** "`orcestor/` workspace papkasi git'ga qo'shilsinmi yoki `.gitignore`'ga tushsinmi?" (`GIT_TRACK_ORCESTOR`: `true` | `false`)
   - **3.4-savol (faqat TRACKING_MODE=db va DB_ENGINE postgres YOKI mysql bo'lsa, 3.5'dan OLDIN so'raladi):** Avval `docker ps --filter name=orcestor-db` (yoki `--filter name=orcestor`) orqali bu mashinada ALLAQACHON ishlab turgan orcestor-konteynerlarni tekshiring, natijani Supervisor_User'ga ko'rsating, keyin so'rang: "Mavjud DB konteynerni (yuqorida ko'rsatilgan) qayta ishlataymi, yoki shu loyiha uchun YANGI, alohida konteyner yarataymi?"
     - **Qayta ishlatish tanlansa:** mavjud konteyner nomi `POSTGRES_CONTAINER_NAME`/`MYSQL_CONTAINER_NAME` sifatida yoziladi, PORT/VOLUME o'sha konteynernikiga moslanadi (`docker inspect <konteyner>` orqali aniqlanadi). **MAJBURIY:** `POSTGRES_DB`/`MYSQL_DATABASE` albatta shu loyihaga XOS qilib beriladi (masalan `orcestor_<loyiha-nomi>`, hech qachon umumiy "orcestor" nomi bilan qoldirilmaydi) — bitta konteyner bir nechta loyihaga xizmat qilishi mumkin, lekin har biri o'z alohida database'iga ega bo'lishi shart (workspace_path ustuni — 3-bo'lim — bunga qo'shimcha himoya, DB_NAME farqi esa BIRINCHI, sodda himoya qatlami).
     - **Yangi konteyner tanlansa:** standart bo'yicha davom etiladi (3.5-savol, keyin struktura shakllantirish qadami — pastga qarang).
   - **3.5-savol (faqat TRACKING_MODE=db va DB_ENGINE postgres YOKI mysql bo'lsa VA 3.4'da "yangi konteyner" tanlangan bo'lsa):** "<DB_ENGINE> ma'lumotlari qaysi papkada (volume) saqlansin? Standart: orcestor/db/pgdata (postgres) yoki orcestor/db/mysqldata (mysql)."
   - **3.9-savol (FAQAT loyiha ESKI bo'lsa):** "`project_status` qachon yangilansin — har taskda avtomatik, yoki faqat siz (Supervisor_User) aytganda?" (`PROJECT_STATUS_UPDATE`: `every_task` | `on_demand`)

2. **Konfiguratsiya faylini yaratish:**
   Olingan javoblar asosida `orcestor/orcestor.config.env` faylini quyidagi mazmunda shakllantiring:
   ```env
   SUPERVISOR_USER=User
   ORCESTOR_AGENT=Claude
   EXECUTER_AGENT=agy

   LANGUAGE=<Javob0_masalan_uz_yoki_en_yoki_ru>
   WORKSPACE_PATH=<joriy_loyiha_papkasining_MUTLAQ_yo'li_avtomatik_aniqlanadi>
   BATCH_SIZE=<Javob1_standart_5>
   TRACKING_MODE=<Javob2_file_yoki_db>
   DB_ENGINE=<Javob2.1_sqlite_yoki_postgres_yoki_mysql>
   GIT_TRACK_ORCESTOR=<Javob3_true_yoki_false>
   PROJECT_STATUS_UPDATE=<Javob3.9_every_task_yoki_on_demand_yoki_bosh_agar_yangi_loyiha>
   ```
   `WORKSPACE_PATH` — **ikkala rejim uchun ham umumiy himoya mexanizmi**
   (batafsil: 3-bo'lim). Savol sifatida so'ralmaydi, loyiha ildizining
   mutlaq (absolute) yo'li avtomatik yozib qo'yiladi.

3. **Strukturani shakllantirish:**
   - **REQUIRED — TRACKING_MODE'dan qat'i nazar (ikkalasida ham) yaratiladi**
     (bular oddiy markdown-jurnal papkalar, task-tracking backend'iga
     bog'liq emas — real loyihada (2026-08-07, `zdes_frontend`) sinovdan
     o'tgan va foydali topilgan):
     - `orcestor/memory/` — Supervisor_User'ning uzoq muddatli,
       qo'lda belgilangan direktivalari (`simple_context.md`dan farqli —
       avtomatik eskirmaydi; `standing_rules.json`/DB `standing_rules`dan
       farqli — bir qatorli qoida emas, to'liq mulohaza/sabab bilan
       hujjatlashtiriladi). Har bir mavzu — alohida `.md` fayl +
       `memory/README.md` — bitta qatorlik indeks (fayl nomi + qisqa tavsif,
       har biriga havola). **Resume paytida FAQAT `memory/README.md`
       (indeks) o'qiladi majburiy tarzda — individual fayllar faqat joriy
       task shu mavzuga aloqador bo'lsa o'qiladi** (batafsil: 2.4-bo'lim).
     - `orcestor/sub_tasks/` — orkestratsiya rasmiy task-lifecycle'i
       (tasks→task_pending→task_compliete yoki DB `tasks` jadvali)
       TASHQARISIDA qilingan ishlar yoki auditlar jurnali (masalan qo'lda
       qilingan refaktoring, read-only tahlil hisobotlari). Fayllar
       `NN-qisqa-nom.md` tarzida raqamlanadi.
     - `orcestor/error_logs/` — uchragan xato + yechim jurnali
       (`NN-qisqa-nom.md`), kelajakda xuddi shu xato qaytarilganda tezkor
       ma'lumot manbai sifatida.
   - **OPTIONAL — faqat loyiha turiga mos kelsa yaratiladi** (bootstrap
     paytida avtomatik YARATILMAYDI, faqat Supervisor_User mos material
     taqdim etganda yoki so'raganda qo'lda ochiladi):
     - `orcestor/project_docs/` — backend API/DTO hujjatlari, dizayn
       referensi va h.k. (faqat loyihada alohida backend/API mavjud bo'lsa
       mantiqiy).
     - `orcestor/template_images/` — UI/dizayn maketlari (screenshot/rasm),
       Supervisor_User rasm-material bergan loyihalarda.
   - **Agar `TRACKING_MODE=file` bo'lsa:**
     Qo'shimcha quyidagi papkalarni yarating:
     - `orcestor/tasks/` — yangi / rejalashtirilayotgan tasklar
     - `orcestor/task_pending/` — ijrodagi tasklar
     - `orcestor/task_compliete/` — yakunlangan tasklar
     - `orcestor/status/` — umumiy holat va reportlar
     - Task olish (claim) — 3-bo'limdagi "Fayl-darajasida atomik claim" qoidasiga qarang.
   - **Agar `TRACKING_MODE=db` bo'lsa:**
     - **DB_ENGINE=sqlite:** faqat `orcestor/db/` papkasi yaratiladi, `python3 scripts/orcestor.py init` chaqiriladi (sqlite3 bilan, Docker kerak emas).
     - **DB_ENGINE=postgres, YANGI konteyner (3.4-javob):** `orcestor/orcestor.config.env` ga POSTGRES_* kalitlari (POSTGRES_CONTAINER_NAME masalan orcestor-db-<loyiha-nomi>, POSTGRES_PORT standart 55432, POSTGRES_USER/PASSWORD=orcestor, POSTGRES_DB=orcestor_<loyiha-nomi>, POSTGRES_VOLUME_PATH=3.5-savol javobi) qo'shiladi. `templates/docker-compose.postgres.yml.template` dan `orcestor/docker-compose.yml` yaratiladi (${VAR} lar config qiymatlari bilan almashtiriladi), `python3 scripts/orcestor.py init` chaqiriladi.
     - **DB_ENGINE=postgres, MAVJUD konteynerni qayta ishlatish (3.4-javob):** `orcestor/docker-compose.yml` yaratilmaydi (konteyner allaqachon boshqa joyda boshqariladi). `orcestor.config.env`ga mavjud konteynerning POSTGRES_CONTAINER_NAME/PORT'i va **albatta loyihaga xos** `POSTGRES_DB=orcestor_<loyiha-nomi>` yoziladi. `python3 scripts/orcestor.py init` chaqirilganda skript konteyner ishlab turganini ko'rib `docker compose up`ni o'tkazib yuboradi, keyin `POSTGRES_DB` mavjud emasligini aniqlab, uni avtomatik yaratadi (kodda mavjud, qo'lda SQL yozish shart emas).
     - **DB_ENGINE=mysql:** postgres bilan bir xil mantiq, MYSQL_* kalitlari (MYSQL_CONTAINER_NAME, MYSQL_PORT standart 33060 — asosiy MySQL 3306 bilan to'qnashmasligi uchun, MYSQL_USER/PASSWORD=orcestor, MYSQL_DATABASE=orcestor_<loyiha-nomi>) va `templates/docker-compose.mysql.yml.template` bilan.
     - ESLAATMA: Bu DB FAQAT orkestratsiya metama'lumotlari (tasks/checkpoints/rules) uchun, loyihaning haqiqiy ilova bazasi bilan aloqasi yo'q. `POSTGRES_DB`/`MYSQL_DATABASE`ni HECH QACHON umumiy/standart nom bilan qoldirmang (masalan yalang'och "orcestor") — har doim loyihaga xos qiling, bu QOIDA 2.1'dagi (3-bo'lim) `workspace_path` himoyasidan TASHQARI, birinchi va soddaroq himoya qatlami.

4. **Boshlang'ich context yaratish:**
   - `templates/simple_context.md.template` dan nusxa olib, `orcestor/simple_context.md` faylini boshlang'ich holatda yarating.
   - **Agar `TRACKING_MODE=file` bo'lsa**, qo'shimcha ravishda
     `templates/standing_rules.example.json` dan nusxa olib
     `orcestor/standing_rules.json` faylini ham yarating (bo'sh massiv
     `[]` bilan boshlansa ham bo'ladi). Bu — DB rejimidagi `standing_rules`
     jadvalining file-mode ekvivalenti (batafsil: 2.4-bo'lim, "Small
     Context Backup"). **Agar `TRACKING_MODE=db` bo'lsa**, bu qadam shart
     emas — `standing_rules` jadvali `orcestor.py init` orqali allaqachon
     yaratiladi (3-qadamga qarang).
   - **Ikkala rejimda ham**: `orcestor/memory/README.md`ni bo'sh indeks
     holatida yarating (masalan sarlavha + "hozircha memory yozuvi yo'q"
     izohi) — 3-qadamda yaratilgan `orcestor/memory/` papkasi uchun.
     Individual `memory/*.md` fayllar hali yaratilmaydi — ular faqat
     Supervisor_User uzoq muddatli direktiva bergan taqdirda, kerak
     bo'lganda qo'shiladi (2.4-bo'lim).

5. **Git konfiguratsiyasi:**
   - `GIT_TRACK_ORCESTOR=false` bo'lsa, loyihadagi `.gitignore` fayliga `orcestor/` qatorini qo'shing (agar `.gitignore` bo'lmasa, uni yarating).

6. **Bootstrap tugagach — `/clear` tavsiyasi (MAJBURIY eslatma, majburiy amal EMAS):**
   - Barcha sozlash (0–5-qadamlar, savol-javoblar, mumkin bo'lgan `project_status` tahlili) shu suhbatning o'zida ancha token sarflagan bo'ladi.
   - Shu sabab, haqiqiy task ishiga o'tishdan OLDIN Supervisor_User'ga aniq tavsiya bering: "Sozlash tugadi. Bu xabar (sozlash suhbati) token sarfi bilan bog'liq — shuning uchun asosiy ishni boshlashdan oldin `/clear` (yoki mos context-tozalash buyrug'i) qilishni tavsiya qilaman. Davom etishni yoki tozalashni o'zingiz tanlaysiz."
   - Bu — FAQAT tavsiya. Qaror har doim Supervisor_User'niki; agar davom etishni tanlasa, shu sessiyada davom eting.
   - Agar Supervisor_User `/clear` (yoki muqobilini) tanlasa — buni bajarishdan oldin `orcestor/simple_context.md` allaqachon (4-qadamda) yaratilgan bo'lishi shart, shunda keyingi sessiya C-bo'lim (Resume) orqali to'g'ri davom etadi.

---

### C) Resume Rejimi (Agar `orcestor/` papkasi mavjud bo'lsa)

1. `orcestor/orcestor.config.env` faylini o'qing, rollar va sozlamalar (`LANGUAGE`, `WORKSPACE_PATH`, `BATCH_SIZE`, `TRACKING_MODE`, `DB_ENGINE`, `PROJECT_STATUS_UPDATE`) bilan tanishing. `LANGUAGE` qayta so'ralmaydi — shu qiymat asosida BARCHA keyingi savol/xabar/hisobotlar shu tilda beriladi.
   - **Majburiy tekshiruv:** saqlangan `WORKSPACE_PATH`ni joriy loyiha papkasining haqiqiy mutlaq yo'li bilan solishtiring. Agar MOS KELMASA — bu `orcestor/` papkasi boshqa joydan ko'chirilgan/nusxalangan/symlink qilingan bo'lishi mumkin. Supervisor_User'ga ANIQ ogohlantiring: "Bu orcestor/ papkasi boshlanishda `<eski_yo'l>`da yaratilgan edi, hozir esa `<joriy_yo'l>`da ishlatilyapti — agar bu nusxa boshqa joyda ham faol bo'lsa, ikkalasi mustaqil ishlab, tasklar/checkpoint holati bir-biriga zid bo'lib qolishi mumkin." Davom etish yoki tozalash — Supervisor_User qarori (batafsil: 3-bo'lim).
2. Minimal checkpoint + standing rules'ni yuklang (batafsil: 2.4-bo'lim,
   "Small Context Backup" — bu qadam shu konsepsiyaning amaliy bajarilishi):
   - **`file` rejimida:** `orcestor/simple_context.md` faylini o'qing —
     **BU YAGONA majburiy o'qiladigan tarix faylidir**, boshqa eski
     tarixiy fayllarni o'qimang. Shu bilan birga `orcestor/standing_rules.json`
     ham MAJBURIY o'qiladi (agar mavjud bo'lsa) — bu cross-session,
     sekin o'zgaruvchi qoidalar ro'yxati, `simple_context.md`dan farqli
     ravishda restartda o'chmaydi.
   - **`db` rejimida:** `python3 scripts/orcestor.py checkpoint get`
     (kerak bo'lsa `--topic <mavzu>` bilan filtrlab) ishlatiladi — bu
     buyruq eng so'nggi (FAQAT bitta) checkpoint yozuvini va tegishli
     standing rules'ni qaytaradi. Hech qachon `session_checkpoints`/
     `standing_rules` jadvallariga qo'lda to'liq `SELECT *` yubormang —
     bu "small context backup" g'oyasini buzadi (sabab: 2.4-bo'lim).
   - **Ikkala rejimda ham**, agar `orcestor/memory/` mavjud bo'lsa,
     `orcestor/memory/README.md` (indeks) o'qiladi — bu MAJBURIY, lekin
     QISQA (bitta qatorlik yozuvlar). Individual `memory/*.md` fayllar
     BU QADAMDA o'qilmaydi — faqat keyinroq, joriy task/savol shu mavzuga
     bevosita aloqador bo'lganda ochiladi (2.4-bo'lim).
3. Agar `orcestor/project_status/overview.md` mavjud bo'lsa — uni o'qing (qisqa, 4-bo'limga qarang) va **ishni boshlashdan oldin uning mazmunini Supervisor_User'ga qisqa bayon qiling** (struktura, oxirgi bajarilgan ishlar, ma'lum muammolar). Bu qadam MAJBURIY — tasklarga o'tishdan oldin bajariladi.
4. `TRACKING_MODE` ga qarab navbatdagi tasklarni toping:
   - `file` rejimida: `orcestor/task_pending/` papkasidagi fayllar.
   - `db` rejimida: `python3 scripts/orcestor.py task list --status TODO` bilan ko'rib chiqiladi, keyingi task esa albatta `python3 scripts/orcestor.py task claim` (atomik) orqali olinadi — hech qachon qo'lda SQL SELECT/UPDATE ishlatilmasin (sabab: 3-bo'lim, "Parallel Orkestratsiya").
5. **Orcestor_Agent** sifatida ishni qolgan joyidan davom ettiring va ijrochiga (`Executer_Agent`) yo'nalish bering.
6. Agar `PROJECT_STATUS_UPDATE=every_task` bo'lsa — har task yakunlangach, `orcestor/project_status/overview.md`ni yangilang (4-bo'limga qarang). Agar `on_demand` bo'lsa — faqat Supervisor_User aniq so'raganda yangilang.

---

## 2. Umumiy Qoidalar va Tamoyillar

1. **Rollar va Identifikatsiya:**
   - Rollar strictly `orcestor.config.env` faylida belgilanadi.
   - Boshqa hech bir hujjatda yoki kodda haqiqiy odam/agent ismi yozilmaydi. Faqat umumiy tokenlar ishlatiladi: `Supervisor_User`, `Orcestor_Agent`, `Executer_Agent`.
   - `Executer_Agent` har doim `agy` (Antigravity CLI) hisoblanadi. `Orcestor_Agent` esa istalgan LLM (Claude, Codex, GPT va h.k.) bo'lishi mumkin.

1.1. **XAVF (real sinovda tasdiqlangan, aniq mexanik sabab bilan): Executer_Agent noto'g'ri workspace'da ishlashi.**
   - Sabab **gallyutsinatsiya yoki "xotira" emas** — bundan ancha oddiyroq va
     jiddiyroq: `agy -p "..."` buyrug'i ANIQ papka/workspace argumentisiz
     chaqirilsa, u ambient/inherited joriy papkaga (`cwd`) tayanadi. Agar bu
     chaqiruv **ichki/nested** tarzda amalga oshsa (masalan `Orcestor_Agent`
     ham `agy` bo'lib, o'zi ichida yana `agy -p ...`ni subprocess sifatida
     chaqirsa), inherited `cwd` HAR DOIM ham joriy, kutilgan loyiha bo'lishi
     shart emas — boshqa (oldingi/faol) workspace bo'lib chiqishi mumkin.
     Natijada Executer_Agent **butunlay boshqa, real loyihani** tahlil
     qiladi/o'zgartiradi, lekin natijani "joriy loyihaga tegishli" deb
     qaytaradi — va bu tashqi ko'rinishda "boshqa loyihadan texnologiya
     sizib kirdi" kabi ko'rinadi, aslida esa noto'g'ri papkada ishlagan.
   - **Oldini olish — QATTIQ QOIDA:** `agy -p ...` chaqiriladigan HAR safar,
     hech qachon ambient `cwd`ga ishonilmasin — buyruqqa ANIQ, mutlaq yo'l
     doim qo'shilsin: `cd "<WORKSPACE_PATH>" && agy -p "..." --dangerously-skip-permissions`
     (`<WORKSPACE_PATH>` — `orcestor.config.env`dagi qiymat, 2-qadamga
     qarang). Implicit/argumentsiz chaqiruv hech qachon ishlatilmasin —
     xuddi shu holat buni isbotladi.
   - **Tekshirish (Orcestor_Agent majburiy, KONKRET vazifasi):** shunchaki
     "tekshirdim" deyish YETARLI EMAS. Executer_Agent natijasini qabul
     qilishdan OLDIN, Orcestor_Agent **o'zi** joriy papkada bitta oddiy
     `ls`/`find` buyrug'ini bajarib, natijadagi kamida 1-2 ta konkret faktni
     (masalan "`src/` papkasi bormi", "`angular.json`/`package.json` bormi,
     va undagi qiymat Executer aytgan bilan mosmi") qo'lda solishtirsin.
     Mos kelmasa — natija RAD ETILADI, qayta (aniq path bilan) so'raladi,
     va bu holat `simple_context.md`ga qisqa qayd etiladi.

2. **Context Boshqaruvi va Update:**
   - Context restart FAQAT `Supervisor_User` so'raganda amalga oshiriladi (qattiq prompt limiti yo'q).
   - Context restart bo'lishidan oldin:
     - **`file` rejimida:** `orcestor/simple_context.md` fayli majburiy
       yangilanishi va joriy holat aks etishi shart.
     - **`db` rejimida:** `python3 scripts/orcestor.py checkpoint add`
       chaqirilishi shart (`--session-id` va `--summary` majburiy,
       ixtiyoriy `--blockers`/`--next-steps`/`--project` bilan) — bu
       `simple_context.md`ni yangilashning DB ekvivalenti.
   - `simple_context.md` (yoki DB'dagi `checkpoint add --summary`) har doim
     **QISQA** bo'lishi shart (taxminan 200-400 so'z). Unda to'liq muloqot
     tarixi emas, faqat:
     - Joriy holat (Current state)
     - Ko'rilgan muammolar (Short blockers/issues)
     - Keyingi qadamlar (Next steps)
     - Restart paytidagi token hisob-kitobi (quyiga qarang)

3. **Token sarfini kuzatib borish (restart samaradorligini o'lchash):**
   - Bu skillning butun maqsadi — sessiya-tarixi (odatda "Messages" toifasi) katta token isrofiga sabab bo'lishining oldini olish (real o'lchov: bitta sessiyada tekshirilganda System prompt/Tools/Memory/Skills jami ~3%, "Messages" esa yolg'iz ~27% — sezilarli farq).
   - Agar Orcestor_Agent shu imkoniyatga ega bo'lsa (masalan Claude Code'da `/context` buyrug'i), context restart QILISHDAN OLDIN joriy token taqsimotini tekshiring va "Messages" ulushini (yoki eng katta toifani) `simple_context.md`ga bitta qisqa qatorda qayd eting (masalan: "Restart oldida: Messages ~27% — kutilganidek").
   - Maqsad — vaqt o'tishi bilan bu ko'rsatkichning pasayib borishini kuzatish (restart intizomi chindan token tejayotganining dalili). Agar ko'rsatkich doim yuqori bo'lib qolsa — restartlar juda kech qilinayotganini bildiradi, Supervisor_User'ga shu haqda ogohlantirish bering.

4. **Small Context Backup — checkpoint, standing rules va memory yuklash intizomi:**
   Bu — 2.1–2.3-bandlardagi context-restart va token-tejash qoidalarining
   **markaziy konsepsiyasi**: har yangi sessiya/restart'da butun tarix yoki
   barcha hujjatlar emas, balki **faqat ayni task uchun kerakli minimal
   checkpoint, tegishli standing rule'lar va (kerak bo'lsa) memory
   fayllari** yuklanadi.

   - **Uch qatlamli model** (real loyihada — `zdes_frontend`, 2026-08-07 —
     sinovdan o'tgan va foydali topilgan uchinchi qatlam bilan):
     - **a) Checkpoint (session-scoped, tez eskiruvchi)** — "qayerga
       kelindik" degan ~200–400 so'zlik qisqa xulosa. `file` rejimida:
       `simple_context.md` (har safar ESKISI ALMASHTIRILADI, qo'shilmaydi).
       `db` rejimida: `session_checkpoints` jadvali (`checkpoint add` bilan
       yoziladi, `checkpoint get` bilan **faqat eng so'nggi qator**
       o'qiladi — `ORDER BY id DESC LIMIT 1`, hech qachon to'liq tarix
       emas).
     - **b) Standing rules (cross-session, sekin o'zgaruvchi, BIR QATOR)** —
       uzoq muddatli, mavzu (`topic`) bo'yicha **qisqa** qoidalar (masalan
       "build-verification", "agent-skills-usage"). `file` rejimida:
       `orcestor/standing_rules.json` (`{topic, rule}` massiv). `db`
       rejimida: `standing_rules` jadvali (`rule add` — topic bo'yicha
       UPSERT, ya'ni bir xil topic qayta yozilsa yangilanadi, dublikat
       qo'shilmaydi; `rule list` yoki `checkpoint get --topic <X>` — faqat
       kerakli mavzu bo'yicha filtrlab o'qiladi).
     - **c) Memory (cross-session, sekin o'zgaruvchi, TO'LIQ HUJJAT)** —
       `orcestor/memory/*.md` — (b)dan farqi: bitta qatorga sig'maydigan,
       **sabab/mulohaza (nega shunday qaror qilingan) bilan** hujjatlash
       kerak bo'lgan direktivalar (masalan model/effort siyosati, ko'p
       bosqichli reja, ish-taqsimoti qoidalari). Har mavzu — alohida fayl;
       `orcestor/memory/README.md` — bitta qatorlik indeks (barcha
       fayllarga havola bilan). **Reload intizomi (b)dan farqli**: indeks
       (`README.md`) har doim MAJBURIY o'qiladi (u qisqa), lekin
       individual `memory/*.md` fayllar **faqat joriy task/savol shu
       mavzuga bevosita aloqador bo'lsa** ochiladi — bu ham xuddi shu
       "kerakli topic bo'yicha filtrlash" tamoyili, faqat DB SELECT o'rniga
       inson/agent qaror qiladi qaysi faylni ochish kerakligini.
   - **Yozuvchi/o'quvchi rollari:** `Executer_Agent` (`agy`) — checkpoint
     yozuvchi (tez/arzon, mexanik ish uchun o'z tokenini ishlatadi).
     `Orcestor_Agent` — o'quvchi va **tasdiqlovchi**: yangi standing rule
     yoki memory fayli qo'shilishidan oldin uni ko'rib chiqadi
     (dublikat/zid qoidaning oldini olish uchun) — bu 2-bo'lim 1-banddagi
     "Rollar" tamoyiliga mos.
   - **MUHIM OGOHLANTIRISH — DB/fayl ishlatishning O'ZI tejamaydi:** agar
     DB rejimida `SELECT * FROM session_checkpoints`/`standing_rules`
     (filtrsiz, to'liq tarix) yuborilsa, file rejimida `simple_context.md`
     cheksiz uzayib ketishiga yo'l qo'yilsa, YOKI `memory/`dagi BARCHA
     fayllar har Resume'da to'liq o'qib chiqilsa — bu to'liq tarixni
     o'qishdan farqsiz, hech narsa tejalmaydi. Tejash faqat uch narsadan
     keladi: (1) checkpoint doim **bitta compact yozuv** bo'lishi (eskisi
     almashtiriladi, tarix jamg'arilmaydi), (2) standing rules **faqat
     kerakli topic bo'yicha** filtrlab olinishi, (3) memory **faqat
     indeks** majburiy o'qilishi, individual fayllar esa mavzu mos
     kelgandagina.

5. **Miyadan Ma'lumot Olish va Mukammal Prompt Yaratish (Digital Brain Integration):**
   - **Context Assembler:** Orcestor_Agent har qanday murakkab vazifani boshlashdan oldin "My Digital Brain" (masalan, `20_Areas/reports_agy/`, `90_System/Orcestor_MOC.md`) bazasidan joriy loyihaga va Foydalanuvchi (Fayzillo) ning shaxsiy uslubiga oid qoidalarni qidirib topadi.
   - **Perfect Prompt Generation (Qat'iy mantiq):** Gemini kabi tezkor agentlar (Executer) erkin logikada adashib ketmasligi uchun, Orcestor_Agent yig'ilgan bilimlarni birlashtirib, **o'ta qat'iy, aniq va tafsilotli mukammal PROMPT** yozadi. 
   - **Execution (Tezkor va Xatosiz Ijro):** Executer_Agent (`agy`) o'ylamaydi va reja tuzmaydi. U faqatgina Orcestor yozib bergan o'ta qat'iy promptni oladi va to'g'ridan-to'g'ri, juda tezlik bilan amaliyotga tatbiq qiladi. Bu - Autonomous Engineering System poydevoridir.

6. **AGY Natijalarini Majburiy Tasdiqlash (Verification Rule):**
   - **Tarixiy Sabab:** AGY (Executer) juda tez bo'lsa-da, o'xshash texnik terminlarni aralashtirib yuborishi va mavjud bo'lmagan buyruqlarni (masalan `mysql:alpine` kabi yo'q taglarni) gallyutsinatsiya qilishi tajribada isbotlangan.
   - **Qoida:** Orcestor_Agent hech qachon Executer_Agent qaytargan murakkab kodlarni, arxitektura xulosalarini yoki buyruqlarni ko'r-ko'rona to'g'ri deb qabul qilmaydi. Orcestor o'z mantiqi (Claude) bilan ularni albatta qayta tekshirishi, xato ko'rsa rad etishi va tuzatishi SHART.

7. **API Kvota (Limit) Tugaganda Harakat (Quota Management):**
   - Agar sessiya davomida Executer_Agent "Quota reached" yoki API limit xatosiga duch kelsa, avtomatik ravishda akkaunt almashtirishga (bash script orqali) urinmaslik kerak.
   - **Qoida:** Orcestor darhol ishni to'xtatadi va Supervisor_User'ga xabar beradi: *"Limit tugadi. Iltimos, terminalda o'zingiz `/logout` qiling va boshqa Google akkaunt bilan `/login` qilib kiring."*
   - Supervisor *"Almashtirildi"* deb tasdiqlamaguncha, navbatdagi tasklarga o'tilmaydi.

8. **Dinamik Agentlar Yaratish va Subtask Boshqaruvi (Agent-Creator Integratsiyasi):**
   - Agar topshiriq doimiy rollarga mos kelmasa, Orcestor_Agent bevosita **Agent-Creator** mantiqini ishga tushirib, yangi sub-agentni noldan yaratadi.
   - **SHAXSIY QOIDA:** Bu Orkestratsiya tizimi hammaviy emas, u **faqat Fayzillo uchun** moslashtirilgan. Shu sababli, har qanday yangi agent yaratishda Orcestor_Agent umumjahon "Best Practice" qoidalariga va eng asosiysi **Fayzilloning Obsidian Digital Brain tajribasiga** (Node.js, NestJS, DRY, Design Patterns) qat'iy tayanadi. Barcha yangi agentlar Fayzilloning uslubida fikrlashi shart.
   - **Subtask Boshqaruv Mantiqi:** Katta vazifalarni yangi agentlarga bo'lishda loyiha/chat tarixidan kelib chiqqan holda **Epic → Feature → Story → Task → Subtask** ierarxiyasiga qat'iy rioya qilinishi shart.
   - Har bir yaratilgan subtask (yoki agentga yuklanadigan topshiriq hujjatida) quyidagi metama'lumotlarni o'z ichiga olishi **majburiy**:
     - **ID** (masalan: `ORG-COMP-001`)
     - **Tavsif** (aniq, londa tushuntirish)
     - **Dependency** (ushbu task tugashi uchun avval qaysi tasklar bitishi kerak)
     - **Kerakli API va Komponentlar**
     - **Definition of Done** (Vazifa qachon "bajarildi" deb hisoblanishi)
     - **Test mezonlari** va **taxminiy murakkablik**.
   - Faqat shu (Enterprise Task Graph) yondashuvi orqaligina AGY yoki boshqa AI agentlari vazifalarni aralashtirib yubormasdan parallel tarzda muvaffaqiyatli bajara oladi.

9. **Vizual Tekshiruv (UI-Analyzer) — [Ixtiyoriy / Muammoli]:**
   - **DIQQAT:** Hozirgi kunda `agy-ui-analyzer` tizimida ayrim xatoliklar mavjud va u qayta ko'rib chiqishni talab etadi.
   - Shu sababli, frontend ishlari yakunlanganda Orcestor_Agent uni avtomatik ishga TUSHIRMAYDI. UI-Analyzer dan foydalanish **faqat va faqat Supervisor_User (Fayzillo) ning aniq ruxsati va xohishi bilangina** amalga oshiriladi.

---

## 3. Parallel Orkestratsiya va Ish Maydoni Izolyatsiyasi — Konflikt Ogohlantirishi

Ikki xil konflikt xavfi bor, ikkalasi ham shu bo'limda yechiladi:
**(a) bitta workspace ichida bir nechta agent bir xil taskni olib ketishi**
(ichki konflikt) va **(b) bir nechta MUSTAQIL loyiha/nusxa bir-biriga
aralashib ketishi** (tashqi/workspace-aro konflikt).

### (a) DB rejimi — ichki konflikt

- QOIDA 1: navbatdagi taskni olishda HECH QACHON qo'lda SELECT keyin UPDATE qilinmasin — doim `python3 scripts/orcestor.py task claim` (atomik, FOR UPDATE SKIP LOCKED) ishlatilsin (barcha uchta DB_ENGINE uchun ham amal qiladi — sqlite'da ham, postgres/mysql'da ham `task claim` ishlatilishi shart). `task claim` avtomatik ravishda joriy `WORKSPACE_PATH`ga tegishli tasklar orasidangina tanlaydi.

### (b) DB rejimi — workspace-aro izolyatsiya

- QOIDA 2: har loyiha o'z POSTGRES_CONTAINER_NAME/POSTGRES_PORT/POSTGRES_VOLUME_PATH (yoki MYSQL_*) kombinatsiyasiga ega bo'lishi kerak — ikkita turli loyiha bir-biriga aralashmasligi shu orqali ta'minlanadi.
- QOIDA 2.1 (qo'shimcha himoya qatlami): `tasks`, `task_events`, `changed_files`, `standing_rules`, `session_checkpoints` jadvallarining BARCHASIDA `workspace_path` ustuni bor va HAR BIR so'rov shu qiymat bilan filtrlanadi (`scripts/orcestor.py`da qattiq kodlangan). Ya'ni QOIDA 2 buzilib, bitta DB bir nechta loyiha orasida (qasddan yoki tasodifan) ulashilib qolsa ham, loyihalar ma'lumotlari aralashmaydi — har biri faqat o'z `workspace_path`iga tegishli qatorlarni ko'radi/o'zgartiradi.

### (a+b) File rejimi — fayl-darajasida atomik claim va workspace izolyatsiyasi

File-based rejimda DB yo'q, shuning uchun yuqoridagi mexanizm boshqacha
amalga oshiriladi:

- QOIDA 3 (ichki konflikt, DB'dagi `task claim`ning fayl ekvivalenti): task olish — faylni `orcestor/tasks/`dan `orcestor/task_pending/`ga **ko'chirish (mv/rename)** orqali amalga oshiriladi, hech qachon fayl ustida joyida (in-place) belgi qo'yish orqali emas. Fayl ko'chirish operatsion tizimda atomik. Agar ko'chirish vaqtida fayl "topilmadi" xatosi chiqsa — bu XATO EMAS, demak boshqa sessiya uni ALLAQACHON claim qilgan; keyingi faylga o'ting, urinishni takrorlamang.
- QOIDA 4 (workspace-aro izolyatsiya): har loyiha o'z, jismonan alohida `orcestor/` papkasiga ega bo'lgani uchun file-mode'da tabiiy izolyatsiya bor — LEKIN agar shu `orcestor/` papka boshqa joyga ko'chirilsa/nusxalansa/symlink qilinsa, ikki nusxa mustaqil ishlab, task holatlari zidlashishi mumkin. Shu xavfni ushlash uchun `WORKSPACE_PATH` (bootstrap'da yozib qo'yilgan mutlaq yo'l) har Resume'da solishtiriladi (C-bo'lim, 1-qadam) — mos kelmasa, Supervisor_User ANIQ ogohlantiriladi.

### Umumiy

- QOIDA 5: agar Supervisor_User bir xil loyihada ataylab bir nechta Orcestor_Agent sessiyasini parallel ishga tushirsa (workspace bitta, sessiya bir nechta — bu XAVFLI EMAS, QOIDA 1/3 buni qoplaydi), bootstrap/resume boshida foydalanuvchiga bu haqda ANIQ ESLATMA ko'rsatilsin: 'Diqqat: shu loyihada boshqa Orcestor_Agent sessiyasi ham ishlayotgan bo'lishi mumkin. Task olishda faqat `task claim` (DB) yoki fayl-ko'chirish (file) protsedurasidan foydalaning.'

---

## 4. Mavjud (eski) loyihada ishga tushirish — `project_status`

`simple_context.md` — sessiya-darajasida, tez eskiradi va restartda qisqa
holatga tushiriladi. `project_status/overview.md` esa BOSHQA maqsad uchun:
loyiha haqidagi bilim **vaqt o'tishi bilan to'planadi**, sessiyadan sessiyaga
o'chmaydi. Ikkalasi turli muammoni yechadi, biri ikkinchisini almashtirmaydi.

**Qachon ishlatiladi:** faqat orkestratsiya loyiha ichida BIRINCHI marta
(bootstrap paytida) ishga tushayotganda VA loyiha ESKI (mavjud kod bazasi,
git tarixi) bo'lsa. Yangi/bo'sh loyihada bu qadam o'tkazib yuboriladi —
o'rganadigan narsa yo'q.

**Tezkor va tejamkor tahlil — QANDAY bajariladi:**
- Tahlilni **Executer_Agent** (`agy`) bajaradi, `--print`/`-p` rejimida,
  **HAR DOIM aniq `WORKSPACE_PATH` bilan** (1.1-bandga qarang — ambient cwd'ga
  ishonib bo'lmaydi, ayniqsa Orcestor_Agent ham `agy` bo'lsa):
  `cd "<WORKSPACE_PATH>" && agy -p "Loyihani tahlil qil: texnologiya steki, papka tuzilishi,
  muhim modullar, aniqlangan konventsiyalar/qoidalar. Qisqa, bullet-point
  xulosa ber, fayl mazmunini so'zma-so'z ko'chirma." --dangerously-skip-permissions`
- **Orcestor_Agent xom loyiha fayllarini o'zi to'liq o'qib token sarflamaydi**
  — faqat Executer_Agent tayyorlagan qisqa xulosani ko'rib chiqadi/tasdiqlaydi
  (xuddi 2-bo'limdagi "Rollar" tamoyiliga mos: Executer — tez/arzon ijrochi,
  Orcestor — tekshiruvchi/tasdiqlovchi).
- **MUHIM (tekshirilgan, real xato asosida):** Executer_Agent natijasida
  gallyutsinatsiya/nomuvofiqlik bo'lishi mumkin — Orcestor_Agent xulosani
  ko'r-ko'rona qabul qilmasdan, kamida asosiy faktlarni (masalan texnologiya
  nomi, papka nomlari) haqiqiy loyiha bilan tez solishtirib tasdiqlashi kerak.

**Natija qayerga saqlanadi:** `orcestor/project_status/overview.md`
(`templates/project_status.md.template` asosida), 4 ta bo'lim bilan:
1. **Struktura** — texnologiya steki, papka tuzilishi, muhim modullar.
2. **Qoidalar va konventsiyalar** — loyihada aniqlangan yozilmagan/yozilgan
   qoidalar (kod uslubi, arxitektura qarorlari, taqiqlar).
3. **Bajarilgan ishlar** — qisqa, o'sib boruvchi tarix (juda uzayib ketsa,
   eng eski yozuvlar ixchamlashtiriladi, lekin butunlay o'chirilmaydi).
4. **Ma'lum muammolar / ochiq savollar** — aniqlangan, hali hal qilinmagan.

**Yangilanish chastotasi:** `orcestor.config.env`dagi `PROJECT_STATUS_UPDATE`
bilan belgilanadi (bootstrap'da so'raladi, 3.9-savol):
- `every_task` — har task yakunida avtomatik yangilanadi.
- `on_demand` — faqat Supervisor_User aniq so'raganda yangilanadi.

**Majburiy qoida:** ishni (birinchi taskni ham, resume qilingan taskni ham)
boshlashdan OLDIN, Orcestor_Agent `project_status/overview.md` mazmunini
Supervisor_User'ga QISQA bayon qilishi shart — foydalanuvchi har doim
ishni boshlashdan oldin joriy loyiha holatini bilishi kerak.


## Manba: `my_digital_brain/skill_sub_management_planning_information_docs/skill-vs-loyiha-qoidalari/qoida.md`

# Qoida (heuristika) — Qoidani qayerga yozish

## Savol 1: Bu qoida barcha loyihalarga tegishlimi?

- **Ha** (masalan "restart oldidan checkpoint yozish shart") → SKILL.md
  nomzodi, lekin SKILL.md'ni o'zgartirish ehtiyotkorlik bilan, faqat
  bir necha loyihada tasdiqlangandan keyin qilinsin.
- **Yo'q** (faqat shu loyiha/stack uchun) → standing_rules.json yoki
  memory/*.md.

## Savol 2: Bu qisqa buyruqmi yoki kontekst/sabab kerakmi?

- **Qisqa, bir qatorlik qoida** ("har doim X qil") → standing_rules.json.
- **Sabab-mulohaza, kelajakda "nega bunday qildik" savoliga javob
  beradigan** → memory/*.md.

## Savol 3: Bu hali eksperimental (sinov bosqichida)mi?

- **Ha** — hali 1-2 marta sinalgan, umumlashtirish erta → suhbat/checkpoint
  darajasida qoldiring, hali fayllashtirmang.
- **Yo'q** — bir necha marta tasdiqlangan, takrorlanuvchi patternga
  aylangan → mos qatlamga (standing_rules yoki memory) yozing.

## Amaliy default

Yangi kuzatuv paydo bo'lganda, avval **memory/*.md**ga yozish xavfsizroq
(kontekst bilan birga, keyin kerak bo'lsa qisqartirib standing_rules'ga
ko'chirish mumkin) — SKILL.md'ga to'g'ridan-to'g'ri yozish oxirgi qadam
bo'lsin, chunki u barcha loyihalarga ta'sir qiladi.


## Manba: `zdes_archive_docs/raw_history/orcestor/analysis/README.md`

# orcestor/analysis/

Bu papka — AGY (yoki Claude Code) og'ir/ko'p-modulga ta'sir qiluvchi arxitektura
qarorlarini kod yozishdan OLDIN qisqa tahlil hujjati sifatida yozib qo'yadigan
joy (masalan: umumiy komponent API dizayni, ma'lumotlar oqimi qarori).

Maqsad: keyingi modullarga ta'sir qiladigan noto'g'ri dizayn qarorlarini kod
yozib bo'lingandan keyin emas, oldin aniqlash — shu orqali AGY'ning cheklangan
resursi behuda ketmaydi (qayta yozishga sarflanmaydi).

Har bir tahlil fayli tegishli task ID bilan nomlanadi, masalan:
`T-005-datatable-api.md`.


## Manba: `zdes_archive_docs/raw_history/session/2026-07-25-responsive-darkmode-audit-handoff.md`

# 2026-07-25 — Backend-tahlil sessiyasi ko'chib keldi + T-033 audit

## Kontekst

`zdes/orcestor/` da backend (`zdes_backend`) tahlilini (Faza 1, `B-A-*`,
17/17 modul ACCEPTED) olib borgan sessiya shu kuni shu tizimga
(`test-zdes-front/orcestor/`, T-0XX) ko'chdi. Sabab: Fayzillo ikkita
parallel Claude Code sessiyasi (backend-tahlil + API-integratsiya)
o'rtasida fayl-konflikt bo'lmasligi uchun hududlarni ajratdi —
`zdes/orcestor/` endi to'liq API-integratsiya sessiyasiga tegishli,
bu sessiya esa shu yerda (T-0XX) frontend responsive/dark-mode/forma UX
ishini davom ettiradi.

To'liq tarix uchun: `../../session/2026-07-25-orcestor-backend-tahlil.md`
(zdes/ ildizida).

## Bugungi ish: T-033 — Responsive/Dark-mode audit (shallow)

Fayzillo so'rovi: "frontda pagelarda muammolar bor... formalar va dark
mode responsive qilish kerak... oldin shallow analiz qil". Natija:
`orcestor/analysis/T-033-responsive-darkmode-forms-audit.md`.

**Asosiy topilmalar:**
- 44 CSS fayldan atigi 4 tasida `@media` bor — responsive deyarli yo'q.
- Dark-mode migratsiyasi (T-013, 2026-07-24) **qisman** — 29 fayl hali
  hardcoded rang ishlatadi, 25 fayl CSS var(--) ishlatadi (ko'p fayl
  ikkalasini ARALASH ishlatadi — to'liq o'tish tugallanmagan).
- Eng yomon holat: `company-form.css` — 27 ta hardcoded rang qoldiq
  (garchi 14 ta var(--) allaqachon bor).
- Hech qanday dark-mode ishi qilinmagan formalar: `advance`,
  `work-schedule`, `terminal`, `leave` (4 ta, bir xil naqsh).
- `position-form.css`, `adjustment-form.css` — deyarli stilsiz, sababi
  hali tekshirilmagan.

**Tavsiya etilgan keyingi tasklar** (hali yozilmagan, Fayzillo
tasdiqlashini kutmoqda):
- T-034 — company-form dark-mode tozalash (eng ustuvor)
- T-035 — advance/work-schedule/terminal/leave formalari dark-mode
- T-036 — barcha 11 formaga responsive (`@media max-width:640px`,
  mavjud konvensiya) qo'shish

To'liq jadval: `orcestor/analysis/T-033-responsive-darkmode-forms-audit.md`.
