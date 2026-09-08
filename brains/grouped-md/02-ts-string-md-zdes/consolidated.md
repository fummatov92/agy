# Zdes loyihasi: Ta'tillar va davomomat moduli (Holiday & Attendance Management)


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-HOLIDAY.md`

## Task ID: B-I-HOLIDAY
### Sarlavha: Holiday modeli — yo'q maydonlarni qo'shish (startDate/endDate, companyId, affectsSalary va h.k.)

**Maqsad (Goal):**
`core/models/holiday.ts` juda yalang'och: faqat `id?, name, date`. Backend
`Holiday` esa sana **oralig'i** (`startDate`/`endDate`, bitta `date` emas),
`companyId`, `branchId`, `affectsSalary`, `note` bilan ishlaydi. Modelni
to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/holiday.md):**
- `Holiday` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  startDate (DateTime/date), endDate (DateTime/date), affectsSalary (boolean,
  default false), note (string | null), createdById (string | null),
  updatedById (string | null), createdAt, updatedAt`.
  **Bitta `date` maydoni yo'q — har doim `startDate`/`endDate` juftligi.**
- `POST/PATCH` DTO: `companyId?`, `branchId?`, `name` (majburiy), `startDate`
  (majburiy, ISO date), `endDate` (majburiy, ISO date, `endDate >= startDate`),
  `affectsSalary?`, `note?`.
- `GET /holidays` — paginatsiya: `{ items: Holiday[], total, page, limit, totalPages }`,
  filtrlar orasida `dateFrom`/`dateTo` bor.
- `DELETE /holidays/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/holiday.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/holiday.ts` — hozirgi holat:
  ```ts
  export interface Holiday {
    id?: string | number;
    name: string;
    date: string;
  }
  ```
  `id` — `string | number` aralash tipdan **faqat `string`ga** o'tkazing (UUID).
  `date` → `startDate`/`endDate` juftligiga almashtiriladi. Yetishmayotgan:
  `companyId`, `branchId`, `affectsSalary`, `note`, `createdAt`, `updatedAt`.
- `src/app/features/holidays/services/holiday.ts` — CRUD metodlari, `date`
  maydoniga bog'liq so'rov/javob parsing bo'lsa `startDate`/`endDate`ga moslang.
- `src/app/features/holidays/pages/holiday-form/holiday-form.ts`,
  `holiday-list/holiday-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`date` → `startDate`/`endDate` property nomlari) moslang. Agar formada
  bitta sana inputi bo'lsa-yu backend ikkita sana kutsa, buni javob faylida
  aniq eslating (HTML input soni o'zgartirish qamrovga kirmaydi — faqat
  mavjud `.ts` mantiqda to'g'ri property nomidan foydalanilishini ta'minlang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi input maydoni qo'shmang).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/holiday.ts`
- `test-zdes-front/src/app/features/holidays/services/holiday.ts`
- `test-zdes-front/src/app/features/holidays/pages/holiday-form/holiday-form.ts`
- `test-zdes-front/src/app/features/holidays/pages/holiday-list/holiday-list.ts`
- `test-zdes-front/project_docs/api/holidays.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Holiday` interfeysi to'liq backend bilan mos (`startDate`/`endDate`, `id: string`).
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-HOLIDAY-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-HOLIDAY.md` va `B-I-HOLIDAY-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-HOLIDAY.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-HOLIDAY
### Sarlavha: Holiday modeli — yo'q maydonlarni qo'shish (startDate/endDate, companyId, affectsSalary va h.k.)

**Maqsad (Goal):**
`core/models/holiday.ts` juda yalang'och: faqat `id?, name, date`. Backend
`Holiday` esa sana **oralig'i** (`startDate`/`endDate`, bitta `date` emas),
`companyId`, `branchId`, `affectsSalary`, `note` bilan ishlaydi. Modelni
to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/holiday.md):**
- `Holiday` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  startDate (DateTime/date), endDate (DateTime/date), affectsSalary (boolean,
  default false), note (string | null), createdById (string | null),
  updatedById (string | null), createdAt, updatedAt`.
  **Bitta `date` maydoni yo'q — har doim `startDate`/`endDate` juftligi.**
- `POST/PATCH` DTO: `companyId?`, `branchId?`, `name` (majburiy), `startDate`
  (majburiy, ISO date), `endDate` (majburiy, ISO date, `endDate >= startDate`),
  `affectsSalary?`, `note?`.
- `GET /holidays` — paginatsiya: `{ items: Holiday[], total, page, limit, totalPages }`,
  filtrlar orasida `dateFrom`/`dateTo` bor.
- `DELETE /holidays/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/holiday.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/holiday.ts` — hozirgi holat:
  ```ts
  export interface Holiday {
    id?: string | number;
    name: string;
    date: string;
  }
  ```
  `id` — `string | number` aralash tipdan **faqat `string`ga** o'tkazing (UUID).
  `date` → `startDate`/`endDate` juftligiga almashtiriladi. Yetishmayotgan:
  `companyId`, `branchId`, `affectsSalary`, `note`, `createdAt`, `updatedAt`.
- `src/app/features/holidays/services/holiday.ts` — CRUD metodlari, `date`
  maydoniga bog'liq so'rov/javob parsing bo'lsa `startDate`/`endDate`ga moslang.
- `src/app/features/holidays/pages/holiday-form/holiday-form.ts`,
  `holiday-list/holiday-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`date` → `startDate`/`endDate` property nomlari) moslang. Agar formada
  bitta sana inputi bo'lsa-yu backend ikkita sana kutsa, buni javob faylida
  aniq eslating (HTML input soni o'zgartirish qamrovga kirmaydi — faqat
  mavjud `.ts` mantiqda to'g'ri property nomidan foydalanilishini ta'minlang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi input maydoni qo'shmang).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/holiday.ts`
- `test-zdes-front/src/app/features/holidays/services/holiday.ts`
- `test-zdes-front/src/app/features/holidays/pages/holiday-form/holiday-form.ts`
- `test-zdes-front/src/app/features/holidays/pages/holiday-list/holiday-list.ts`
- `test-zdes-front/project_docs/api/holidays.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Holiday` interfeysi to'liq backend bilan mos (`startDate`/`endDate`, `id: string`).
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-HOLIDAY-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-HOLIDAY.md` va `B-I-HOLIDAY-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-COMPANY.md`

## Task ID: B-I-COMPANY
### Sarlavha: Company modeli — backendda yo'q maydonlarni olib tashlash, javob shaklini tekshirish

**Maqsad (Goal):**
`core/models/company.ts` da backendda umuman mavjud bo'lmagan uchta maydon bor
(`currency`, `workDayStart`, `workDayEnd`) — bular render/forma logikasida
noto'g'ri qiymatlarga (har doim `undefined`) tayanishga sabab bo'lishi mumkin.
Modelni `backend_crud_review/company.md`ga aynan moslab to'g'rilash.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/company.md):**
- `Company` javob/DB maydonlari (hammasi, 6 endpoint bo'yicha bir xil):
  `id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt`.
  **`currency`, `workDayStart`, `workDayEnd` degan maydonlar backendda YO'Q.**
- `POST/PATCH` DTO maydonlari: `name` (majburiy, 1-255), `legalName?`, `phone?` (≤50),
  `email?` (`@IsEmail`), `address?` (≤500), `logoUrl?` (≤500).
- `GET /companies` javobi — paginatsiya: `{ items: Company[], total, page, limit, totalPages }`.
- `DELETE /companies/:id` javobi: `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/company.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/company.ts` — `Company` interfeysida `currency?`,
  `workDayStart?`, `workDayEnd?` maydonlari bor, bular backend javobida
  hech qachon kelmaydi (o'chirilishi kerak, agar boshqa hech qayerda ataylab
  frontend-only maydon sifatida ishlatilmasa — shuni ham tekshiring:
  `company-form.ts`/`company-list.ts`da shu 3 maydon ishlatilayotgan bo'lsa,
  formadagi mos input/logikani ham olib tashlang, chunki backendga hech qachon
  yuborilmaydi/qaytmaydi).
- `src/app/features/company/services/company.ts` — `getAll`/`getById`/`create`/
  `update`/`delete` allaqachon bir nechta javob shaklini (`res.data.items`,
  `res.items`, `res.data`, massiv) himoyalab qayta ishlaydi — bu servis fayli
  o'zi to'g'ri ko'rinadi, faqat `Company` tipi to'g'rilangandan keyin qayta
  tekshiring (TS xatosi chiqmasligi uchun).
- `src/app/features/company/pages/company-form/company-form.ts` va
  `company-list/company-list.ts` — model o'zgarishidan keyin shu fayllardagi
  `.ts` mantiqni (forma maydonlari, jadval ustunlari uchun property access)
  moslang. **HTML/CSS ga tegmang.**

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — `company-form.html/css`, `company-list.html/css`ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/company.ts`
- `test-zdes-front/src/app/features/company/services/company.ts`
- `test-zdes-front/src/app/features/company/pages/company-form/company-form.ts`
- `test-zdes-front/src/app/features/company/pages/company-list/company-list.ts`
- `test-zdes-front/project_docs/api/company.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Company` interfeysi faqat backendda mavjud maydonlarni o'z ichiga oladi (yuqoridagi ro'yxat).
- `currency`/`workDayStart`/`workDayEnd`ga bog'liq forma/jadval kodi olib tashlangan yoki (agar ataylab frontend-only ekanligi aniqlansa) buni response.md da aniq izohlang, o'chirmang.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `orcestor/task_pending/B-I-COMPANY-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-COMPANY.md` va `B-I-COMPANY-response.md`ni `orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-WORK-SCHEDULE-response.md`

# B-I-WORK-SCHEDULE Progress

## Xulosa
`WorkSchedule` modeli backend talablariga mos ravishda to'liq qayta yozildi.
- Barcha `id` tiplari (`number`) `string` ga o'zgartirildi, chunki u UUID.
- Model interfeysiga `companyId`, `branchId`, `workDays`, `graceMinutes`, `isDefault`, `isActive`, `createdAt`, `updatedAt` kabi yangi maydonlar qo'shildi.
- `WorkScheduleService` xizmatida qo'shimcha backend endpoint'lari (masalan: `toggle-status`, `set-default`, `assign-user`, `unassign-user`) ulandi va id parametrlari `string` ga o'zgartirildi.
- Komponentlar (form, list) yangilangan string tipidagi `scheduleId` ni ishlatishga o'tkazildi.
- `npm run build` hech qanday xatolarsiz to'liq o'tdi.

## O'zgargan fayllar
| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/work-schedule.ts` | O'zgartirilgan | Backend formati bilan moslashtirilib to'liq qayta yozildi |
| `test-zdes-front/src/app/features/work-schedules/services/work-schedule.ts` | O'zgartirilgan | API tiplari va yangi metodlar (toggle, default, assign, unassign) qo'shildi |
| `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.ts` | O'zgartirilgan | scheduleId string qilib o'zgartirildi |
| `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-list/work-schedule-list.ts` | O'zgartirilgan | deleteWorkSchedule string id qabul qiladigan qilindi |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-WORK-SCHEDULE.md`

## Task ID: B-I-WORK-SCHEDULE
### Sarlavha: WorkSchedule modeli — to'liq qayta yozish (id string/UUID, workDays, graceMinutes, isDefault, isActive)

**Maqsad (Goal):**
`core/models/work-schedule.ts` juda yalang'och: `id?: number`, faqat `name,
startTime, endTime`. Backend `WorkSchedule` esa UUID `id`, `companyId`,
`branchId`, `workDays` (haftaning qaysi kunlari — 1-7 sonlar massivi),
`graceMinutes`, `isDefault`, `isActive`, `createdAt`, `updatedAt` bilan
ishlaydi. Modelni to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/work-schedule.md):**
- `WorkSchedule` javob/DB maydonlari:
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  startTime (string, "HH:mm"), endTime (string, "HH:mm"), workDays (number[], 1-7
  oralig'ida, JSON ustunda saqlanadi), graceMinutes (number, default 0),
  isDefault (boolean, default false), isActive (boolean, default true),
  createdAt, updatedAt`.
- `POST/PATCH` DTO qo'shimcha: `userId?` (create/update paytida shu userga
  biriktirish uchun, javobda saqlanmaydi — alohida `assign-user`/`unassign-user`
  endpointlari ham bor).
- `PATCH /work-schedules/:id/toggle-status` — body: `{ isActive?: boolean }`.
- `PATCH /work-schedules/:id/set-default` — body yo'q, `isDefault: true` qiladi
  (shu kompaniyadagi boshqa barcha grafiklarni `false` qiladi).
- `PATCH /work-schedules/:id/assign-user` va `.../unassign-user` — foydalanuvchini
  shu ish grafigiga biriktirish/uzish (alohida endpoint, `User.workScheduleId`ga ta'sir qiladi).
- `GET /work-schedules` — paginatsiya: `{ items, total, page, limit, totalPages }`.
- `DELETE /work-schedules/:id` — javob shakli uchun `../backend_crud_review/work-schedule.md`ga qarang.
- To'liq tafsilot: `../backend_crud_review/work-schedule.md` (9 endpoint, shu jumladan assign/unassign-user).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/work-schedule.ts` — hozirgi holat:
  ```ts
  export interface WorkSchedule {
    id?: number;
    name: string;
    startTime: string;
    endTime: string;
  }
  ```
  `id` **`number` emas, `string` (UUID)**. Yetishmayotgan: `companyId`,
  `branchId`, `workDays`, `graceMinutes`, `isDefault`, `isActive`, `createdAt`, `updatedAt`.
- `src/app/features/work-schedules/services/work-schedule.ts` — CRUD metodlari;
  `toggle-status`/`set-default`/`assign-user`/`unassign-user` uchun alohida
  metod bormi tekshiring, yo'q bo'lsa qo'shing (faqat request/response tipi
  darajasida, mavjud CRUD pattern bilan bir xil uslubda).
- `src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.ts`,
  `work-schedule-list/work-schedule-list.ts` — model o'zgarishidan keyin `.ts`
  mantiqni (`id` tipi, `workDays` bilan ishlash) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi kun-tanlash UI elementi qo'shmang, faqat mavjud kod to'g'ri tipdan foydalansin).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/work-schedule.ts`
- `test-zdes-front/src/app/features/work-schedules/services/work-schedule.ts`
- `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.ts`
- `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-list/work-schedule-list.ts`
- `test-zdes-front/project_docs/api/work-schedules.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `WorkSchedule` interfeysi to'liq backend bilan mos, `id`/`companyId`/`branchId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-WORK-SCHEDULE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-WORK-SCHEDULE.md` va `B-I-WORK-SCHEDULE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-WORK-SCHEDULE.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-WORK-SCHEDULE
### Sarlavha: WorkSchedule modeli — to'liq qayta yozish (id string/UUID, workDays, graceMinutes, isDefault, isActive)

**Maqsad (Goal):**
`core/models/work-schedule.ts` juda yalang'och: `id?: number`, faqat `name,
startTime, endTime`. Backend `WorkSchedule` esa UUID `id`, `companyId`,
`branchId`, `workDays` (haftaning qaysi kunlari — 1-7 sonlar massivi),
`graceMinutes`, `isDefault`, `isActive`, `createdAt`, `updatedAt` bilan
ishlaydi. Modelni to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/work-schedule.md):**
- `WorkSchedule` javob/DB maydonlari:
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  startTime (string, "HH:mm"), endTime (string, "HH:mm"), workDays (number[], 1-7
  oralig'ida, JSON ustunda saqlanadi), graceMinutes (number, default 0),
  isDefault (boolean, default false), isActive (boolean, default true),
  createdAt, updatedAt`.
- `POST/PATCH` DTO qo'shimcha: `userId?` (create/update paytida shu userga
  biriktirish uchun, javobda saqlanmaydi — alohida `assign-user`/`unassign-user`
  endpointlari ham bor).
- `PATCH /work-schedules/:id/toggle-status` — body: `{ isActive?: boolean }`.
- `PATCH /work-schedules/:id/set-default` — body yo'q, `isDefault: true` qiladi
  (shu kompaniyadagi boshqa barcha grafiklarni `false` qiladi).
- `PATCH /work-schedules/:id/assign-user` va `.../unassign-user` — foydalanuvchini
  shu ish grafigiga biriktirish/uzish (alohida endpoint, `User.workScheduleId`ga ta'sir qiladi).
- `GET /work-schedules` — paginatsiya: `{ items, total, page, limit, totalPages }`.
- `DELETE /work-schedules/:id` — javob shakli uchun `../backend_crud_review/work-schedule.md`ga qarang.
- To'liq tafsilot: `../backend_crud_review/work-schedule.md` (9 endpoint, shu jumladan assign/unassign-user).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/work-schedule.ts` — hozirgi holat:
  ```ts
  export interface WorkSchedule {
    id?: number;
    name: string;
    startTime: string;
    endTime: string;
  }
  ```
  `id` **`number` emas, `string` (UUID)**. Yetishmayotgan: `companyId`,
  `branchId`, `workDays`, `graceMinutes`, `isDefault`, `isActive`, `createdAt`, `updatedAt`.
- `src/app/features/work-schedules/services/work-schedule.ts` — CRUD metodlari;
  `toggle-status`/`set-default`/`assign-user`/`unassign-user` uchun alohida
  metod bormi tekshiring, yo'q bo'lsa qo'shing (faqat request/response tipi
  darajasida, mavjud CRUD pattern bilan bir xil uslubda).
- `src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.ts`,
  `work-schedule-list/work-schedule-list.ts` — model o'zgarishidan keyin `.ts`
  mantiqni (`id` tipi, `workDays` bilan ishlash) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi kun-tanlash UI elementi qo'shmang, faqat mavjud kod to'g'ri tipdan foydalansin).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/work-schedule.ts`
- `test-zdes-front/src/app/features/work-schedules/services/work-schedule.ts`
- `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.ts`
- `test-zdes-front/src/app/features/work-schedules/pages/work-schedule-list/work-schedule-list.ts`
- `test-zdes-front/project_docs/api/work-schedules.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `WorkSchedule` interfeysi to'liq backend bilan mos, `id`/`companyId`/`branchId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-WORK-SCHEDULE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-WORK-SCHEDULE.md` va `B-I-WORK-SCHEDULE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-DASHBOARD.md`

## Task ID: B-I-DASHBOARD
### Sarlavha: Dashboard — statik mock stat-cardlarni real servis chaqiruvlariga ulash

**Maqsad (Goal):**
`dashboard.ts` hozir **100% statik** — hech qanday servis chaqiruvi yo'q,
barcha qiymatlar qattiq yozilgan (`'0'`, `'0%'`). Backendda alohida
`dashboard` moduli/endpoint **yo'q** (`../backend_crud_review/dashboard.md`da
tasdiqlangan) — shuning uchun bu task boshqa modullarning allaqachon mavjud
`GET` endpointlariga tayanadi.

**MUHIM — BOG'LIQLIK:** Bu task quyidagi servislar to'g'ri tipda ishlashiga
tayanadi: `EmployeeService` (`B-I-USER`), `AttendanceService` (`B-I-ATTENDANCE`),
`LeaveService` (`B-I-EMPLOYEE-LEAVE`), `NotificationService` (`B-I-NOTIFICATION`).
**Agar shu tasklar hali bajarilmagan bo'lsa, avval ularni bajaring — aks holda
bu yerda noto'g'ri/eskirgan tipga tayanib yana bir marta noto'g'ri kod
yozilishi mumkin.** `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`da shu tasklarning
`B-I-*-response.md` fayllari bor-yo'qligini tekshirib boshlang.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Chaqirilayotgan servislar (`EmployeeService` va h.k.) buni
allaqachon to'g'ri unwrap qilgan bo'lishi kerak — shunchaki ularning
qaytargan `Observable<T[]>`/`Observable<PaginatedResult<T>>` natijasidan
foydalaning, o'zingiz yana bir marta `.data` deb ochishga urinmang.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/dashboard.md):**
- Alohida `/api/v1/dashboard` endpoint yo'q. Statistikalar mavjud modul
  endpointlaridan olinadi:
  - `GET /api/v1/users` — jami xodimlar (`total` paginatsiya maydonida).
  - `GET /api/v1/attendance?dateFrom=...&dateTo=...` — bugungi davomat (`total`,
    yoki `items` ichidan `status` bo'yicha hisoblash — `backend_crud_review/attendance.md`ga qarang).
  - `GET /api/v1/employee-leaves?...` — ochiq ta'til so'rovlari (eslatma:
    `B-I-EMPLOYEE-LEAVE`da topilganidek, backendda tasdiqlash `status`
    maydoni YO'Q — "ochiq so'rov" tushunchasi backendda mos kelmasligi
    mumkin, buni javob faylida aniq eslating).
  - `GET /api/v1/notifications?isRead=false` — o'qilmagan bildirishnomalar soni (`total`).
  - To'liq ro'yxat: `../backend_crud_review/dashboard.md`.

**Kontekst (Context — test-zdes-front hozirgi holati, o'zingiz o'qib solishtiring):**
- `src/app/features/dashboard/pages/dashboard/dashboard.ts` — hozirgi holat
  butunlay statik (`stats: DashboardStat[]` qattiq yozilgan qiymatlar bilan).
  Buni to'g'ridan-to'g'ri tuzatilgan servislarni (`EmployeeService`,
  `AttendanceService`, `LeaveService`, `NotificationService`) inject qilib,
  4 ta stat-cardni real `total`/hisoblangan qiymat bilan to'ldiradigan qilib
  yozing (Angular Signal yoki oddiy `async`/`Observable` bog'lash — `.ts`
  ichida, mavjud komponent strukturasini saqlagan holda).
- `dashboard.html`/`dashboard.css`ga tegmang — faqat `.ts` ichida signal/state
  bog'lashni yozing, hozirgi 4 ta stat-card strukturasi (`label`/`value`) saqlansin.
- Har bir servisning aniq qaysi metodini (`getAll`, paginatsiya parametri
  bilan) chaqirish kerakligini o'sha servis faylini o'qib aniqlang.

**Cheklovlar (Constraints):**
- Faqat `.ts` — HTML/CSS ga tegmang, yangi stat-card qo'shmang, mavjud 4
  tasini to'ldiring.
- `zdes_backend`ga yozmang.
- Boshqa modul fayllariga tegmang (faqat mavjud servislarni **chaqiring**,
  ularning ichiga o'zgartirish kiritmang).
- Agar biror stat uchun backendda mos endpoint/aniq mantiq topilmasa (masalan
  "ochiq ta'til so'rovi" tushunchasi), taxmin qilib yangi backend semantikasi
  o'ylab topmang — javob faylida aniq yozing va shu stat-cardni statik
  qoldiring (qolganlarini ulang).

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/features/dashboard/pages/dashboard/dashboard.ts`
- `test-zdes-front/project_docs/api/dashboard.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- Kamida "Jami xodimlar" va "O'qilmagan bildirishnomalar" real servis chaqiruvi bilan ishlaydi (bular eng aniq/oson bog'lanadigan statlar).
- Boshqa 2 ta stat uchun yoki real ulash, yoki aniq eskalatsiya (javob faylida) qilingan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-DASHBOARD-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-DASHBOARD.md` va `B-I-DASHBOARD-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-SETTING-response.md`

# Task B-I-SETTING Response

## Xulosa
`Setting` servisi va uning komponenti to'liq backend-dagi generic key-value modelga moslashtirildi. 
1. `setting.ts` dagi model `{ id, companyId, key, value, createdAt, updatedAt }` qilib o'zgartirildi. API orqali keladigan `data` ResponseInterceptor'dan to'g'ri o'qib olinishi uchun `map(res => res?.data ?? res)` qo'shildi. Servis metodlari CRUD operatsiyalari va paginatsiyani qo'llab-quvvatlaydigan holatga keltirildi.
2. `settings-page.ts` backend'ning generic tabiatiga moslandi. Barcha formadagi sozlamalar bazada JSON formatida bitta o'ziga xos `key: "company_settings"` bilan saqlanadigan bo'ldi. Dastlab `getAll` chaqirilib ushbu key qidiriladi, topilsa uning ID va `value` qiymatlari formaga o'zlashtiriladi, topilmasa yangi yaratiladi (create) yoki tahrirlanadi (update).
3. Dastur build qilinganda TypeScript xatolari kuzatilmadi.

## O'zgargan fayllar
| Fayl | Turi | Qisqa sabab |
|---|---|---|
| src/app/features/settings/services/setting.ts | o'zgartirilgan | Model va servis metodlarini backend generic key-value store'iga moslashtirish, data unwrap (map) |
| src/app/features/settings/pages/settings-page/settings-page.ts | o'zgartirilgan | Componentni yangi servis modeliga moslashtirish (key = 'company_settings' dan foydalanish) |


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_16.md`

# Step 16: Company Create DTO Fix & Branch Map Location Picker

## 📅 Bajarilgan Ishlar:

1. **Company Create / Update DTO Moslashtiruvi (`company-detail.ts` & `company-detail.html`)**:
   - NestJS `CreateCompanyDto` va `UpdateCompanyDto` sxemalariga to'liq moslashtirildi.
   - Frontenddan backend qabul qilmaydigan ortiqcha (`currency`, `workDayStart`, `workDayEnd`) maydonlar tozalandi va haqiqiy `legalName`, `phone`, `email`, `address`, `logoUrl` maydonlari qo'shildi.
   - Kompaniya hali yaratilmagan bo'lsa `POST /companies`, mavjud bo'lsa `PATCH /companies/:id` orqali saqlanishi ta'minlandi.

2. **Branch Interaktiv Map Picker va Manzil Qidiruv (`branch-form`)**:
   - Loyihaga **OpenStreetMap Leaflet Engine** ulandi ([index.html](file:///home/fayzillo/Desktop/zdes/test-zdes-front/src/index.html)).
   - **Xaritadan tanlash**: Xaritaga bosganda yoki pin-ni sudraganda `latitude` va `longitude` avtomatik olinadi hamda *Reverse Geocoding* orqali manzil matni to'ldiriladi.
   - **Manzil Qidiruvi**: Inputga manzil matnini kiritib **"🔍 Xaritada Qidirish"** tugmasi bosilganda xarita avtomatik o'sha koordinataga boradi va marker qo'yadi.
   - `latitude`, `longitude` hamda `radius` qiymatlari NestJS `CreateBranchDto` talablariga mos ravishda backendga yuboriladigan qilindi.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-AUTH.md`

## Task ID: B-I-AUTH
### Sarlavha: Auth — login/refresh/me response tiplarini backendga moslash

**Maqsad (Goal):**
`core/models/user.ts` dagi `LoginResponse` (va bog'liq tiplar) hozir noto'g'ri
"enveloped" shaklda yozilgan (`{ success, statusCode, message, data: { accessToken, user } }`).
Backend haqiqatda **flat** javob qaytaradi (`backend_crud_review/auth.md`).
Tipni backendga aynan moslab to'g'rilash — asosiy maqsad shu (response/request
type correctness), keyin shunga qarab `auth.ts` servisidagi parsing mantig'ini
soddalashtirish.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/auth.md):**
- `POST /api/v1/auth/login` javobi (flat, `data` wrapper YO'Q):
  `{ tokenType: string, accessToken: string, refreshToken: string, expiresIn: number, user: {...} }`
  — `user` obyekti: `id, login, role, companyId, branchId, departmentId, positionId, firstName, lastName, middleName, phone, email, employeeNo, faceDeviceUserId, isActive, isBlocked` (barchasi backend `User` modelidan, ko'pi `string | null` ixtiyoriy).
- `POST /api/v1/auth/refresh` — so'rov: `{ refreshToken: string }`; javob: login bilan bir xil shakl (`tokenType, accessToken, refreshToken, expiresIn, user`).
- `POST /api/v1/auth/logout` — so'rov: `{ refreshToken: string }`; javob: `{ success: true }` kabi oddiy tasdiq (aniqlik uchun `backend_crud_review/auth.md`dagi tegishli endpoint bo'limiga qarang).
- `GET /api/v1/auth/me` — javob: to'liq joriy foydalanuvchi `User` obyekti (login javobidagi `user` bilan bir xil maydon to'plami).
- To'liq tafsilot: `../backend_crud_review/auth.md` (4 endpoint, 8 bo'lim: DTO, response, error, DB struktura).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/user.ts` — `LoginResponse` interfeysi noto'g'ri: majburiy
  `data: { accessToken, refreshToken?, user }` wrapper bilan yozilgan, `tokenType`
  va `expiresIn` maydonlari umuman yo'q.
- `src/app/core/services/auth.ts` — `login()` metodi hozir ham `response.data?.accessToken`,
  ham `(response as any).accessToken` fallback bilan himoyalangan (ikkala holatga
  moslashtirilgan), chunki haqiqiy shakl noaniq edi. Endi backend tasdiqlangani
  uchun (**flat**, `data` yo'q) bu ikki xillik olib tashlanishi va tip to'g'ridan-to'g'ri
  flat shaklga mos yozilishi kerak.
- `src/app/features/auth/pages/login/login.ts` — login formasi shu servisdan foydalanadi.

**Cheklovlar (Constraints):**
- Faqat `.ts` fayllardagi tip/servis/data-binding mantig'ida ishlang — `login.html`/`login.css`ga tegmang.
- `zdes_backend`ga yozmang (bu tizimda hech qachon ruxsat yo'q).
- Boshqa modul (company/branch/...) fayllariga tegmang.
- `LoginCredentials` interfeysi allaqachon backend `LoginDto` bilan mos (`login, password, deviceType?, deviceName?`) — o'zgartirish shart emas, faqat tekshiring.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/user.ts`
- `test-zdes-front/src/app/core/services/auth.ts`
- `test-zdes-front/src/app/features/auth/pages/login/login.ts` (faqat kerak bo'lsa, tip o'zgarishi tufayli property nomi o'zgarganda)
- `test-zdes-front/project_docs/api/auth.md` (agar mavjud bo'lsa, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `LoginResponse` (va kerak bo'lsa yangi `RefreshResponse` tipi, agar refresh javobi alohida ishlatilsa) flat shaklga mos: `tokenType`, `accessToken`, `refreshToken`, `expiresIn`, `user`.
- `auth.ts` ichidagi ikki xil-shakl fallback mantig'i olib tashlangan, endi faqat flat shakl bilan ishlaydi.
- `User` interfeysi login/me javobidagi haqiqiy maydonlar bilan mos (`middleName`, `employeeNo`, `faceDeviceUserId`, `isBlocked` kabi yo'q maydonlarni qo'shing/to'g'rilang).
- `npm run build` (test-zdes-front ichida) xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-AUTH-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi (yangi/o'zgartirilgan/o'chirilgan) | Qisqa sabab).
- `B-I-AUTH.md` va `B-I-AUTH-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-SALARY-ADJUSTMENT.md`

## Task ID: B-I-SALARY-ADJUSTMENT
### Sarlavha: SalaryAdjustment modeli — companyId/category/month qo'shish, id tipini to'g'irlash

**Maqsad (Goal):**
`core/models/salary-adjustment.ts` da `id`/`employeeId` `number` deb yozilgan
(backendda UUID `string`), va `category`/`month`/`companyId`/audit maydonlari
butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/salary-adjustment.md):**
- `SalaryAdjustment` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), type
  (AdjustmentType), category (AdjustmentCategory, default manual), amount
  (number, Decimal(15,2)), date (string/DateTime), month (string, "YYYY-MM"),
  reason (string | null), createdById (string | null), updatedById (string | null),
  createdAt, updatedAt`.
- `AdjustmentType`/`AdjustmentCategory` enum qiymatlari to'liq sanalmagan
  (misolda `AdjustmentType.bonus`, default `AdjustmentCategory.manual` ko'rsatilgan)
  — qat'iy union o'ylab topmang (frontenddagi `'bonus' | 'penalty'` union
  to'g'ri bo'lishi mumkin, lekin tasdiqlanmagan — xohlasangiz `string` qilib
  xavfsizroq qoldiring, javob faylida qaysi variantni tanlaganingizni yozing).
- `GET /salary-adjustments` — paginatsiya: `{ items, total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/salary-adjustment.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/salary-adjustment.ts` — hozirgi holat:
  ```ts
  export interface SalaryAdjustment {
    id: number;
    employeeId: number;
    amount: number;
    type: 'bonus' | 'penalty';
    reason?: string;
    date: string;
  }
  ```
  `id`/`employeeId` — **`number` emas, `string` (UUID)**. Yetishmayotgan:
  `companyId`, `category`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/salary-adjustments/services/salary-adjustment.ts` — CRUD
  metodlari, `id` tipini `string`ga moslang.
- `src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.ts`,
  `adjustment-list/adjustment-list.ts` — model o'zgarishidan keyin `.ts`
  mantiqni moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/salary-adjustment.ts`
- `test-zdes-front/src/app/features/salary-adjustments/services/salary-adjustment.ts`
- `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.ts`
- `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-list/adjustment-list.ts`
- `test-zdes-front/project_docs/api/salary-adjustments.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `SalaryAdjustment` interfeysi to'liq backend bilan mos, `id`/`employeeId`/`companyId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-SALARY-ADJUSTMENT-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-SALARY-ADJUSTMENT.md` va `B-I-SALARY-ADJUSTMENT-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-ADVANCE.md`

## Task ID: B-I-ADVANCE
### Sarlavha: Advance modeli — companyId/month/audit maydonlarini qo'shish, id tipini to'g'irlash

**Maqsad (Goal):**
`core/models/advance.ts` juda yalang'och va `id`/`employeeId` aralash
(`string | number`) tipda yozilgan. Backend `Advance` UUID `id`, `companyId`,
`month`, audit maydonlari (`createdById`/`updatedById`) bilan ishlaydi.
Modelni to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/advance.md):**
- `Advance` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), amount (number,
  Decimal(15,2)), date (string/DateTime), month (string, "YYYY-MM", ≤7 belgi),
  note (string | null), createdById (string | null), updatedById (string | null),
  createdAt, updatedAt`.
- `POST` DTO: `companyId?`, `employeeId` (majburiy), `amount` (majburiy, `Min(0)`),
  `date` (majburiy, ISO), `month?`, `note?`.
- `GET /advances` — paginatsiya: `{ items: Advance[], total, page, limit, totalPages }`.
- `DELETE /advances/:id` — javob shakli uchun `../backend_crud_review/advance.md`ga qarang.
- To'liq tafsilot: `../backend_crud_review/advance.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/advance.ts` — hozirgi holat:
  ```ts
  export interface Advance {
    id: string | number;
    employeeId: string | number;
    amount: number;
    reason?: string;
    date: string;
  }
  ```
  `id`/`employeeId` **faqat `string`ga** (UUID) o'tkazing. `reason` maydoni
  backendda yo'q — backendda bu `note` deb ataladi, nomini to'g'irlang.
  Yetishmayotgan: `companyId`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/advances/services/advance.ts` — CRUD metodlari, `id` tipi
  va `reason`→`note` nomlanishini moslang.
- `src/app/features/advances/pages/advance-form/advance-form.ts`,
  `advance-list/advance-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`reason` ishlatilgan joylarni `note`ga) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (agar formadagi input nomi `reason` bo'lsa-yu HTML label/`formControlName` ham o'zgarishi kerak bo'lsa, `.ts`dagi FormGroup control nomini o'zgartirish HTML bilan bog'liq — bunday holatni javob faylida aniq eslating, xatarli/noaniq bo'lsa eskalatsiya qiling).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/advance.ts`
- `test-zdes-front/src/app/features/advances/services/advance.ts`
- `test-zdes-front/src/app/features/advances/pages/advance-form/advance-form.ts`
- `test-zdes-front/src/app/features/advances/pages/advance-list/advance-list.ts`
- `test-zdes-front/project_docs/api/advances.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Advance` interfeysi to'liq backend bilan mos, `id`/`employeeId`/`companyId` `string` tipida, `note` (`reason` emas).
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-ADVANCE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-ADVANCE.md` va `B-I-ADVANCE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_pending/B-I-DEPARTMENT.md`

## Task ID: B-I-DEPARTMENT
### Sarlavha: Department — tip mosligini tasdiqlash, servis/komponent javob shaklini tekshirish

**Maqsad (Goal):**
`core/models/department.ts` maydon jihatidan `backend_crud_review/department.md`ga
allaqachon yaqin mos ko'rinadi (boshqa modullardagi kabi aniq nomuvofiqlik
topilmadi). Bu task **tasdiqlash + servis/paginatsiya darajasidagi** ishga
qaratilgan: `department.ts` servisi va list/form komponentlari haqiqatda
backend javobini (paginatsiyali `{items,total,...}`) to'g'ri parslayotganini
tekshirish va kerak bo'lsa tuzatish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/department.md):**
- `Department` javob/DB maydonlari: `id, companyId, branchId, name, isActive, createdAt, updatedAt`.
- `POST/PATCH` DTO: `companyId?`, `branchId?` (`string | null`), `name` (majburiy, 1-255).
- `GET /departments` — paginatsiya: `{ items: Department[], total, page, limit, totalPages }`.
- `DELETE /departments/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/department.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/department.ts` — maydonlar mos ko'rinadi, lekin
  `branchId`/`companyId` ixtiyoriylik (`?`) va `null` qabul qilishini backend
  bilan solishtirib tasdiqlang (backendda `branchId` request DTOda
  `string | null` bo'lishi mumkin — modelda ham shu nuance saqlansin).
- `src/app/features/departments/services/department.ts` — `getAll` metodi
  paginatsiyali javobni to'g'ri unwrap qilyaptimi (`company.ts`dagi kabi
  bir nechta shaklga chidamli pattern bormi yoki oddiy massiv deb kutyaptimi) —
  tekshirib, kerak bo'lsa `company.ts` servisidagi patternga moslang.
- `src/app/features/departments/pages/department-list/department-list.ts` —
  `zdes/review/tasks/step_16.md`da Signal-based (`OnPush`) qilib qayta
  yozilgan — shu Signal state bilan paginatsiya javobi (`items` massivi)
  to'g'ri bog'langanini tasdiqlang.
- `src/app/features/departments/pages/department-form/department-form.ts` —
  `branchId` dropdown (step_9.md bo'yicha allaqachon dynamic select qilingan)
  `Department` tipidagi `branchId?: string | null` bilan mos ishlayotganini
  tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/department.ts`
- `test-zdes-front/src/app/features/departments/services/department.ts`
- `test-zdes-front/src/app/features/departments/pages/department-form/department-form.ts`
- `test-zdes-front/src/app/features/departments/pages/department-list/department-list.ts`
- `test-zdes-front/project_docs/api/departments.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Department` tipi va servis javob-parsing mantig'i backend bilan tasdiqlangan/mos.
- Paginatsiya javobi list komponentida xato bermasdan render bo'ladi (bo'sh massiv holatini ham hisobga oling).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-DEPARTMENT-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-DEPARTMENT.md` va `B-I-DEPARTMENT-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-ADVANCE.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-ADVANCE
### Sarlavha: Advance modeli — companyId/month/audit maydonlarini qo'shish, id tipini to'g'irlash

**Maqsad (Goal):**
`core/models/advance.ts` juda yalang'och va `id`/`employeeId` aralash
(`string | number`) tipda yozilgan. Backend `Advance` UUID `id`, `companyId`,
`month`, audit maydonlari (`createdById`/`updatedById`) bilan ishlaydi.
Modelni to'liq qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/advance.md):**
- `Advance` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), amount (number,
  Decimal(15,2)), date (string/DateTime), month (string, "YYYY-MM", ≤7 belgi),
  note (string | null), createdById (string | null), updatedById (string | null),
  createdAt, updatedAt`.
- `POST` DTO: `companyId?`, `employeeId` (majburiy), `amount` (majburiy, `Min(0)`),
  `date` (majburiy, ISO), `month?`, `note?`.
- `GET /advances` — paginatsiya: `{ items: Advance[], total, page, limit, totalPages }`.
- `DELETE /advances/:id` — javob shakli uchun `../backend_crud_review/advance.md`ga qarang.
- To'liq tafsilot: `../backend_crud_review/advance.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/advance.ts` — hozirgi holat:
  ```ts
  export interface Advance {
    id: string | number;
    employeeId: string | number;
    amount: number;
    reason?: string;
    date: string;
  }
  ```
  `id`/`employeeId` **faqat `string`ga** (UUID) o'tkazing. `reason` maydoni
  backendda yo'q — backendda bu `note` deb ataladi, nomini to'g'irlang.
  Yetishmayotgan: `companyId`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/advances/services/advance.ts` — CRUD metodlari, `id` tipi
  va `reason`→`note` nomlanishini moslang.
- `src/app/features/advances/pages/advance-form/advance-form.ts`,
  `advance-list/advance-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`reason` ishlatilgan joylarni `note`ga) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (agar formadagi input nomi `reason` bo'lsa-yu HTML label/`formControlName` ham o'zgarishi kerak bo'lsa, `.ts`dagi FormGroup control nomini o'zgartirish HTML bilan bog'liq — bunday holatni javob faylida aniq eslating, xatarli/noaniq bo'lsa eskalatsiya qiling).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/advance.ts`
- `test-zdes-front/src/app/features/advances/services/advance.ts`
- `test-zdes-front/src/app/features/advances/pages/advance-form/advance-form.ts`
- `test-zdes-front/src/app/features/advances/pages/advance-list/advance-list.ts`
- `test-zdes-front/project_docs/api/advances.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Advance` interfeysi to'liq backend bilan mos, `id`/`employeeId`/`companyId` `string` tipida, `note` (`reason` emas).
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-ADVANCE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-ADVANCE.md` va `B-I-ADVANCE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-HOLIDAY-response.md`

# B-I-HOLIDAY Natijasi

## Bajarilgan Ishlar
1. `core/models/holiday.ts` dagi `Holiday` modeli backend bilan moslashtirildi (`startDate`, `endDate`, `companyId` va h.k. qo'shildi, `id` tipi `string` ga o'zgartirildi).
2. `features/holidays/services/holiday.ts` da barcha CRUD operatsiyalari uchun global javobni yechish (`res?.data ?? res`) va `id` ni `string` sifatida qabul qilish amalga oshirildi.
3. `features/holidays/pages/holiday-form/holiday-form.ts` dagi mantiq model bilan moslashib, bitta `date` form qiymatini ham `startDate`, ham `endDate` uchun ishlatishga o'tkazildi (frontend dagi forma tuzilishiga tegilmasdan).
4. `features/holidays/pages/holiday-list/holiday-list.html` va `holiday-list.ts` da `date` o'rniga yangi `startDate` ga o'zgartirildi (HTML dagi xatoni tuzatish uchun).
5. `npm run build` muvaffaqiyatli o'tdi.
6. DB'ga task tugallanganligi va uning o'zgargan fayllari kiritildi.

## O'zgargan Fayllar

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/holiday.ts` | o'zgartirilgan | Holiday modeli backendga moslashtirildi |
| `test-zdes-front/src/app/features/holidays/services/holiday.ts` | o'zgartirilgan | .data unwrap qilindi, id tipi o'zgardi |
| `test-zdes-front/src/app/features/holidays/pages/holiday-form/holiday-form.ts` | o'zgartirilgan | startDate/endDate TS mapping qo'shildi |
| `test-zdes-front/src/app/features/holidays/pages/holiday-list/holiday-list.ts` | o'zgartirilgan | id tipi faqat string ga o'zgartirildi |
| `test-zdes-front/src/app/features/holidays/pages/holiday-list/holiday-list.html` | o'zgartirilgan | build xatosini oldini olish uchun date startDate ga o'zgartirildi |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-POSITION.md`

## Task ID: B-I-POSITION
### Sarlavha: Position modeli — yo'q maydonlarni qo'shish (companyId, isActive, createdAt, updatedAt)

**Maqsad (Goal):**
`core/models/position.ts` juda yalang'och: faqat `id, name, departmentId`.
Backend `Position` javobida bundan ancha ko'p maydon bor (`companyId`, `isActive`,
`createdAt`, `updatedAt`). Bu yetishmovchilik position-list/form da status
toggle, kompaniya scoping va sana ko'rsatish kabi funksiyalarning ishlamasligiga
yoki noto'g'ri (undefined) render bo'lishiga sabab bo'ladi.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/position.md):**
- `Position` javob/DB maydonlari (barcha 6 endpoint bo'yicha bir xil):
  `id, companyId, departmentId, name, isActive, createdAt, updatedAt`.
- `POST/PATCH` DTO: `companyId?`, `departmentId?`, `name` (majburiy, 1-255).
- `GET /positions` — paginatsiya: `{ items: Position[], total, page, limit, totalPages }`.
- `DELETE /positions/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/position.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/position.ts` — hozirgi holat:
  ```ts
  export interface Position {
    id: string;
    name: string;
    departmentId?: string;
  }
  ```
  Yetishmayotgan: `companyId?: string`, `isActive?: boolean`, `createdAt?: string`, `updatedAt?: string`.
- `src/app/features/positions/services/position.ts` — CRUD metodlari, paginatsiya
  javobini qanday parslashini tekshiring (`company.ts`dagi chidamli pattern bilan solishtiring).
- `src/app/features/positions/pages/position-list/position-list.ts` — `isActive`
  ustuni/badge yo'qligi sababli hozir status ko'rsatilmayotgan bo'lishi mumkin —
  tip to'ldirilgach shu komponentda status render qilish uchun zarur bo'lsa
  `.ts` mantig'ini (property binding) ham moslang (jadval ustuni QO'SHISH emas,
  faqat mavjud bo'lsa property nomini to'g'irlash — yangi UI elementi qo'shish
  HTML/CSS qamroviga kirgani uchun chetda qoladi, faqat mavjud kod ishlaydigan bo'lsin).
- `src/app/features/positions/pages/position-form/position-form.ts` — `departmentId`
  dropdown (step_9.md bo'yicha dynamic select) `Position` tipi bilan mos ekanini
  tasdiqlang, `companyId` (superadmin uchun) hisobga olinganini tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi UI elementi qo'shmang).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/position.ts`
- `test-zdes-front/src/app/features/positions/services/position.ts`
- `test-zdes-front/src/app/features/positions/pages/position-form/position-form.ts`
- `test-zdes-front/src/app/features/positions/pages/position-list/position-list.ts`
- `test-zdes-front/project_docs/api/positions.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Position` interfeysi to'liq: `id, companyId?, departmentId?, name, isActive?, createdAt?, updatedAt?`.
- Servis/komponent `.ts` fayllari yangi maydonlar bilan TS xatosiz ishlaydi.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-POSITION-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-POSITION.md` va `B-I-POSITION-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-DEPARTMENT.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-DEPARTMENT
### Sarlavha: Department — tip mosligini tasdiqlash, servis/komponent javob shaklini tekshirish

**Maqsad (Goal):**
`core/models/department.ts` maydon jihatidan `backend_crud_review/department.md`ga
allaqachon yaqin mos ko'rinadi (boshqa modullardagi kabi aniq nomuvofiqlik
topilmadi). Bu task **tasdiqlash + servis/paginatsiya darajasidagi** ishga
qaratilgan: `department.ts` servisi va list/form komponentlari haqiqatda
backend javobini (paginatsiyali `{items,total,...}`) to'g'ri parslayotganini
tekshirish va kerak bo'lsa tuzatish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/department.md):**
- `Department` javob/DB maydonlari: `id, companyId, branchId, name, isActive, createdAt, updatedAt`.
- `POST/PATCH` DTO: `companyId?`, `branchId?` (`string | null`), `name` (majburiy, 1-255).
- `GET /departments` — paginatsiya: `{ items: Department[], total, page, limit, totalPages }`.
- `DELETE /departments/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/department.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/department.ts` — maydonlar mos ko'rinadi, lekin
  `branchId`/`companyId` ixtiyoriylik (`?`) va `null` qabul qilishini backend
  bilan solishtirib tasdiqlang (backendda `branchId` request DTOda
  `string | null` bo'lishi mumkin — modelda ham shu nuance saqlansin).
- `src/app/features/departments/services/department.ts` — `getAll` metodi
  paginatsiyali javobni to'g'ri unwrap qilyaptimi (`company.ts`dagi kabi
  bir nechta shaklga chidamli pattern bormi yoki oddiy massiv deb kutyaptimi) —
  tekshirib, kerak bo'lsa `company.ts` servisidagi patternga moslang.
- `src/app/features/departments/pages/department-list/department-list.ts` —
  `zdes/review/tasks/step_16.md`da Signal-based (`OnPush`) qilib qayta
  yozilgan — shu Signal state bilan paginatsiya javobi (`items` massivi)
  to'g'ri bog'langanini tasdiqlang.
- `src/app/features/departments/pages/department-form/department-form.ts` —
  `branchId` dropdown (step_9.md bo'yicha allaqachon dynamic select qilingan)
  `Department` tipidagi `branchId?: string | null` bilan mos ishlayotganini
  tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/department.ts`
- `test-zdes-front/src/app/features/departments/services/department.ts`
- `test-zdes-front/src/app/features/departments/pages/department-form/department-form.ts`
- `test-zdes-front/src/app/features/departments/pages/department-list/department-list.ts`
- `test-zdes-front/project_docs/api/departments.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Department` tipi va servis javob-parsing mantig'i backend bilan tasdiqlangan/mos.
- Paginatsiya javobi list komponentida xato bermasdan render bo'ladi (bo'sh massiv holatini ham hisobga oling).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-DEPARTMENT-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-DEPARTMENT.md` va `B-I-DEPARTMENT-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-AUTH.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-AUTH
### Sarlavha: Auth — login/refresh/me response tiplarini backendga moslash

**Maqsad (Goal):**
`core/models/user.ts` dagi `LoginResponse` (va bog'liq tiplar) hozir noto'g'ri
"enveloped" shaklda yozilgan (`{ success, statusCode, message, data: { accessToken, user } }`).
Backend haqiqatda **flat** javob qaytaradi (`backend_crud_review/auth.md`).
Tipni backendga aynan moslab to'g'rilash — asosiy maqsad shu (response/request
type correctness), keyin shunga qarab `auth.ts` servisidagi parsing mantig'ini
soddalashtirish.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/auth.md):**
- `POST /api/v1/auth/login` javobi (flat, `data` wrapper YO'Q):
  `{ tokenType: string, accessToken: string, refreshToken: string, expiresIn: number, user: {...} }`
  — `user` obyekti: `id, login, role, companyId, branchId, departmentId, positionId, firstName, lastName, middleName, phone, email, employeeNo, faceDeviceUserId, isActive, isBlocked` (barchasi backend `User` modelidan, ko'pi `string | null` ixtiyoriy).
- `POST /api/v1/auth/refresh` — so'rov: `{ refreshToken: string }`; javob: login bilan bir xil shakl (`tokenType, accessToken, refreshToken, expiresIn, user`).
- `POST /api/v1/auth/logout` — so'rov: `{ refreshToken: string }`; javob: `{ success: true }` kabi oddiy tasdiq (aniqlik uchun `backend_crud_review/auth.md`dagi tegishli endpoint bo'limiga qarang).
- `GET /api/v1/auth/me` — javob: to'liq joriy foydalanuvchi `User` obyekti (login javobidagi `user` bilan bir xil maydon to'plami).
- To'liq tafsilot: `../backend_crud_review/auth.md` (4 endpoint, 8 bo'lim: DTO, response, error, DB struktura).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/user.ts` — `LoginResponse` interfeysi noto'g'ri: majburiy
  `data: { accessToken, refreshToken?, user }` wrapper bilan yozilgan, `tokenType`
  va `expiresIn` maydonlari umuman yo'q.
- `src/app/core/services/auth.ts` — `login()` metodi hozir ham `response.data?.accessToken`,
  ham `(response as any).accessToken` fallback bilan himoyalangan (ikkala holatga
  moslashtirilgan), chunki haqiqiy shakl noaniq edi. Endi backend tasdiqlangani
  uchun (**flat**, `data` yo'q) bu ikki xillik olib tashlanishi va tip to'g'ridan-to'g'ri
  flat shaklga mos yozilishi kerak.
- `src/app/features/auth/pages/login/login.ts` — login formasi shu servisdan foydalanadi.

**Cheklovlar (Constraints):**
- Faqat `.ts` fayllardagi tip/servis/data-binding mantig'ida ishlang — `login.html`/`login.css`ga tegmang.
- `zdes_backend`ga yozmang (bu tizimda hech qachon ruxsat yo'q).
- Boshqa modul (company/branch/...) fayllariga tegmang.
- `LoginCredentials` interfeysi allaqachon backend `LoginDto` bilan mos (`login, password, deviceType?, deviceName?`) — o'zgartirish shart emas, faqat tekshiring.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/user.ts`
- `test-zdes-front/src/app/core/services/auth.ts`
- `test-zdes-front/src/app/features/auth/pages/login/login.ts` (faqat kerak bo'lsa, tip o'zgarishi tufayli property nomi o'zgarganda)
- `test-zdes-front/project_docs/api/auth.md` (agar mavjud bo'lsa, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `LoginResponse` (va kerak bo'lsa yangi `RefreshResponse` tipi, agar refresh javobi alohida ishlatilsa) flat shaklga mos: `tokenType`, `accessToken`, `refreshToken`, `expiresIn`, `user`.
- `auth.ts` ichidagi ikki xil-shakl fallback mantig'i olib tashlangan, endi faqat flat shakl bilan ishlaydi.
- `User` interfeysi login/me javobidagi haqiqiy maydonlar bilan mos (`middleName`, `employeeNo`, `faceDeviceUserId`, `isBlocked` kabi yo'q maydonlarni qo'shing/to'g'rilang).
- `npm run build` (test-zdes-front ichida) xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `orcestor/task_pending/B-I-AUTH-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi (yangi/o'zgartirilgan/o'chirilgan) | Qisqa sabab).
- `B-I-AUTH.md` va `B-I-AUTH-response.md`ni `orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-USER.md`

## Task ID: B-I-USER
### Sarlavha: Employee (backend `user` moduli) — model maydonlarini backendga to'liq moslash

**Maqsad (Goal):**
Backend `user` moduli frontendda `employees` feature'iga mos keladi
(`core/models/employee.ts`). Hozirgi `Employee` interfeysida backendda yo'q
ikkita maydon (`fullName`, `status`, `hiredAt`) va backendda bor, lekin
frontendda yo'q ko'plab maydon bor (`managerId`, `workScheduleId`, `address`,
`passportSerial`, `dateOfBirth`, `avatarUrl`, `faceImageUrl`, `baseSalary`).
Asosiy maqsad — response/request tiplarni backendga aynan moslash.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/user.md):**
- `User` javob maydonlari (`POST/GET/PATCH /api/v1/users` bo'yicha bir xil):
  `id, login, role, companyId, branchId, departmentId, positionId, managerId,
  workScheduleId, employeeNo, firstName, lastName, middleName, phone, email,
  address, passportSerial, dateOfBirth, avatarUrl, faceDeviceUserId,
  faceImageUrl, baseSalary, isActive, isBlocked, createdAt, updatedAt`.
  **`fullName`, `status`, `hiredAt` degan maydonlar backendda YO'Q.**
- `dateOfBirth`: `DateTime` (`@db.Date`, faqat sana), `baseSalary`: `Decimal(15,2)`
  (JSON orqali odatda `string` yoki `number` kelishi mumkin — real javobda qanday
  serializatsiya qilinganini komponentda ishlatishdan oldin tekshiring).
- `PATCH /users/me` — o'zini yangilash uchun cheklangan maydon to'plami bor
  (parolni bu orqali o'zgartirib bo'lmaydi — `change-password` alohida endpoint).
- `PATCH /users/:id/toggle-status`, `toggle-blocked`, `change-password` — alohida
  kichik endpointlar, `isActive`/`isBlocked`/parolni navbatma-navbat boshqaradi.
- `DELETE /users/:id` — javob shakli uchun `../backend_crud_review/user.md`dagi
  DELETE bo'limiga qarang.
- To'liq tafsilot (9 endpoint, 8 bo'limlik tahlil): `../backend_crud_review/user.md`.

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/employee.ts` — hozirgi holat: `id?, login?, firstName?,
  lastName?, middleName?, fullName?, phone?, email?, role?, companyId?,
  branchId?, departmentId?, positionId?, isActive?, isBlocked?, employeeNo?,
  faceDeviceUserId?, status?: 'active'|'inactive', hiredAt?, createdAt?, updatedAt?`.
  - `status: 'active'|'inactive'` — backendda bunday enum yo'q, haqiqiy holat
    `isActive: boolean` orqali ifodalanadi. Komponentlarda `status` ishlatilgan
    joylarni topib, `isActive`ga o'tkazing (yoki ikkalasi ham kerak bo'lsa,
    `status`ni `isActive`dan hisoblanadigan derived qiymat qiling — backendga
    yubormang).
  - `hiredAt` — backendda mos maydon yo'q (ehtimol `createdAt` yoki `dateOfBirth`
    bilan adashtirilgan) — ishlatilgan joylarni tekshirib, kerak bo'lsa `createdAt`ga
    almashtiring yoki butunlay olib tashlang.
  - `fullName` — backendda yo'q, hisoblab chiqariladigan (`firstName + lastName`)
    frontend-only qulaylik bo'lishi mumkin — agar shunday ishlatilsa qoldiring,
    lekin izohda "backend maydoni emas, computed" deb belgilang.
  - Yetishmayotgan: `managerId?`, `workScheduleId?`, `address?`, `passportSerial?`,
    `dateOfBirth?`, `avatarUrl?`, `faceImageUrl?`, `baseSalary?`.
- `src/app/features/employees/services/employee.ts` — CRUD + `toggle-status`/
  `toggle-blocked`/`change-password` uchun alohida metodlar bormi tekshiring,
  yo'q bo'lsa backend endpointlariga mos qo'shing (faqat shu servis fayli
  ichida, request/response tipi darajasida).
- `src/app/features/employees/pages/employee-form/employee-form.ts`,
  `employee-detail/employee-detail.ts`, `employee-list/employee-list.ts` —
  model o'zgarishidan keyin `.ts` mantiqni (property access, forma default
  qiymatlari) moslang.
- Eslatma: `core/models/user.ts` dagi `User` (auth/login javobi) va
  `core/models/employee.ts` dagi `Employee` bir xil backend `User` modelidan
  kelsa-da, ikki xil interfeys sifatida saqlanmoqda (login qisqartirilgan
  maydon to'plami qaytaradi, `/users/:id` esa to'liq) — buni ataylab shunday
  qoldiring, birlashtirmang (alohida modul, `B-I-AUTH`da ko'rib chiqiladi).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- `auth`/`user.ts` (login modeli) ga tegmang — bu `B-I-AUTH` qamroviga kiradi.
- `face-register` komponentiga (`faceDescriptor`/face-recognition oqimi) tegmang — bu alohida, murakkabroq oqim, shu task doirasida emas.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/employee.ts`
- `test-zdes-front/src/app/features/employees/services/employee.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-form/employee-form.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-detail/employee-detail.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-list/employee-list.ts`
- `test-zdes-front/project_docs/api/employees.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Employee` interfeysi backend `User` javobiga to'liq mos (yuqoridagi to'liq ro'yxat), backendda yo'q maydonlar (`status`, `hiredAt`) tozalangan yoki aniq derived/frontend-only deb izohlangan.
- Servis metodlari (`toggle-status`, `toggle-blocked`, `change-password` kabi) mavjud bo'lsa to'g'ri tip bilan ishlaydi.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-USER-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-USER.md` va `B-I-USER-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-ADVANCE-response.md`

# B-I-ADVANCE - Advance modeli yangilanishi

## Bajarilgan ishlar xulosasi
Advance moduli bo'yicha berilgan barcha talablar va cheklovlar to'liq bajarildi. Xususan:
- `Advance` modelidagi `id` va `employeeId` tiplari faqat `string` (UUID) ga o'zgartirildi.
- Backend maydonlari: `companyId`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt` modelga qo'shildi. `reason` nomi backendga mos ravishda `note` ga o'zgartirildi.
- `AdvanceService` interfeyslarida id parametrlari `string` ga o'tkazildi va backend tomonidan global interceptor orqali keladigan `data` o'ramini ochish uchun `map((res: any) => res?.data ?? res)` o'zgarishi barcha endpoint metodlariga (getById, create, update, delete) qo'shildi.
- `advance-form.ts` va `advance-list.ts` da HTML (va `formControlName`) larni o'zgartirmaslik (cheklov: HTML/CSS ga tegmaslik) maqsadida Typescript qismi moslashtirildi:
  - Formada kiritilgan (yoki serverdan olingan) `reason` qiymatlari tarmoq orqali yuborilganda `note` ga o'tkazilmoqda.
  - Listda kelayotgan Advance obyektlari massivida har bir elementdan `note` qabul qilinib, list interfeysi HTMLda o'rnatilgan `<td\>{{ advance.reason }}</td\>` build xatosi bermasligi uchun `.ts` tarafda `reason` xususiyatiga biriktirilgan holda type-safe tarzda o'rab (mapping) berildi.
- Build muvaffaqiyatli xatosiz yakunlandi (`npm run build`).

## O'zgargan fayllar
| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/advance.ts` | O'zgartirilgan | Modelga backend audit maydonlari qo'shildi, tiplar moslashtirildi |
| `test-zdes-front/src/app/features/advances/services/advance.ts` | O'zgartirilgan | id tiplari stringga o'tkazildi va response data mapper (unwrap) qo'shildi |
| `test-zdes-front/src/app/features/advances/pages/advance-form/advance-form.ts` | O'zgartirilgan | HTML o'zgarmasligi uchun formadagi `reason` ma'lumotlari zaprosda `note`ga o'tkazildi |
| `test-zdes-front/src/app/features/advances/pages/advance-list/advance-list.ts` | O'zgartirilgan | HTML buildni buzuqmasligi uchun keladigan tipni modifikatsiyalab (reason -> note) maplandi |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-NOTIFICATION-response.md`

## B-I-NOTIFICATION Natijasi

**Xulosa:**
- `core/models/notification.ts` ga yetishmayotgan maydonlar (`userId`, `icon`, `updatedAt`) qo'shildi. `id` maydoni faqat `string` qilib o'zgartirildi.
- `features/notifications/services/notification.ts` da `markAsRead` payloadida `read: true` o'rniga backend kutayotgan `isRead: true` beriladigan bo'ldi.
- **ESKALATSIYA (Chegaraviy holat):** `Notification` modelida `read` ni `isRead` ga o'zgartirish `notification-list.html` shablonini (`!notification.read` va h.k.) ham o'zgartirishni talab etadi. Topshiriqdagi cheklovlarga muvofiq ("Faqat .ts tip/servis/data-binding — HTML/CSS ga tegmang" va "Agar read→isRead almashtirish HTML shablonini ham o'zgartirishga majbur qilsa, kodni o'zgartirmang — javob faylida aniq eskalatsiya qiling"), **`.ts` fayllarida `read` nomi `isRead` ga o'zgartirilmadi** va xuddi shunday qoldirildi. Bu holat HTML tomonini ham o'zgartirish orqali to'liq hal qilinishi kerak.

### O'zgargan fayllar

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/notification.ts` | o'zgartirilgan | Backendga mos `userId`, `icon`, `updatedAt` maydonlari qo'shildi, `id` tipi to'g'rilandi. `read` o'zgarishsiz qoldi (eskalatsiya). |
| `test-zdes-front/src/app/features/notifications/services/notification.ts` | o'zgartirilgan | `markAsRead` payloadiga backend kutgan `isRead: true` berildi. |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-TERMINAL.md`

## Task ID: B-I-TERMINAL
### Sarlavha: Terminal modeli — to'liq qayta yozish (id string/UUID, barcha maydonlar backendga mos)

**Maqsad (Goal):**
`core/models/terminal.ts` hozir juda eskirgan/taxminiy: `id: number`,
`branchId?: number`, faqat 4 maydon. Backend `Terminal` esa UUID `id`, 12
maydon va ikkita enum (`TerminalType`, `TerminalStatus`) bilan ishlaydi.
Modelni backend bilan to'liq moslab qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/terminal.md):**
- `Terminal` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  serialNumber (string, unique), ipAddress (string | null), port (number | null),
  type (TerminalType, default zkteco_face), status (TerminalStatus, default active),
  connectionConfig (Record<string, unknown> | null), lastSyncAt (string | null),
  createdAt, updatedAt`.
  **`TerminalType`/`TerminalStatus` aniq qiymatlari tahlil hujjatida sanab
  o'tilmagan** — faqat defaultlari ma'lum (`zkteco_face`, `active`). Qat'iy
  enum union yozmang; `string` sifatida qoldiring (aniq qiymatlar ro'yxati
  kerak bo'lsa, buni javob faylida eslatib qo'ying — keyingi taskda backend
  tahlili to'ldirilishi mumkin).
- `GET /terminals` — paginatsiya: `{ items: Terminal[], total, page, limit, totalPages }`.
- `DELETE /terminals/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/terminal.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/terminal.ts` — hozirgi holat:
  ```ts
  export interface Terminal {
    id: number;
    name: string;
    branchId?: number;
    ipAddress?: string;
  }
  ```
  `id`/`branchId` **`number` emas, `string` (UUID)** bo'lishi kerak. Yetishmayotgan:
  `companyId`, `serialNumber`, `port`, `type`, `status`, `connectionConfig`,
  `lastSyncAt`, `createdAt`, `updatedAt`.
- `src/app/features/terminals/services/terminal.ts` — CRUD metodlari, `id`
  parametrlari hozir `number` deb yozilgan bo'lishi mumkin — `string`ga
  moslang, paginatsiya javobini qanday parslashini tekshiring.
- `src/app/features/terminals/pages/terminal-form/terminal-form.ts`,
  `terminal-list/terminal-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`id` tipi, forma default qiymatlari) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/terminal.ts`
- `test-zdes-front/src/app/features/terminals/services/terminal.ts`
- `test-zdes-front/src/app/features/terminals/pages/terminal-form/terminal-form.ts`
- `test-zdes-front/src/app/features/terminals/pages/terminal-list/terminal-list.ts`
- `test-zdes-front/project_docs/api/terminals.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Terminal` interfeysi to'liq backend bilan mos (yuqoridagi to'liq ro'yxat), `id`/`branchId`/`companyId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-TERMINAL-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-TERMINAL.md` va `B-I-TERMINAL-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-NOTIFICATION.md`

## Task ID: B-I-NOTIFICATION
### Sarlavha: Notification modeli — `read` → `isRead`, yo'q maydonlarni qo'shish

**Maqsad (Goal):**
`core/models/notification.ts` da maydon nomi backend bilan mos emas:
frontend `read: boolean`, backend `isRead: boolean`. Bu — filter/belgilash
mantig'ining jimgina ishlamay qolishiga sabab bo'ladigan tipik nomlanish
xatosi. Shuningdek `userId` va `icon` maydonlari butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/notification.md):**
- `Notification` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), userId (string | null), title (string), message (string),
  icon (NotificationIcon | null), isRead (boolean, default false), createdAt, updatedAt`.
  **`read` degan maydon YO'Q — nomi `isRead`.**
- `NotificationIcon` enum qiymatlari tahlil hujjatida to'liq sanalmagan (misolda
  `NotificationIcon.money` ko'rsatilgan) — qat'iy union yozmang, `string`
  sifatida qoldiring.
- `GET /notifications` — paginatsiya: `{ items: Notification[], total, page, limit, totalPages }`.
- `PATCH /notifications/:id` — odatda `isRead`ni belgilash uchun ishlatiladi.
- To'liq tafsilot: `../backend_crud_review/notification.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/notification.ts` — hozirgi holat:
  ```ts
  export interface Notification {
    id: string | number;
    title: string;
    message: string;
    read: boolean;
    createdAt: string;
  }
  ```
  `id` — faqat `string`. `read` → `isRead`ga o'zgartiring. Yetishmayotgan:
  `userId`, `icon`, `updatedAt`.
- `src/app/features/notifications/services/notification.ts` — CRUD/mark-as-read
  metodlari `read` propertysiga tayanadigan bo'lsa, `isRead`ga moslang.
- `src/app/features/notifications/pages/notification-list/notification-list.ts` —
  `notification.read` ishlatilgan barcha joylarni `notification.isRead`ga
  o'tkazing (bu `.ts` ichidagi property access, HTML/CSS ga tegilmaydi —
  agar HTML shablonida `notification.read` interpolatsiyasi bo'lsa, bu holatni
  javob faylida aniq eslating, chegaraviy holat sifatida).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar `read`→`isRead` almashtirish HTML shablonini ham o'zgartirishga majbur
  qilsa, kodni o'zgartirmang — javob faylida aniq eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/notification.ts`
- `test-zdes-front/src/app/features/notifications/services/notification.ts`
- `test-zdes-front/src/app/features/notifications/pages/notification-list/notification-list.ts`
- `test-zdes-front/project_docs/api/notifications.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Notification` interfeysi to'liq backend bilan mos (`isRead`, `id: string`, `userId`, `icon`).
- `.ts` fayllardagi barcha `read` foydalanishi `isRead`ga moslangan (yoki HTML bog'liqligi aniq eskalatsiya qilingan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-NOTIFICATION-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-NOTIFICATION.md` va `B-I-NOTIFICATION-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-POSITION.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-POSITION
### Sarlavha: Position modeli — yo'q maydonlarni qo'shish (companyId, isActive, createdAt, updatedAt)

**Maqsad (Goal):**
`core/models/position.ts` juda yalang'och: faqat `id, name, departmentId`.
Backend `Position` javobida bundan ancha ko'p maydon bor (`companyId`, `isActive`,
`createdAt`, `updatedAt`). Bu yetishmovchilik position-list/form da status
toggle, kompaniya scoping va sana ko'rsatish kabi funksiyalarning ishlamasligiga
yoki noto'g'ri (undefined) render bo'lishiga sabab bo'ladi.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/position.md):**
- `Position` javob/DB maydonlari (barcha 6 endpoint bo'yicha bir xil):
  `id, companyId, departmentId, name, isActive, createdAt, updatedAt`.
- `POST/PATCH` DTO: `companyId?`, `departmentId?`, `name` (majburiy, 1-255).
- `GET /positions` — paginatsiya: `{ items: Position[], total, page, limit, totalPages }`.
- `DELETE /positions/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/position.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/position.ts` — hozirgi holat:
  ```ts
  export interface Position {
    id: string;
    name: string;
    departmentId?: string;
  }
  ```
  Yetishmayotgan: `companyId?: string`, `isActive?: boolean`, `createdAt?: string`, `updatedAt?: string`.
- `src/app/features/positions/services/position.ts` — CRUD metodlari, paginatsiya
  javobini qanday parslashini tekshiring (`company.ts`dagi chidamli pattern bilan solishtiring).
- `src/app/features/positions/pages/position-list/position-list.ts` — `isActive`
  ustuni/badge yo'qligi sababli hozir status ko'rsatilmayotgan bo'lishi mumkin —
  tip to'ldirilgach shu komponentda status render qilish uchun zarur bo'lsa
  `.ts` mantig'ini (property binding) ham moslang (jadval ustuni QO'SHISH emas,
  faqat mavjud bo'lsa property nomini to'g'irlash — yangi UI elementi qo'shish
  HTML/CSS qamroviga kirgani uchun chetda qoladi, faqat mavjud kod ishlaydigan bo'lsin).
- `src/app/features/positions/pages/position-form/position-form.ts` — `departmentId`
  dropdown (step_9.md bo'yicha dynamic select) `Position` tipi bilan mos ekanini
  tasdiqlang, `companyId` (superadmin uchun) hisobga olinganini tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang (yangi UI elementi qo'shmang).
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/position.ts`
- `test-zdes-front/src/app/features/positions/services/position.ts`
- `test-zdes-front/src/app/features/positions/pages/position-form/position-form.ts`
- `test-zdes-front/src/app/features/positions/pages/position-list/position-list.ts`
- `test-zdes-front/project_docs/api/positions.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Position` interfeysi to'liq: `id, companyId?, departmentId?, name, isActive?, createdAt?, updatedAt?`.
- Servis/komponent `.ts` fayllari yangi maydonlar bilan TS xatosiz ishlaydi.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-POSITION-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-POSITION.md` va `B-I-POSITION-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-EMPLOYEE-LEAVE.md`

## Task ID: B-I-EMPLOYEE-LEAVE
### Sarlavha: EmployeeLeave modeli — maydon nomlarini va yo'q "approval status" mantig'ini to'g'irlash

**Maqsad (Goal):**
`core/models/employee-leave.ts` backendda **umuman mavjud bo'lmagan**
tasdiqlash oqimini (`status: 'pending'|'approved'|'rejected'`) taxmin qilib
yozilgan, va maydon nomlari ham mos emas (`startDate/endDate` o'rniga backendda
`fromDate/toDate`). Buni tuzatish — ayniqsa `status` maydoni: agar
`leave-list.ts`/`leave-form.ts`da tasdiqlash UI logikasi shunga tayansa, bu
render/funksionallik xatosi keltirib chiqaradi (backend hech qachon bunday
maydon qaytarmaydi).

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/employee-leave.md):**
- `EmployeeLeave` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string), companyId (string), branchId (string | null), employeeId (string),
  type (LeaveType, default vacation), fromDate (string/DateTime), toDate (string/DateTime),
  days (number), affectsSalary (boolean, default false), reason (string | null),
  createdById (string | null), updatedById (string | null), createdAt, updatedAt`.
  **`status` (pending/approved/rejected) degan maydon backendda YO'Q — tasdiqlash
  workflow'i bu modulda mavjud emas.**
- `LeaveType` enum qiymatlari tahlil hujjatida to'liq sanalmagan (faqat
  default `vacation` va misolda `vacation` ko'rsatilgan) — qat'iy union
  yozmang, `string` sifatida qoldiring va javob faylida shuni eslating.
- `POST/PATCH` DTO: `employeeId` (majburiy), `companyId?`, `branchId?`,
  `type`, `fromDate`, `toDate`, `days?` (berilmasa backend hisoblaydi),
  `affectsSalary?`, `reason?`.
- `GET /employee-leaves` — paginatsiya: `{ items: EmployeeLeave[], total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/employee-leave.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/employee-leave.ts` — hozirgi holat:
  ```ts
  export interface EmployeeLeave {
    id: number;
    employeeId: number;
    startDate: string;
    endDate: string;
    type: 'vacation' | 'sick' | 'unpaid';
    status: 'pending' | 'approved' | 'rejected';
  }
  ```
  `id`/`employeeId` **`number` emas, `string` (UUID)**. `startDate`/`endDate`
  → `fromDate`/`toDate`ga o'zgartirilishi kerak. **`status` maydoni butunlay
  olib tashlanishi kerak** (yoki komponentlarda ishlatilayotgan bo'lsa, bu
  aniq "backend workflow yo'q" degan topilma sifatida javob faylida
  hujjatlashtirilib, komponent mantig'i shunga qarab moslashtirilishi kerak —
  masalan approve/reject tugmalari bo'lsa, ular hozircha hech qanday real
  endpointga ulanmagani aniq bo'ladi). Yetishmayotgan: `companyId`, `branchId`,
  `days`, `affectsSalary`, `reason`, `createdAt`, `updatedAt`.
- `src/app/features/leaves/services/leave.ts` — CRUD metodlari, maydon nomi
  o'zgarishidan (`fromDate`/`toDate`) keyin qayta tekshiring.
- `src/app/features/leaves/pages/leave-form/leave-form.ts`,
  `leave-list/leave-list.ts` — **agar bu fayllarda `status`ga bog'liq
  tasdiqlash/rad etish tugmalari yoki filtri bo'lsa, buni javob faylida
  aniq ta'kidlang** — bu HTML/CSS o'zgarishi talab qiladigan chegaraviy holat
  bo'lishi mumkin (`requirements.MD` 0-bo'lim), shu holatda kodni o'zgartirmasdan
  faqat aniqlang va eskalatsiya qiling (task scope'ini kengaytirmang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar `status` maydonini olib tashlash HTML shablonini ham o'zgartirishga
  majbur qilsa (masalan `*ngIf="leave.status === 'pending'"`), **bunday
  holatni avtomatik hal qilmang** — javob faylida aniq tavsiflab, Claude Code
  (orchestrator) ko'rib chiqishini so'rang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/employee-leave.ts`
- `test-zdes-front/src/app/features/leaves/services/leave.ts`
- `test-zdes-front/src/app/features/leaves/pages/leave-form/leave-form.ts`
- `test-zdes-front/src/app/features/leaves/pages/leave-list/leave-list.ts`
- `test-zdes-front/project_docs/api/leaves.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `EmployeeLeave` interfeysi backendga mos (`fromDate`/`toDate`, `status` yo'q, `id`/`employeeId` `string`).
- `status`ga bog'liq HTML mantiq topilgan bo'lsa, javob faylida aniq eskalatsiya qilingan (kod o'zgartirilmagan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-EMPLOYEE-LEAVE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-EMPLOYEE-LEAVE.md` va `B-I-EMPLOYEE-LEAVE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-SALARY-ADJUSTMENT-response.md`

# B-I-SALARY-ADJUSTMENT Response

## Bajarilgan ishlar:
- `SalaryAdjustment` modeli backendga to'liq moslashtirildi: `id`, `companyId`, `employeeId` tiplari `string` ga o'zgartirildi; yangi maydonlar qo'shildi (`category`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt`). `type` maydoni string qilindi.
- `SalaryAdjustmentService` CRUD metodlarining barchasida `id` parametri tipi `string` ga o'zgartirildi.
- `AdjustmentList` va `AdjustmentForm` komponentlarida `.ts` mantiqdagi `id` tipi (shuningdek formdan o'qib olishdagi unary operator olib tashlanishi) `string` qilib to'g'rilandi.
- `test-zdes-front` build qilindi.

## O'zgargan fayllar
| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/salary-adjustment.ts` | o'zgartirilgan | DB va backend interfeysi bilan moslash uchun id va maydonlar tiplari va soni to'g'rilandi |
| `test-zdes-front/src/app/features/salary-adjustments/services/salary-adjustment.ts` | o'zgartirilgan | CRUD API da id tipini string sifatida qabul qilishga moslashtirildi |
| `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-list/adjustment-list.ts` | o'zgartirilgan | delete id tipini string ga o'tkazildi |
| `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.ts` | o'zgartirilgan | url param dan id ni string tarzida olishga o'zgartirildi |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-AUTH-response.md`

# B-I-AUTH: Response

## Muhim qadamlar
1. `backend_crud_review/auth.md` faylidagi backend API hujjatlari o'qib chiqildi va tekshirildi (User, LoginResponse, RefreshResponse va boshqalar).
2. `src/app/core/models/user.ts` faylidagi `User` va `LoginResponse` interfeyslari flat (tekis) strukturaga hamda backend ma'lumotlariga to'liq moslandi (id, login, role va boshqa ixtiyoriy maydonlar). `username` maydoni olib tashlandi, chunki backendda faqat `login` ishlatiladi.
3. `src/app/core/services/auth.ts` faylida xatolikka olib kelishi mumkin bo'lgan fallback (.data.accessToken va .accessToken) tekshiruvlari o'chirildi, endilikda u to'g'ridan-to'g'ri `response.accessToken` hamda `response.user` sifatida flat ravishda ishlatilmoqda. `_loadUserFromToken` dagi `username` o'chirildi.
4. `username` interfeysdan olib tashlanganligi sababli dasturni build qilishda yuzaga kelgan TypeScript (TS2339) xatoliklari (ya'ni `src/app/shared/components/layout/header/header.ts` va `src/app/shared/components/profile-modal/profile-modal.html`) to'g'rilandi.
5. `npm run build` muvaffaqiyatli bajarildi (xatolarsiz o'tdi).

## O'zgargan fayllar jadvali

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `src/app/core/models/user.ts` | O'zgartirilgan | Backend `LoginResponse` va `User` ob'yektlarini flat strukturasiga aynan moslash va barcha ixtiyoriy maydonlarni kiritish uchun. |
| `src/app/core/services/auth.ts` | O'zgartirilgan | Flat (tekis) API response bilan ishlash, eskirgan `.data` wrapper'ini va `username` larni olib tashlash. |
| `src/app/shared/components/layout/header/header.ts` | O'zgartirilgan | `User` ob'yektidan olib tashlangan `username` hususiyati murojaatlarini `login` ga almashtirish. |
| `src/app/shared/components/profile-modal/profile-modal.html` | O'zgartirilgan | Template ichida ishlatilgan `user?.username` havolalarini olib tashlash. |


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-COMPANY.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-COMPANY
### Sarlavha: Company modeli — backendda yo'q maydonlarni olib tashlash, javob shaklini tekshirish

**Maqsad (Goal):**
`core/models/company.ts` da backendda umuman mavjud bo'lmagan uchta maydon bor
(`currency`, `workDayStart`, `workDayEnd`) — bular render/forma logikasida
noto'g'ri qiymatlarga (har doim `undefined`) tayanishga sabab bo'lishi mumkin.
Modelni `backend_crud_review/company.md`ga aynan moslab to'g'rilash.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/company.md):**
- `Company` javob/DB maydonlari (hammasi, 6 endpoint bo'yicha bir xil):
  `id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt`.
  **`currency`, `workDayStart`, `workDayEnd` degan maydonlar backendda YO'Q.**
- `POST/PATCH` DTO maydonlari: `name` (majburiy, 1-255), `legalName?`, `phone?` (≤50),
  `email?` (`@IsEmail`), `address?` (≤500), `logoUrl?` (≤500).
- `GET /companies` javobi — paginatsiya: `{ items: Company[], total, page, limit, totalPages }`.
- `DELETE /companies/:id` javobi: `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/company.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/company.ts` — `Company` interfeysida `currency?`,
  `workDayStart?`, `workDayEnd?` maydonlari bor, bular backend javobida
  hech qachon kelmaydi (o'chirilishi kerak, agar boshqa hech qayerda ataylab
  frontend-only maydon sifatida ishlatilmasa — shuni ham tekshiring:
  `company-form.ts`/`company-list.ts`da shu 3 maydon ishlatilayotgan bo'lsa,
  formadagi mos input/logikani ham olib tashlang, chunki backendga hech qachon
  yuborilmaydi/qaytmaydi).
- `src/app/features/company/services/company.ts` — `getAll`/`getById`/`create`/
  `update`/`delete` allaqachon bir nechta javob shaklini (`res.data.items`,
  `res.items`, `res.data`, massiv) himoyalab qayta ishlaydi — bu servis fayli
  o'zi to'g'ri ko'rinadi, faqat `Company` tipi to'g'rilangandan keyin qayta
  tekshiring (TS xatosi chiqmasligi uchun).
- `src/app/features/company/pages/company-form/company-form.ts` va
  `company-list/company-list.ts` — model o'zgarishidan keyin shu fayllardagi
  `.ts` mantiqni (forma maydonlari, jadval ustunlari uchun property access)
  moslang. **HTML/CSS ga tegmang.**

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — `company-form.html/css`, `company-list.html/css`ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/company.ts`
- `test-zdes-front/src/app/features/company/services/company.ts`
- `test-zdes-front/src/app/features/company/pages/company-form/company-form.ts`
- `test-zdes-front/src/app/features/company/pages/company-list/company-list.ts`
- `test-zdes-front/project_docs/api/company.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Company` interfeysi faqat backendda mavjud maydonlarni o'z ichiga oladi (yuqoridagi ro'yxat).
- `currency`/`workDayStart`/`workDayEnd`ga bog'liq forma/jadval kodi olib tashlangan yoki (agar ataylab frontend-only ekanligi aniqlansa) buni response.md da aniq izohlang, o'chirmang.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-COMPANY-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-COMPANY.md` va `B-I-COMPANY-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-BRANCH.md`

## Task ID: B-I-BRANCH
### Sarlavha: Branch modeli — backendda yo'q `phone` maydonini olib tashlash

**Maqsad (Goal):**
`core/models/branch.ts` da backend `Branch` modelida umuman mavjud bo'lmagan
`phone` maydoni bor. (`zdes/review/tasks/step_18.md`da bu `branch-form`
komponentida qisman qo'lda tuzatilgan edi, lekin model va servis darajasida
hali ham mavjud bo'lishi mumkin — shu safar tizimli tekshiring.) Modelni
`backend_crud_review/branch.md`ga aynan moslang.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/branch.md):**
- `Branch` javob/DB maydonlari (barcha 6 endpoint bo'yicha bir xil):
  `id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt`.
  **`phone` degan maydon backendda YO'Q.**
- `POST/PATCH` DTO: `companyId?`, `name` (majburiy, 1-255), `address?` (≤500),
  `latitude?` (`@IsLatitude`), `longitude?` (`@IsLongitude`), `radius?` (int, `@default(100)`).
- `GET /branches` — paginatsiya: `{ items: Branch[], total, page, limit, totalPages }`.
- `DELETE /branches/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/branch.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/branch.ts` — `Branch` interfeysida `phone?: string | null`
  hali ham bor — bu maydonni olib tashlang.
- `src/app/features/branches/services/branch.ts` — CRUD metodlari, `Branch`
  tipiga bog'liq — tip o'zgargandan keyin qayta tekshiring.
- `src/app/features/branches/pages/branch-form/branch-form.ts` — `step_18.md`
  bo'yicha `phone` maydoni allaqachon formadan olib tashlangan bo'lishi mumkin;
  shunga qaramay bu faylni ochib, hali ham `phone`ga bog'liq forma-control/model
  qoldiq bor-yo'qligini tekshiring va bo'lsa tozalang. Shuningdek `companyId`
  (superadmin uchun) va `latitude/longitude/radius` maydonlarining `Branch`
  tipiga mosligini tasdiqlang.
- `src/app/features/branches/pages/branch-list/branch-list.ts` — jadval ustunlari
  `Branch` tipiga mos property'lardan foydalanishini tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — `branch-form.html/css`, `branch-list.html/css`ga
  (shu jumladan Leaflet xarita komponenti UI qismiga) tegmang, faqat `.ts`dagi
  ma'lumot bog'lanishi/tip mantig'ini to'g'rilang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/branch.ts`
- `test-zdes-front/src/app/features/branches/services/branch.ts`
- `test-zdes-front/src/app/features/branches/pages/branch-form/branch-form.ts`
- `test-zdes-front/src/app/features/branches/pages/branch-list/branch-list.ts`
- `test-zdes-front/project_docs/api/branches.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Branch` interfeysida `phone` yo'q, qolgan maydonlar backend bilan mos.
- `branch-form.ts`da `phone`ga bog'liq qoldiq mantiq (agar bor bo'lsa) tozalangan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-BRANCH-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-BRANCH.md` va `B-I-BRANCH-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-SETTING.md`

## Task ID: B-I-SETTING
### Sarlavha: Setting — generic key-value modelga to'liq qayta qurish (hozirgi `CompanySettings` butunlay noto'g'ri)

**Maqsad (Goal):**
`features/settings/services/setting.ts` backendni **butunlay boshqacha**
narsa deb taxmin qilib yozilgan: frontend `GET /settings`ni bitta flat
`CompanySettings` obyekti (`companyName, currency, workDayStart, workDayEnd`)
qaytaradi deb kutadi. Aslida backend `Setting` — **generic key-value store**
(`{ id, companyId, key, value: Json, createdAt, updatedAt }`) va `GET /settings`
**paginatsiyali ro'yxat** (`{ items: Setting[], total, page, limit, totalPages }`)
qaytaradi. Bu ehtimol renderdagi asosiy sabablardan biri — servis butunlay
noto'g'ri shaklga tayanadi. Model/servisni to'liq qayta qurish kerak.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan). Bu ayniqsa `B-I-SETTING`
uchun muhim, chunki hozirgi `setting.ts` servisi butunlay noto'g'ri model
bilan yozilgan va `.data` unwrap qilishni umuman hisobga olmagan.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/setting.md):**
- `Setting` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), key (string, ≤255), value (Record<string,
  unknown> | null, Json ustun), createdAt, updatedAt`.
  **`companyName`, `currency`, `workDayStart`, `workDayEnd` degan alohida
  maydonlar YO'Q** — bular, agar kerak bo'lsa, `key: "company_settings"` (yoki
  shunga o'xshash) nomli bitta `Setting` yozuvining `value` JSON obyekti
  ichida saqlanishi mumkin, lekin bu **taxmin** — haqiqiy `key` qiymati (masalan
  `attendance_kpi_template` misolda ko'rsatilgan) hujjatda tasdiqlangan emas.
  Qaysi `key`(lar) frontendda kerakligini komponentlardan (`settings-page.ts`)
  aniqlab, javob faylida aniq yozing.
- `POST/PATCH` DTO: `companyId?`, `key` (majburiy, ≤255), `value?` (`Record<string, unknown>`).
- `GET /settings/:id`, `PATCH /settings/:id`, `DELETE /settings/:id` — bitta
  `Setting` yozuvi bo'yicha ishlaydi.
- Har bir `(companyId, key)` juftligi **unique** — bir xil kalit bilan ikkita
  yozuv bo'lishi mumkin emas.
- To'liq tafsilot: `../backend_crud_review/setting.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati, o'zingiz o'qib solishtiring):**
- `src/app/features/settings/services/setting.ts` — hozirgi holat (butunlay
  noto'g'ri model bilan, yuqorida ko'rsatilgan):
  ```ts
  export interface CompanySettings {
    companyName: string;
    currency: string;
    workDayStart: string;
    workDayEnd: string;
  }
  export class Setting {
    get(): Observable<CompanySettings> { return this.http.get<CompanySettings>('/settings'); }
    update(settings: ..., id?: string): Observable<CompanySettings> { ... }
  }
  ```
- `src/app/features/settings/pages/settings-page/settings-page.ts` — ushbu
  faylni o'qib, aynan qaysi "sozlama" qiymatlari (masalan valyuta, ish
  vaqti va h.k.) UI orqali ko'rsatilayotganini/tahrirlanayotganini aniqlang.
  Shu asosda: (a) yangi `Setting` interfeysini (`id, companyId, key, value, createdAt, updatedAt`)
  yozing, (b) `SettingService`ni haqiqiy backend shakliga mos servis metodlariga
  (`getAll` — paginatsiyali ro'yxat, `getByKey`/`getOne`, `create`, `update`, `delete`)
  qayta quring, (c) `settings-page.ts`dagi `.ts` mantiqni shu yangi servis bilan
  ishlaydigan qilib moslang (masalan bitta `key` bo'yicha `value` obyektidan
  kerakli maydonlarni o'qish/yozish).
- Bu modul boshqalardan farqli — o'zingiz komponentni o'qib qanday ishlatilishini
  aniqlang, keyin mos servis/komponent mantig'ini yozing.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar UI qaysi `key`/`value` shaklini kutishi noaniq bo'lib qolsa (masalan
  bir nechta turli sozlama ekrani bir xil `key`ga tayanadimi), **taxmin qilib
  yangi backend `key` semantikasi o'ylab topmang** — javob faylida aniq
  noaniqlikni yozib, eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/features/settings/services/setting.ts`
- `test-zdes-front/src/app/features/settings/pages/settings-page/settings-page.ts`
- `test-zdes-front/project_docs/api/settings.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Setting`/servis to'liq backend generic key-value shakliga mos (`id, companyId, key, value, createdAt, updatedAt`, paginatsiyali `getAll`).
- `settings-page.ts` yangi servis bilan TS xatosiz ishlaydi.
- Noaniq `key` semantikasi (agar bo'lsa) javob faylida aniq hujjatlashtirilgan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-SETTING-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-SETTING.md` va `B-I-SETTING-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-EMPLOYEE-LEAVE.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-EMPLOYEE-LEAVE
### Sarlavha: EmployeeLeave modeli — maydon nomlarini va yo'q "approval status" mantig'ini to'g'irlash

**Maqsad (Goal):**
`core/models/employee-leave.ts` backendda **umuman mavjud bo'lmagan**
tasdiqlash oqimini (`status: 'pending'|'approved'|'rejected'`) taxmin qilib
yozilgan, va maydon nomlari ham mos emas (`startDate/endDate` o'rniga backendda
`fromDate/toDate`). Buni tuzatish — ayniqsa `status` maydoni: agar
`leave-list.ts`/`leave-form.ts`da tasdiqlash UI logikasi shunga tayansa, bu
render/funksionallik xatosi keltirib chiqaradi (backend hech qachon bunday
maydon qaytarmaydi).

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/employee-leave.md):**
- `EmployeeLeave` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string), companyId (string), branchId (string | null), employeeId (string),
  type (LeaveType, default vacation), fromDate (string/DateTime), toDate (string/DateTime),
  days (number), affectsSalary (boolean, default false), reason (string | null),
  createdById (string | null), updatedById (string | null), createdAt, updatedAt`.
  **`status` (pending/approved/rejected) degan maydon backendda YO'Q — tasdiqlash
  workflow'i bu modulda mavjud emas.**
- `LeaveType` enum qiymatlari tahlil hujjatida to'liq sanalmagan (faqat
  default `vacation` va misolda `vacation` ko'rsatilgan) — qat'iy union
  yozmang, `string` sifatida qoldiring va javob faylida shuni eslating.
- `POST/PATCH` DTO: `employeeId` (majburiy), `companyId?`, `branchId?`,
  `type`, `fromDate`, `toDate`, `days?` (berilmasa backend hisoblaydi),
  `affectsSalary?`, `reason?`.
- `GET /employee-leaves` — paginatsiya: `{ items: EmployeeLeave[], total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/employee-leave.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/employee-leave.ts` — hozirgi holat:
  ```ts
  export interface EmployeeLeave {
    id: number;
    employeeId: number;
    startDate: string;
    endDate: string;
    type: 'vacation' | 'sick' | 'unpaid';
    status: 'pending' | 'approved' | 'rejected';
  }
  ```
  `id`/`employeeId` **`number` emas, `string` (UUID)**. `startDate`/`endDate`
  → `fromDate`/`toDate`ga o'zgartirilishi kerak. **`status` maydoni butunlay
  olib tashlanishi kerak** (yoki komponentlarda ishlatilayotgan bo'lsa, bu
  aniq "backend workflow yo'q" degan topilma sifatida javob faylida
  hujjatlashtirilib, komponent mantig'i shunga qarab moslashtirilishi kerak —
  masalan approve/reject tugmalari bo'lsa, ular hozircha hech qanday real
  endpointga ulanmagani aniq bo'ladi). Yetishmayotgan: `companyId`, `branchId`,
  `days`, `affectsSalary`, `reason`, `createdAt`, `updatedAt`.
- `src/app/features/leaves/services/leave.ts` — CRUD metodlari, maydon nomi
  o'zgarishidan (`fromDate`/`toDate`) keyin qayta tekshiring.
- `src/app/features/leaves/pages/leave-form/leave-form.ts`,
  `leave-list/leave-list.ts` — **agar bu fayllarda `status`ga bog'liq
  tasdiqlash/rad etish tugmalari yoki filtri bo'lsa, buni javob faylida
  aniq ta'kidlang** — bu HTML/CSS o'zgarishi talab qiladigan chegaraviy holat
  bo'lishi mumkin (`requirements.MD` 0-bo'lim), shu holatda kodni o'zgartirmasdan
  faqat aniqlang va eskalatsiya qiling (task scope'ini kengaytirmang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar `status` maydonini olib tashlash HTML shablonini ham o'zgartirishga
  majbur qilsa (masalan `*ngIf="leave.status === 'pending'"`), **bunday
  holatni avtomatik hal qilmang** — javob faylida aniq tavsiflab, Claude Code
  (orchestrator) ko'rib chiqishini so'rang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/employee-leave.ts`
- `test-zdes-front/src/app/features/leaves/services/leave.ts`
- `test-zdes-front/src/app/features/leaves/pages/leave-form/leave-form.ts`
- `test-zdes-front/src/app/features/leaves/pages/leave-list/leave-list.ts`
- `test-zdes-front/project_docs/api/leaves.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `EmployeeLeave` interfeysi backendga mos (`fromDate`/`toDate`, `status` yo'q, `id`/`employeeId` `string`).
- `status`ga bog'liq HTML mantiq topilgan bo'lsa, javob faylida aniq eskalatsiya qilingan (kod o'zgartirilmagan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-EMPLOYEE-LEAVE-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-EMPLOYEE-LEAVE.md` va `B-I-EMPLOYEE-LEAVE-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-BRANCH.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-BRANCH
### Sarlavha: Branch modeli — backendda yo'q `phone` maydonini olib tashlash

**Maqsad (Goal):**
`core/models/branch.ts` da backend `Branch` modelida umuman mavjud bo'lmagan
`phone` maydoni bor. (`zdes/review/tasks/step_18.md`da bu `branch-form`
komponentida qisman qo'lda tuzatilgan edi, lekin model va servis darajasida
hali ham mavjud bo'lishi mumkin — shu safar tizimli tekshiring.) Modelni
`backend_crud_review/branch.md`ga aynan moslang.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/branch.md):**
- `Branch` javob/DB maydonlari (barcha 6 endpoint bo'yicha bir xil):
  `id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt`.
  **`phone` degan maydon backendda YO'Q.**
- `POST/PATCH` DTO: `companyId?`, `name` (majburiy, 1-255), `address?` (≤500),
  `latitude?` (`@IsLatitude`), `longitude?` (`@IsLongitude`), `radius?` (int, `@default(100)`).
- `GET /branches` — paginatsiya: `{ items: Branch[], total, page, limit, totalPages }`.
- `DELETE /branches/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/branch.md` (6 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/branch.ts` — `Branch` interfeysida `phone?: string | null`
  hali ham bor — bu maydonni olib tashlang.
- `src/app/features/branches/services/branch.ts` — CRUD metodlari, `Branch`
  tipiga bog'liq — tip o'zgargandan keyin qayta tekshiring.
- `src/app/features/branches/pages/branch-form/branch-form.ts` — `step_18.md`
  bo'yicha `phone` maydoni allaqachon formadan olib tashlangan bo'lishi mumkin;
  shunga qaramay bu faylni ochib, hali ham `phone`ga bog'liq forma-control/model
  qoldiq bor-yo'qligini tekshiring va bo'lsa tozalang. Shuningdek `companyId`
  (superadmin uchun) va `latitude/longitude/radius` maydonlarining `Branch`
  tipiga mosligini tasdiqlang.
- `src/app/features/branches/pages/branch-list/branch-list.ts` — jadval ustunlari
  `Branch` tipiga mos property'lardan foydalanishini tekshiring.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — `branch-form.html/css`, `branch-list.html/css`ga
  (shu jumladan Leaflet xarita komponenti UI qismiga) tegmang, faqat `.ts`dagi
  ma'lumot bog'lanishi/tip mantig'ini to'g'rilang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/branch.ts`
- `test-zdes-front/src/app/features/branches/services/branch.ts`
- `test-zdes-front/src/app/features/branches/pages/branch-form/branch-form.ts`
- `test-zdes-front/src/app/features/branches/pages/branch-list/branch-list.ts`
- `test-zdes-front/project_docs/api/branches.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Branch` interfeysida `phone` yo'q, qolgan maydonlar backend bilan mos.
- `branch-form.ts`da `phone`ga bog'liq qoldiq mantiq (agar bor bo'lsa) tozalangan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-BRANCH-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-BRANCH.md` va `B-I-BRANCH-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-PAYROLL.md`

## Task ID: B-I-PAYROLL
### Sarlavha: Payroll modeli — `period`/`deductions`/`totalAmount` maydonlarini backendga moslash

**Maqsad (Goal):**
`core/models/payroll.ts` backend bilan maydon nomlari darajasida mos emas:
`period` (backendda `month`), `deductions`/`totalAmount` (backendda bunday
yagona maydonlar yo'q — `totalBonus`, `totalPenalty`, `totalAdvance`,
`netSalary` alohida-alohida saqlanadi), va `status`/`paidAt`/`paidById`
butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/payroll.md):**
- `Payroll` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), month (string,
  "YYYY-MM"), baseSalary (number, default 0), totalBonus (number, default 0),
  totalPenalty (number, default 0), totalAdvance (number, default 0),
  netSalary (number, default 0), status (PayrollStatus, default draft),
  paidAt (string | null), paidById (string | null), createdById (string | null),
  updatedById (string | null), createdAt, updatedAt`.
  **`period`, `deductions`, `totalAmount` degan maydonlar backendda YO'Q.**
- `PayrollStatus` enum qiymatlari to'liq sanalmagan (faqat default `draft`
  ma'lum) — qat'iy union yozmang, `string` sifatida qoldiring.
- `GET /payrolls` — paginatsiya: `{ items: Payroll[], total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/payroll.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/payroll.ts` — hozirgi holat:
  ```ts
  export interface Payroll {
    id: string | number;
    employeeId: string | number;
    period: string;
    baseSalary: number;
    deductions: number;
    totalAmount: number;
  }
  ```
  `id`/`employeeId` — faqat `string`. `period` → `month`. `deductions`/`totalAmount`
  → `totalBonus`, `totalPenalty`, `totalAdvance`, `netSalary`ga almashtiring
  (bittalab maydon sifatida, yig'indi emas). Yetishmayotgan: `companyId`,
  `status`, `paidAt`, `paidById`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/payroll/services/payroll.ts` — CRUD/paginatsiya metodlari,
  maydon nomlari o'zgarishidan keyin qayta tekshiring.
- `src/app/features/payroll/pages/payroll-list/payroll-list.ts`,
  `payroll-detail/payroll-detail.ts` — `period`/`deductions`/`totalAmount`
  ishlatilgan barcha `.ts` joylarni yangi maydon nomlariga moslang. Agar
  jadval/detail HTML shablonida shu eski nomlar interpolatsiya qilinsa, buni
  javob faylida aniq eskalatsiya qiling (HTML o'zgartirmang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Maydon nomi o'zgarishi HTML shablonini ham o'zgartirishga majbur qilsa, kod yozmang — eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/payroll.ts`
- `test-zdes-front/src/app/features/payroll/services/payroll.ts`
- `test-zdes-front/src/app/features/payroll/pages/payroll-list/payroll-list.ts`
- `test-zdes-front/src/app/features/payroll/pages/payroll-detail/payroll-detail.ts`
- `test-zdes-front/project_docs/api/payroll.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Payroll` interfeysi to'liq backend bilan mos (yuqoridagi to'liq ro'yxat).
- `.ts` fayllarda eski nomlarga (`period`/`deductions`/`totalAmount`) qoldiq bog'liqlik yo'q (yoki aniq eskalatsiya qilingan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-PAYROLL-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-PAYROLL.md` va `B-I-PAYROLL-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-COMPANY-response.md`

# B-I-COMPANY Response

## Qadamlar (Steps)
1. `core/models/company.ts` faylidagi backendda yo'q `currency`, `workDayStart`, `workDayEnd` maydonlari olib tashlandi.
2. `features/company/pages/company-form/company-form.ts` va `features/company/pages/company-list/company-list.ts` fayllari tekshirildi; bu maydonlar umuman ishlatilmagan ekan, kodni buzmaydi.
3. `features/company/services/company.ts` tekshirildi, mavjud `res.data` yoki `res.data.items` unwrap qilish logikasi xavfsiz holatda qoldirildi (chunki backend dagi `ResponseInterceptor` ga to'g'ri moslashgan).
4. `npm run build` orqali xatoliklar yo'qligi tekshirildi.

## O'zgargan fayllar (Changed Files)

| Fayl | Turi | Qisqa sabab |
|------|------|-------------|
| `src/app/core/models/company.ts` | .ts | Backendda yo'q maydonlarni (currency, workDayStart, workDayEnd) olib tashlash. |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-NOTIFICATION.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-NOTIFICATION
### Sarlavha: Notification modeli — `read` → `isRead`, yo'q maydonlarni qo'shish

**Maqsad (Goal):**
`core/models/notification.ts` da maydon nomi backend bilan mos emas:
frontend `read: boolean`, backend `isRead: boolean`. Bu — filter/belgilash
mantig'ining jimgina ishlamay qolishiga sabab bo'ladigan tipik nomlanish
xatosi. Shuningdek `userId` va `icon` maydonlari butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/notification.md):**
- `Notification` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), userId (string | null), title (string), message (string),
  icon (NotificationIcon | null), isRead (boolean, default false), createdAt, updatedAt`.
  **`read` degan maydon YO'Q — nomi `isRead`.**
- `NotificationIcon` enum qiymatlari tahlil hujjatida to'liq sanalmagan (misolda
  `NotificationIcon.money` ko'rsatilgan) — qat'iy union yozmang, `string`
  sifatida qoldiring.
- `GET /notifications` — paginatsiya: `{ items: Notification[], total, page, limit, totalPages }`.
- `PATCH /notifications/:id` — odatda `isRead`ni belgilash uchun ishlatiladi.
- To'liq tafsilot: `../backend_crud_review/notification.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/notification.ts` — hozirgi holat:
  ```ts
  export interface Notification {
    id: string | number;
    title: string;
    message: string;
    read: boolean;
    createdAt: string;
  }
  ```
  `id` — faqat `string`. `read` → `isRead`ga o'zgartiring. Yetishmayotgan:
  `userId`, `icon`, `updatedAt`.
- `src/app/features/notifications/services/notification.ts` — CRUD/mark-as-read
  metodlari `read` propertysiga tayanadigan bo'lsa, `isRead`ga moslang.
- `src/app/features/notifications/pages/notification-list/notification-list.ts` —
  `notification.read` ishlatilgan barcha joylarni `notification.isRead`ga
  o'tkazing (bu `.ts` ichidagi property access, HTML/CSS ga tegilmaydi —
  agar HTML shablonida `notification.read` interpolatsiyasi bo'lsa, bu holatni
  javob faylida aniq eslating, chegaraviy holat sifatida).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar `read`→`isRead` almashtirish HTML shablonini ham o'zgartirishga majbur
  qilsa, kodni o'zgartirmang — javob faylida aniq eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/notification.ts`
- `test-zdes-front/src/app/features/notifications/services/notification.ts`
- `test-zdes-front/src/app/features/notifications/pages/notification-list/notification-list.ts`
- `test-zdes-front/project_docs/api/notifications.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Notification` interfeysi to'liq backend bilan mos (`isRead`, `id: string`, `userId`, `icon`).
- `.ts` fayllardagi barcha `read` foydalanishi `isRead`ga moslangan (yoki HTML bog'liqligi aniq eskalatsiya qilingan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-NOTIFICATION-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-NOTIFICATION.md` va `B-I-NOTIFICATION-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-PAYROLL.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-PAYROLL
### Sarlavha: Payroll modeli — `period`/`deductions`/`totalAmount` maydonlarini backendga moslash

**Maqsad (Goal):**
`core/models/payroll.ts` backend bilan maydon nomlari darajasida mos emas:
`period` (backendda `month`), `deductions`/`totalAmount` (backendda bunday
yagona maydonlar yo'q — `totalBonus`, `totalPenalty`, `totalAdvance`,
`netSalary` alohida-alohida saqlanadi), va `status`/`paidAt`/`paidById`
butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/payroll.md):**
- `Payroll` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), month (string,
  "YYYY-MM"), baseSalary (number, default 0), totalBonus (number, default 0),
  totalPenalty (number, default 0), totalAdvance (number, default 0),
  netSalary (number, default 0), status (PayrollStatus, default draft),
  paidAt (string | null), paidById (string | null), createdById (string | null),
  updatedById (string | null), createdAt, updatedAt`.
  **`period`, `deductions`, `totalAmount` degan maydonlar backendda YO'Q.**
- `PayrollStatus` enum qiymatlari to'liq sanalmagan (faqat default `draft`
  ma'lum) — qat'iy union yozmang, `string` sifatida qoldiring.
- `GET /payrolls` — paginatsiya: `{ items: Payroll[], total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/payroll.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/payroll.ts` — hozirgi holat:
  ```ts
  export interface Payroll {
    id: string | number;
    employeeId: string | number;
    period: string;
    baseSalary: number;
    deductions: number;
    totalAmount: number;
  }
  ```
  `id`/`employeeId` — faqat `string`. `period` → `month`. `deductions`/`totalAmount`
  → `totalBonus`, `totalPenalty`, `totalAdvance`, `netSalary`ga almashtiring
  (bittalab maydon sifatida, yig'indi emas). Yetishmayotgan: `companyId`,
  `status`, `paidAt`, `paidById`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/payroll/services/payroll.ts` — CRUD/paginatsiya metodlari,
  maydon nomlari o'zgarishidan keyin qayta tekshiring.
- `src/app/features/payroll/pages/payroll-list/payroll-list.ts`,
  `payroll-detail/payroll-detail.ts` — `period`/`deductions`/`totalAmount`
  ishlatilgan barcha `.ts` joylarni yangi maydon nomlariga moslang. Agar
  jadval/detail HTML shablonida shu eski nomlar interpolatsiya qilinsa, buni
  javob faylida aniq eskalatsiya qiling (HTML o'zgartirmang).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Maydon nomi o'zgarishi HTML shablonini ham o'zgartirishga majbur qilsa, kod yozmang — eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/payroll.ts`
- `test-zdes-front/src/app/features/payroll/services/payroll.ts`
- `test-zdes-front/src/app/features/payroll/pages/payroll-list/payroll-list.ts`
- `test-zdes-front/src/app/features/payroll/pages/payroll-detail/payroll-detail.ts`
- `test-zdes-front/project_docs/api/payroll.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Payroll` interfeysi to'liq backend bilan mos (yuqoridagi to'liq ro'yxat).
- `.ts` fayllarda eski nomlarga (`period`/`deductions`/`totalAmount`) qoldiq bog'liqlik yo'q (yoki aniq eskalatsiya qilingan).
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-PAYROLL-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-PAYROLL.md` va `B-I-PAYROLL-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-POSITION-response.md`

# B-I-POSITION Task Response

## Bajarilgan Ishlar (Completed Steps)
1. **Model Yangilanishi (`core/models/position.ts`)**: 
   - `Position` interfeysiga yetishmayotgan maydonlar: `companyId?: string`, `isActive?: boolean`, `createdAt?: string`, `updatedAt?: string` qo'shildi.

2. **Forma O'zgarishlari (`features/positions/pages/position-form/position-form.ts`)**:
   - `PositionForm`dagi reaktiv formada `companyId` va `isActive` maydonlari hisobga olinib, forma guruhiga mos qiymatlar (`companyId: ['']`, `isActive: [true]`) bilan biriktirildi. Shunday qilib, agar backend formadagi bu maydonlarni kutyotgan bo'lsa, to'g'ri yuboriladi.

3. **Backend Javoblari O'ramini Tekshirish**:
   - `services/position.ts` tekshirildi. U yerda javob o'ramini ochish (unwrap qilish) amali (`res?.data?.items` va hokazo) allaqachon bajarilganligi aniqlandi. Backend global `ResponseInterceptor` talabiga mosligi isbotlandi, qo'shimcha o'zgartirish shart qilinmadi.
   
4. **Tekshirish va Kompilyatsiya**:
   - TypeScript modellari muvaffaqiyatli ulanganligi tekshirildi va `npm run build` amali xatosiz o'tdi.

## O'zgargan fayllar (Changed Files)

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `src/app/core/models/position.ts` | Model | Backend `Position` javobidagi maydonlarni (`companyId, isActive, createdAt, updatedAt`) qo'shish uchun. |
| `src/app/features/positions/pages/position-form/position-form.ts` | Komponent TS | `companyId` va `isActive`ni `FormGroup` tarkibiga qo'shish uchun. |


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-A-SALARY-ADJUSTMENT-response.md`

# Task B-A-SALARY-ADJUSTMENT Response

## Jarayon:
1. `zdes_backend/src/modules/salary-adjustment` papkasi o'qildi. Uning ichidagi controller, service, va DTO fayllar ko'rib chiqildi:
   - `salary-adjustment.controller.ts`
   - `salary-adjustment.service.ts`
   - `dto/create-salary-adjustment.dto.ts`
   - `dto/salary-adjustment-query.dto.ts`
   - `dto/update-salary-adjustment.dto.ts`
2. Endpointlarni va Swagger DTO dagi namunalarni (example) to'liq oldik, xatolar (exceptions) va service funksiyalari o'qildi.
3. Ma'lumotlar bazasi tuzilishini tahlil qilish uchun `zdes_backend/prisma/schema.prisma` fayli o'qildi. Undan `SalaryAdjustment` modelining ta'rifi (ustunlar majburiyligi, ularning tiplari va default qiymatlari) va uning boshqa jadvallar bilan (User va Company modellari bilan) bo'lgan aloqalari o'rganildi.
4. Tahlil natijalari to'liq strukturada `backend_crud_review/salary-adjustment.md` fayliga yozildi.
5. Zdes_backend'dagi hech qanday fayl tahrirlanmadi yoki buzilmadi. Loyiha faqat o'qish (read-only) rejimida ko'rildi.

## Yakuniy Xulosa
SalaryAdjustment modulining 5 ta asosiy endpointlari to'liq qamrab olindi va ma'lumotlar bazasi strukturalari bilan birga review fayliga joylashtirildi. 

### Tahlil qilingan endpointlar ro'yxati (jami 5 ta):
1. `POST /api/v1/salary-adjustments` (Oylik tuzatishni yaratish)
2. `GET /api/v1/salary-adjustments` (Barcha oylik tuzatishlarni ko'rish)
3. `GET /api/v1/salary-adjustments/:id` (Bitta oylik tuzatishni olish)
4. `PATCH /api/v1/salary-adjustments/:id` (Oylik tuzatishni tahrirlash)
5. `DELETE /api/v1/salary-adjustments/:id` (Oylik tuzatishni o'chirish)


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-SETTING.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-SETTING
### Sarlavha: Setting — generic key-value modelga to'liq qayta qurish (hozirgi `CompanySettings` butunlay noto'g'ri)

**Maqsad (Goal):**
`features/settings/services/setting.ts` backendni **butunlay boshqacha**
narsa deb taxmin qilib yozilgan: frontend `GET /settings`ni bitta flat
`CompanySettings` obyekti (`companyName, currency, workDayStart, workDayEnd`)
qaytaradi deb kutadi. Aslida backend `Setting` — **generic key-value store**
(`{ id, companyId, key, value: Json, createdAt, updatedAt }`) va `GET /settings`
**paginatsiyali ro'yxat** (`{ items: Setting[], total, page, limit, totalPages }`)
qaytaradi. Bu ehtimol renderdagi asosiy sabablardan biri — servis butunlay
noto'g'ri shaklga tayanadi. Model/servisni to'liq qayta qurish kerak.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan). Bu ayniqsa `B-I-SETTING`
uchun muhim, chunki hozirgi `setting.ts` servisi butunlay noto'g'ri model
bilan yozilgan va `.data` unwrap qilishni umuman hisobga olmagan.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/setting.md):**
- `Setting` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), key (string, ≤255), value (Record<string,
  unknown> | null, Json ustun), createdAt, updatedAt`.
  **`companyName`, `currency`, `workDayStart`, `workDayEnd` degan alohida
  maydonlar YO'Q** — bular, agar kerak bo'lsa, `key: "company_settings"` (yoki
  shunga o'xshash) nomli bitta `Setting` yozuvining `value` JSON obyekti
  ichida saqlanishi mumkin, lekin bu **taxmin** — haqiqiy `key` qiymati (masalan
  `attendance_kpi_template` misolda ko'rsatilgan) hujjatda tasdiqlangan emas.
  Qaysi `key`(lar) frontendda kerakligini komponentlardan (`settings-page.ts`)
  aniqlab, javob faylida aniq yozing.
- `POST/PATCH` DTO: `companyId?`, `key` (majburiy, ≤255), `value?` (`Record<string, unknown>`).
- `GET /settings/:id`, `PATCH /settings/:id`, `DELETE /settings/:id` — bitta
  `Setting` yozuvi bo'yicha ishlaydi.
- Har bir `(companyId, key)` juftligi **unique** — bir xil kalit bilan ikkita
  yozuv bo'lishi mumkin emas.
- To'liq tafsilot: `../backend_crud_review/setting.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati, o'zingiz o'qib solishtiring):**
- `src/app/features/settings/services/setting.ts` — hozirgi holat (butunlay
  noto'g'ri model bilan, yuqorida ko'rsatilgan):
  ```ts
  export interface CompanySettings {
    companyName: string;
    currency: string;
    workDayStart: string;
    workDayEnd: string;
  }
  export class Setting {
    get(): Observable<CompanySettings> { return this.http.get<CompanySettings>('/settings'); }
    update(settings: ..., id?: string): Observable<CompanySettings> { ... }
  }
  ```
- `src/app/features/settings/pages/settings-page/settings-page.ts` — ushbu
  faylni o'qib, aynan qaysi "sozlama" qiymatlari (masalan valyuta, ish
  vaqti va h.k.) UI orqali ko'rsatilayotganini/tahrirlanayotganini aniqlang.
  Shu asosda: (a) yangi `Setting` interfeysini (`id, companyId, key, value, createdAt, updatedAt`)
  yozing, (b) `SettingService`ni haqiqiy backend shakliga mos servis metodlariga
  (`getAll` — paginatsiyali ro'yxat, `getByKey`/`getOne`, `create`, `update`, `delete`)
  qayta quring, (c) `settings-page.ts`dagi `.ts` mantiqni shu yangi servis bilan
  ishlaydigan qilib moslang (masalan bitta `key` bo'yicha `value` obyektidan
  kerakli maydonlarni o'qish/yozish).
- Bu modul boshqalardan farqli — o'zingiz komponentni o'qib qanday ishlatilishini
  aniqlang, keyin mos servis/komponent mantig'ini yozing.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.
- Agar UI qaysi `key`/`value` shaklini kutishi noaniq bo'lib qolsa (masalan
  bir nechta turli sozlama ekrani bir xil `key`ga tayanadimi), **taxmin qilib
  yangi backend `key` semantikasi o'ylab topmang** — javob faylida aniq
  noaniqlikni yozib, eskalatsiya qiling.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/features/settings/services/setting.ts`
- `test-zdes-front/src/app/features/settings/pages/settings-page/settings-page.ts`
- `test-zdes-front/project_docs/api/settings.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Setting`/servis to'liq backend generic key-value shakliga mos (`id, companyId, key, value, createdAt, updatedAt`, paginatsiyali `getAll`).
- `settings-page.ts` yangi servis bilan TS xatosiz ishlaydi.
- Noaniq `key` semantikasi (agar bo'lsa) javob faylida aniq hujjatlashtirilgan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-SETTING-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-SETTING.md` va `B-I-SETTING-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-A-WORK-SCHEDULE-response.md`

# Task B-A-WORK-SCHEDULE (Analysis — Faza 1) - Response

## Jarayon:
1. `zdes_backend/src/modules/work-schedule` va boshqa kerakli jildlardagi fayllarni (`work-schedule.controller.ts`, `work-schedule.service.ts`, `dto` fayllari va `schema.prisma`) o'qib chiqdim.
2. 9 ta kerakli endpointlarni ajratib, har birining vazifasi, DTO'lari, Controller'i va Service logikasini o'rgandim.
3. `schema.prisma` orqali `WorkSchedule` modelining ustunlari turlarini, hamda u qaysi modellar bilan bog'langanligini (chiquvchi va kiruvchi relatsiyalari bilan, masalan, `User.workScheduleId -> WorkSchedule.id`) tekshirdim.
4. Olingan barcha ma'lumotlarni ko'rsatilgan 8 bo'limli strukturaga moslab, `backend_crud_review/work-schedule.md` fayliga to'liq ko'chirib yozdim. 

## Tahlil qilingan endpointlar (jami 9 ta):
1. `GET /api/v1/work-schedules`
2. `GET /api/v1/work-schedules/:id`
3. `POST /api/v1/work-schedules`
4. `PATCH /api/v1/work-schedules/:id`
5. `PATCH /api/v1/work-schedules/:id/toggle-status`
6. `PATCH /api/v1/work-schedules/:id/set-default`
7. `PATCH /api/v1/work-schedules/:id/assign-user`
8. `PATCH /api/v1/work-schedules/:id/unassign-user`
9. `DELETE /api/v1/work-schedules/:id`

## Yakuniy xulosa:
`backend_crud_review/work-schedule.md` fayli muvaffaqiyatli yaratildi va 9 ta endpoint tahlili barcha cheklovlarga rioya qilingan holda bajarildi. DTO validation detallari, guard ma'lumotlari, Swagger misollari, va barcha kiruvchi-chiquvchi database relation'lari yozildi.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-DASHBOARD.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-DASHBOARD
### Sarlavha: Dashboard — statik mock stat-cardlarni real servis chaqiruvlariga ulash

**Maqsad (Goal):**
`dashboard.ts` hozir **100% statik** — hech qanday servis chaqiruvi yo'q,
barcha qiymatlar qattiq yozilgan (`'0'`, `'0%'`). Backendda alohida
`dashboard` moduli/endpoint **yo'q** (`../backend_crud_review/dashboard.md`da
tasdiqlangan) — shuning uchun bu task boshqa modullarning allaqachon mavjud
`GET` endpointlariga tayanadi.

**MUHIM — BOG'LIQLIK:** Bu task quyidagi servislar to'g'ri tipda ishlashiga
tayanadi: `EmployeeService` (`B-I-USER`), `AttendanceService` (`B-I-ATTENDANCE`),
`LeaveService` (`B-I-EMPLOYEE-LEAVE`), `NotificationService` (`B-I-NOTIFICATION`).
**Agar shu tasklar hali bajarilmagan bo'lsa, avval ularni bajaring — aks holda
bu yerda noto'g'ri/eskirgan tipga tayanib yana bir marta noto'g'ri kod
yozilishi mumkin.** `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`da shu tasklarning
`B-I-*-response.md` fayllari bor-yo'qligini tekshirib boshlang.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Chaqirilayotgan servislar (`EmployeeService` va h.k.) buni
allaqachon to'g'ri unwrap qilgan bo'lishi kerak — shunchaki ularning
qaytargan `Observable<T[]>`/`Observable<PaginatedResult<T>>` natijasidan
foydalaning, o'zingiz yana bir marta `.data` deb ochishga urinmang.

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/dashboard.md):**
- Alohida `/api/v1/dashboard` endpoint yo'q. Statistikalar mavjud modul
  endpointlaridan olinadi:
  - `GET /api/v1/users` — jami xodimlar (`total` paginatsiya maydonida).
  - `GET /api/v1/attendance?dateFrom=...&dateTo=...` — bugungi davomat (`total`,
    yoki `items` ichidan `status` bo'yicha hisoblash — `backend_crud_review/attendance.md`ga qarang).
  - `GET /api/v1/employee-leaves?...` — ochiq ta'til so'rovlari (eslatma:
    `B-I-EMPLOYEE-LEAVE`da topilganidek, backendda tasdiqlash `status`
    maydoni YO'Q — "ochiq so'rov" tushunchasi backendda mos kelmasligi
    mumkin, buni javob faylida aniq eslating).
  - `GET /api/v1/notifications?isRead=false` — o'qilmagan bildirishnomalar soni (`total`).
  - To'liq ro'yxat: `../backend_crud_review/dashboard.md`.

**Kontekst (Context — test-zdes-front hozirgi holati, o'zingiz o'qib solishtiring):**
- `src/app/features/dashboard/pages/dashboard/dashboard.ts` — hozirgi holat
  butunlay statik (`stats: DashboardStat[]` qattiq yozilgan qiymatlar bilan).
  Buni to'g'ridan-to'g'ri tuzatilgan servislarni (`EmployeeService`,
  `AttendanceService`, `LeaveService`, `NotificationService`) inject qilib,
  4 ta stat-cardni real `total`/hisoblangan qiymat bilan to'ldiradigan qilib
  yozing (Angular Signal yoki oddiy `async`/`Observable` bog'lash — `.ts`
  ichida, mavjud komponent strukturasini saqlagan holda).
- `dashboard.html`/`dashboard.css`ga tegmang — faqat `.ts` ichida signal/state
  bog'lashni yozing, hozirgi 4 ta stat-card strukturasi (`label`/`value`) saqlansin.
- Har bir servisning aniq qaysi metodini (`getAll`, paginatsiya parametri
  bilan) chaqirish kerakligini o'sha servis faylini o'qib aniqlang.

**Cheklovlar (Constraints):**
- Faqat `.ts` — HTML/CSS ga tegmang, yangi stat-card qo'shmang, mavjud 4
  tasini to'ldiring.
- `zdes_backend`ga yozmang.
- Boshqa modul fayllariga tegmang (faqat mavjud servislarni **chaqiring**,
  ularning ichiga o'zgartirish kiritmang).
- Agar biror stat uchun backendda mos endpoint/aniq mantiq topilmasa (masalan
  "ochiq ta'til so'rovi" tushunchasi), taxmin qilib yangi backend semantikasi
  o'ylab topmang — javob faylida aniq yozing va shu stat-cardni statik
  qoldiring (qolganlarini ulang).

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/features/dashboard/pages/dashboard/dashboard.ts`
- `test-zdes-front/project_docs/api/dashboard.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- Kamida "Jami xodimlar" va "O'qilmagan bildirishnomalar" real servis chaqiruvi bilan ishlaydi (bular eng aniq/oson bog'lanadigan statlar).
- Boshqa 2 ta stat uchun yoki real ulash, yoki aniq eskalatsiya (javob faylida) qilingan.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-DASHBOARD-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-DASHBOARD.md` va `B-I-DASHBOARD-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-I-USER-response.md`

# Employee (backend `user` moduli) — Model maydonlarini backendga to'liq moslashish xulosasi

## Bajarilgan ishlar:
1. `src/app/core/models/employee.ts` faylida `Employee` interfeysi backenddagi `User` javobiga moslashtirildi.
2. O'chirilgan maydonlar: `status`, `hiredAt`.
3. Qo'shilgan maydonlar: `managerId`, `workScheduleId`, `address`, `passportSerial`, `dateOfBirth`, `avatarUrl`, `faceImageUrl`, `baseSalary`.
4. `fullName` maydoni saqlab qolindi va unga `/** Frontend-only computed field (firstName + lastName). Not from backend. */` izohi yozildi.
5. `src/app/features/employees/pages/employee-detail/employee-detail.html` faylida `status` o'rniga `isActive` ishlatildi va `hiredAt` o'rniga `createdAt` sanasi ko'rsatiladigan qilindi.
6. `src/app/features/employees/services/employee.ts` (EmployeeService) xizmatiga `toggleStatus`, `toggleBlocked`, va `changePassword` uchun yangi metodlar (API requestlari) qo'shildi, ApiResponse strukturasi buzilmagan holda.
7. Frontend ilova muvaffaqiyatli build bo'ldi (`npm run build`). Xatolar yo'q.

## O'zgargan fayllar:

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `test-zdes-front/src/app/core/models/employee.ts` | Model | Backend `User` javobidagi barcha kerakli maydonlarni qo'shish va ortiqchalarini olib tashlash. |
| `test-zdes-front/src/app/features/employees/pages/employee-detail/employee-detail.html` | HTML Template | O'chirilgan `status` va `hiredAt` xususiyatlari o'rniga `isActive` va `createdAt` ni ishlatish uchun. |
| `test-zdes-front/src/app/features/employees/services/employee.ts` | Service | Yangi `toggleStatus`, `toggleBlocked` va `changePassword` metodlarini qo'shish uchun. |


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-USER.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-USER
### Sarlavha: Employee (backend `user` moduli) — model maydonlarini backendga to'liq moslash

**Maqsad (Goal):**
Backend `user` moduli frontendda `employees` feature'iga mos keladi
(`core/models/employee.ts`). Hozirgi `Employee` interfeysida backendda yo'q
ikkita maydon (`fullName`, `status`, `hiredAt`) va backendda bor, lekin
frontendda yo'q ko'plab maydon bor (`managerId`, `workScheduleId`, `address`,
`passportSerial`, `dateOfBirth`, `avatarUrl`, `faceImageUrl`, `baseSalary`).
Asosiy maqsad — response/request tiplarni backendga aynan moslash.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/user.md):**
- `User` javob maydonlari (`POST/GET/PATCH /api/v1/users` bo'yicha bir xil):
  `id, login, role, companyId, branchId, departmentId, positionId, managerId,
  workScheduleId, employeeNo, firstName, lastName, middleName, phone, email,
  address, passportSerial, dateOfBirth, avatarUrl, faceDeviceUserId,
  faceImageUrl, baseSalary, isActive, isBlocked, createdAt, updatedAt`.
  **`fullName`, `status`, `hiredAt` degan maydonlar backendda YO'Q.**
- `dateOfBirth`: `DateTime` (`@db.Date`, faqat sana), `baseSalary`: `Decimal(15,2)`
  (JSON orqali odatda `string` yoki `number` kelishi mumkin — real javobda qanday
  serializatsiya qilinganini komponentda ishlatishdan oldin tekshiring).
- `PATCH /users/me` — o'zini yangilash uchun cheklangan maydon to'plami bor
  (parolni bu orqali o'zgartirib bo'lmaydi — `change-password` alohida endpoint).
- `PATCH /users/:id/toggle-status`, `toggle-blocked`, `change-password` — alohida
  kichik endpointlar, `isActive`/`isBlocked`/parolni navbatma-navbat boshqaradi.
- `DELETE /users/:id` — javob shakli uchun `../backend_crud_review/user.md`dagi
  DELETE bo'limiga qarang.
- To'liq tafsilot (9 endpoint, 8 bo'limlik tahlil): `../backend_crud_review/user.md`.

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/employee.ts` — hozirgi holat: `id?, login?, firstName?,
  lastName?, middleName?, fullName?, phone?, email?, role?, companyId?,
  branchId?, departmentId?, positionId?, isActive?, isBlocked?, employeeNo?,
  faceDeviceUserId?, status?: 'active'|'inactive', hiredAt?, createdAt?, updatedAt?`.
  - `status: 'active'|'inactive'` — backendda bunday enum yo'q, haqiqiy holat
    `isActive: boolean` orqali ifodalanadi. Komponentlarda `status` ishlatilgan
    joylarni topib, `isActive`ga o'tkazing (yoki ikkalasi ham kerak bo'lsa,
    `status`ni `isActive`dan hisoblanadigan derived qiymat qiling — backendga
    yubormang).
  - `hiredAt` — backendda mos maydon yo'q (ehtimol `createdAt` yoki `dateOfBirth`
    bilan adashtirilgan) — ishlatilgan joylarni tekshirib, kerak bo'lsa `createdAt`ga
    almashtiring yoki butunlay olib tashlang.
  - `fullName` — backendda yo'q, hisoblab chiqariladigan (`firstName + lastName`)
    frontend-only qulaylik bo'lishi mumkin — agar shunday ishlatilsa qoldiring,
    lekin izohda "backend maydoni emas, computed" deb belgilang.
  - Yetishmayotgan: `managerId?`, `workScheduleId?`, `address?`, `passportSerial?`,
    `dateOfBirth?`, `avatarUrl?`, `faceImageUrl?`, `baseSalary?`.
- `src/app/features/employees/services/employee.ts` — CRUD + `toggle-status`/
  `toggle-blocked`/`change-password` uchun alohida metodlar bormi tekshiring,
  yo'q bo'lsa backend endpointlariga mos qo'shing (faqat shu servis fayli
  ichida, request/response tipi darajasida).
- `src/app/features/employees/pages/employee-form/employee-form.ts`,
  `employee-detail/employee-detail.ts`, `employee-list/employee-list.ts` —
  model o'zgarishidan keyin `.ts` mantiqni (property access, forma default
  qiymatlari) moslang.
- Eslatma: `core/models/user.ts` dagi `User` (auth/login javobi) va
  `core/models/employee.ts` dagi `Employee` bir xil backend `User` modelidan
  kelsa-da, ikki xil interfeys sifatida saqlanmoqda (login qisqartirilgan
  maydon to'plami qaytaradi, `/users/:id` esa to'liq) — buni ataylab shunday
  qoldiring, birlashtirmang (alohida modul, `B-I-AUTH`da ko'rib chiqiladi).

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- `auth`/`user.ts` (login modeli) ga tegmang — bu `B-I-AUTH` qamroviga kiradi.
- `face-register` komponentiga (`faceDescriptor`/face-recognition oqimi) tegmang — bu alohida, murakkabroq oqim, shu task doirasida emas.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/employee.ts`
- `test-zdes-front/src/app/features/employees/services/employee.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-form/employee-form.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-detail/employee-detail.ts`
- `test-zdes-front/src/app/features/employees/pages/employee-list/employee-list.ts`
- `test-zdes-front/project_docs/api/employees.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Employee` interfeysi backend `User` javobiga to'liq mos (yuqoridagi to'liq ro'yxat), backendda yo'q maydonlar (`status`, `hiredAt`) tozalangan yoki aniq derived/frontend-only deb izohlangan.
- Servis metodlari (`toggle-status`, `toggle-blocked`, `change-password` kabi) mavjud bo'lsa to'g'ri tip bilan ishlaydi.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-USER-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-USER.md` va `B-I-USER-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-SALARY-ADJUSTMENT.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-SALARY-ADJUSTMENT
### Sarlavha: SalaryAdjustment modeli — companyId/category/month qo'shish, id tipini to'g'irlash

**Maqsad (Goal):**
`core/models/salary-adjustment.ts` da `id`/`employeeId` `number` deb yozilgan
(backendda UUID `string`), va `category`/`month`/`companyId`/audit maydonlari
butunlay yo'q.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`). **Agar servis hali umuman `.data` unwrap qilmasa** (masalan yangi/yalang'och servis), buni `map((res: any) => res?.data ?? res)` pattern bilan QO'SHING — `B-I-WORK-SCHEDULE`da AGY yangi metod qo'shganda buni unutib, funksional regressiya yozgan edi (Claude Code tuzatgan).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/salary-adjustment.md):**
- `SalaryAdjustment` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), employeeId (string), type
  (AdjustmentType), category (AdjustmentCategory, default manual), amount
  (number, Decimal(15,2)), date (string/DateTime), month (string, "YYYY-MM"),
  reason (string | null), createdById (string | null), updatedById (string | null),
  createdAt, updatedAt`.
- `AdjustmentType`/`AdjustmentCategory` enum qiymatlari to'liq sanalmagan
  (misolda `AdjustmentType.bonus`, default `AdjustmentCategory.manual` ko'rsatilgan)
  — qat'iy union o'ylab topmang (frontenddagi `'bonus' | 'penalty'` union
  to'g'ri bo'lishi mumkin, lekin tasdiqlanmagan — xohlasangiz `string` qilib
  xavfsizroq qoldiring, javob faylida qaysi variantni tanlaganingizni yozing).
- `GET /salary-adjustments` — paginatsiya: `{ items, total, page, limit, totalPages }`.
- To'liq tafsilot: `../backend_crud_review/salary-adjustment.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/salary-adjustment.ts` — hozirgi holat:
  ```ts
  export interface SalaryAdjustment {
    id: number;
    employeeId: number;
    amount: number;
    type: 'bonus' | 'penalty';
    reason?: string;
    date: string;
  }
  ```
  `id`/`employeeId` — **`number` emas, `string` (UUID)**. Yetishmayotgan:
  `companyId`, `category`, `month`, `createdById`, `updatedById`, `createdAt`, `updatedAt`.
- `src/app/features/salary-adjustments/services/salary-adjustment.ts` — CRUD
  metodlari, `id` tipini `string`ga moslang.
- `src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.ts`,
  `adjustment-list/adjustment-list.ts` — model o'zgarishidan keyin `.ts`
  mantiqni moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/salary-adjustment.ts`
- `test-zdes-front/src/app/features/salary-adjustments/services/salary-adjustment.ts`
- `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.ts`
- `test-zdes-front/src/app/features/salary-adjustments/pages/adjustment-list/adjustment-list.ts`
- `test-zdes-front/project_docs/api/salary-adjustments.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `SalaryAdjustment` interfeysi to'liq backend bilan mos, `id`/`employeeId`/`companyId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-SALARY-ADJUSTMENT-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-SALARY-ADJUSTMENT.md` va `B-I-SALARY-ADJUSTMENT-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/B-A-PAYROLL-response.md`

# B-A-PAYROLL Response

## Jarayon
- `src/modules/payroll/payroll.controller.ts` faylini o'qidim va 5 ta endpoint borligini aniqladim (POST, GET, GET /:id, PATCH /:id, DELETE /:id).
- `src/modules/payroll/dto/*` fayllarini o'qib, DTO'lar, ularning xossalari, swagger example misollari va validatsiya dekoratorlarini tahlil qildim.
- `src/modules/payroll/payroll.service.ts` faylini o'qib, qaysi errorlar qaytarilishi mumkinligini va logika ishini qarab chiqdim.
- `prisma/schema.prisma` faylidan `Payroll` modelini va unga bo'lgan munosabatlarni tekshirib (grep orqali boshqa modellarda `payrollId` yo'qligini tekshirdim), DB strukturasini aniqladim.
- Hamma ma'lumotlarni so'ralgan struktura asosida `backend_crud_review/payroll.md` fayliga yozdim.

## Tahlil qilingan endpointlar
Tahlil qilingan endpointlar soni: 5 ta.
1. `POST /api/v1/payrolls`
2. `GET /api/v1/payrolls`
3. `GET /api/v1/payrolls/:id`
4. `PATCH /api/v1/payrolls/:id`
5. `DELETE /api/v1/payrolls/:id`

## Yakuniy xulosa
`payroll` modulidagi barcha 5 ta endpoint muvaffaqiyatli tahlil qilindi. Tahlil natijasi `backend_crud_review/payroll.md` ga yozildi va unda har bir model, dto, misollar, validation qoidalari va aloqalari (Cascade, va hk) yoritildi. Fayllarda hech qanday o'zgarish amalga oshirilmadi (read-only shartiga ko'ra).


## Manba: `zdes_archive_docs/raw_history/orcestor/front_integration_tasks/B-I-TERMINAL.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

## Task ID: B-I-TERMINAL
### Sarlavha: Terminal modeli — to'liq qayta yozish (id string/UUID, barcha maydonlar backendga mos)

**Maqsad (Goal):**
`core/models/terminal.ts` hozir juda eskirgan/taxminiy: `id: number`,
`branchId?: number`, faqat 4 maydon. Backend `Terminal` esa UUID `id`, 12
maydon va ikkita enum (`TerminalType`, `TerminalStatus`) bilan ishlaydi.
Modelni backend bilan to'liq moslab qayta yozish.

**MUHIM — global response o'rami (2026-07-26):** Backend global `ResponseInterceptor`
orqali HAR BIR javobni `{ success, statusCode, message, data: <pastdagi shakl>,
path, timestamp }` ko'rinishida o'raydi (`zdes_backend/src/main.ts` +
`common/interceptors/response.interceptor.ts`) — bu `backend_crud_review/*.md`da
yozilmagan. Agar servis allaqachon `.data`/`.items` unwrap qilsa (`core/models/api-response.ts`
dagi `ApiResponse<T>`/`PaginatedResult<T>`), **buni olib tashlamang** — faqat
ichki `T` tipini quyidagiga moslang (`B-I-AUTH`da AGY aynan shu xatoni qilib
login'ni buzgan edi — `orcestor/errors/B-I-AUTH.md`).

**Backend manba (Backend Source — read-only kontekst, ../backend_crud_review/terminal.md):**
- `Terminal` javob/DB maydonlari (5 endpoint bo'yicha bir xil):
  `id (string, UUID), companyId (string), branchId (string | null), name (string),
  serialNumber (string, unique), ipAddress (string | null), port (number | null),
  type (TerminalType, default zkteco_face), status (TerminalStatus, default active),
  connectionConfig (Record<string, unknown> | null), lastSyncAt (string | null),
  createdAt, updatedAt`.
  **`TerminalType`/`TerminalStatus` aniq qiymatlari tahlil hujjatida sanab
  o'tilmagan** — faqat defaultlari ma'lum (`zkteco_face`, `active`). Qat'iy
  enum union yozmang; `string` sifatida qoldiring (aniq qiymatlar ro'yxati
  kerak bo'lsa, buni javob faylida eslatib qo'ying — keyingi taskda backend
  tahlili to'ldirilishi mumkin).
- `GET /terminals` — paginatsiya: `{ items: Terminal[], total, page, limit, totalPages }`.
- `DELETE /terminals/:id` — `{ success: true, id: string }`.
- To'liq tafsilot: `../backend_crud_review/terminal.md` (5 endpoint, 8 bo'lim).

**Kontekst (Context — test-zdes-front hozirgi holati):**
- `src/app/core/models/terminal.ts` — hozirgi holat:
  ```ts
  export interface Terminal {
    id: number;
    name: string;
    branchId?: number;
    ipAddress?: string;
  }
  ```
  `id`/`branchId` **`number` emas, `string` (UUID)** bo'lishi kerak. Yetishmayotgan:
  `companyId`, `serialNumber`, `port`, `type`, `status`, `connectionConfig`,
  `lastSyncAt`, `createdAt`, `updatedAt`.
- `src/app/features/terminals/services/terminal.ts` — CRUD metodlari, `id`
  parametrlari hozir `number` deb yozilgan bo'lishi mumkin — `string`ga
  moslang, paginatsiya javobini qanday parslashini tekshiring.
- `src/app/features/terminals/pages/terminal-form/terminal-form.ts`,
  `terminal-list/terminal-list.ts` — model o'zgarishidan keyin `.ts` mantiqni
  (`id` tipi, forma default qiymatlari) moslang.

**Cheklovlar (Constraints):**
- Faqat `.ts` tip/servis/data-binding — HTML/CSS ga tegmang.
- `zdes_backend`ga yozmang.
- Boshqa modulga tegmang.

**Ish doirasidagi fayllar (Files in scope):**
- `test-zdes-front/src/app/core/models/terminal.ts`
- `test-zdes-front/src/app/features/terminals/services/terminal.ts`
- `test-zdes-front/src/app/features/terminals/pages/terminal-form/terminal-form.ts`
- `test-zdes-front/src/app/features/terminals/pages/terminal-list/terminal-list.ts`
- `test-zdes-front/project_docs/api/terminals.md` (agar mavjud, mos yangilang)

**Bajarilgan deb hisoblanish mezoni (Definition of Done):**
- `Terminal` interfeysi to'liq backend bilan mos (yuqoridagi to'liq ro'yxat), `id`/`branchId`/`companyId` `string` tipida.
- Servis/komponent fayllari yangi tip bilan TS xatosiz.
- `npm run build` xatosiz o'tadi.

**Tavsiya etilgan Antigravity rejimi (Mode):**
Agent-driven

**Natijani qayerga yozish kerak (Report back):**
- Har bir muhim qadamni darhol `/home/fayzillo/Desktop/zdes/orcestor/task_pending/B-I-TERMINAL-response.md` fayliga yozib boring.
- Tugagach, yakuniy xulosa + "O'zgargan fayllar" jadvali qo'shing (Fayl | Turi | Qisqa sabab).
- `B-I-TERMINAL.md` va `B-I-TERMINAL-response.md`ni `/home/fayzillo/Desktop/zdes/orcestor/task_compliete/`ga ko'chiring.
