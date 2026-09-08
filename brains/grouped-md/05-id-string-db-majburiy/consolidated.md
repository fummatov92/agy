# API Sozlamalari, Xabarnomalar va Prisma Tizim Arxitekturasi (API & DB Settings)


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/setting.md`

# Setting Module API Documentation

## 1. POST /api/v1/settings
**Point**: `POST /api/v1/settings`
Yangi sozlamani (setting) yaratish.

**ApiBody / Misollar**:
```json
{
  "companyId": "ffbf3676-4428-415b-9e6b-0833f249072d", // Admin uchun avtomatik to'ldiriladi, Superadmin uchun kiritilishi mumkin
  "key": "attendance_kpi_template",
  "value": { "latePenaltyPerMinute": 1000 }
}
```

**Guard**:
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`
- `@CurrentUser()`

**DTO**:
`CreateSettingDto`:
- `companyId` (IsOptional, IsUUID)
- `key` (IsString, MinLength(1), MaxLength(255), Required)
- `value` (IsOptional, IsObject)

**Service**:
1. `resolveScopedCompanyId` orqali actor va kiritilgan `companyId` bo'yicha haqiqiy `companyId` aniqlanadi.
2. `ensureCompanyExists` orqali company mavjudligi tekshiriladi.
3. `normalizeRequired` orqali `key` tekshiriladi (bo'sh emasligi).
4. `ensureUniqueKey` orqali berilgan company uchun bu `key` oldin kiritilmagani tekshiriladi.
5. Prisma orqali ma'lumot saqlanadi va qaytariladi.

**Response**:
```json
{
  "id": "e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b",
  "companyId": "ffbf3676-4428-415b-9e6b-0833f249072d",
  "key": "attendance_kpi_template",
  "value": {
    "latePenaltyPerMinute": 1000
  },
  "createdAt": "2026-08-22T17:25:35.000Z",
  "updatedAt": "2026-08-22T17:25:35.000Z"
}
```

**Error case**:
- `404 Not Found`: "Company not found"
- `409 Conflict`: "Setting key is required" yoki "Setting key already exists for this company"
- `401 Unauthorized`: Token yaroqsiz bo'lsa yoki topilmasa

**DB struktura**:
Model `Setting`:
- `id` (String, UUID, pk)
- `companyId` (String, UUID, relation to Company)
- `key` (String, VarChar(255))
- `value` (Json, null bo'lishi mumkin)
- `createdAt` (DateTime)
- `updatedAt` (DateTime)
Unique constraint: `@@unique([companyId, key])`

**cURL**:
```bash
curl -X POST http://localhost:4000/api/v1/settings \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"key": "attendance_kpi_template", "value": {"latePenaltyPerMinute": 1000}}'
```

---

## 2. GET /api/v1/settings
**Point**: `GET /api/v1/settings`
Sozlamalar ro'yxatini olish (pagination bilan).

**ApiBody / Misollar**:
URL parametrlar (Query):
- `companyId` (UUID, optional)
- `search` (string, optional)
- `page` (number, default: 1)
- `limit` (number, default: 10)

**Guard**:
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`
- `@CurrentUser()`

**DTO**:
`SettingQueryDto`:
- `companyId` (IsOptional, IsUUID)
- `search` (IsOptional, IsString)
- `page` (IsOptional, Type Number, IsInt, Min 1)
- `limit` (IsOptional, Type Number, IsInt, Min 1, Max 100)

**Service**:
1. Actor va query `companyId` asosida `resolveCompanyBranchScope` funksiyasi yordamida ruxsat berilgan `companyId` olinadi.
2. `search` parametri bo'lsa, `key` ustuni bo'yicha qidiriladi (case-insensitive).
3. Prisma orqali pagination bilan so'rov yuboriladi va umumiy soni hisoblanadi (transaction).

**Response**:
```json
{
  "items": [
    {
      "id": "e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b",
      "companyId": "ffbf3676-4428-415b-9e6b-0833f249072d",
      "key": "attendance_kpi_template",
      "value": {
        "latePenaltyPerMinute": 1000
      },
      "createdAt": "2026-08-22T17:25:35.000Z",
      "updatedAt": "2026-08-22T17:25:35.000Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "totalPages": 1
}
```

**Error case**:
- `401 Unauthorized`: Token yaroqsiz bo'lsa
- `400 Bad Request`: Validatsiyadan o'tmasa

**DB struktura**:
(Yuqorida ko'rsatilgan kabi).

**cURL**:
```bash
curl -X GET "http://localhost:4000/api/v1/settings?page=1&limit=10&search=attendance" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 3. GET /api/v1/settings/:id
**Point**: `GET /api/v1/settings/:id`
Bitta sozlamani `id` orqali olish.

**ApiBody / Misollar**:
URL parametr:
- `id` (UUID)

**Guard**:
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`
- `@CurrentUser()`

**DTO**:
Parametr: `ParseUUIDPipe`

**Service**:
1. `findSettingByIdOrThrow` funksiyasi yordamida setting olinadi, yo'q bo'lsa `404` qaytadi.
2. `assertWithinScope` orqali joriy foydalanuvchining unga ruxsati bor-yo'qligi tekshiriladi.
3. Sozlama qaytariladi.

**Response**:
```json
{
  "id": "e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b",
  "companyId": "ffbf3676-4428-415b-9e6b-0833f249072d",
  "key": "attendance_kpi_template",
  "value": {
    "latePenaltyPerMinute": 1000
  },
  "createdAt": "2026-08-22T17:25:35.000Z",
  "updatedAt": "2026-08-22T17:25:35.000Z"
}
```

**Error case**:
- `404 Not Found`: "Setting not found"
- `403 Forbidden`: Actor ushbu kompaniya ma'lumotlarini ko'rishga ruxsati bo'lmasa
- `401 Unauthorized`: Token yaroqsiz

**DB struktura**:
(Yuqorida ko'rsatilgan).

**cURL**:
```bash
curl -X GET "http://localhost:4000/api/v1/settings/e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 4. PATCH /api/v1/settings/:id
**Point**: `PATCH /api/v1/settings/:id`
Mavjud sozlamani tahrirlash.

**ApiBody / Misollar**:
```json
{
  "value": { "latePenaltyPerMinute": 1500 }
}
```

**Guard**:
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`
- `@CurrentUser()`

**DTO**:
`UpdateSettingDto`: `CreateSettingDto` ning qisman (Partial) varianti. URL da `id` (ParseUUIDPipe).

**Service**:
1. Eski setting `findSettingByIdOrThrow` orqali olinadi.
2. `assertWithinScope` yordamida tekshiriladi.
3. Yangi `companyId` berilgan bo'lsa uni tekshiriladi, yo'qsa eskisi qoldiriladi.
4. Yangi `key` berilgan bo'lsa uni validate qilinadi.
5. Yangi company/key kombinatsiyasi uchun unikallik tekshiriladi (`ensureUniqueKey`).
6. Prisma orqali update qilinadi.

**Response**:
```json
{
  "id": "e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b",
  "companyId": "ffbf3676-4428-415b-9e6b-0833f249072d",
  "key": "attendance_kpi_template",
  "value": {
    "latePenaltyPerMinute": 1500
  },
  "createdAt": "2026-08-22T17:25:35.000Z",
  "updatedAt": "2026-08-22T17:35:00.000Z"
}
```

**Error case**:
- `404 Not Found`: "Setting not found" yoki "Company not found"
- `409 Conflict`: "Setting key already exists for this company"
- `403 Forbidden`: Scope ruxsati yo'q

**DB struktura**:
(Yuqorida ko'rsatilgan).

**cURL**:
```bash
curl -X PATCH http://localhost:4000/api/v1/settings/e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"value": {"latePenaltyPerMinute": 1500}}'
```

---

## 5. DELETE /api/v1/settings/:id
**Point**: `DELETE /api/v1/settings/:id`
Mavjud sozlamani o'chirish.

**ApiBody / Misollar**:
URL parametr:
- `id` (UUID)

**Guard**:
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`
- `@CurrentUser()`

**DTO**:
Parametr: `ParseUUIDPipe`

**Service**:
1. `findSettingByIdOrThrow` yordamida record tekshiriladi.
2. `assertWithinScope` orqali ushbu o'chirishga ruxsat so'raladi.
3. Prisma delete orqali o'chiriladi.
4. O'chirilgan yozuv id si qaytariladi.

**Response**:
```json
{
  "success": true,
  "id": "e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b"
}
```

**Error case**:
- `404 Not Found`: "Setting not found"
- `403 Forbidden`: Ruxsat yo'q

**DB struktura**:
(Yuqorida ko'rsatilgan).

**cURL**:
```bash
curl -X DELETE http://localhost:4000/api/v1/settings/e5b1c6d0-a7b6-4f7a-8f5c-8b8b9b8b9b8b \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/holiday.md`

### Endpoint: POST /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/holidays`
- Controller class + method nomi: `HolidayController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `Navruz holiday`
- `startDate`: `2026-03-21`
- `endDate`: `2026-03-22`
- `affectsSalary`: `false`
- `note`: `Official company holiday`

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `CreateHolidayDto` (src/modules/holiday/dto/create-holiday.dto.ts)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `startDate`: string, `@Type(() => String)`, `@IsDateString()`
- `endDate`: string, `@Type(() => String)`, `@IsDateString()`
- `affectsSalary`: boolean, `@IsOptional()`, `@IsBoolean()`
- `note`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Service method: `HolidayService.create` (src/modules/holiday/holiday.service.ts:create)
- Mantiq: Aktyor ruxsatlarini hisobga olgan holda kompaniya va (ixtiyoriy) filialni tekshiradi. Yozilgan sana oralig'ining to'g'riligini (endDate >= startDate) ham tekshiradi. Barcha shartlar bajarilganda, ma'lumotlar bazasida yangi Holiday (ta'til/bayram) yozuvini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan `Holiday` obyekti to'liq qaytariladi.
- Maydonlari: `id` (String), `companyId` (String), `branchId` (String, null bo'lishi mumkin), `name` (String), `startDate` (DateTime), `endDate` (DateTime), `affectsSalary` (Boolean), `note` (String, null bo'lishi mumkin), `createdById` (String), `updatedById` (String), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: "Company not found" - agar kompaniya topilmasa (404)
- `NotFoundException`: "Branch not found" - agar filial topilmasa (404)
- `ConflictException`: "Branch does not belong to the selected company" - agar filial boshqa kompaniyaga tegishli bo'lsa (409)
- `ConflictException`: "Holiday name is required" - agar nom bo'sh yoki faqat probellardan iborat bo'lsa (409)
- `BadRequestException`: "Holiday end date must be after start date" - agar tugash sanasi boshlanish sanasidan oldin bo'lsa (400)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif:
  - `id`: String, Majburiy, `@id`, `@default(uuid())`, `@db.Uuid`
  - `companyId`: String, Majburiy, `@db.Uuid`
  - `branchId`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `name`: String, Majburiy, `@db.VarChar(255)`
  - `startDate`: DateTime, Majburiy, `@db.Date`
  - `endDate`: DateTime, Majburiy, `@db.Date`
  - `affectsSalary`: Boolean, Majburiy, `@default(false)`
  - `note`: String, Ixtiyoriy (`?`)
  - `createdById`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `Company`: `companyId -> Company.id (onDelete: Cascade)`
  - `Branch`: `branchId -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - (Topilmadi - hech qaysi boshqa model Holiday modeliga ishora qilmaydi)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([startDate])`
  - `@@index([endDate])`

---

### Endpoint: GET /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays`
- Controller class + method nomi: `HolidayController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (GET so'rovi bo'lgani uchun query parametrlar qabul qiladi).
- Query parametr misollari (`HolidayQueryDto` asosida):
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `search`: `navruz`
  - `affectsSalary`: `true`
  - `dateFrom`: `2026-03-01`
  - `dateTo`: `2026-03-31`
  - `page`: `1` (default: 1)
  - `limit`: `10` (default: 10)

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `HolidayQueryDto` (src/modules/holiday/dto/holiday-query.dto.ts)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `affectsSalary`: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- `dateFrom`: string, `@IsOptional()`, `@IsString()`
- `dateTo`: string, `@IsOptional()`, `@IsString()`
- `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `HolidayService.findAll` (src/modules/holiday/holiday.service.ts:findAll)
- Mantiq: Berilgan filtrlarga (qidiruv so'zi, companyId, branchId, affectsSalary, va sana oralig'i) va aktyor ruxsat doirasiga asoslanib `Holiday` modelidan ma'lumotlarni izlaydi. Paginatsiya qilingan (limit/page) qilib ro'yxat va umumiy sonini (`total`) qaytaradi. Sana bo'yicha filter qilinganda Date(dateFrom) va Date(dateTo) obyektlari asosida qoplanishlar tekshiriladi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya qilingan obyekt:
  - `items`: `Holiday` model obyektlar massivi
  - `total`: Topilgan barcha yozuvlar soni (Number)
  - `page`: Joriy sahifa raqami (Number)
  - `limit`: Bitta sahifadagi yozuvlar limiti (Number)
  - `totalPages`: Jami sahifalar soni (Number)

**7. Error case:**
- Boshqa maxsus xatolar ko'rsatilmagan (lekin avtorizatsiya va noto'g'ri so'rov xatoliklari bo'lishi mumkin).

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif (POST /api/v1/holidays dagi bilan bir xil).
- Relations / references (Chiquvchi va Kiruvchi) va Indekslar - yuqorida keltirilgandek bir xil. Paginatsiya va ro'yxat qidirish uchun `@@index([companyId])`, `@@index([branchId])`, `@@index([startDate])`, `@@index([endDate])` indekslar ishlatilishi nazarda tutilgan.

---

### Endpoint: GET /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. Faqat url ichida `id` parametri keladi.

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- DTO klassi yo'q. Parametr sifatida `id: string` (`ParseUUIDPipe` bilan) qabul qiladi.

**5. Service:**
- Service method: `HolidayService.findOne` (src/modules/holiday/holiday.service.ts:findOne)
- Mantiq: Berilgan `id` yordamida `Holiday` ni qidiradi va joriy foydalanuvchi (actor) uchun ushbu obyektga kirish ruxsati borligini tekshiradi (`assertWithinScope`). Topilsa qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Topilgan bitta `Holiday` obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: "Holiday not found" - agar ushbu `id` bilan yozuv topilmasa (404)
- `ForbiddenException`: "Access denied" (yoki `assertWithinScope` ichida otiladigan huquq etishmovchiligi xatosi, agar aktyor ushbu company/branch ga ruxsati bo'lmasa). (403 odatda)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif va bog'lanishlar - POST dagi kabi bir xil. Bitta obyekt bo'yicha ma'lumotlar olinadi.

---

### Endpoint: PATCH /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `UpdateHolidayDto` (CreateHolidayDto ning Partial ko'rinishi) quyidagi ehtimoliy qiymatlarga ega:
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `name`: `Navruz holiday`
  - `startDate`: `2026-03-21`
  - `endDate`: `2026-03-22`
  - `affectsSalary`: `false`
  - `note`: `Official company holiday`

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `UpdateHolidayDto` (src/modules/holiday/dto/update-holiday.dto.ts) -> Bu `PartialType(CreateHolidayDto)` hisoblanadi.
- Barcha maydonlari (companyId, branchId, name, startDate, endDate, affectsSalary, note) ixtiyoriy (`@IsOptional()`). Validatsiya dekoratorlari xuddi `CreateHolidayDto` dagi kabi.

**5. Service:**
- Service method: `HolidayService.update` (src/modules/holiday/holiday.service.ts:update)
- Mantiq: Dastlab ko'rsatilgan `id` dagi holiday borligiga ishonch hosil qiladi va foydalanuvchining unga ruxsatini tekshiradi (`assertWithinScope`). So'ngra yangi kiritilgan ma'lumotlarga qarab tegishli `Company` va `Branch` larni bazada mavjudligini hamda aktyor ruxsatlarini qaytadan tekshiradi. Yana endDate >= startDate oraliq validatsiyasidan o'tadi va bazadagi ma'lumotni yangilaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Holiday` obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: "Holiday not found" - holiday topilmasa (404)
- (Yana `assertWithinScope` xatoligi ehtimoli)
- `NotFoundException`: "Company not found" (404)
- `NotFoundException`: "Branch not found" (404)
- `ConflictException`: "Branch does not belong to the selected company" (409)
- `ConflictException`: "Holiday name is required" (409)
- `BadRequestException`: "Holiday end date must be after start date" (400)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif, Relations va Indekslar POST bo'limidagi bilan aynan bir xil.

---

### Endpoint: DELETE /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- DTO klassi yo'q. URL ichidan `id` parametri `ParseUUIDPipe` orqali keladi.

**5. Service:**
- Service method: `HolidayService.delete` (src/modules/holiday/holiday.service.ts:delete)
- Mantiq: Yozuvni qidirib topadi, foydalanuvchining huquqlarini tekshiradi (`assertWithinScope`) va `Holiday` jadvalidan to'liq o'chirib yuboradi (hard delete). 

**6. Response:**
- Qaytariladigan javob shakli: `success` (Boolean) true qiymati va o'chirilgan holidayning `id` si qatnashgan obyekt: `{ success: true, id: string }`.

**7. Error case:**
- `NotFoundException`: "Holiday not found" (404)
- Ruxsat etishmovchiligi xatosi (`assertWithinScope` orqali) (403)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif (POST bilan bir xil).
- Relations / references (Chiquvchi):
  - `Company`: `companyId -> Company.id (onDelete: Cascade)`
  - `Branch`: `branchId -> Branch.id (onDelete: SetNull)`
- **Relations / references (Kiruvchi - O'chirilganda nima bo'ladi):**
  - Hech qaysi boshqa model ushbu `Holiday` modeliga xorijiy kalit (Foreign Key) orqali ishora qilmaydi. Shuning uchun o'chirish hech qanday boshqa modellarda to'g'ridan-to'g'ri o'zgarishga (masalan SetNull yoki Cascade delete) sabab bo'lmaydi. Xavfsiz o'chirish mumkin.
- Indekslar: yuqoridagi bo'limlardagidek.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/holiday.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

### Endpoint: POST /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/holidays`
- Controller class + method nomi: `HolidayController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `Navruz holiday`
- `startDate`: `2026-03-21`
- `endDate`: `2026-03-22`
- `affectsSalary`: `false`
- `note`: `Official company holiday`
- `companyId`: misol yo'q
- `branchId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar)

**4. DTO:**
- Request DTO: `CreateHolidayDto`
- `name`: Tip - String, majburiy, min: 1, max: 255
- `startDate`: Tip - String, majburiy, DateString
- `endDate`: Tip - String, majburiy, DateString
- `affectsSalary`: Tip - Boolean, ixtiyoriy, default: false
- `note`: Tip - String, ixtiyoriy, max: 1000
- `companyId`: Tip - String, ixtiyoriy, UUID
- `branchId`: Tip - String, ixtiyoriy, UUID

**5. Service:**
- Service method: `create`
- Tavsifi: `resolveScopedCompanyId` va `resolveCompanyBranchScope` orqali actor'ning huquqlari tekshiriladi. `startDate` va `endDate` sanalari tekshiriladi (`endDate < startDate` bo'lsa xatolik). Yangi `Holiday` yozuvi bazaga qo'shiladi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Holiday` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "7f09805d-222a-43d9-952a-3c480ad73105",
    "companyId": "01b2390a-1e4e-4f30-a887-86c318610be2",
    "branchId": null,
    "name": "Navruz holiday",
    "startDate": "2026-03-21T00:00:00.000Z",
    "endDate": "2026-03-22T00:00:00.000Z",
    "affectsSalary": false,
    "note": "Official company holiday",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T16:35:00.000Z",
    "updatedAt": "2026-08-22T16:35:00.000Z"
  },
  "path": "/api/v1/holidays",
  "timestamp": "2026-08-22T21:45:00.000Z"
}
```

**7. Error case:**
- `BadRequestException`: "Holiday end date must be after start date"
- `UnauthorizedException`: "Invalid token signature"
- `NotFoundException`: "Company not found", "Branch not found"
- `ConflictException`: "Holiday name is required", "Branch does not belong to the selected company"

**8. DB struktura:**
- Prisma modeli: `Holiday` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `startDate`: `DateTime`, majburiy, `@db.Date`
  - `endDate`: `DateTime`, majburiy, `@db.Date`
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id`
  - `branchId -> Branch.id`
- Relations (Kiruvchi): Yo'q

**cURL:**
```bash
curl -s -X POST http://localhost:4000/api/v1/holidays \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "name": "Navruz holiday",
  "startDate": "2026-03-21",
  "endDate": "2026-03-22",
  "affectsSalary": false,
  "note": "Official company holiday"
}'
```

---

### Endpoint: GET /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays`
- Controller class + method nomi: `HolidayController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `search`: `navruz`
  - `affectsSalary`: `true`
  - `dateFrom`: `2026-03-01`
  - `dateTo`: `2026-03-31`
  - `page`: `1`
  - `limit`: `10`
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `HolidayQueryDto`
- `companyId`: Tip - String, ixtiyoriy, UUID
- `branchId`: Tip - String, ixtiyoriy, UUID
- `search`: Tip - String, ixtiyoriy
- `affectsSalary`: Tip - Boolean, ixtiyoriy
- `dateFrom`: Tip - String, ixtiyoriy
- `dateTo`: Tip - String, ixtiyoriy
- `page`: Tip - Number, ixtiyoriy, default: 1
- `limit`: Tip - Number, ixtiyoriy, default: 10

**5. Service:**
- Service method: `findAll`
- Tavsifi: Actor huquqlariga ko'ra `companyId` va `branchId` aniqlanadi. Sana bo'yicha filter (`dateFrom`, `dateTo`), qidiruv (`search`) va `affectsSalary` bo'yicha bazadan ma'lumotlar olinadi. Pagination bilan qaytariladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "7f09805d-222a-43d9-952a-3c480ad73105",
        "companyId": "01b2390a-1e4e-4f30-a887-86c318610be2",
        "branchId": null,
        "name": "Navruz holiday",
        "startDate": "2026-03-21T00:00:00.000Z",
        "endDate": "2026-03-22T00:00:00.000Z",
        "affectsSalary": false,
        "note": "Official company holiday",
        "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
        "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
        "createdAt": "2026-08-22T16:35:00.000Z",
        "updatedAt": "2026-08-22T16:35:00.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/holidays?page=1&limit=10",
  "timestamp": "2026-08-22T21:45:00.000Z"
}
```

**7. Error case:**
- `UnauthorizedException`: "Invalid token signature"

**8. DB struktura:**
- Prisma modeli: `Holiday` (prisma/schema.prisma)
- (Yuqoridagi bilan bir xil)

**cURL:**
```bash
curl -s -X GET "http://localhost:4000/api/v1/holidays?page=1&limit=10" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string UUID sifatida olinadi, masalan `ParseUUIDPipe` bilan).

**5. Service:**
- Service method: `findOne`
- Tavsifi: ID orqali holiday topiladi (`findHolidayByIdOrThrow`). `assertWithinScope` orqali ruxsat tekshiriladi. Topilgan obyekt qaytariladi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Holiday` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7f09805d-222a-43d9-952a-3c480ad73105",
    "companyId": "01b2390a-1e4e-4f30-a887-86c318610be2",
    "branchId": null,
    "name": "Navruz holiday",
    "startDate": "2026-03-21T00:00:00.000Z",
    "endDate": "2026-03-22T00:00:00.000Z",
    "affectsSalary": false,
    "note": "Official company holiday",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T16:35:00.000Z",
    "updatedAt": "2026-08-22T16:35:00.000Z"
  },
  "path": "/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105",
  "timestamp": "2026-08-22T21:45:00.000Z"
}
```

**7. Error case:**
- `UnauthorizedException`: "Invalid token signature"
- `ForbiddenException`: Scope'dan tashqari bo'lsa
- `NotFoundException`: "Holiday not found"

**8. DB struktura:**
- Prisma modeli: `Holiday` (prisma/schema.prisma)
- (Yuqoridagi bilan bir xil)

**cURL:**
```bash
curl -s -X GET http://localhost:4000/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105 \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `Updated Navruz holiday`
- `affectsSalary`: `true`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateHolidayDto` (CreateHolidayDto'ning Partial varianti)

**5. Service:**
- Service method: `update`
- Tavsifi: ID orqali mavjud holiday topiladi. Actor ruxsatlari (`assertWithinScope`) tekshiriladi. Kiritilgan qiymatlar o'zgartirilib bazada saqlanadi. `updatedById` actor'ning ID'si bilan yangilanadi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `Holiday` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7f09805d-222a-43d9-952a-3c480ad73105",
    "companyId": "01b2390a-1e4e-4f30-a887-86c318610be2",
    "branchId": null,
    "name": "Updated Navruz holiday",
    "startDate": "2026-03-21T00:00:00.000Z",
    "endDate": "2026-03-22T00:00:00.000Z",
    "affectsSalary": true,
    "note": "Official company holiday",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T16:35:00.000Z",
    "updatedAt": "2026-08-22T16:40:00.000Z"
  },
  "path": "/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105",
  "timestamp": "2026-08-22T21:45:00.000Z"
}
```

**7. Error case:**
- `BadRequestException`: "Holiday end date must be after start date"
- `UnauthorizedException`: "Invalid token signature"
- `ForbiddenException`: Scope'dan tashqari bo'lsa
- `NotFoundException`: "Holiday not found", "Company not found", "Branch not found"
- `ConflictException`: "Branch does not belong to the selected company", "Holiday name is required"

**8. DB struktura:**
- Prisma modeli: `Holiday` (prisma/schema.prisma)
- (Yuqoridagi bilan bir xil)

**cURL:**
```bash
curl -s -X PATCH http://localhost:4000/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105 \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated Navruz holiday",
  "affectsSalary": true
}'
```

---

### Endpoint: DELETE /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string UUID sifatida olinadi).

**5. Service:**
- Service method: `delete`
- Tavsifi: ID orqali holiday topiladi. `assertWithinScope` orqali ruxsat tekshiriladi. Bazadan o'chirib tashlanadi va muvaffaqiyatli xabar qaytariladi.

**6. Response:**
- Qaytariladigan javob shakli:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7f09805d-222a-43d9-952a-3c480ad73105"
  },
  "path": "/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105",
  "timestamp": "2026-08-22T21:45:00.000Z"
}
```

**7. Error case:**
- `UnauthorizedException`: "Invalid token signature"
- `ForbiddenException`: Scope'dan tashqari bo'lsa
- `NotFoundException`: "Holiday not found"

**8. DB struktura:**
- Prisma modeli: `Holiday` (prisma/schema.prisma)
- (Yuqoridagi bilan bir xil)

**cURL:**
```bash
curl -s -X DELETE http://localhost:4000/api/v1/holidays/7f09805d-222a-43d9-952a-3c480ad73105 \
-H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/attendance.md`

### Endpoint: GET /api/v1/attendance/kpi-template/:companyId
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:getKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/kpi-template/:companyId`
- Controller class + method nomi: `AttendanceController.getKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` ko'rsatilmagan (lekin `@ApiBearerAuth()` bor, ehtimol global guard)
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: Yo'q (faqat Param: `companyId` ParseUUIDPipe)

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.getKpiTemplate` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Bajaruvchi ko'rsatilgan kompaniyaga tegishli yoki ruxsati borligini tekshiradi va shu kompaniya uchun KPI shablonini (`Setting` jadvalidan) yoki bazaviy standart (default) shablonni qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli (AttendanceKpiTemplateDto):
  - companyId: string (UUID)
  - latePenaltyPerMinute: number
  - earlyLeavePenaltyPerMinute: number
  - overtimeBonusPerMinute: number
  - faceSimilarityThreshold: number

**7. Error case:**
- `ForbiddenException`: Agar actor shu kompaniyaga tegishli/ruxsati bo'lmasa.
- `NotFoundException`: Agar kompaniya bazada topilmasa.

**8. DB struktura:**
Model: `Setting`, `Company` (ushbu endpoint asosan shablon o'qiydi).
Umumiy modul uchun tegishli `Attendance` modeli tarkibi:
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar (Attendance):
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: PUT /api/v1/attendance/kpi-template
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:upsertKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PUT /api/v1/attendance/kpi-template`
- Controller class + method nomi: `AttendanceController.upsertKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `latePenaltyPerMinute`: 1000
- `earlyLeavePenaltyPerMinute`: 1000
- `overtimeBonusPerMinute`: 1000
- `faceSimilarityThreshold`: 90

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` ko'rsatilmagan
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: `AttendanceKpiTemplateDto` (`zdes_backend/src/modules/attendance/dto/attendance-kpi-template.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `latePenaltyPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `earlyLeavePenaltyPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `overtimeBonusPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `faceSimilarityThreshold`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.upsertKpiTemplate` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Kompaniya mavjudligini tekshiradi va DTO dagi ma'lumotlar bilan `Setting` jadvaliga `ATTENDANCE_KPI_SETTING_KEY` kaliti ostida KPI shablonini yangilaydi yoki yaratadi (upsert).

**6. Response:**
- Qaytariladigan javob shakli (AttendanceKpiTemplateDto):
  - companyId: string
  - latePenaltyPerMinute: number
  - earlyLeavePenaltyPerMinute: number
  - overtimeBonusPerMinute: number
  - faceSimilarityThreshold: number

**7. Error case:**
- `ForbiddenException`: Agar foydalanuvchi ko'rsatilgan kompaniyaga huquqi bo'lmasa.
- `NotFoundException`: Agar kompaniya bazada topilmasa.

**8. DB struktura:**
Model: `Setting`, `Company` (ushbu endpoint shablonni Settings ga yozadi).
Model `Attendance` (modul asosi):
- (Yuqoridagi Endpoint 1dagi kabi majburiy qatorlar bu yerda ham amalda, barchasi yuqorida to'liq keltirilgan: id, companyId, date va h.k.)

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

---
### Endpoint: POST /api/v1/attendance/check-in
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:checkIn

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-in`
- Controller class + method nomi: `AttendanceController.checkIn`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `employeeId`: misol yo'q
- `terminalId`: misol yo'q
- `imageBase64`: misol yo'q
- `contentType`: 'image/jpeg'
- `eventTime`: '2026-06-08T09:05:00.000Z'
- `notes`: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckInDto` (`zdes_backend/src/modules/attendance/dto/attendance-check-in.dto.ts`)
- Maydonlar:
  - `employeeId`: string, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `imageBase64`: string, `@IsString()`, `@MinLength(10)`
  - `contentType`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
  - `eventTime`: string (optional), `@IsOptional()`, `@IsISO8601()`
  - `notes`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.checkIn` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Xodimni AWS yordamida yuz orqali verifikatsiya qiladi va tekshiradi. Shundan so'ng `Attendance` jadvaliga check-in vaqtini (yangi yozuv yaratish yoki update qilish orqali) qayd etadi, kechikish va qo'shimcha ishlashni hisoblab `SalaryAdjustment` yozuvlarini ham yaratadi (yoki eskilarini o'chirib qayta yozadi).

**6. Response:**
- Qaytariladigan javob shakli:
  - id: string
  - companyId: string
  - branchId: string | null
  - employeeId: string
  - terminalId: string | null
  - date: Date
  - checkIn: Date | null
  - checkOut: Date | null
  - status: AttendanceStatus
  - source: AttendanceSource
  - workStartTime: string | null
  - workEndTime: string | null
  - workedMinutes: number
  - lateMinutes: number
  - earlyLeaveMinutes: number
  - overtimeMinutes: number
  - checkInImageUrl: string | null
  - checkOutImageUrl: string | null
  - notes: string | null
  - faceSimilarity: number | undefined
  - appliedAdjustments: AttendanceAdjustmentDto[]
  - createdAt: Date
  - updatedAt: Date

**7. Error case:**
- `BadRequestException`: Yuz rasmi bo'sh bo'lsa yoki noto'g'ri sanali vaqt kelsa.
- `NotFoundException`: Xodim yoki Terminal topilmasa.
- `ConflictException`: Xodim rasmi bo'lmasa, Terminal noto'g'ri kompaniyaga tegishli bo'lmasa, yuz tekshiruvi yetarli similarity bermasa yoki shu sana uchun xodim allaqachon check-in qilgan bo'lsa.
- `ForbiddenException`: Xodim bloklangan bo'lsa.

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: POST /api/v1/attendance/check-out
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:checkOut

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-out`
- Controller class + method nomi: `AttendanceController.checkOut`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `employeeId`: misol yo'q
- `terminalId`: misol yo'q
- `imageBase64`: misol yo'q
- `contentType`: 'image/jpeg'
- `eventTime`: '2026-06-08T18:10:00.000Z'
- `notes`: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckOutDto` (`zdes_backend/src/modules/attendance/dto/attendance-check-out.dto.ts`)
- Maydonlar:
  - `employeeId`: string, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `imageBase64`: string, `@IsString()`, `@MinLength(10)`
  - `contentType`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
  - `eventTime`: string (optional), `@IsOptional()`, `@IsISO8601()`
  - `notes`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.checkOut` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Xodimni AWS orqali yuz orqali verifikatsiya qiladi va tekshiradi. Shundan so'ng bazadagi bugungi check-in yozuvini yangilab, `checkOut` vaqtini qo'shadi hamda KPI bo'yicha ishlagan vaqt/overtime larni hisoblab `SalaryAdjustment` qatorlarini sinxronizatsiya qiladi.

**6. Response:**
- Qaytariladigan javob shakli: Check-in bilan bir xil shaklda (id, date, status, checkIn, checkOut, workStartTime, lateMinutes va h.k. obyekti + faceSimilarity + appliedAdjustments massivi).

**7. Error case:**
- `BadRequestException`: Yuz rasmi bo'sh bo'lsa yoki noto'g'ri sana kelsa.
- `NotFoundException`: Xodim, Terminal topilmasa.
- `ConflictException`: Xodim rasmi bo'lmasa, check-in qilinmagan bo'lsa, allaqachon check-out qilingan bo'lsa yoki verifikatsiya darajasi past bo'lsa.
- `ForbiddenException`: Xodim bloklangan bo'lsa.

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: GET /api/v1/attendance
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance`
- Controller class + method nomi: `AttendanceController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceQueryDto` (`zdes_backend/src/modules/attendance/dto/attendance-query.dto.ts`) (Query parametrlar)
- Maydonlar:
  - `companyId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `branchId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `employeeId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `status`: AttendanceStatus (optional), `@IsOptional()`, `@IsEnum(AttendanceStatus)`
  - `dateFrom`: string (optional), `@IsOptional()`, `@IsISO8601({ strict: true })`
  - `dateTo`: string (optional), `@IsOptional()`, `@IsISO8601({ strict: true })`
  - `page`: number (optional), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
  - `limit`: number (optional), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.findAll` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Bajaruvchining huquqlari bo'yicha filial yoki kompaniya ma'lumotlari filtrlanadi. Query parametrlar bo'yicha paginatsiya asosida Attendance jadvallarini sanaga va yaratilgan vaqtiga ko'ra kamayish tartibida ro'yxatini qaytaradi. Har bir element uchun salary adjustments ham yuklanadi.

**6. Response:**
- Qaytariladigan javob shakli (Paginatsiya):
  - `items`: [Attendance javob obyekti massivi (id, checkIn, status, va boshqalar qatori appliedAdjustments)]
  - `total`: number
  - `page`: number
  - `limit`: number
  - `totalPages`: number

**7. Error case:**
- Asosan ruxsatlar bilan bog'liq bo'lishi mumkin (masalan, scope dan tashqaridagi companyId kiritilsa).

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar (Qidiruv ushbu indekslarga tayanadi):
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: GET /api/v1/attendance/:id
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/:id`
- Controller class + method nomi: `AttendanceController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Yo'q (faqat Param: `id` ParseUUIDPipe)

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.findOne` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Baza ichidan belgilangan id yordamida Attendance yozuvini oladi. Bajaruvchi uchun scope ni tekshiradi va adjustmentlar ro'yxatini yuklab obyekt qilib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Bitta obyekt sifatida.
  - id: string
  - companyId: string
  - branchId: string | null
  - employeeId: string
  - terminalId: string | null
  - date: Date
  - checkIn: Date | null
  - checkOut: Date | null
  - status: AttendanceStatus
  - source: AttendanceSource
  - workStartTime: string | null
  - workEndTime: string | null
  - workedMinutes: number
  - lateMinutes: number
  - earlyLeaveMinutes: number
  - overtimeMinutes: number
  - checkInImageUrl: string | null
  - checkOutImageUrl: string | null
  - notes: string | null
  - faceSimilarity: number | undefined
  - appliedAdjustments: AttendanceAdjustmentDto[]
  - createdAt: Date
  - updatedAt: Date

**7. Error case:**
- `NotFoundException`: Agar Attendance bazada topilmasa.
- `ForbiddenException`: Agar topilgan yozuv foydalanuvchining huquq doirasida bo'lmasa (`assertWithinScope` orqali).

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/raw-attendance-log.md`

### Endpoint: POST /api/v1/raw-attendance-logs
**Controller:** src/modules/raw-attendance-log/raw-attendance-log.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/raw-attendance-logs`
- Controller class + method nomi: `RawAttendanceLogController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: `50d3ee8c-6762-49dd-81de-546525d02c61`
- `terminalId`: `4ad303cb-8ed9-4f93-aa71-2c0e471152a6`
- `employeeId`: `uuid`
- `attendanceId`: `uuid`
- `deviceUserId`: `1001`
- `eventTime`: `2026-06-08T08:30:00.000Z`
- `eventType`: `check_in`
- `rawPayload`: `{ "source": "manual" }`
- `processed`: `false`
- `error`: `No matching employee`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `CreateRawAttendanceLogDto`
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `terminalId`: Tip - String, Validatorlar - `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `attendanceId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `deviceUserId`: Tip - String, Validatorlar - `@IsString()`, `@MaxLength(100)`
- `eventTime`: Tip - String, Validatorlar - `@IsDateString()`
- `eventType`: Tip - TerminalEventType, Validatorlar - `@IsOptional()`, `@IsEnum(TerminalEventType)`
- `rawPayload`: Tip - Object, Validatorlar - `@IsOptional()`, `@IsObject()`
- `processed`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@IsBoolean()`
- `error`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`

**5. Service:**
- Service method: `create`
- Tavsifi: `companyId`, `terminalId`, `employeeId` va `attendanceId` bazada mavjudligi va tegishliligi (so'rov yuborgan aktyorning scope doirasida) tekshiriladi va yangi xom davomat logini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `RawAttendanceLog` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "c76f6a72-4d2b-4e89-9a74-d890d9a74070",
    "companyId": "50d3ee8c-6762-49dd-81de-546525d02c61",
    "terminalId": "4ad303cb-8ed9-4f93-aa71-2c0e471152a6",
    "employeeId": null,
    "attendanceId": null,
    "deviceUserId": "1001",
    "eventTime": "2026-06-08T08:30:00.000Z",
    "eventType": "check_in",
    "rawPayload": {
      "source": "manual"
    },
    "processed": false,
    "error": null,
    "createdAt": "2026-08-22T17:15:20.924Z",
    "updatedAt": "2026-08-22T17:15:20.924Z"
  },
  "path": "/api/v1/raw-attendance-logs",
  "timestamp": "2026-08-22T17:15:20.924Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Company not found', 'Terminal not found', 'Employee not found', 'Attendance not found'
- `ConflictException`: 'Terminal does not belong to the selected company', 'Employee does not belong to the selected company', 'Attendance does not belong to the selected company', 'Device user id is required'
- `ForbiddenException`: 'Actor is not assigned to a company', 'You do not have access to this resource'

**8. DB struktura:**
- Prisma modeli: `RawAttendanceLog`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `terminalId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `attendanceId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `deviceUserId`: `String`, majburiy, `@db.VarChar(100)`
  - `eventTime`: `DateTime`, majburiy, `@db.Timestamptz(6)`
  - `eventType`: `TerminalEventType`, majburiy, `@default(unknown)`
  - `rawPayload`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `processed`: `Boolean`, majburiy, `@default(false)`
  - `error`: `String`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `attendanceId -> Attendance.id`
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id`
  - `terminalId -> Terminal.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@unique([terminalId, eventTime, deviceUserId, eventType])`
  - `@@index([companyId])`
  - `@@index([terminalId])`
  - `@@index([employeeId])`
  - `@@index([attendanceId])`
  - `@@index([eventTime])`
  - `@@index([processed])`

**cURL misol:**
```bash
curl -X POST "http://localhost:4000/api/v1/raw-attendance-logs" \
-H "Authorization: Bearer eyJhbGci..." \
-H "Content-Type: application/json" \
-d '{
  "terminalId": "4ad303cb-8ed9-4f93-aa71-2c0e471152a6",
  "deviceUserId": "1001",
  "eventTime": "2026-06-08T08:30:00.000Z",
  "eventType": "check_in"
}'
```

---

### Endpoint: GET /api/v1/raw-attendance-logs
**Controller:** src/modules/raw-attendance-log/raw-attendance-log.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/raw-attendance-logs`
- Controller class + method nomi: `RawAttendanceLogController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. (Query parametrlar orqali ishlash).
- Query parametr misollari:
  - `companyId`: `uuid`
  - `terminalId`: `uuid`
  - `employeeId`: `uuid`
  - `attendanceId`: `uuid`
  - `eventType`: `check_in`
  - `processed`: `false`
  - `deviceUserId`: `1001`
  - `eventFrom`: `2026-06-08`
  - `eventTo`: `2026-06-10`
  - `page`: `1`
  - `limit`: `10`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `RawAttendanceLogQueryDto`
- Barcha qidiruv parametrlari va paginatsiya qiymatlari (`page`, `limit`).

**5. Service:**
- Service method: `findAll`
- Tavsifi: Berilgan parametrlar yordamida qidiruv qilinadi, admin/manager faqat o'z filiali/kompaniyasi loglarini ko'ra oladi (`resolveCompanyBranchScope`).

**6. Response:**
- Paginatsiya shaklidagi obyekt:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "c76f6a72-4d2b-4e89-9a74-d890d9a74070",
        "companyId": "50d3ee8c-6762-49dd-81de-546525d02c61",
        "terminalId": "4ad303cb-8ed9-4f93-aa71-2c0e471152a6",
        "employeeId": null,
        "attendanceId": null,
        "deviceUserId": "1001",
        "eventTime": "2026-06-08T08:30:00.000Z",
        "eventType": "check_in",
        "rawPayload": {
          "source": "manual"
        },
        "processed": false,
        "error": null,
        "createdAt": "2026-08-22T17:15:20.924Z",
        "updatedAt": "2026-08-22T17:15:20.924Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/raw-attendance-logs?limit=10",
  "timestamp": "2026-08-22T17:15:20.924Z"
}
```

**7. Error case:**
- `ForbiddenException`: 'Actor is not assigned to a company', 'You do not have access to this resource'

**8. DB struktura:**
- Prisma modeli: `RawAttendanceLog` (ustun va indekslari yuqoridagidek).

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/raw-attendance-logs?limit=10&page=1" \
-H "Authorization: Bearer eyJhbGci..."
```

---

### Endpoint: GET /api/v1/raw-attendance-logs/:id
**Controller:** src/modules/raw-attendance-log/raw-attendance-log.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/raw-attendance-logs/:id`
- Controller class + method nomi: `RawAttendanceLogController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Param `id`).

**5. Service:**
- Service method: `findOne`
- Tavsifi: ID bo'yicha bazadan log olinadi va ruxsatlar tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c76f6a72-4d2b-4e89-9a74-d890d9a74070",
    "companyId": "50d3ee8c-6762-49dd-81de-546525d02c61",
    "terminalId": "4ad303cb-8ed9-4f93-aa71-2c0e471152a6",
    "employeeId": null,
    "attendanceId": null,
    "deviceUserId": "1001",
    "eventTime": "2026-06-08T08:30:00.000Z",
    "eventType": "check_in",
    "rawPayload": {
      "source": "manual"
    },
    "processed": false,
    "error": null,
    "createdAt": "2026-08-22T17:15:20.924Z",
    "updatedAt": "2026-08-22T17:15:20.924Z"
  },
  "path": "/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070",
  "timestamp": "2026-08-22T17:15:20.924Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Raw attendance log not found'

**8. DB struktura:**
- Prisma modeli: `RawAttendanceLog`

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070" \
-H "Authorization: Bearer eyJhbGci..."
```

---

### Endpoint: PATCH /api/v1/raw-attendance-logs/:id
**Controller:** src/modules/raw-attendance-log/raw-attendance-log.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/raw-attendance-logs/:id`
- Controller class + method nomi: `RawAttendanceLogController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `processed`: `true`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateRawAttendanceLogDto` (CreateRawAttendanceLogDto'dan Partial)

**5. Service:**
- Service method: `update`
- Tavsifi: Baza tekshiruvlari va scope ruxsatlari ta'minlanib log yozuvi yangilanadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c76f6a72-4d2b-4e89-9a74-d890d9a74070",
    "companyId": "50d3ee8c-6762-49dd-81de-546525d02c61",
    "terminalId": "4ad303cb-8ed9-4f93-aa71-2c0e471152a6",
    "employeeId": null,
    "attendanceId": null,
    "deviceUserId": "1001",
    "eventTime": "2026-06-08T08:30:00.000Z",
    "eventType": "check_in",
    "rawPayload": {
      "source": "manual"
    },
    "processed": true,
    "error": null,
    "createdAt": "2026-08-22T17:15:20.924Z",
    "updatedAt": "2026-08-22T17:15:20.924Z"
  },
  "path": "/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070",
  "timestamp": "2026-08-22T17:15:20.924Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Raw attendance log not found'
- Validatsiya va moslik xatoliklari.

**8. DB struktura:**
- Prisma modeli: `RawAttendanceLog`

**cURL misol:**
```bash
curl -X PATCH "http://localhost:4000/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070" \
-H "Authorization: Bearer eyJhbGci..." \
-H "Content-Type: application/json" \
-d '{
  "processed": true
}'
```

---

### Endpoint: DELETE /api/v1/raw-attendance-logs/:id
**Controller:** src/modules/raw-attendance-log/raw-attendance-log.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/raw-attendance-logs/:id`
- Controller class + method nomi: `RawAttendanceLogController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO yo'q.

**5. Service:**
- Service method: `delete`
- Tavsifi: Keltirilgan ID yordamida log topiladi, ruxsat tekshiriladi va o'chiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c76f6a72-4d2b-4e89-9a74-d890d9a74070"
  },
  "path": "/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070",
  "timestamp": "2026-08-22T17:15:20.924Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Raw attendance log not found'

**8. DB struktura:**
- Prisma modeli: `RawAttendanceLog`

**cURL misol:**
```bash
curl -X DELETE "http://localhost:4000/api/v1/raw-attendance-logs/c76f6a72-4d2b-4e89-9a74-d890d9a74070" \
-H "Authorization: Bearer eyJhbGci..."
```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/company.md`

# Company Moduli API Hujjatlari

Kompaniya ma'lumotlarini boshqarish uchun `Company` modulidagi barcha endpointlar. Barcha so'rovlar uchun avtorizatsiya va `superadmin` roli talab qilinadi.

Asosiy URL: `http://localhost:4000/api/v1`

---

### Endpoint: POST /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/companies`
- Controller class + method nomi: `CompanyController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "name": "ZDES",
  "legalName": "ZDES LLC",
  "phone": "+998901234567",
  "email": "info@zdes.uz",
  "address": "Tashkent city, Yunusobod district",
  "timezone": "Asia/Tashkent"
}
```

**3. Guard:**
- `@Roles('superadmin')` (Controller yoki Method darajasida)
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `CreateCompanyDto`
- `name`: String, Majburiy. Min uzunlik 1, Max uzunlik 255.
- `legalName`: String, Ixtiyoriy. Max uzunlik 255.
- `phone`: String, Ixtiyoriy. Max uzunlik 50.
- `email`: Email, Ixtiyoriy. Max uzunlik 255.
- `address`: String, Ixtiyoriy. Max uzunlik 500.
- `timezone`: IANA Timezone string, Ixtiyoriy. Standart: "Asia/Tashkent".

**5. Service:**
- Service method: `create`
- Tavsifi: Yuborilgan ism (`name`) bo'sh emasligiga va bazada takrorlanmasligiga ishonch hosil qiladi. Ma'lumotlarni tozalaydi va yangi kompaniya yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Company` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "11111111-2222-3333-4444-555555555555",
    "name": "ZDES",
    "legalName": "ZDES LLC",
    "phone": "+998901234567",
    "email": "info@zdes.uz",
    "address": "Tashkent city, Yunusobod district",
    "logoUrl": null,
    "timezone": "Asia/Tashkent",
    "isActive": true,
    "stoppedAt": null,
    "createdAt": "2026-08-22T16:32:05.000Z",
    "updatedAt": "2026-08-22T16:32:05.000Z"
  },
  "path": "/api/v1/companies",
  "timestamp": "2026-08-22T16:32:05.123Z"
}
```

**7. Error case:**
- `401 Unauthorized`: Noto'g'ri yoki muddati o'tgan token.
- `403 Forbidden`: Foydalanuvchi "superadmin" emas.
- `409 ConflictException`: "Company name already exists" yoki "Company name is required".
- `400 Bad Request`: Validatsiyadan o'ta olmasa.

**8. DB struktura:**
- Prisma modeli: `Company` (prisma/schema.prisma)
- Ustun ta'riflari: `id` (UUID), `name` (String, unique), `legalName`, `phone`, `email`, `address`, `logoUrl`, `timezone`, `isActive` (Boolean), `stoppedAt` (DateTime), `createdAt`, `updatedAt`.
- Relations: `users`, `branches`, `departments`, `positions`, `workSchedules`, `workScheduleLinks`, `terminals`, `holidays`, `employeeLeaves`, `attendances`, `rawAttendanceLogs`, `salaryAdjustments`, `advances`, `payrolls`, `settings`.

**cURL misoli:**
```bash
curl -X POST http://localhost:4000/api/v1/companies \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ZDES",
    "legalName": "ZDES LLC",
    "phone": "+998901234567",
    "email": "info@zdes.uz",
    "address": "Tashkent city",
    "timezone": "Asia/Tashkent"
  }'
```

---

### Endpoint: GET /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/companies`
- Controller class + method nomi: `CompanyController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Query parametr misollari:
  - `page`: `1`
  - `limit`: `10`
  - `search`: `zdes`
  - `isActive`: `true`

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `CompanyQueryDto`
- `search`: String, Ixtiyoriy. Qidiruv so'zi.
- `isActive`: Boolean, Ixtiyoriy.
- `page`: Integer (Min: 1), Ixtiyoriy. Standart: 1.
- `limit`: Integer (Min: 1, Max: 100), Ixtiyoriy. Standart: 10.

**5. Service:**
- Service method: `findAll`
- Tavsifi: Paginatsiya va qidiruv orqali barcha kompaniyalarni bazadan olib keladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "11111111-2222-3333-4444-555555555555",
        "name": "ZDES",
        "legalName": "ZDES LLC",
        "phone": "+998901234567",
        "email": "info@zdes.uz",
        "address": "Tashkent city",
        "logoUrl": null,
        "timezone": "Asia/Tashkent",
        "isActive": true,
        "stoppedAt": null,
        "createdAt": "2026-08-22T16:32:05.000Z",
        "updatedAt": "2026-08-22T16:32:05.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/companies?page=1&limit=10&search=zdes",
  "timestamp": "2026-08-22T16:35:05.123Z"
}
```

**7. Error case:**
- `401 Unauthorized`
- `403 Forbidden`
- `400 Bad Request`

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X GET "http://localhost:4000/api/v1/companies?page=1&limit=10&search=zdes" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/companies/:id`
- Controller class + method nomi: `CompanyController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` ParseUUIDPipe bilan tekshiriladi).

**5. Service:**
- Service method: `findOne`
- Tavsifi: Berilgan ID yordamida bitta kompaniya yozuvini oladi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Company` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "11111111-2222-3333-4444-555555555555",
    "name": "ZDES",
    "legalName": "ZDES LLC",
    "phone": "+998901234567",
    "email": "info@zdes.uz",
    "address": "Tashkent",
    "logoUrl": null,
    "timezone": "Asia/Tashkent",
    "isActive": true,
    "stoppedAt": null,
    "createdAt": "2026-08-22T16:32:05.000Z",
    "updatedAt": "2026-08-22T16:32:05.000Z"
  },
  "path": "/api/v1/companies/11111111-2222-3333-4444-555555555555",
  "timestamp": "2026-08-22T16:38:05.123Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found"
- `400 Bad Request`: Validation failed (uuid is expected)

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X GET "http://localhost:4000/api/v1/companies/11111111-2222-3333-4444-555555555555" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/companies/:id`
- Controller class + method nomi: `CompanyController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "name": "ZDES New",
  "timezone": "Asia/Samarkand"
}
```

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `UpdateCompanyDto` (Barcha maydonlar ixtiyoriy).

**5. Service:**
- Service method: `update`
- Tavsifi: Mavjud kompaniyani topib tekshiradi va uzatilgan yangi ma'lumotlar bilan bazada yangilaydi.

**6. Response:**
- Yangilangan Prisma `Company` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "11111111-2222-3333-4444-555555555555",
    "name": "ZDES New",
    "legalName": "ZDES LLC",
    "phone": "+998901234567",
    "email": "info@zdes.uz",
    "address": "Tashkent",
    "logoUrl": null,
    "timezone": "Asia/Samarkand",
    "isActive": true,
    "stoppedAt": null,
    "createdAt": "2026-08-22T16:32:05.000Z",
    "updatedAt": "2026-08-22T16:40:00.000Z"
  },
  "path": "/api/v1/companies/11111111-2222-3333-4444-555555555555",
  "timestamp": "2026-08-22T16:40:05.123Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found"
- `409 ConflictException`: "Company name already exists"

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X PATCH "http://localhost:4000/api/v1/companies/11111111-2222-3333-4444-555555555555" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "ZDES New"}'
```

---

### Endpoint: POST /api/v1/companies/:id/logo
**Controller:** src/modules/company/company.controller.ts:uploadLogo

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/companies/:id/logo`
- Controller class + method nomi: `CompanyController` -> `uploadLogo`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `multipart/form-data` ko'rinishida `file` kaliti ostida rasm fayli.

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- `file`: `Express.Multer.File`

**5. Service:**
- Service method: `uploadLogo` (yoki fayl yuklash xizmati)
- Tavsifi: Faylni rasmligini tasdiqlab, saqlaydi va kompaniya `logoUrl` maydonini yangilaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "11111111-2222-3333-4444-555555555555",
    "name": "ZDES New",
    "logoUrl": "https://api.yourdomain.com/uploads/logos/xyz-123.jpg",
    "isActive": true,
    "createdAt": "2026-08-22T16:32:05.000Z",
    "updatedAt": "2026-08-22T16:42:00.000Z"
  },
  "path": "/api/v1/companies/11111111-2222-3333-4444-555555555555/logo",
  "timestamp": "2026-08-22T16:42:05.123Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found"
- `400 Bad Request`: Rasm formati xato yoki fayl yo'q.

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X POST "http://localhost:4000/api/v1/companies/11111111-2222-3333-4444-555555555555/logo" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/logo.png"
```

---

### Endpoint: PATCH /api/v1/companies/:id/toggle-status
**Controller:** src/modules/company/company.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/companies/:id/toggle-status`
- Controller class + method nomi: `CompanyController` -> `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "isActive": false
}
```

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `ToggleCompanyStatusDto` (Ixtiyoriy `isActive` boolean maydoni).

**5. Service:**
- Service method: `toggleStatus`
- Tavsifi: Kompaniya holatini almashtiradi (aktiv yoki nofaol). Agar nofaol bo'lsa `stoppedAt` yoziladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "11111111-2222-3333-4444-555555555555",
    "name": "ZDES",
    "isActive": false,
    "stoppedAt": "2026-08-22T16:45:00.000Z",
    "createdAt": "2026-08-22T16:32:05.000Z",
    "updatedAt": "2026-08-22T16:45:00.000Z"
  },
  "path": "/api/v1/companies/11111111-2222-3333-4444-555555555555/toggle-status",
  "timestamp": "2026-08-22T16:45:05.123Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found"

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X PATCH "http://localhost:4000/api/v1/companies/11111111-2222-3333-4444-555555555555/toggle-status" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"isActive": false}'
```

---

### Endpoint: DELETE /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/companies/:id`
- Controller class + method nomi: `CompanyController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO qo'llanilmagan (`@Param('id', ParseUUIDPipe)`).

**5. Service:**
- Service method: `delete`
- Tavsifi: Kompaniyani bazadan o'chiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "11111111-2222-3333-4444-555555555555"
  },
  "path": "/api/v1/companies/11111111-2222-3333-4444-555555555555",
  "timestamp": "2026-08-22T16:48:05.123Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found"

**8. DB struktura:**
- Prisma modeli: `Company` (Xuddi POST bilan bir xil).

**cURL misoli:**
```bash
curl -X DELETE "http://localhost:4000/api/v1/companies/11111111-2222-3333-4444-555555555555" \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/payroll.md`

### Endpoint: POST /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/payrolls`
- Controller class + method nomi: `PayrollController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: `123e4567-e89b-12d3-a456-426614174000` (Ixtiyoriy)
- `employeeId`: `987e6543-e21b-12d3-a456-426614174000`
- `month`: `2026-06`
- `baseSalary`: `4000000`
- `totalBonus`: `500000`
- `totalPenalty`: `100000`
- `totalAdvance`: `200000`
- `netSalary`: `4200000`
- `status`: `draft`
- `paidAt`: `2026-06-30T10:00:00.000Z`
- `paidById`: `111e2222-e89b-12d3-a456-426614174000`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `CreatePayrollDto` (src/modules/payroll/dto/create-payroll.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsUUID()`
- `month`: Tip - String, Validatorlar - `@IsString()`
- `baseSalary`: Tip - Number, Validatorlar - `@IsOptional()`, `@IsNumber()`
- `totalBonus`: Tip - Number, Validatorlar - `@IsOptional()`, `@IsNumber()`
- `totalPenalty`: Tip - Number, Validatorlar - `@IsOptional()`, `@IsNumber()`
- `totalAdvance`: Tip - Number, Validatorlar - `@IsOptional()`, `@IsNumber()`
- `netSalary`: Tip - Number, Validatorlar - `@IsOptional()`, `@IsNumber()`
- `status`: Tip - PayrollStatus (enum), Validatorlar - `@IsOptional()`, `@IsEnum(PayrollStatus)`
- `paidAt`: Tip - String, Validatorlar - `@IsOptional()`, `@IsDateString()`
- `paidById`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`

**5. Service:**
- Service method: `create` (src/modules/payroll/payroll.service.ts)
- Tavsifi: Xodim (`employeeId`) va kompaniya mavjudligi/ruxsat (scope) tekshiriladi. Bitta xodim uchun bir xil oyga (`month`) ikkita Payroll yaratilmasligini nazorat qiladi. Yangi Payroll yozuvini Prisma orqali DB ga yozadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Payroll` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
    "companyId": "123e4567-e89b-12d3-a456-426614174000",
    "employeeId": "987e6543-e21b-12d3-a456-426614174000",
    "month": "2026-06",
    "baseSalary": "4000000",
    "totalBonus": "500000",
    "totalPenalty": "100000",
    "totalAdvance": "200000",
    "netSalary": "4200000",
    "status": "draft",
    "paidAt": "2026-06-30T10:00:00.000Z",
    "paidById": "111e2222-e89b-12d3-a456-426614174000",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:00:00.000Z"
  },
  "path": "/api/v1/payrolls",
  "timestamp": "2026-08-22T17:01:00.000Z"
}
```

*cURL Misol:*
```bash
curl -X POST http://localhost:4000/api/v1/payrolls \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "employeeId": "987e6543-e21b-12d3-a456-426614174000",
  "month": "2026-06",
  "baseSalary": 4000000
}'
```

**7. Error case:**
- `NotFoundException`: 'Company not found', 'Employee not found', 'Paid by user not found'.
- `ConflictException`: 'Payroll month is required', 'Employee does not belong to the selected company', 'Payroll already exists for this employee and month'.

**8. DB struktura:**
- Prisma modeli: `Payroll` (prisma/schema.prisma)
- Ustun ta'riflari: id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt
- Relations (Chiquvchi): `Company`, `User` (employee va paidBy) jadvallari bilan relation o'rnatilgan.
- Indekslar: `@@unique([employeeId, month])` indeksi mavjud.

---

### Endpoint: GET /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/payrolls`
- Controller class + method nomi: `PayrollController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.
- Query parametr misollari:
  - `page`: `1`
  - `limit`: `10`
  - `companyId`: `123e4567-e89b-12d3-a456-426614174000`
  - `employeeId`: `987e6543-e21b-12d3-a456-426614174000`
  - `month`: `2026-06`
  - `status`: `draft`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `PayrollQueryDto` (src/modules/payroll/dto/payroll-query.dto.ts)

**5. Service:**
- Service method: `findAll` (src/modules/payroll/payroll.service.ts)
- Tavsifi: Query parametrlari asosida scope bo'yicha filterlarni tuzadi. Pagination bilan ro'yxatni `month` DESC va `createdAt` DESC tartibida qaytaradi.

**6. Response:**
- Paginatsiya shaklidagi obyekt.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
        "companyId": "123e4567-e89b-12d3-a456-426614174000",
        "employeeId": "987e6543-e21b-12d3-a456-426614174000",
        "month": "2026-06",
        "baseSalary": "4000000",
        "totalBonus": "0",
        "totalPenalty": "0",
        "totalAdvance": "0",
        "netSalary": "4000000",
        "status": "draft",
        "paidAt": null,
        "paidById": null,
        "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
        "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
        "createdAt": "2026-08-22T17:00:00.000Z",
        "updatedAt": "2026-08-22T17:00:00.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/payrolls?page=1&limit=10&month=2026-06",
  "timestamp": "2026-08-22T17:01:00.000Z"
}
```

*cURL Misol:*
```bash
curl -X GET "http://localhost:4000/api/v1/payrolls?page=1&limit=10&month=2026-06" \
-H "Authorization: Bearer <TOKEN>"
```

**7. Error case:**
- Invalid query parametrlari uchun format xatoliklari.

**8. DB struktura:**
- Prisma modeli: `Payroll` (prisma/schema.prisma)

---

### Endpoint: GET /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/payrolls/:id`
- Controller class + method nomi: `PayrollController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (ID uchun `ParseUUIDPipe`).

**5. Service:**
- Service method: `findOne` (src/modules/payroll/payroll.service.ts)
- Tavsifi: ID orqali DB dan qidiradi. Actor ning tegishli dataga ruxsati bor-yo'qligini tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Payroll` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
    "companyId": "123e4567-e89b-12d3-a456-426614174000",
    "employeeId": "987e6543-e21b-12d3-a456-426614174000",
    "month": "2026-06",
    "baseSalary": "4000000",
    "totalBonus": "500000",
    "totalPenalty": "100000",
    "totalAdvance": "200000",
    "netSalary": "4200000",
    "status": "draft",
    "paidAt": "2026-06-30T10:00:00.000Z",
    "paidById": "111e2222-e89b-12d3-a456-426614174000",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:00:00.000Z"
  },
  "path": "/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
  "timestamp": "2026-08-22T17:01:00.000Z"
}
```

*cURL Misol:*
```bash
curl -X GET "http://localhost:4000/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a" \
-H "Authorization: Bearer <TOKEN>"
```

**7. Error case:**
- `NotFoundException`: 'Payroll not found'
- Ruxsatsiz datani so'raganda exception.

**8. DB struktura:**
- Prisma modeli: `Payroll` (prisma/schema.prisma)

---

### Endpoint: PATCH /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/payrolls/:id`
- Controller class + method nomi: `PayrollController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `status`: `paid`
- `netSalary`: `4300000`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdatePayrollDto` (Partial form of CreatePayrollDto)

**5. Service:**
- Service method: `update` (src/modules/payroll/payroll.service.ts)
- Tavsifi: Mavjud yozuvni tortib, ruxtsatni tekshiradi. Yangi qiymatlarni DB ga saqlaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `Payroll` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
    "companyId": "123e4567-e89b-12d3-a456-426614174000",
    "employeeId": "987e6543-e21b-12d3-a456-426614174000",
    "month": "2026-06",
    "baseSalary": "4000000",
    "totalBonus": "500000",
    "totalPenalty": "100000",
    "totalAdvance": "200000",
    "netSalary": "4300000",
    "status": "paid",
    "paidAt": "2026-06-30T10:00:00.000Z",
    "paidById": "111e2222-e89b-12d3-a456-426614174000",
    "createdById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "updatedById": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:15:00.000Z"
  },
  "path": "/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
  "timestamp": "2026-08-22T17:05:00.000Z"
}
```

*cURL Misol:*
```bash
curl -X PATCH http://localhost:4000/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "status": "paid",
  "netSalary": 4300000
}'
```

**7. Error case:**
- `NotFoundException`: Yozuv, company, employee topilmasa.
- `ConflictException`: "Payroll already exists for this employee and month" (agar oy o'zgarsa).

**8. DB struktura:**
- Prisma modeli: `Payroll` (prisma/schema.prisma)

---

### Endpoint: DELETE /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/payrolls/:id`
- Controller class + method nomi: `PayrollController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (ID uchun `ParseUUIDPipe`).

**5. Service:**
- Service method: `delete` (src/modules/payroll/payroll.service.ts)
- Tavsifi: ID bo'yicha bazada mavjudligi va ruxsat tekshiriladi. Prisma orqali o'chiradi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: boolean, data: { id: string } }`
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c33f4a20-b49b-4b1f-9988-c7e1694f4c9a"
  },
  "path": "/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a",
  "timestamp": "2026-08-22T17:06:00.000Z"
}
```

*cURL Misol:*
```bash
curl -X DELETE http://localhost:4000/api/v1/payrolls/c33f4a20-b49b-4b1f-9988-c7e1694f4c9a \
-H "Authorization: Bearer <TOKEN>"
```

**7. Error case:**
- `NotFoundException`: 'Payroll not found' (topilmasa).

**8. DB struktura:**
- Prisma modeli: `Payroll` (prisma/schema.prisma)


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/department.md`

### Endpoint: POST /api/v1/departments
**Controller:** src/modules/department/department.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/departments`
- Controller class + method nomi: `DepartmentController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `IT Department`
- `companyId`: `087c324a-06c2-4a48-91f8-f65d653fbf27` (superadmin uchun majburiy)
- `branchId`: null

cURL misoli:
```bash
curl -X POST http://localhost:4000/api/v1/departments \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "IT Department",
        "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27"
      }'
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `CreateDepartmentDto`
- `name`: Tip - String, Validatorlar - min=1, max=255, majburiy.
- `companyId`: Tip - String, Validatorlar - UUID, ixtiyoriy (superadmin uchun kerak).
- `branchId`: Tip - String, Validatorlar - UUID, null bo'lishi mumkin, ixtiyoriy.

**5. Service:**
- Service method: `create`
- Tavsifi: `companyId` mavjudligini tekshiradi (agar kiritilmagan bo'lsa `actor` orqali topadi), `branchId` tanlangan kompaniyaga tegishli ekanligini tasdiqlaydi. Nom `company` va `branch` ichida takrorlanmas (unique) bo'lishi shart.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `Department` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
    "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27",
    "branchId": null,
    "name": "IT Department",
    "isActive": true,
    "createdAt": "2026-08-22T16:37:07.167Z",
    "updatedAt": "2026-08-22T16:37:07.167Z"
  },
  "path": "/api/v1/departments",
  "timestamp": "2026-08-22T16:37:07.176Z"
}
```

**7. Error case:**
- `401 Unauthorized`: Noto'g'ri yoki muddati tugagan JWT token yuborilsa.
- `403 Forbidden`: Agar admin/manager roldagi foydalanuvchi boshqa kompaniya yoki filial ma'lumotlariga aralashmoqchi bo'lsa.
- `404 NotFoundException`: Kompaniya yoki filial topilmasa.
- `409 ConflictException`: `Department name already exists for this company and branch` - nom takrorlansa, `Branch does not belong to the selected company` - tanlangan filial boshqa kompaniyaga tegishli bo'lsa, `Department name is required` - nom kiritilmasa.
- `400 Bad Request`: DTO validatsiyadan o'tmasa.

**8. DB struktura:**
- Prisma modeli: `Department` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
- Relations (Kiruvchi): `users` (User[]), `positions` (Position[])
- Indekslar: 
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/departments
**Controller:** src/modules/department/department.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments`
- Controller class + method nomi: `DepartmentController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q
- Query parametrlar:
  - `page`: `1`
  - `limit`: `10`
  - `search`: `IT`
  - `isActive`: `true`
  - `companyId`: `087c324a-06c2-4a48-91f8-f65d653fbf27`
  - `branchId`: misol yo'q

cURL misoli:
```bash
curl -X GET "http://localhost:4000/api/v1/departments?limit=10&page=1" \
  -H "Authorization: Bearer <TOKEN>"
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `DepartmentQueryDto`
- `page`: Tip - Number (default 1)
- `limit`: Tip - Number (default 10)
- `search`: Tip - String
- `companyId`: Tip - String, Validatorlar - UUID, ixtiyoriy.
- `branchId`: Tip - String, Validatorlar - UUID, ixtiyoriy.
- `isActive`: Tip - Boolean, ixtiyoriy.

**5. Service:**
- Service method: `findAll`
- Tavsifi: Foydalanuvchining roli doirasida ruxsat berilgan `companyId` va `branchId` orqali barcha bo'limlarni sahifalab va qidiruv bo'yicha filterlab qaytaradi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
        "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27",
        "branchId": null,
        "name": "IT Department",
        "isActive": true,
        "createdAt": "2026-08-22T16:37:07.167Z",
        "updatedAt": "2026-08-22T16:37:07.167Z"
      }
    ],
    "total": 17,
    "page": 1,
    "limit": 10,
    "totalPages": 2
  },
  "path": "/api/v1/departments?limit=10&page=1&companyId=087c324a-06c2-4a48-91f8-f65d653fbf27",
  "timestamp": "2026-08-22T16:37:07.216Z"
}
```

**7. Error case:**
- Bazaviy exception'lar bo'lishi mumkin. Noto'g'ri token uchun 401.

**8. DB struktura:**
- Xuddi yuqoridagi kabi (POST bo'limiga qarang).

---

### Endpoint: GET /api/v1/departments/:id
**Controller:** src/modules/department/department.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

cURL misoli:
```bash
curl -X GET "http://localhost:4000/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd" \
  -H "Authorization: Bearer <TOKEN>"
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO yo'q, faqat parametr `:id`.

**5. Service:**
- Service method: `findOne`
- Tavsifi: `id` bo'yicha topadi va `actor` doirasida kirishga ruxsat borligini tekshiradi (`assertWithinScope`).

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
    "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27",
    "branchId": null,
    "name": "IT Department",
    "isActive": true,
    "createdAt": "2026-08-22T16:37:07.167Z",
    "updatedAt": "2026-08-22T16:37:07.167Z"
  },
  "path": "/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
  "timestamp": "2026-08-22T16:37:07.246Z"
}
```

**7. Error case:**
- `404 NotFoundException`: Berilgan `id` bilan `Department` topilmasa.
- `403 Forbidden`: Ruxsat doirasidan tashqari bo'lsa.

**8. DB struktura:**
- Xuddi yuqoridagi kabi.

---

### Endpoint: PATCH /api/v1/departments/:id
**Controller:** src/modules/department/department.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `Software Engineering`

cURL misoli:
```bash
curl -X PATCH http://localhost:4000/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Software Engineering"
      }'
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateDepartmentDto` (Partial form of CreateDepartmentDto).

**5. Service:**
- Service method: `update`
- Tavsifi: Mavjud bo'limni tekshiradi, ruxsat doirasini tekshiradi. Yangi nomning takrorlanmasligini va filial tegishliligini ta'minlaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
    "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27",
    "branchId": null,
    "name": "Software Engineering",
    "isActive": true,
    "createdAt": "2026-08-22T16:37:07.167Z",
    "updatedAt": "2026-08-22T16:37:07.270Z"
  },
  "path": "/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
  "timestamp": "2026-08-22T16:37:07.274Z"
}
```

**7. Error case:**
- `404 NotFoundException`: Bo'lim topilmasa.
- `409 ConflictException`: Nom takrorlansa yoki boshqa konflikt.
- `403 Forbidden`: Ruxsat yetarli bo'lmasa.

**8. DB struktura:**
- Xuddi yuqoridagi kabi.

---

### Endpoint: PATCH /api/v1/departments/:id/toggle-status
**Controller:** src/modules/department/department.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id/toggle-status`
- Controller class + method nomi: `DepartmentController` -> `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `isActive`: `false`

cURL misoli:
```bash
curl -X PATCH http://localhost:4000/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd/toggle-status \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "isActive": false
      }'
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `ToggleDepartmentStatusDto`
- `isActive`: Tip - Boolean, ixtiyoriy (berilmasa qiymatni teskarisiga o'zgartiradi).

**5. Service:**
- Service method: `toggleStatus`
- Tavsifi: Status maydonini o'zgartiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
    "companyId": "087c324a-06c2-4a48-91f8-f65d653fbf27",
    "branchId": null,
    "name": "Software Engineering",
    "isActive": false,
    "createdAt": "2026-08-22T16:37:07.167Z",
    "updatedAt": "2026-08-22T16:37:07.308Z"
  },
  "path": "/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd/toggle-status",
  "timestamp": "2026-08-22T16:37:07.312Z"
}
```

**7. Error case:**
- `404 NotFoundException`: Bo'lim topilmasa.
- `403 Forbidden`: Ruxsat yetarli bo'lmasa.

**8. DB struktura:**
- Xuddi yuqoridagi kabi.

---

### Endpoint: DELETE /api/v1/departments/:id
**Controller:** src/modules/department/department.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

cURL misoli:
```bash
curl -X DELETE "http://localhost:4000/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd" \
  -H "Authorization: Bearer <TOKEN>"
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO yo'q.

**5. Service:**
- Service method: `delete`
- Tavsifi: Bo'limni `id` bo'yicha topadi, ruxsatni tekshirib DB dan o'chiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd"
  },
  "path": "/api/v1/departments/af48b4fc-14ac-409c-9e4a-c71e1e9bc5cd",
  "timestamp": "2026-08-22T16:37:07.358Z"
}
```

**7. Error case:**
- `404 NotFoundException`: Bo'lim topilmasa.
- `403 Forbidden`: Ruxsat yetarli bo'lmasa.

**8. DB struktura:**
- Xuddi yuqoridagi kabi.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/branch.md`

### Endpoint: POST /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/branches`
- Controller class + method nomi: `BranchController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "name": "Test Branch API",
  "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
  "address": "Some test address",
  "latitude": 40.3842,
  "longitude": 71.7843,
  "radius": 50
}
```

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: `CreateBranchDto`
- `name`: Tip - String, Validatorlar - min:1, max:255, required
- `companyId`: Tip - String (UUID), ixtiyoriy (admin uchun avtomatik to'ldiriladi)
- `address`: Tip - String, ixtiyoriy, max:500
- `latitude`: Tip - Number, ixtiyoriy, valid latitude
- `longitude`: Tip - Number, ixtiyoriy, valid longitude
- `radius`: Tip - Number, ixtiyoriy, min:1, default 100

**5. Service:**
- Service method: `create`
- Tavsifi: Kiritilgan `companyId` mavjudligi tekshiriladi. Filial noyobligi tekshiriladi va DB ga saqlanadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "ca3e0228-a82c-4709-b4bc-606df56283eb",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "name": "Test Branch API",
    "address": "Some test address",
    "latitude": null,
    "longitude": null,
    "radius": 50,
    "isActive": true,
    "createdAt": "2026-08-22T16:35:10.812Z",
    "updatedAt": "2026-08-22T16:35:10.812Z"
  },
  "path": "/api/v1/branches",
  "timestamp": "2026-08-22T16:35:10.817Z"
}
```

**7. Error case:**
- `401 Unauthorized` (Token yaroqsiz)
- `404 NotFoundException`: 'Company not found'
- `409 ConflictException`: 'Branch name already exists in this company' yoki 'Branch name is required'

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String` @id @default(uuid()) @db.Uuid
  - `companyId`: `String` @db.Uuid
  - `name`: `String` @db.VarChar(255)
  - `address`: `String?` @db.VarChar(500)
  - `latitude`: `Float?`
  - `longitude`: `Float?`
  - `radius`: `Int?` @default(100)
  - `isActive`: `Boolean` @default(true)
  - `createdAt`: `DateTime` @default(now())
  - `updatedAt`: `DateTime` @updatedAt

**cURL misol:**
```bash
curl -X POST \
  http://localhost:4000/api/v1/branches \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Branch API", "companyId": "105a743b-8e71-4e87-aaff-131f27837a22", "address": "Some test address", "radius": 50}'
```

---

### Endpoint: GET /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches`
- Controller class + method nomi: `BranchController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- URL Parameters: `?page=1&limit=10&search=main&isActive=true&companyId=105a743b-8e71-4e87-aaff-131f27837a22`

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Query parametrlar:
  - `page`: Tip - Int, ixtiyoriy, min:1, default 1
  - `limit`: Tip - Int, ixtiyoriy, min:1, max:100, default 10
  - `search`: Tip - String, ixtiyoriy
  - `isActive`: Tip - Boolean, ixtiyoriy
  - `companyId`: Tip - String (UUID), ixtiyoriy

**5. Service:**
- Service method: `findAll`
- Tavsifi: Pagination, qidiruv va filter bo'yicha filiallarni ro'yxatini qaytaradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "185f58bd-6fb8-4564-83b5-a06be12e009f",
        "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
        "name": "TexnoSoft Uzbekistan — Fargona Filiali",
        "address": "Fargona sh., Al-Fargoniiy ko'chasi 88",
        "latitude": 40.3842,
        "longitude": 71.7843,
        "radius": 100,
        "isActive": true,
        "createdAt": "2026-08-06T15:15:58.056Z",
        "updatedAt": "2026-08-06T15:15:58.056Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/branches",
  "timestamp": "2026-08-22T16:34:56.026Z"
}
```

**7. Error case:**
- `401 Unauthorized` (Token yaroqsiz)
- `403 Forbidden` (Boshqa kompaniya ma'lumotlarini so'rashda ruxsat yo'q)

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)
- Ustun ta'riflari huddi yuqoridagidek.

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/branches?page=1&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches/:id`
- Controller class + method nomi: `BranchController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- URL Parameter: `id` = UUID

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` ParseUUIDPipe).

**5. Service:**
- Service method: `findOne`
- Tavsifi: Filial ID bo'yicha qidiriladi. Admin o'z kompaniyasiga tegishli ekanligini `assertWithinScope` orqali tekshiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "185f58bd-6fb8-4564-83b5-a06be12e009f",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "name": "TexnoSoft Uzbekistan — Fargona Filiali",
    "address": "Fargona sh., Al-Fargoniiy ko'chasi 88",
    "latitude": 40.3842,
    "longitude": 71.7843,
    "radius": 100,
    "isActive": true,
    "createdAt": "2026-08-06T15:15:58.056Z",
    "updatedAt": "2026-08-06T15:15:58.056Z"
  },
  "path": "/api/v1/branches/185f58bd-6fb8-4564-83b5-a06be12e009f",
  "timestamp": "2026-08-22T16:35:04.723Z"
}
```

**7. Error case:**
- `401 Unauthorized`
- `404 NotFoundException`: 'Branch not found'
- `403 Forbidden`

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/branches/185f58bd-6fb8-4564-83b5-a06be12e009f" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id`
- Controller class + method nomi: `BranchController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "name": "Updated Branch API",
  "address": "Some test address",
  "radius": 50
}
```

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: `UpdateBranchDto` (PartialType CreateBranchDto).

**5. Service:**
- Service method: `update`
- Tavsifi: Filial ma'lumotlari qisman yangilanadi, kompaniya va noyob nom tekshiruvi amalga oshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "ca3e0228-a82c-4709-b4bc-606df56283eb",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "name": "Updated Branch API",
    "address": "Some test address",
    "latitude": null,
    "longitude": null,
    "radius": 50,
    "isActive": true,
    "createdAt": "2026-08-22T16:35:10.812Z",
    "updatedAt": "2026-08-22T16:35:21.110Z"
  },
  "path": "/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb",
  "timestamp": "2026-08-22T16:35:21.126Z"
}
```

**7. Error case:**
- `401 Unauthorized`
- `404 NotFoundException`: 'Branch not found', 'Company not found'
- `409 ConflictException`: 'Branch name already exists in this company'
- `403 Forbidden`

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)

**cURL misol:**
```bash
curl -X PATCH \
  http://localhost:4000/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Branch API"}'
```

---

### Endpoint: PATCH /api/v1/branches/:id/toggle-status
**Controller:** src/modules/branch/branch.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id/toggle-status`
- Controller class + method nomi: `BranchController` -> `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "isActive": false
}
```

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- `isActive`: Tip - Boolean, ixtiyoriy

**5. Service:**
- Service method: `toggleStatus`
- Tavsifi: Filial faollik holatini (isActive) o'zgartirish. Agar body bo'sh bo'lsa teskarisiga o'zgartiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "ca3e0228-a82c-4709-b4bc-606df56283eb",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "name": "Updated Branch API",
    "address": "Some test address",
    "latitude": null,
    "longitude": null,
    "radius": 50,
    "isActive": false,
    "createdAt": "2026-08-22T16:35:10.812Z",
    "updatedAt": "2026-08-22T16:35:27.809Z"
  },
  "path": "/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb/toggle-status",
  "timestamp": "2026-08-22T16:35:27.814Z"
}
```

**7. Error case:**
- `401 Unauthorized`
- `404 NotFoundException`: 'Branch not found'
- `403 Forbidden`

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)

**cURL misol:**
```bash
curl -X PATCH \
  http://localhost:4000/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb/toggle-status \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Endpoint: DELETE /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/branches/:id`
- Controller class + method nomi: `BranchController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat URL Parameter: `id` = UUID

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` ParseUUIDPipe).

**5. Service:**
- Service method: `delete`
- Tavsifi: Filial izlanadi va huquqi borligi tasdiqlanadi. Baza ob'ekti (Prisma orqali) butunlay o'chiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "ca3e0228-a82c-4709-b4bc-606df56283eb"
  },
  "path": "/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb",
  "timestamp": "2026-08-22T16:35:33.961Z"
}
```

**7. Error case:**
- `401 Unauthorized`
- `404 NotFoundException`: 'Branch not found'
- `403 Forbidden`

**8. DB struktura:**
- Prisma modeli: `Branch` (prisma/schema.prisma)

**cURL misol:**
```bash
curl -X DELETE \
  http://localhost:4000/api/v1/branches/ca3e0228-a82c-4709-b4bc-606df56283eb \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/advance.md`

### Endpoint: POST /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/advances`
- Controller class + method nomi: `AdvanceController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
  "employeeId": "62bcbc6f-5c2f-46ee-a134-0cb105ef4014",
  "amount": 500000.5,
  "date": "2026-06-08",
  "month": "2026-06",
  "note": "Advance for travel expenses"
}
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `CreateAdvanceDto`
- `companyId`: Tip - String, Validatorlar - Ixtiyoriy admin/manager uchun
- `employeeId`: Tip - String, Validatorlar - Majburiy
- `amount`: Tip - Number, Validatorlar - Majburiy
- `date`: Tip - String (ISO8601 strict), Validatorlar - Majburiy
- `month`: Tip - String, Validatorlar - Ixtiyoriy
- `note`: Tip - String, Validatorlar - Ixtiyoriy

**5. Service:**
- Service method: `create`
- Tavsifi: `companyId` bo'yicha kompaniya borligi tekshiriladi. Xodim ushbu kompaniyaga tegishliligi hamda filial ruxsatlari borligi scope bo'yicha tahlil qilinadi. Sana orqali tegishli `month` formati yasaladi. Avans yozuvi bazaga qo'shiladi va notification yuboriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "328e3cec-ed51-4e5f-90b2-c8cc73c92f0b",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "employeeId": "62bcbc6f-5c2f-46ee-a134-0cb105ef4014",
    "amount": "500000.5",
    "date": "2026-06-08T00:00:00.000Z",
    "month": "2026-06",
    "note": "Advance for travel expenses",
    "createdById": "f259d335-49b7-4560-ae15-75e9db7864cc",
    "updatedById": "f259d335-49b7-4560-ae15-75e9db7864cc",
    "createdAt": "2026-08-22T16:40:00.000Z",
    "updatedAt": "2026-08-22T16:40:00.000Z"
  }
}
```

**7. Error case:**
- `NotFoundException`: 'Company not found', 'Employee not found'
- `ConflictException`: 'Employee does not belong to the selected company'
- `ForbiddenException`: Scope muammosi bo'lsa

**8. DB struktura:**
- Prisma modeli: `Advance`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `amount`: `Decimal`, majburiy, `@db.Decimal(15, 2)`
  - `date`: `DateTime`, majburiy, `@db.Date`
  - `month`: `String`, majburiy, `@db.VarChar(7)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`

**cURL misoli:**
```bash
curl -X POST http://localhost:4000/api/v1/advances \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"companyId":"105a743b-8e71-4e87-aaff-131f27837a22","employeeId":"62bcbc6f-5c2f-46ee-a134-0cb105ef4014","amount":500000.5,"date":"2026-06-08","month":"2026-06","note":"Xizmat safari uchun"}'
```

---

### Endpoint: GET /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances`
- Controller class + method nomi: `AdvanceController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Query parametrlar orqali:
  - `companyId`: `105a743b-8e71-4e87-aaff-131f27837a22`
  - `employeeId`: `62bcbc6f-5c2f-46ee-a134-0cb105ef4014`
  - `month`: `2026-06`
  - `dateFrom`: `2026-06-01`
  - `dateTo`: `2026-06-30`
  - `page`: `1`
  - `limit`: `10`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `AdvanceQueryDto`

**5. Service:**
- Service method: `findAll`
- Tavsifi: Xodim/kompaniya uchun scope ruxsatlari inobatga olinib where filter yig'iladi. DB dan sanasi va createdAt bo'yicha kamayish tartibida paginatsiyalanib qaytariladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "328e3cec-ed51-4e5f-90b2-c8cc73c92f0b",
        "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
        "employeeId": "62bcbc6f-5c2f-46ee-a134-0cb105ef4014",
        "amount": "865426.8",
        "date": "2026-07-15T00:00:00.000Z",
        "month": "2026-07",
        "note": "Mid-month advance",
        "createdById": null,
        "updatedById": null,
        "createdAt": "2026-08-07T14:16:35.051Z",
        "updatedAt": "2026-08-07T14:16:35.051Z"
      }
    ],
    "total": 281,
    "page": 1,
    "limit": 10,
    "totalPages": 29
  },
  "path": "/api/v1/advances",
  "timestamp": "2026-08-22T16:39:02.902Z"
}
```

**7. Error case:**
- Maxsus xatolik tashlamaydi, agar scope ruxsatsiz bo'lsa xato qaytishi mumkin.

**8. DB struktura:**
- Prisma modeli: `Advance`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `amount`: `Decimal`, majburiy, `@db.Decimal(15, 2)`
  - `date`: `DateTime`, majburiy, `@db.Date`
  - `month`: `String`, majburiy, `@db.VarChar(7)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`

**cURL misoli:**
```bash
curl -X GET "http://localhost:4000/api/v1/advances?page=1&limit=10" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, URL parametr `id` UUID bo'lishi kerak.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Faqat ParseUUIDPipe orqali tekshiriladi.

**5. Service:**
- Service method: `findOne`
- Tavsifi: ID bo'yicha Advance olinadi va actor uchun ruxsat berilgan scope ichidami (assertRecordInScope) tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "328e3cec-ed51-4e5f-90b2-c8cc73c92f0b",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "employeeId": "62bcbc6f-5c2f-46ee-a134-0cb105ef4014",
    "amount": "865426.8",
    "date": "2026-07-15T00:00:00.000Z",
    "month": "2026-07",
    "note": "Mid-month advance",
    "createdById": null,
    "updatedById": null,
    "createdAt": "2026-08-07T14:16:35.051Z",
    "updatedAt": "2026-08-07T14:16:35.051Z"
  },
  "path": "/api/v1/advances/328e3cec-ed51-4e5f-90b2-c8cc73c92f0b",
  "timestamp": "2026-08-22T16:39:14.879Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Advance not found'
- `ForbiddenException`: Avans boshqa kompaniya/filialga tegishli bo'lsa

**8. DB struktura:**
- Prisma modeli: `Advance`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `amount`: `Decimal`, majburiy, `@db.Decimal(15, 2)`
  - `date`: `DateTime`, majburiy, `@db.Date`
  - `month`: `String`, majburiy, `@db.VarChar(7)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`

**cURL misoli:**
```bash
curl -X GET "http://localhost:4000/api/v1/advances/328e3cec-ed51-4e5f-90b2-c8cc73c92f0b" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "amount": 600000,
  "note": "Updated note"
}
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateAdvanceDto`

**5. Service:**
- Service method: `update`
- Tavsifi: Advance bazada borligi va scope bo'yicha ruxsat tekshiriladi. Yangilanish bazada saqlanadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "328e3cec-ed51-4e5f-90b2-c8cc73c92f0b",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "employeeId": "62bcbc6f-5c2f-46ee-a134-0cb105ef4014",
    "amount": "600000",
    "date": "2026-07-15T00:00:00.000Z",
    "month": "2026-07",
    "note": "Updated note",
    "createdById": null,
    "updatedById": "f259d335-49b7-4560-ae15-75e9db7864cc",
    "createdAt": "2026-08-07T14:16:35.051Z",
    "updatedAt": "2026-08-22T16:45:00.000Z"
  }
}
```

**7. Error case:**
- `NotFoundException`: 'Advance not found', 'Company/Employee not found'
- `ConflictException`: 'Employee does not belong to the selected company'
- `ForbiddenException`: Scope xatoligi

**8. DB struktura:**
- Prisma modeli: `Advance`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `amount`: `Decimal`, majburiy, `@db.Decimal(15, 2)`
  - `date`: `DateTime`, majburiy, `@db.Date`
  - `month`: `String`, majburiy, `@db.VarChar(7)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`

**cURL misoli:**
```bash
curl -X PATCH http://localhost:4000/api/v1/advances/328e3cec-ed51-4e5f-90b2-c8cc73c92f0b \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"amount": 600000}'
```

---

### Endpoint: DELETE /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, URL parametr `id` (UUID)

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Faqat ParseUUIDPipe

**5. Service:**
- Service method: `delete`
- Tavsifi: Advance borligi va unga scope tegishliligi tekshirib (assertRecordInScope) so'ngra delete qilinadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "328e3cec-ed51-4e5f-90b2-c8cc73c92f0b"
  }
}
```

**7. Error case:**
- `NotFoundException`: 'Advance not found'
- `ForbiddenException`: Avans boshqa scope ga tegishli bo'lsa

**8. DB struktura:**
- Prisma modeli: `Advance`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `amount`: `Decimal`, majburiy, `@db.Decimal(15, 2)`
  - `date`: `DateTime`, majburiy, `@db.Date`
  - `month`: `String`, majburiy, `@db.VarChar(7)`
  - `note`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`

**cURL misoli:**
```bash
curl -X DELETE http://localhost:4000/api/v1/advances/328e3cec-ed51-4e5f-90b2-c8cc73c92f0b \
-H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_5.md`

# Step 5: Full Modules API Endpoints & Verbs Alignment

## 📅 Bajarilgan Ishlar:

NestJS controllerlariga muvofiq ravishda barcha frontend modullaridagi API endpointlari va HTTP metodlari (HTTP `PUT` ➔ HTTP `PATCH`) to'liq sinxronlashtirildi:

1. **`CompanyService`**:
   - `/companies` -> `PATCH /companies/:id`
2. **`EmployeeService`**:
   - `/users` -> `PATCH /users/:id`
3. **`LeaveService`**:
   - `/employee-leaves` -> `PATCH /employee-leaves/:id`
4. **`AdvanceService`**:
   - `/advances` -> `PATCH /advances/:id`
5. **`TerminalService`**:
   - `/terminals` -> `PATCH /terminals/:id`
6. **`SettingService`**:
   - `/settings` -> `PATCH /settings/:id`
7. **`SalaryAdjustmentService`**:
   - `/salary-adjustments` -> `PATCH /salary-adjustments/:id`
8. **`WorkScheduleService`**:
   - `/work-schedules` -> `PATCH /work-schedules/:id`
9. **`HolidayService`**:
   - `/holidays` -> `PATCH /holidays/:id`


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/advance.md`

### Endpoint: POST /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/advances`
- Controller class + method nomi: `AdvanceController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `employeeId`: misol yo'q
- `amount`: 500000
- `date`: 2026-06-08
- `month`: 2026-06
- `note`: Advance for travel expenses

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `CreateAdvanceDto` (src/modules/advance/dto/create-advance.dto.ts)
- `companyId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `employeeId`: required, string, `@IsUUID()`
- `amount`: required, number, `@Type(() => Number)`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`
- `date`: required, string, `@IsISO8601({ strict: true })`
- `month`: optional, string, `@IsOptional()`, `@IsString()`, `@MaxLength(7)`
- `note`: optional, string, `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.create` (src/modules/advance/advance.service.ts)
- Tavsif: Yangi avans yozuvini yaratadi. Berilgan kompaniya va xodim (employeeId) foydalanuvchi huquqi (scope) doirasida ekanini tekshiradi va `advance` jadvaliga yangi yozuv qo'shadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan Advance obyekti
  - `id`: String
  - `companyId`: String
  - `employeeId`: String
  - `amount`: Decimal
  - `date`: DateTime
  - `month`: String
  - `note`: String (yoki null)
  - `createdById`: String
  - `updatedById`: String
  - `createdAt`: DateTime
  - `updatedAt`: DateTime

**7. Error case:**
- `NotFoundException`: 'Company not found' - agar berilgan `companyId` topilmasa (404)
- `NotFoundException`: 'Employee not found' - agar xodim topilmasa (404)
- `ConflictException`: 'Employee does not belong to the selected company' - agar xodim ko'rsatilgan kompaniyada ishlamasa (409)
- `ForbiddenException`: (assertWithinScope orqali) agar foydalanuvchining ushbu ma'lumotga kirish huquqi bo'lmasa

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q (Boshqa modellar Advance modeliga bog'lanmagan)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: GET /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances`
- Controller class + method nomi: `AdvanceController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query orqali beriladi)
- Query misollari:
  - `companyId`: misol yo'q
  - `employeeId`: misol yo'q
  - `month`: 2026-06
  - `dateFrom`: 2026-06-01
  - `dateTo`: 2026-06-30
  - `page`: 1
  - `limit`: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `AdvanceQueryDto` (src/modules/advance/dto/advance-query.dto.ts)
- `companyId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `employeeId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `month`: optional, string, `@IsOptional()`
- `dateFrom`: optional, string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `dateTo`: optional, string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `page`: optional, number (default 1), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: optional, number (default 10), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.findAll` (src/modules/advance/advance.service.ts)
- Tavsif: Joriy foydalanuvchining huquqlaridan (scope) kelib chiqib tegishli kompaniya/filial uchun barcha avanslarni sahifalab (paginated) qaytaradi. Sana oralig'i, oyi, xodimi kabi filterlarni qo'llaydi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya qilingan obyekti
  - `items`: Advance modelidagi obyektlar massivi
  - `total`: number (jami elementlar soni)
  - `page`: number (joriy sahifa)
  - `limit`: number (sahifa hajmi)
  - `totalPages`: number (jami sahifalar soni)

**7. Error case:**
- Ushbu endpoint uchun asosan validation xatolari (BadRequestException) chiqadi. Alohida exception'lar yozilmagan. Maxsus ruxsatlar tekshiruvi doirasida natijalar avtomatik qisqartiriladi.

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: GET /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `@Param('id', ParseUUIDPipe)` orqali URL dan ID qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.findOne` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID bo'yicha bitta avans (Advance) ma'lumotini bazadan topadi. Foydalanuvchining ushbu yozuvni ko'rishga huquqi bor-yo'qligini tekshiradi (scope check).

**6. Response:**
- Qaytariladigan javob shakli: Bitta Advance obyekti (xuddi create javobidagi kabi)

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: agar topilgan avans foydalanuvchi huquqlari (scope) doirasidan tashqarida bo'lsa (403)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi: (yuqoridagi kabi, bir xil)
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: PATCH /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- (CreateAdvanceDto dan meros bo'lgani uchun)
- `companyId`: misol yo'q
- `employeeId`: misol yo'q
- `amount`: 500000
- `date`: 2026-06-08
- `month`: 2026-06
- `note`: Advance for travel expenses

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `UpdateAdvanceDto` (src/modules/advance/dto/update-advance.dto.ts) (PartialType(CreateAdvanceDto))
- Barcha maydonlar ixtiyoriy (`@IsOptional`):
  - `companyId`: optional, string, `@IsUUID()`
  - `employeeId`: optional, string, `@IsUUID()`
  - `amount`: optional, number, `@Type(() => Number)`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`
  - `date`: optional, string, `@IsISO8601({ strict: true })`
  - `month`: optional, string, `@IsString()`, `@MaxLength(7)`
  - `note`: optional, string, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.update` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID bo'yicha mavjud avansni yangilaydi. Yangilanayotgan xodim va kompaniyaning foydalanuvchi scope'iga mos kelishini tekshiradi hamda ma'lumotlarni bazada o'zgartiradi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Advance obyekti

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: agar avans foydalanuvchi huquqlari (scope) doirasida bo'lmasa (403)
- `NotFoundException`: 'Company not found' - agar berilgan `companyId` topilmasa (404)
- `NotFoundException`: 'Employee not found' - agar berilgan `employeeId` topilmasa (404)
- `ConflictException`: 'Employee does not belong to the selected company' - xodim belgilangan kompaniyada ishlamasa (409)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: DELETE /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `@Param('id', ParseUUIDPipe)` orqali URL dan ID qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.delete` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID ga ko'ra avans yozuvini (Advance) topib o'chiradi. O'chirishdan oldin foydalanuvchining huquqlarini (scope check) tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Muvaffaqiyat statusi va o'chirilgan ID (`{ success: true, id: string }`)

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: yozuvni o'chirishga foydalanuvchi huquqi bo'lmasa (403)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q (Shuning uchun o'chirish paytida Cascade ta'sir qiladigan bog'liq obyektlar yo'q)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_12.md`

# Step 12: Production Backend & Development Frontend Execution

## 📅 Bajarilgan Ishlar:

1. **Backend Production Execution**:
   - Backend `npm run start:prod` orqali Production rejimida ishga tushirildi (Port: 3000).
   - API manzili: `http://localhost:3000/api/v1`
   - Swagger hujjati: `http://localhost:3000/api/v1/docs`

2. **Frontend Development Execution**:
   - Frontend `npm start` (ng serve) dev server orqali Development rejimida ishga tushirildi (Port: 4200).
   - Manzil: `http://localhost:4200/`

3. **Sinov Ma'lumotlari**:
   - SuperAdmin: `superAdmin` / `superAdminPass`
   - Admin: `admin` / `Password123`


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/terminal.md`

# Terminal API Documentation

Base URL: `http://localhost:4000/api/v1`

Authorization Header (Bearer token required):
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZmYmYzNjc2LTQ0MjgtNDE1Yi05ZTZiLTA4MzNmMjQ5MDcyZCIsInJvbGUiOiJBRE1JTiIsImlhdCI6MTc4NDQ4MTgyMiwiZXhwIjoxNzg0NTY4MjIyfQ.YpWKCIn7JtiOqxVwcPC1-Yp9g96yDG4fYULnt2CIFeQ
```
---

## 1. Create Terminal

- **Point**: `POST /terminals`
- **ApiBody / Example Payload**:
```json
{
  "companyId": "<company-uuid>",            // optional for admin/manager, required for superadmin
  "branchId": "<branch-uuid>",              // optional
  "name": "Main Gate Terminal",
  "serialNumber": "TRN-001",
  "ipAddress": "192.168.1.100",
  "port": 4370,
  "type": "zkteco_face",
  "status": "active",
  "connectionConfig": { "username": "admin", "password": "12345" },
  "lastSyncAt": "2026-06-08T10:00:00.000Z"
}
```
- **Guard**: `@Roles('superadmin', 'admin', 'manager')` + `@ApiBearerAuth()`
- **DTO**: `CreateTerminalDto`
  - `companyId` – optional UUID, `@IsOptional() @IsUUID()`
  - `branchId` – optional UUID, `@IsOptional() @IsUUID()`
  - `name` – required string, `@MinLength(1) @MaxLength(255)`
  - `serialNumber` – required string, same limits
  - `ipAddress` – optional, must be a valid IP (`@IsIP()`)
  - `port` – optional integer 1‑65535 (`@IsInt() @Min(1) @Max(65535)`)
  - `type` – optional enum `TerminalType`
  - `status` – optional enum `TerminalStatus`
  - `connectionConfig` – optional object (`@IsObject()`)
  - `lastSyncAt` – optional ISO date string
- **Service**: `TerminalService.create(dto, actor)`
  1. Resolve scoped `companyId` (checks admin/manager scope).
  2. Resolve branch scope and verify branch belongs to the company.
  3. Verify the company exists (`ensureCompanyExists`).
  4. Normalise required `name` and `serialNumber` (trim, throw `ConflictException` if empty).
  5. Ensure `serialNumber` is unique (`ensureSerialNumberUnique`).
  6. Persist via Prisma `terminal.create`.
- **Response** (example, successful creation):
```json
{
  "id": "c1a2b3d4-5678-90ab-cdef-1234567890ab",
  "companyId": "<company-uuid>",
  "branchId": "<branch-uuid>",
  "name": "Main Gate Terminal",
  "serialNumber": "TRN-001",
  "ipAddress": "192.168.1.100",
  "port": 4370,
  "type": "zkteco_face",
  "status": "active",
  "connectionConfig": { "username": "admin", "password": "12345" },
  "lastSyncAt": "2026-06-08T10:00:00.000Z",
  "createdAt": "2026-08-22T22:40:00.000Z",
  "updatedAt": "2026-08-22T22:40:00.000Z"
}
```
- **Error case**:
  - `ConflictException` – serial number already exists.
  - `ConflictException` – required fields missing after trimming.
  - `NotFoundException` – referenced company or branch not found.
  - `ConflictException` – branch does not belong to the selected company.
- **cURL example**:
```bash
curl -X POST http://localhost:4000/api/v1/terminals \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Main Gate Terminal","serialNumber":"TRN-001","ipAddress":"192.168.1.100","port":4370}'
```
---

## 2. Get Terminals (list)

- **Point**: `GET /terminals`
- **ApiBody / Query Params** (all optional):
```text
companyId=<uuid>
branchId=<uuid>
type=<TerminalType>
status=<TerminalStatus>
search=<string>
page=<int> (default 1)
limit=<int> (default 10, max 100)
```
- **Guard**: `@Roles('superadmin', 'admin', 'manager')` + `@ApiBearerAuth()`
- **DTO**: `TerminalQueryDto`
  - All fields are optional, validated with `@IsOptional()`, `@IsUUID()`, `@IsEnum()`, `@IsString()`, `@IsInt()`, `@Min()`, `@Max()`.
- **Service**: `TerminalService.findAll(query, actor)`
  1. Build pagination (`skip`, `take`).
  2. Build Prisma `where` object based on scope and supplied filters.
  3. Execute `findMany` & `count` in a transaction.
  4. Return paginated payload.
- **Response** (example):
```json
{
  "items": [
    {
      "id": "c1a2b3d4-5678-90ab-cdef-1234567890ab",
      "companyId": "<company-uuid>",
      "branchId": "<branch-uuid>",
      "name": "Main Gate Terminal",
      "serialNumber": "TRN-001",
      "ipAddress": "192.168.1.100",
      "port": 4370,
      "type": "zkteco_face",
      "status": "active",
      "connectionConfig": { "username": "admin", "password": "12345" },
      "lastSyncAt": "2026-06-08T10:00:00.000Z",
      "createdAt": "2026-08-22T22:40:00.000Z",
      "updatedAt": "2026-08-22T22:40:00.000Z"
    }
    /** more items */
  ],
  "total": 42,
  "page": 1,
  "limit": 10,
  "totalPages": 5
}
```
- **Error case**:
  - `NotFoundException` – if scoped company/branch does not exist (handled in scope util).
- **cURL example**:
```bash
curl -X GET "http://localhost:4000/api/v1/terminals?limit=5&page=2" \
  -H "Authorization: Bearer <TOKEN>"
```
---

## 3. Get Terminal by ID

- **Point**: `GET /terminals/:id`
- **ApiBody**: URL param `id` (UUID, validated with `ParseUUIDPipe`).
- **Guard**: `@Roles('superadmin', 'admin', 'manager')`
- **DTO**: No body, only param.
- **Service**: `TerminalService.findOne(id, actor)`
  1. Retrieve terminal via `findTerminalByIdOrThrow`.
  2. Assert that the terminal is within the actor's scope (`assertWithinScope`).
- **Response** (example):
```json
{
  "id": "c1a2b3d4-5678-90ab-cdef-1234567890ab",
  "companyId": "<company-uuid>",
  "branchId": "<branch-uuid>",
  "name": "Main Gate Terminal",
  "serialNumber": "TRN-001",
  "ipAddress": "192.168.1.100",
  "port": 4370,
  "type": "zkteco_face",
  "status": "active",
  "connectionConfig": { "username": "admin", "password": "12345" },
  "lastSyncAt": "2026-06-08T10:00:00.000Z",
  "createdAt": "2026-08-22T22:40:00.000Z",
  "updatedAt": "2026-08-22T22:40:00.000Z"
}
```
- **Error case**:
  - `NotFoundException` – terminal not found.
  - `ConflictException` – when actor attempts to access a terminal outside their scoped company/branch.
- **cURL example**:
```bash
curl -X GET http://localhost:4000/api/v1/terminals/c1a2b3d4-5678-90ab-cdef-1234567890ab \
  -H "Authorization: Bearer <TOKEN>"
```
---

## 4. Update Terminal

- **Point**: `PATCH /terminals/:id`
- **ApiBody / Example Payload** (all fields optional, partial update):
```json
{
  "name": "Updated Terminal Name",
  "ipAddress": "192.168.1.101",
  "port": 4380,
  "status": "inactive",
  "connectionConfig": { "username": "admin", "password": "newpass" }
}
```
- **Guard**: `@Roles('superadmin', 'admin', 'manager')`
- **DTO**: `UpdateTerminalDto` – extends `PartialType(CreateTerminalDto)`, so all fields are optional with same validation rules.
- **Service**: `TerminalService.update(id, dto, actor)`
  1. Load existing terminal, verify scope.
  2. Resolve possible new `companyId` / `branchId` respecting scope.
  3. If `serialNumber` is provided, ensure uniqueness (excluding current id).
  4. Build Prisma `data` object with only provided fields (normalising required fields where needed).
  5. Execute `prisma.terminal.update`.
- **Response** (example):
```json
{
  "id": "c1a2b3d4-5678-90ab-cdef-1234567890ab",
  "companyId": "<company-uuid>",
  "branchId": "<branch-uuid>",
  "name": "Updated Terminal Name",
  "serialNumber": "TRN-001",
  "ipAddress": "192.168.1.101",
  "port": 4380,
  "type": "zkteco_face",
  "status": "inactive",
  "connectionConfig": { "username": "admin", "password": "newpass" },
  "lastSyncAt": "2026-06-08T10:00:00.000Z",
  "createdAt": "2026-08-22T22:40:00.000Z",
  "updatedAt": "2026-08-22T23:00:00.000Z"
}
```
- **Error case**:
  - `NotFoundException` – terminal not found.
  - `ConflictException` – serial number conflict.
  - `NotFoundException` – new company/branch does not exist.
  - `ConflictException` – branch does not belong to the selected company.
- **cURL example**:
```bash
curl -X PATCH http://localhost:4000/api/v1/terminals/c1a2b3d4-5678-90ab-cdef-1234567890ab \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Terminal Name","status":"inactive"}'
```
---

## 5. Delete Terminal

- **Point**: `DELETE /terminals/:id`
- **Guard**: `@Roles('superadmin', 'admin', 'manager')`
- **Service**: `TerminalService.delete(id, actor)`
  1. Locate terminal, verify scope.
  2. Perform `prisma.terminal.delete`.
  3. Return simple success object.
- **Response** (example):
```json
{ "success": true, "id": "c1a2b3d4-5678-90ab-cdef-1234567890ab" }
```
- **Error case**:
  - `NotFoundException` – terminal not found.
  - `ConflictException` – attempting to delete a terminal outside of actor's scope.
- **cURL example**:
```bash
curl -X DELETE http://localhost:4000/api/v1/terminals/c1a2b3d4-5678-90ab-cdef-1234567890ab \
  -H "Authorization: Bearer <TOKEN>"
```
---

## 6. DB Structure (Prisma `Terminal` model)

```prisma
model Terminal {
  id                String          @id @default(uuid()) @db.Uuid
  companyId         String          @db.Uuid
  branchId          String?         @db.Uuid

  name              String          @db.VarChar(255)
  serialNumber      String          @unique @db.VarChar(255)
  ipAddress         String?         @db.VarChar(100)
  port              Int?
  type              TerminalType    @default(zkteco_face)
  status            TerminalStatus  @default(active)

  connectionConfig  Json?           @db.Json
  lastSyncAt        DateTime?       @db.Timestamptz(6)

  company           Company         @relation(fields: [companyId], references: [id], onDelete: Cascade)
  branch            Branch?         @relation(fields: [branchId], references: [id], onDelete: SetNull)

  attendances       Attendance[]
  rawAttendanceLogs RawAttendanceLog[]

  createdAt         DateTime        @default(now()) @db.Timestamptz(6)
  updatedAt         DateTime        @updatedAt @db.Timestamptz(6)

  @@index([companyId])
  @@index([branchId])
  @@index([status])
}
```

---

*All examples assume a valid JWT token with role `admin` (or higher). Adjust the payload according to the actor's scope.*


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/payroll.md`

### Endpoint: POST /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/payrolls
- PayrollController create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- month: 2026-06
- baseSalary: 4000000
- totalBonus: 500000
- totalPenalty: 100000
- totalAdvance: 200000
- netSalary: 4200000
- status: draft
- paidAt: 2026-06-30T10:00:00.000Z
- paidById: misol yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- CreatePayrollDto src/modules/payroll/dto/create-payroll.dto.ts
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- month: string, @IsString()
- baseSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalBonus: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalPenalty: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalAdvance: number, @IsOptional(), @Type(() => Number), @IsNumber()
- netSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- paidAt: string, @IsOptional(), @IsDateString()
- paidById: string, @IsOptional(), @IsUUID()

**5. Service:**
- create src/modules/payroll/payroll.service.ts
- Yaratilish jarayonida ruxsatlarni tekshiradi, company va employee borligini tekshiradi, shu oydagi xodimga tegishli payroll yo'qligini tekshirib keyin bazaga Payroll yozadi.

**6. Response:**
- Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Company not found' - company topilmasa
- NotFoundException: 'Employee not found' - employee topilmasa
- ConflictException: 'Employee does not belong to the selected company' - employee va company mos kelmasa
- ConflictException: 'Payroll month is required' - month probel bo'lsa
- NotFoundException: 'Paid by user not found' - to'lovchi foydalanuvchi topilmasa
- ConflictException: 'Payroll already exists for this employee and month' - unique constraint buzilsa (shu oydagi ishhaqi qilingan bo'lsa)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: GET /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/payrolls
- PayrollController findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- PayrollQueryDto src/modules/payroll/dto/payroll-query.dto.ts
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsOptional(), @IsUUID()
- month: string, @IsOptional(), @IsString()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- page: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1)
- limit: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1), @Max(100)

**5. Service:**
- findAll src/modules/payroll/payroll.service.ts
- Ruxsat etilgan scope bo'yicha filterlab, page va limit yordamida ro'yxatni paginatsiya bilan qaytaradi.

**6. Response:**
- Paginatsiya qilingan javob qaytaradi:
  - items: Payroll[] (massiv)
  - total: number
  - page: number
  - limit: number
  - totalPages: number

**7. Error case:**
- (Ochiq tashlanadigan alohida Exception yo'q, default validation exception)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: GET /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/payrolls/:id
- PayrollController findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- (Request DTO yo'q, faqat ParseUUIDPipe)

**5. Service:**
- findOne src/modules/payroll/payroll.service.ts
- Id bo'yicha bazadan izlaydi va ruxsatlarini tekshirib obyektni qaytaradi.

**6. Response:**
- Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id li yozuv topilmasa

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: PATCH /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/payrolls/:id
- PayrollController update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- month: 2026-06
- baseSalary: 4000000
- totalBonus: 500000
- totalPenalty: 100000
- totalAdvance: 200000
- netSalary: 4200000
- status: draft
- paidAt: 2026-06-30T10:00:00.000Z
- paidById: misol yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- UpdatePayrollDto src/modules/payroll/dto/update-payroll.dto.ts (PartialType)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- month: string, @IsString()
- baseSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalBonus: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalPenalty: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalAdvance: number, @IsOptional(), @Type(() => Number), @IsNumber()
- netSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- paidAt: string, @IsOptional(), @IsDateString()
- paidById: string, @IsOptional(), @IsUUID()

**5. Service:**
- update src/modules/payroll/payroll.service.ts
- Mavjud yozuvni topib, ma'lumotlarini ruxsatlar bilan tahrirlaydi (jumladan unique payroll bor-yo'qligini employee va oy bo'yicha tekshiradi).

**6. Response:**
- Yangilangan Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id bo'yicha ishhaqi topilmasa
- NotFoundException: 'Company not found' - company topilmasa
- NotFoundException: 'Employee not found' - employee topilmasa
- ConflictException: 'Employee does not belong to the selected company' - employee va company mos kelmasa
- ConflictException: 'Payroll month is required' - month probel bo'lsa
- NotFoundException: 'Paid by user not found' - to'lovchi foydalanuvchi topilmasa
- ConflictException: 'Payroll already exists for this employee and month' - unique constraint buzilsa (boshqa id li)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: DELETE /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/payrolls/:id
- PayrollController delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- (Request DTO yo'q, faqat ParseUUIDPipe)

**5. Service:**
- delete src/modules/payroll/payroll.service.ts
- Bazadan yozuvni izlaydi va o'chirib tashlaydi.

**6. Response:**
- `{ success: true, id: string }`

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id bo'yicha ishhaqi topilmasa

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/employee-leave.md`

### Endpoint: POST /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar)

**4. DTO:**
- Request DTO: `CreateEmployeeLeaveDto` (src/modules/employee-leave/dto/create-employee-leave.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsUUID()`
- `type`: Tip - LeaveType (enum), Validatorlar - `@IsEnum(LeaveType)`
- `fromDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `toDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `days`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@IsBoolean()`
- `reason`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Service method: `create` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Xodimni, kompaniya va filiallarni tekshiradi, kunlarni hisoblaydi (agar berilmagan bo'lsa) va `EmployeeLeave` jadvaliga yangi ta'til yozuvini qo'shadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti (aniq maydonlar: `id` (String), `companyId` (String), `branchId` (String?), `employeeId` (String), `type` (LeaveType), `fromDate` (DateTime), `toDate` (DateTime), `days` (Int), `affectsSalary` (Boolean), `reason` (String?), `createdById` (String?), `updatedById` (String?), `createdAt` (DateTime), `updatedAt` (DateTime)).

**7. Error case:**
- `NotFoundException`: 'Company not found' (kompaniya topilmasa), 'Branch not found' (filial topilmasa), 'Employee not found' (xodim topilmasa).
- `ConflictException`: 'Branch does not belong to the selected company' (filial tegishli emas), 'Employee does not belong to the selected company' (xodim tegishli emas), 'Employee does not belong to the selected branch' (xodim filialga tegishli emas).
- `BadRequestException`: 'Leave end date must be after start date' (sana xato bo'lsa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q (Boshqa modellar ushbu modelga ishora qilmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `type`: `vacation`
  - `affectsSalary`: `false`
  - `search`: `medical`
  - `dateFrom`: `2026-06-01`
  - `dateTo`: `2026-06-30`
  - `page`: `1`
  - `limit`: `10`
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `EmployeeLeaveQueryDto` (src/modules/employee-leave/dto/employee-leave-query.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `type`: Tip - LeaveType, Validatorlar - `@IsOptional()`, `@IsEnum(LeaveType)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- `search`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateFrom`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateTo`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `page`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `findAll` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Filterlar (kompaniya, xodim, filial, sana) bo'yicha ruxsat doirasida xodimlar ta'tillari ro'yxatini va paginatsiyani bazadan olib keladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
  - `items`: EmployeeLeave obyektlari massivi (Array)
    - `id`: UUID (String)
    - `companyId`: Kompaniya ID (UUID)
    - `branchId`: Filial ID (UUID, null bo'lishi mumkin)
    - `employeeId`: Xodim ID (UUID)
    - `type`: Ta'till turi - LeaveType enum (vacation, sick_leave, personal, maternity, unpaid)
    - `durationType`: Vaqt turi - DurationType enum (single_day, multi_day, half_day, hourly)
    - `fromDate`: Boshlanish sanasi (ISO 8601)
    - `toDate`: Tugash sanasi (ISO 8601)
    - `days`: Kunlar soni (Number)
    - `leaveHours`: Ta'till soatlari (Number, null bo'lishi mumkin)
    - `status`: Holati - LeaveStatus enum (pending, approved, rejected)
    - `requestedById`: So'rov qilgan shaxs ID (UUID, null bo'lishi mumkin)
    - `respondedById`: Javob bergan shaxs ID (UUID, null bo'lishi mumkin)
    - `respondedAt`: Javob berilgan vaqti (ISO 8601, null bo'lishi mumkin)
    - `affectsSalary`: Oylik ta'sirlaydi (Boolean)
    - `reason`: Sababı (String, null bo'lishi mumkin)
    - `createdById`: Yaratgan shaxs ID (UUID, null bo'lishi mumkin)
    - `updatedById`: Yangilagan shaxs ID (UUID, null bo'lishi mumkin)
    - `createdAt`: Yaratilgan vaqti (ISO 8601)
    - `updatedAt`: Yangilangan vaqti (ISO 8601)
  - `total`: Umumiy miqdor (Number)
  - `page`: Joriy sahifa (Number)
  - `limit`: Sahifadagi limit (Number)
  - `totalPages`: Jami sahifalar soni (Number)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "0396bcba-6715-4e50-aab7-4804f7534249",
        "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
        "branchId": null,
        "employeeId": "23143592-0250-43a3-9b99-534bd892fd8e",
        "type": "vacation",
        "durationType": "multi_day",
        "fromDate": "2026-07-06T00:00:00.000Z",
        "toDate": "2026-07-09T00:00:00.000Z",
        "days": 4,
        "leaveHours": null,
        "status": "approved",
        "requestedById": null,
        "respondedById": null,
        "respondedAt": null,
        "affectsSalary": false,
        "reason": null,
        "createdById": null,
        "updatedById": null,
        "createdAt": "2026-08-07T14:16:35.046Z",
        "updatedAt": "2026-08-07T14:16:35.046Z"
      }
    ],
    "total": 93,
    "page": 1,
    "limit": 10,
    "totalPages": 10
  },
  "path": "/api/v1/employee-leaves?limit=10",
  "timestamp": "2026-08-21T10:22:10.581Z"
}
```

**7. Error case:**
- Maxsus xatolik tashlamaydi (bazaviy exception'lar bo'lishi mumkin xolos).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string sifatida olinadi).

**5. Service:**
- Service method: `findOne` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Berilgan ID yordamida bitta ta'til yozuvini oladi va foydalanuvchining unga ruxsati borligini (scope) tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "0396bcba-6715-4e50-aab7-4804f7534249",
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "branchId": null,
    "employeeId": "23143592-0250-43a3-9b99-534bd892fd8e",
    "type": "vacation",
    "durationType": "multi_day",
    "fromDate": "2026-07-06T00:00:00.000Z",
    "toDate": "2026-07-09T00:00:00.000Z",
    "days": 4,
    "leaveHours": null,
    "status": "approved",
    "requestedById": null,
    "respondedById": null,
    "respondedAt": null,
    "affectsSalary": false,
    "reason": null,
    "createdById": null,
    "updatedById": null,
    "createdAt": "2026-08-07T14:16:35.046Z",
    "updatedAt": "2026-08-07T14:16:35.046Z"
  },
  "path": "/api/v1/employee-leaves/0396bcba-6715-4e50-aab7-4804f7534249",
  "timestamp": "2026-08-21T11:25:08.115Z"
}
```

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (berilgan id dagi ta'til topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: PATCH /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
(CreateEmployeeLeaveDto dan meros orqali olingan PartialType)
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateEmployeeLeaveDto` (src/modules/employee-leave/dto/update-employee-leave.dto.ts) - `PartialType(CreateEmployeeLeaveDto)`
- Maydonlar tip va validatorlari CreateEmployeeLeaveDto kabi, faqat barchasi ixtiyoriy bo'ladi.

**5. Service:**
- Service method: `update` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Mavjud ta'tilni topib tekshiradi va uzatilgan yangi ma'lumotlar bilan ma'lumotlar bazasida yozuvni yangilaydi (shuningdek sana oralig'ini qayta hisoblaydi).

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `EmployeeLeave` obyekti.

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (ta'til obyektini yoki kompaniya, xodim filialni topa olmasa).
- `ConflictException`: Kompaniya va filiallar mos tushmaganda.
- `BadRequestException`: 'Leave end date must be after start date' (Sana noto'g'ri bo'lganda).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: DELETE /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string).

**5. Service:**
- Service method: `delete` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Ta'til obyekti ID bo'yicha topiladi, scope orqali tekshiriladi va xavfsiz holatda o'chiriladi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: boolean, id: string }`

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (o'chirilishi kerak bo'lgan obyekt topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Kiruvchi reference'lar (ya'ni ushbu `EmployeeLeave` ni ko'rsatadigan boshqa modellar) butunlay YO'Q. (Yani EmployeeLeave o'chirilsa, hech qaysi boshqa jadvalga cascade yoki null qilib ta'sir ko'rsatmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: POST /api/v1/employee-leaves/request
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:request

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/employee-leaves/request`
- Controller class + method nomi: `EmployeeLeaveController` -> `request`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `type`: `vacation` (yoki sick, unpaid va hk.)
- `durationType`: `daily` (yoki hourly)
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12` (kunlik bo'lsa, ixtiyoriy lekin tavsiya etiladi)
- `leaveHours`: 2 (soatbay bo'lsa, max 3)
- `reason`: `Doctor appointment`

**3. Guard:**
- `@Roles('employee')` (Faqat xodimlar ruxsat etiladi)

**4. DTO:**
- Request DTO: `RequestEmployeeLeaveDto` (src/modules/employee-leave/dto/request-employee-leave.dto.ts)

**5. Service:**
- Service method: `request` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Xodim o'zi uchun ta'til so'raydi. Holati tasdiqlanishni kutayotgan (pending) bo'ladi.

**6. Response:**
- Yaratilgan `EmployeeLeave` obyekti.

---

### Endpoint: PATCH /api/v1/employee-leaves/:id/approve
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:approve

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/employee-leaves/:id/approve`
- Controller class + method nomi: `EmployeeLeaveController` -> `approve`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat `:id` parametri qabul qilinadi.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO yo'q.

**5. Service:**
- Service method: `approve` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Kutayotgan (pending) ta'til arizasini tasdiqlaydi.

**6. Response:**
- Yangilangan `EmployeeLeave` obyekti qaytariladi.

---

### Endpoint: PATCH /api/v1/employee-leaves/:id/reject
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:reject

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/employee-leaves/:id/reject`
- Controller class + method nomi: `EmployeeLeaveController` -> `reject`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat `:id` parametri qabul qilinadi.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO yo'q.

**5. Service:**
- Service method: `reject` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Kutayotgan (pending) ta'til arizasini rad etadi.

**6. Response:**
- Yangilangan `EmployeeLeave` obyekti qaytariladi.


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/company.md`

### Endpoint: POST /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/companies
- Controller class: CompanyController, method: create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
name: 'ZDES'
legalName: 'ZDES LLC'
phone: '+998901234567'
email: 'info@zdes.uz'
address: 'Tashkent city, Yunusobod district'
logoUrl: 'https://cdn.example.com/logos/zdes.png'

**3. Guard:**
- Class darajasida: `@Roles('superadmin')` (faqat superadmin ruxsat etilgan)
- Hech qanday `@Public()` qo'llanilmagan.

**4. DTO:**
- CreateCompanyDto (src/modules/company/dto/create-company.dto.ts)
- name: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- legalName: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- phone: string, `@IsOptional()`, `@IsString()`, `@MaxLength(50)`
- email: string, `@IsOptional()`, `@IsEmail()`, `@MaxLength(255)`
- address: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- logoUrl: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`

**5. Service:**
- CompanyService:create (src/modules/company/company.service.ts)
- Kompaniya nomini (name) normalizatsiya qilib (trimToNull orqali), uning yagonaligini (unique) tekshiradi va Prisma orqali bazaga yangi kompaniya yozuvini yaratadi.

**6. Response:**
- Yaratilgan Company obyekti to'liq qaytariladi.
- id: string
- name: string
- legalName: string | null
- phone: string | null
- email: string | null
- address: string | null
- logoUrl: string | null
- isActive: boolean
- stoppedAt: Date | null
- createdAt: Date
- updatedAt: Date

**7. Error case:**
- `ConflictException`: Kompaniya nomi kiritilmagan bo'lsa ('Company name is required') yoki shu nomdagi kompaniya allaqachon mavjud bo'lsa ('Company name already exists') (409 Conflict).

**8. DB struktura:**
- Model: `Company`
- O'qiydigan/yozadigan maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - name: String, majburiy, `@unique`, `@db.VarChar(255)`
  - legalName: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - phone: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - email: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - address: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - logoUrl: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - isActive: Boolean, majburiy, `@default(true)`
  - stoppedAt: DateTime, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references: Company modelida boshqa modelga ishora qiluvchi FK (`@relation(fields: [...])`) yo'q. Ammo bu boshqa modellar uchun asosiy (parent) model hisoblanadi.

---

### Endpoint: GET /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/companies
- Controller class: CompanyController, method: findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.
Query parametrlari uchun misollar (CompanyQueryDto):
search: 'zdes' (misol yo'q qismidan olingan ApiPropertyOptional example)
isActive: true
page: 1
limit: 10

**3. Guard:**
- Class darajasida: `@Roles('superadmin')` (faqat superadmin ruxsat etilgan)

**4. DTO:**
- CompanyQueryDto (src/modules/company/dto/company-query.dto.ts)
- search: string, `@IsOptional()`, `@IsString()`
- isActive: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- page: number = 1, `@IsOptional()`, `@Type`, `@IsInt()`, `@Min(1)`
- limit: number = 10, `@IsOptional()`, `@Type`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- CompanyService:findAll (src/modules/company/company.service.ts)
- Kompaniyalar ro'yxatini paginatsiya (page, limit) va filter (isActive, search) bilan bazadan olib beradi. `search` qidiruvi `name`, `legalName`, `phone`, va `email` bo'yicha ishlaydi.

**6. Response:**
- Paginatsiya shaklidagi ob'ekt:
  - items: Company[] (Kompaniyalar ro'yxati)
  - total: number
  - page: number
  - limit: number
  - totalPages: number

**7. Error case:**
- Maxsus biznes mantiqi xatolari yo'q. Noto'g'ri so'rov parametrlari berilsa (masalan limit = 0), 400 Bad Request validatsiya xatosi chiqishi mumkin.

**8. DB struktura:**
- Model: `Company`
- O'qiladigan maydonlar: Barcha maydonlar o'qiladi (id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt). Ularning tiplari yuqoridagi Endpoint POST /api/v1/companies bo'limida keltirilganidek.
- Indekslar: 
  - `@@index([isActive])` (findAll usulida filterlash tezligi uchun ishlaydi).
- Relations / references: Hech qanday bog'lanish (FK) ishlatilmaydi.

---

### Endpoint: GET /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/companies/:id
- Controller class: CompanyController, method: findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- DTO class ishlatilmagan. Parametrda `id: string` qabul qilinadi (`ParseUUIDPipe` orqali validatsiya qilinadi).

**5. Service:**
- CompanyService:findOne (src/modules/company/company.service.ts)
- Berilgan UUID yordamida bazadan aniq bitta kompaniyani qidirib topib beradi. Topilmasa exception tashlaydi.

**6. Response:**
- Bitta to'liq Company obyekti (id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt) qaytariladi.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha kompaniya bazadan topilmasa ('Company not found') (404 Not Found).
- 400 Bad Request: ID to'g'ri UUID formatida bo'lmasa (`ParseUUIDPipe` orqali).

**8. DB struktura:**
- Model: `Company`
- O'qiladigan maydon: `id` String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id` (va kompaniyaning boshqa barcha maydonlari qaytariladi).
- Relations / references: Company o'zida tashqi modelga `@relation` (fields bilan) yo'q.

---

### Endpoint: PATCH /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/companies/:id
- Controller class: CompanyController, method: update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
*(UpdateCompanyDto CreateCompanyDto'ning PartialType versiyasi bo'lgani uchun barcha misol qiymatlar o'zgarishsiz o'tadi)*
name: 'ZDES'
legalName: 'ZDES LLC'
phone: '+998901234567'
email: 'info@zdes.uz'
address: 'Tashkent city, Yunusobod district'
logoUrl: 'https://cdn.example.com/logos/zdes.png'

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- UpdateCompanyDto (src/modules/company/dto/update-company.dto.ts)
- PartialType(CreateCompanyDto) (barcha name, legalName, phone, email, address, logoUrl maydonlari ixtiyoriy holatda).

**5. Service:**
- CompanyService:update (src/modules/company/company.service.ts)
- Kompaniyani ID orqali qidirib topadi, yuborilgan yangi maydonlarni (agar mavjud bo'lsa) normalizatsiya qilib bazada yangilaydi. `name` yuborilgan bo'lsa boshqa kompaniyalar ismlari bilan to'qnashmasligini tekshiradi.

**6. Response:**
- Yangilangan Company obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa ('Company not found') (404 Not Found).
- `ConflictException`: Yangi uzatilgan `name` boshqa kompaniyada allaqachon mavjud bo'lsa ('Company name already exists') (409 Conflict).

**8. DB struktura:**
- Model: `Company`
- Yoziladigan (o'zgartirilishi mumkin bo'lgan) maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id` (qidiruv uchun)
  - name: String, majburiy, `@unique`, `@db.VarChar(255)`
  - legalName: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - phone: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - email: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - address: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - logoUrl: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references: FK bog'lanish ishlatilmaydi.

---

### Endpoint: PATCH /api/v1/companies/:id/toggle-status
**Controller:** src/modules/company/company.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- PATCH /api/v1/companies/:id/toggle-status
- Controller class: CompanyController, method: toggleStatus

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- ToggleCompanyStatusDto (src/modules/company/dto/toggle-company-status.dto.ts)
- isActive: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- CompanyService:toggleStatus (src/modules/company/company.service.ts)
- Kompaniyaning holatini faol yoki nofaol holatga o'tkazadi (isActive). Agar isActive=false qilinsa, qo'shimcha tarzda `stoppedAt` maydoniga hozirgi vaqtni yozib qo'yadi.

**6. Response:**
- Holati o'zgargan (yangilangan) Company obyekti qaytariladi.

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa (404 Not Found).

**8. DB struktura:**
- Model: `Company`
- O'qiydigan va yozadigan maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - isActive: Boolean, majburiy, `@default(true)`
  - stoppedAt: DateTime, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Indekslar: `@@index([isActive])` (holati bo'yicha filterlarni tezlatish uchun yozilgan).

---

### Endpoint: DELETE /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/companies/:id
- Controller class: CompanyController, method: delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- DTO yo'q. Parametrda id: string (`ParseUUIDPipe`).

**5. Service:**
- CompanyService:delete (src/modules/company/company.service.ts)
- Kompaniyaning mavjudligini ID orqali tekshiradi va topilsa bazadan o'chiradi.

**6. Response:**
- O'chirilganligini tasdiqlovchi ob'ekt: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa ('Company not found') (404 Not Found).

**8. DB struktura:**
- Model: `Company`
- O'chiriladigan asosiy yozuv ID si qidiriladi:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
- **Relations / references:** (O'chirish operatsiyasida Company'ga qaram bo'lgan jadvallar to'liq ta'sir qiladi, chunki ular quyidagicha bog'langan):
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
  - `Department.companyId -> Company.id (onDelete: Cascade)`
  - `Position.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `Terminal.companyId -> Company.id (onDelete: Cascade)`
  - `Attendance.companyId -> Company.id (onDelete: Cascade)`
  - `RawAttendanceLog.companyId -> Company.id (onDelete: Cascade)`
  - `SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Holiday.companyId -> Company.id (onDelete: Cascade)`
  - `EmployeeLeave.companyId -> Company.id (onDelete: Cascade)`
  - `Payroll.companyId -> Company.id (onDelete: Cascade)`
  - `Setting.companyId -> Company.id (onDelete: Cascade)`
  - `User.companyId -> Company.id (onDelete: SetNull)`
  (Bu degani kompaniya o'chganda User'larda companyId NULL bo'ladi, boshqa barcha bog'langan ma'lumotlar esa zanjirli tarzda to'liq o'chib ketadi.)


## Manba: `zdes_archive_docs/raw_history/combined_review.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

### Endpoint: POST /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/advances`
- Controller class + method nomi: `AdvanceController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `employeeId`: misol yo'q
- `amount`: 500000
- `date`: 2026-06-08
- `month`: 2026-06
- `note`: Advance for travel expenses

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `CreateAdvanceDto` (src/modules/advance/dto/create-advance.dto.ts)
- `companyId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `employeeId`: required, string, `@IsUUID()`
- `amount`: required, number, `@Type(() => Number)`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`
- `date`: required, string, `@IsISO8601({ strict: true })`
- `month`: optional, string, `@IsOptional()`, `@IsString()`, `@MaxLength(7)`
- `note`: optional, string, `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.create` (src/modules/advance/advance.service.ts)
- Tavsif: Yangi avans yozuvini yaratadi. Berilgan kompaniya va xodim (employeeId) foydalanuvchi huquqi (scope) doirasida ekanini tekshiradi va `advance` jadvaliga yangi yozuv qo'shadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan Advance obyekti
  - `id`: String
  - `companyId`: String
  - `employeeId`: String
  - `amount`: Decimal
  - `date`: DateTime
  - `month`: String
  - `note`: String (yoki null)
  - `createdById`: String
  - `updatedById`: String
  - `createdAt`: DateTime
  - `updatedAt`: DateTime

**7. Error case:**
- `NotFoundException`: 'Company not found' - agar berilgan `companyId` topilmasa (404)
- `NotFoundException`: 'Employee not found' - agar xodim topilmasa (404)
- `ConflictException`: 'Employee does not belong to the selected company' - agar xodim ko'rsatilgan kompaniyada ishlamasa (409)
- `ForbiddenException`: (assertWithinScope orqali) agar foydalanuvchining ushbu ma'lumotga kirish huquqi bo'lmasa

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q (Boshqa modellar Advance modeliga bog'lanmagan)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: GET /api/v1/advances
**Controller:** src/modules/advance/advance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances`
- Controller class + method nomi: `AdvanceController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query orqali beriladi)
- Query misollari:
  - `companyId`: misol yo'q
  - `employeeId`: misol yo'q
  - `month`: 2026-06
  - `dateFrom`: 2026-06-01
  - `dateTo`: 2026-06-30
  - `page`: 1
  - `limit`: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `AdvanceQueryDto` (src/modules/advance/dto/advance-query.dto.ts)
- `companyId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `employeeId`: optional, string, `@IsOptional()`, `@IsUUID()`
- `month`: optional, string, `@IsOptional()`
- `dateFrom`: optional, string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `dateTo`: optional, string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `page`: optional, number (default 1), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: optional, number (default 10), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.findAll` (src/modules/advance/advance.service.ts)
- Tavsif: Joriy foydalanuvchining huquqlaridan (scope) kelib chiqib tegishli kompaniya/filial uchun barcha avanslarni sahifalab (paginated) qaytaradi. Sana oralig'i, oyi, xodimi kabi filterlarni qo'llaydi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya qilingan obyekti
  - `items`: Advance modelidagi obyektlar massivi
  - `total`: number (jami elementlar soni)
  - `page`: number (joriy sahifa)
  - `limit`: number (sahifa hajmi)
  - `totalPages`: number (jami sahifalar soni)

**7. Error case:**
- Ushbu endpoint uchun asosan validation xatolari (BadRequestException) chiqadi. Alohida exception'lar yozilmagan. Maxsus ruxsatlar tekshiruvi doirasida natijalar avtomatik qisqartiriladi.

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: GET /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `@Param('id', ParseUUIDPipe)` orqali URL dan ID qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.findOne` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID bo'yicha bitta avans (Advance) ma'lumotini bazadan topadi. Foydalanuvchining ushbu yozuvni ko'rishga huquqi bor-yo'qligini tekshiradi (scope check).

**6. Response:**
- Qaytariladigan javob shakli: Bitta Advance obyekti (xuddi create javobidagi kabi)

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: agar topilgan avans foydalanuvchi huquqlari (scope) doirasidan tashqarida bo'lsa (403)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi: (yuqoridagi kabi, bir xil)
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: PATCH /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- (CreateAdvanceDto dan meros bo'lgani uchun)
- `companyId`: misol yo'q
- `employeeId`: misol yo'q
- `amount`: 500000
- `date`: 2026-06-08
- `month`: 2026-06
- `note`: Advance for travel expenses

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `UpdateAdvanceDto` (src/modules/advance/dto/update-advance.dto.ts) (PartialType(CreateAdvanceDto))
- Barcha maydonlar ixtiyoriy (`@IsOptional`):
  - `companyId`: optional, string, `@IsUUID()`
  - `employeeId`: optional, string, `@IsUUID()`
  - `amount`: optional, number, `@Type(() => Number)`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`
  - `date`: optional, string, `@IsISO8601({ strict: true })`
  - `month`: optional, string, `@IsString()`, `@MaxLength(7)`
  - `note`: optional, string, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.update` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID bo'yicha mavjud avansni yangilaydi. Yangilanayotgan xodim va kompaniyaning foydalanuvchi scope'iga mos kelishini tekshiradi hamda ma'lumotlarni bazada o'zgartiradi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Advance obyekti

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: agar avans foydalanuvchi huquqlari (scope) doirasida bo'lmasa (403)
- `NotFoundException`: 'Company not found' - agar berilgan `companyId` topilmasa (404)
- `NotFoundException`: 'Employee not found' - agar berilgan `employeeId` topilmasa (404)
- `ConflictException`: 'Employee does not belong to the selected company' - xodim belgilangan kompaniyada ishlamasa (409)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`

---

### Endpoint: DELETE /api/v1/advances/:id
**Controller:** src/modules/advance/advance.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/advances/:id`
- Controller class + method nomi: `AdvanceController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `@Param('id', ParseUUIDPipe)` orqali URL dan ID qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AdvanceService.delete` (src/modules/advance/advance.service.ts)
- Tavsif: Berilgan ID ga ko'ra avans yozuvini (Advance) topib o'chiradi. O'chirishdan oldin foydalanuvchining huquqlarini (scope check) tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Muvaffaqiyat statusi va o'chirilgan ID (`{ success: true, id: string }`)

**7. Error case:**
- `NotFoundException`: 'Advance not found' - avans ID bo'yicha topilmasa (404)
- `ForbiddenException`: yozuvni o'chirishga foydalanuvchi huquqi bo'lmasa (403)

**8. DB struktura:**
- Prisma model: `Advance`
- Maydonlar ta'rifi:
  - `id`: String @id @default(uuid()) @db.Uuid
  - `companyId`: String @db.Uuid
  - `employeeId`: String @db.Uuid
  - `amount`: Decimal @db.Decimal(15, 2)
  - `date`: DateTime @db.Date
  - `month`: String @db.VarChar(7)
  - `note`: String?
  - `createdById`: String? @db.Uuid
  - `updatedById`: String? @db.Uuid
  - `createdAt`: DateTime @default(now()) @db.Timestamptz(6)
  - `updatedAt`: DateTime @updatedAt @db.Timestamptz(6)
- **Relations / references (Chiquvchi):**
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
- **Relations / references (Kiruvchi):**
  - Yo'q (Shuning uchun o'chirish paytida Cascade ta'sir qiladigan bog'liq obyektlar yo'q)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([employeeId])`
  - `@@index([month])`
  - `@@index([date])`
### Endpoint: GET /api/v1/attendance/kpi-template/:companyId
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:getKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/kpi-template/:companyId`
- Controller class + method nomi: `AttendanceController.getKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` ko'rsatilmagan (lekin `@ApiBearerAuth()` bor, ehtimol global guard)
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: Yo'q (faqat Param: `companyId` ParseUUIDPipe)

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.getKpiTemplate` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Bajaruvchi ko'rsatilgan kompaniyaga tegishli yoki ruxsati borligini tekshiradi va shu kompaniya uchun KPI shablonini (`Setting` jadvalidan) yoki bazaviy standart (default) shablonni qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli (AttendanceKpiTemplateDto):
  - companyId: string (UUID)
  - latePenaltyPerMinute: number
  - earlyLeavePenaltyPerMinute: number
  - overtimeBonusPerMinute: number
  - faceSimilarityThreshold: number

**7. Error case:**
- `ForbiddenException`: Agar actor shu kompaniyaga tegishli/ruxsati bo'lmasa.
- `NotFoundException`: Agar kompaniya bazada topilmasa.

**8. DB struktura:**
Model: `Setting`, `Company` (ushbu endpoint asosan shablon o'qiydi).
Umumiy modul uchun tegishli `Attendance` modeli tarkibi:
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar (Attendance):
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: PUT /api/v1/attendance/kpi-template
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:upsertKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PUT /api/v1/attendance/kpi-template`
- Controller class + method nomi: `AttendanceController.upsertKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `latePenaltyPerMinute`: 1000
- `earlyLeavePenaltyPerMinute`: 1000
- `overtimeBonusPerMinute`: 1000
- `faceSimilarityThreshold`: 90

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` ko'rsatilmagan
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: `AttendanceKpiTemplateDto` (`zdes_backend/src/modules/attendance/dto/attendance-kpi-template.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `latePenaltyPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `earlyLeavePenaltyPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `overtimeBonusPerMinute`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`
  - `faceSimilarityThreshold`: number, `@IsOptional()`, `@IsNumber()`, `@Min(0)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.upsertKpiTemplate` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Kompaniya mavjudligini tekshiradi va DTO dagi ma'lumotlar bilan `Setting` jadvaliga `ATTENDANCE_KPI_SETTING_KEY` kaliti ostida KPI shablonini yangilaydi yoki yaratadi (upsert).

**6. Response:**
- Qaytariladigan javob shakli (AttendanceKpiTemplateDto):
  - companyId: string
  - latePenaltyPerMinute: number
  - earlyLeavePenaltyPerMinute: number
  - overtimeBonusPerMinute: number
  - faceSimilarityThreshold: number

**7. Error case:**
- `ForbiddenException`: Agar foydalanuvchi ko'rsatilgan kompaniyaga huquqi bo'lmasa.
- `NotFoundException`: Agar kompaniya bazada topilmasa.

**8. DB struktura:**
Model: `Setting`, `Company` (ushbu endpoint shablonni Settings ga yozadi).
Model `Attendance` (modul asosi):
- (Yuqoridagi Endpoint 1dagi kabi majburiy qatorlar bu yerda ham amalda, barchasi yuqorida to'liq keltirilgan: id, companyId, date va h.k.)

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

---
### Endpoint: POST /api/v1/attendance/check-in
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:checkIn

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-in`
- Controller class + method nomi: `AttendanceController.checkIn`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `employeeId`: misol yo'q
- `terminalId`: misol yo'q
- `imageBase64`: misol yo'q
- `contentType`: 'image/jpeg'
- `eventTime`: '2026-06-08T09:05:00.000Z'
- `notes`: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckInDto` (`zdes_backend/src/modules/attendance/dto/attendance-check-in.dto.ts`)
- Maydonlar:
  - `employeeId`: string, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `imageBase64`: string, `@IsString()`, `@MinLength(10)`
  - `contentType`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
  - `eventTime`: string (optional), `@IsOptional()`, `@IsISO8601()`
  - `notes`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.checkIn` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Xodimni AWS yordamida yuz orqali verifikatsiya qiladi va tekshiradi. Shundan so'ng `Attendance` jadvaliga check-in vaqtini (yangi yozuv yaratish yoki update qilish orqali) qayd etadi, kechikish va qo'shimcha ishlashni hisoblab `SalaryAdjustment` yozuvlarini ham yaratadi (yoki eskilarini o'chirib qayta yozadi).

**6. Response:**
- Qaytariladigan javob shakli:
  - id: string
  - companyId: string
  - branchId: string | null
  - employeeId: string
  - terminalId: string | null
  - date: Date
  - checkIn: Date | null
  - checkOut: Date | null
  - status: AttendanceStatus
  - source: AttendanceSource
  - workStartTime: string | null
  - workEndTime: string | null
  - workedMinutes: number
  - lateMinutes: number
  - earlyLeaveMinutes: number
  - overtimeMinutes: number
  - checkInImageUrl: string | null
  - checkOutImageUrl: string | null
  - notes: string | null
  - faceSimilarity: number | undefined
  - appliedAdjustments: AttendanceAdjustmentDto[]
  - createdAt: Date
  - updatedAt: Date

**7. Error case:**
- `BadRequestException`: Yuz rasmi bo'sh bo'lsa yoki noto'g'ri sanali vaqt kelsa.
- `NotFoundException`: Xodim yoki Terminal topilmasa.
- `ConflictException`: Xodim rasmi bo'lmasa, Terminal noto'g'ri kompaniyaga tegishli bo'lmasa, yuz tekshiruvi yetarli similarity bermasa yoki shu sana uchun xodim allaqachon check-in qilgan bo'lsa.
- `ForbiddenException`: Xodim bloklangan bo'lsa.

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: POST /api/v1/attendance/check-out
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:checkOut

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-out`
- Controller class + method nomi: `AttendanceController.checkOut`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `employeeId`: misol yo'q
- `terminalId`: misol yo'q
- `imageBase64`: misol yo'q
- `contentType`: 'image/jpeg'
- `eventTime`: '2026-06-08T18:10:00.000Z'
- `notes`: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckOutDto` (`zdes_backend/src/modules/attendance/dto/attendance-check-out.dto.ts`)
- Maydonlar:
  - `employeeId`: string, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `imageBase64`: string, `@IsString()`, `@MinLength(10)`
  - `contentType`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
  - `eventTime`: string (optional), `@IsOptional()`, `@IsISO8601()`
  - `notes`: string (optional), `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.checkOut` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Xodimni AWS orqali yuz orqali verifikatsiya qiladi va tekshiradi. Shundan so'ng bazadagi bugungi check-in yozuvini yangilab, `checkOut` vaqtini qo'shadi hamda KPI bo'yicha ishlagan vaqt/overtime larni hisoblab `SalaryAdjustment` qatorlarini sinxronizatsiya qiladi.

**6. Response:**
- Qaytariladigan javob shakli: Check-in bilan bir xil shaklda (id, date, status, checkIn, checkOut, workStartTime, lateMinutes va h.k. obyekti + faceSimilarity + appliedAdjustments massivi).

**7. Error case:**
- `BadRequestException`: Yuz rasmi bo'sh bo'lsa yoki noto'g'ri sana kelsa.
- `NotFoundException`: Xodim, Terminal topilmasa.
- `ConflictException`: Xodim rasmi bo'lmasa, check-in qilinmagan bo'lsa, allaqachon check-out qilingan bo'lsa yoki verifikatsiya darajasi past bo'lsa.
- `ForbiddenException`: Xodim bloklangan bo'lsa.

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: GET /api/v1/attendance
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance`
- Controller class + method nomi: `AttendanceController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceQueryDto` (`zdes_backend/src/modules/attendance/dto/attendance-query.dto.ts`) (Query parametrlar)
- Maydonlar:
  - `companyId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `branchId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `employeeId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `terminalId`: string (optional), `@IsOptional()`, `@IsUUID()`
  - `status`: AttendanceStatus (optional), `@IsOptional()`, `@IsEnum(AttendanceStatus)`
  - `dateFrom`: string (optional), `@IsOptional()`, `@IsISO8601({ strict: true })`
  - `dateTo`: string (optional), `@IsOptional()`, `@IsISO8601({ strict: true })`
  - `page`: number (optional), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
  - `limit`: number (optional), `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.findAll` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Bajaruvchining huquqlari bo'yicha filial yoki kompaniya ma'lumotlari filtrlanadi. Query parametrlar bo'yicha paginatsiya asosida Attendance jadvallarini sanaga va yaratilgan vaqtiga ko'ra kamayish tartibida ro'yxatini qaytaradi. Har bir element uchun salary adjustments ham yuklanadi.

**6. Response:**
- Qaytariladigan javob shakli (Paginatsiya):
  - `items`: [Attendance javob obyekti massivi (id, checkIn, status, va boshqalar qatori appliedAdjustments)]
  - `total`: number
  - `page`: number
  - `limit`: number
  - `totalPages`: number

**7. Error case:**
- Asosan ruxsatlar bilan bog'liq bo'lishi mumkin (masalan, scope dan tashqaridagi companyId kiritilsa).

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar (Qidiruv ushbu indekslarga tayanadi):
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`

---
### Endpoint: GET /api/v1/attendance/:id
**Controller:** zdes_backend/src/modules/attendance/attendance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/:id`
- Controller class + method nomi: `AttendanceController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- Qo'llangan guard'lar: class yoki metod darajasida `@UseGuards(...)` yo'q
- Ruxsat etilgan rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Yo'q (faqat Param: `id` ParseUUIDPipe)

**5. Service:**
- Chaqirilayotgan service method: `AttendanceService.findOne` (`zdes_backend/src/modules/attendance/services/attendance.service.ts`)
- Mantiq tavsifi: Baza ichidan belgilangan id yordamida Attendance yozuvini oladi. Bajaruvchi uchun scope ni tekshiradi va adjustmentlar ro'yxatini yuklab obyekt qilib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Bitta obyekt sifatida.
  - id: string
  - companyId: string
  - branchId: string | null
  - employeeId: string
  - terminalId: string | null
  - date: Date
  - checkIn: Date | null
  - checkOut: Date | null
  - status: AttendanceStatus
  - source: AttendanceSource
  - workStartTime: string | null
  - workEndTime: string | null
  - workedMinutes: number
  - lateMinutes: number
  - earlyLeaveMinutes: number
  - overtimeMinutes: number
  - checkInImageUrl: string | null
  - checkOutImageUrl: string | null
  - notes: string | null
  - faceSimilarity: number | undefined
  - appliedAdjustments: AttendanceAdjustmentDto[]
  - createdAt: Date
  - updatedAt: Date

**7. Error case:**
- `NotFoundException`: Agar Attendance bazada topilmasa.
- `ForbiddenException`: Agar topilgan yozuv foydalanuvchining huquq doirasida bo'lmasa (`assertWithinScope` orqali).

**8. DB struktura:**
Model: `Attendance`
- `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
- `companyId`: String, majburiy, `@db.Uuid`
- `branchId`: String?, ixtiyoriy, `@db.Uuid`
- `employeeId`: String, majburiy, `@db.Uuid`
- `terminalId`: String?, ixtiyoriy, `@db.Uuid`
- `date`: DateTime, majburiy, `@db.Date`
- `checkIn`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `checkOut`: DateTime?, ixtiyoriy, `@db.Timestamptz(6)`
- `status`: enum AttendanceStatus, majburiy, `@default(present)`
- `source`: enum AttendanceSource, majburiy, `@default(terminal)`
- `workStartTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workEndTime`: String?, ixtiyoriy, `@db.VarChar(10)`
- `workedMinutes`: Int, majburiy, `@default(0)`
- `lateMinutes`: Int, majburiy, `@default(0)`
- `earlyLeaveMinutes`: Int, majburiy, `@default(0)`
- `overtimeMinutes`: Int, majburiy, `@default(0)`
- `checkInImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `checkOutImageUrl`: String?, ixtiyoriy, `@db.VarChar(500)`
- `notes`: String?, ixtiyoriy
- `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
- `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`

Chiquvchi (Outgoing Relations):
- `Attendance.companyId -> Company.id (onDelete: Cascade)`
- `Attendance.branchId -> Branch.id (onDelete: SetNull)`
- `Attendance.employeeId -> User.id (onDelete: Cascade)`
- `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`

Kiruvchi (Incoming Relations):
- `RawAttendanceLog.attendanceId -> Attendance.id (onDelete: SetNull)`

Indekslar/Uniquelar:
- `@@unique([employeeId, date])`
- `@@index([companyId])`
- `@@index([branchId])`
- `@@index([employeeId])`
- `@@index([terminalId])`
- `@@index([date])`
- `@@index([status])`
### Endpoint: POST /api/v1/auth/login
**Controller:** src/modules/auth/controllers/auth.controller.ts:login

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/login`
- Controller class + method nomi: `AuthController.login`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- login: 'admin'
- password: '1234'
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `LoginDto` (`src/modules/auth/dto/login.dto.ts`)
- Har bir maydon:
  - `login`: `string`, `@IsString()`
  - `password`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.login` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Baza bo'yicha `login` yoki `email` orqali foydalanuvchini izlaydi va parolni tekshiradi (faqat superadmin, admin, manager ruxsat etilgan). Muvaffaqiyatli bo'lsa yangi refresh token yaratib bazaga (`RefreshToken` modeliga) yozadi va JWT access token hamda foydalanuvchi ma'lumotlarini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `tokenType`: `string` ('Bearer')
  - `accessToken`: `string`
  - `refreshToken`: `string`
  - `expiresIn`: `number`
  - `user`: ob'ekt (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('Login and password are required') - login yoki parol jo'natilmasa.
- `UnauthorizedException` ('Invalid login or password') - foydalanuvchi topilmasa yoki parol noto'g'ri bo'lsa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login. Employee users authenticate through turnstile integration.') - foydalanuvchi roli ruxsat etilmagan bo'lsa.
- `ForbiddenException` ('User is inactive') - foydalanuvchi faol bo'lmasa.
- `ForbiddenException` ('User is blocked') - foydalanuvchi bloklangan bo'lsa.

**8. DB struktura:**
- `User` modeli (o'qish):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `login`: `String @unique @db.VarChar(255)`
  - `email`: `String? @unique @db.VarChar(255)` (ixtiyoriy, `login` bo'yicha topilmasa shu orqali ham qidiriladi)
  - `passwordHash`: `String @db.VarChar(255)`
  - `role`: `UserRole @default(employee)` (enum)
  - `isActive`: `Boolean @default(true)`
  - `isBlocked`: `Boolean @default(false)`
  - `companyId`, `branchId`, `departmentId`, `positionId`: hammasi `String? @db.Uuid` (ixtiyoriy FK)
  - `firstName`, `lastName`, `middleName`, `phone`: `String? @db.VarChar(...)` (ixtiyoriy)
  - `employeeNo`: `String? @db.VarChar(100)`
  - `faceDeviceUserId`: `String? @db.VarChar(100)`
- **Relations (User):**
  - `User.companyId -> Company.id` (`onDelete: SetNull`)
  - `User.branchId -> Branch.id` (`onDelete: SetNull`)
  - `User.departmentId -> Department.id` (`onDelete: SetNull`)
  - `User.positionId -> Position.id` (`onDelete: SetNull`)
- `RefreshToken` modeli (yozish/create):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `userId`: `String @db.Uuid` (majburiy FK)
  - `token`: `String` (xeshlangan refresh token qiymati)
  - `expiresAt`: `DateTime @db.Timestamptz(6)` (majburiy)
  - `deviceType`: `String? @db.VarChar(100)` (ixtiyoriy)
  - `deviceName`: `String? @db.VarChar(255)` (ixtiyoriy)
  - `userAgent`: `String?` (ixtiyoriy)
  - `ipAddress`: `String? @db.VarChar(100)` (ixtiyoriy)
  - `lastUsedAt`: `DateTime? @db.Timestamptz(6)` (bu yozuvda `new Date()` bilan to'ldiriladi)
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade` — user o'chirilsa uning barcha refresh tokenlari ham o'chadi)
- **Indexlar:** `@@index([userId])`, `@@index([expiresAt])` (`RefreshToken`); `User.login`/`User.email` `@unique`.


### Endpoint: POST /api/v1/auth/refresh
**Controller:** src/modules/auth/controllers/auth.controller.ts:refresh

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/refresh`
- Controller class + method nomi: `AuthController.refresh`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- refreshToken: misol yo'q (`@ApiProperty()` — example ko'rsatilmagan)
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `RefreshTokenDto` (`src/modules/auth/dto/refresh-token.dto.ts`)
- Har bir maydon:
  - `refreshToken`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.refresh` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Berilgan refresh tokenni xeshlangan holatda bazadan qidiradi va amal qilish muddati o'tmaganligini tekshiradi. Muddat o'tgan bo'lsa, tokenni o'chiradi; agar amal qilsa `RefreshToken` ni so'nggi ishlatilgan vaqti va meta-ma'lumotlarini yangilaydi hamda yangi access token qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `tokenType`: `string` ('Bearer')
  - `accessToken`: `string`
  - `refreshToken`: mavjud emas (undefined)
  - `expiresIn`: `number`
  - `user`: ob'ekt (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('Refresh token is required') - refresh token jo'natilmasa.
- `UnauthorizedException` ('Refresh token is invalid') - token bazadan topilmasa.
- `UnauthorizedException` ('Refresh token expired') - tokenning amal qilish muddati tugagan bo'lsa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login...') - topilgan foydalanuvchi roli noto'g'ri bo'lsa.
- `ForbiddenException` ('User is inactive' / 'User is blocked') - foydalanuvchi bloklangan yoki faol bo'lmasa.

**8. DB struktura:**
- `RefreshToken` modeli (o'qish + yangilash):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `userId`: `String @db.Uuid` (majburiy FK)
  - `token`: `String` (xeshlangan qiymat bo'yicha qidiriladi, `findFirst`)
  - `expiresAt`: `DateTime @db.Timestamptz(6)` — muddat tekshiriladi, o'tgan bo'lsa yozuv o'chiriladi (`delete`)
  - `deviceType`, `deviceName`: `String? @db.VarChar(...)` (yangilanadi, `update`)
  - `userAgent`: `String?`, `ipAddress`: `String? @db.VarChar(100)` (yangilanadi)
  - `lastUsedAt`: `DateTime? @db.Timestamptz(6)` (yangilanadi, `new Date()`)
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade`) — `include: { user: true }` bilan birga o'qiladi
- `User` modeli (o'qish, `RefreshToken.user` orqali):
  - `id`, `login`, `role` (`UserRole`), `isActive` (`Boolean`), `isBlocked` (`Boolean`) — `ensureUserCanLogin` tekshiruvi uchun
  - `companyId`, `branchId`, `departmentId`, `positionId`: `String? @db.Uuid` — javobga qaytariladi
- **Relations (User, javobga qaytarilganda):**
  - `User.companyId -> Company.id`, `User.branchId -> Branch.id`,
    `User.departmentId -> Department.id`, `User.positionId -> Position.id`
    (barchasi `onDelete: SetNull`)
- **Indexlar:** `@@index([userId])`, `@@index([expiresAt])`.


### Endpoint: POST /api/v1/auth/logout
**Controller:** src/modules/auth/controllers/auth.controller.ts:logout

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/logout`
- Controller class + method nomi: `AuthController.logout`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- refreshToken: misol yo'q (`@ApiProperty()` — example ko'rsatilmagan)
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `RefreshTokenDto` (`src/modules/auth/dto/refresh-token.dto.ts`)
- Har bir maydon:
  - `refreshToken`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.logout` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Berilgan refresh tokenni xeshlangan holatda bazadan izlaydi va mos keluvchi yozuvlarni `RefreshToken` jadvalidan o'chiradi. Token bo'sh bo'lsa, xato bermasdan muvaffaqiyat holatini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `success`: `boolean` (`true`)

**7. Error case:**
- Ushbu endpoint to'g'ridan-to'g'ri xatolik (Exception) tashlamaydi. Noto'g'ri yoki bo'sh token yuborilsa ham `{ success: true }` qaytaradi.

**8. DB struktura:**
- `RefreshToken` modeli (o'chirish, `deleteMany`):
  - `token`: `String` — xeshlangan qiymat bo'yicha mos yozuvlar qidiriladi va o'chiriladi (`where: { token: ... }`)
  - Boshqa maydonlarga (`userId`, `expiresAt`, va h.k.) bu operatsiyada tegilmaydi, faqat `token` shart sifatida ishlatiladi.
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade`) — bu endpointda ishlatilmaydi (foydalanuvchi o'qilmaydi), lekin modelning o'zida mavjud.


### Endpoint: GET /api/v1/auth/me
**Controller:** src/modules/auth/controllers/auth.controller.ts:me

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/auth/me`
- Controller class + method nomi: `AuthController.me`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (GET so'rov, DTO ishlatilmaydi).

**3. Guard:**
- Qo'llangan guard'lar: Metod darajasida `@Roles('superadmin', 'admin', 'manager')`.
- Qaysi rollar ruxsat etilgan: `superadmin`, `admin`, `manager`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: Body qabul qilinmaydi, faqat tokendan kirgan user payloadi ishlatiladi (DTO yo'q, `@CurrentUser() user: AccessTokenPayload` ishlatilgan).

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.getCurrentUser` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Token orqali olingan foydalanuvchi id'si bo'yicha `User` jadvalidan ma'lumotlarni qidiradi. Uning faolligini tekshiradi va ruxsat berilgan bo'lsa, foydalanuvchining ochiq profil ma'lumotlarini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - Foydalanuvchi ob'ekti (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('User not found') - bazadan foydalanuvchi topilmasa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login...') - topilgan foydalanuvchi roli noto'g'ri bo'lsa.
- `ForbiddenException` ('User is inactive') - foydalanuvchi faol bo'lmasa.
- `ForbiddenException` ('User is blocked') - foydalanuvchi bloklangan bo'lsa.

**8. DB struktura:**
- `User` modeli (o'qish, `findUnique({ where: { id } })`):
  - `id`: `String @id @default(uuid()) @db.Uuid` (token payload'dagi `sub` bilan qidiriladi)
  - `login`, `role` (`UserRole`), `isActive` (`Boolean`), `isBlocked` (`Boolean`) — `ensureUserCanLogin` tekshiruvi uchun
  - `companyId`, `branchId`, `departmentId`, `positionId`: `String? @db.Uuid`
  - `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`: javobga qaytariladi
- **Relations (User):**
  - `User.companyId -> Company.id` (`onDelete: SetNull`)
  - `User.branchId -> Branch.id` (`onDelete: SetNull`)
  - `User.departmentId -> Department.id` (`onDelete: SetNull`)
  - `User.positionId -> Position.id` (`onDelete: SetNull`)
- **Indexlar:** `User.id` — `@id` (birlamchi kalit, qo'shimcha indeks shart emas).
### Endpoint: POST /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/branches`
- Controller class + method nomi: `BranchController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- name: 'Main Branch'
- address: 'Tashkent city, Chilonzor district'
- latitude: 41.2995
- longitude: 69.2401
- radius: 100

**3. Guard:**
- Token talab qilinadi (`@ApiBearerAuth()` va `@CurrentUser()` dekoratorlari yordamida `AccessTokenPayload` kutiladi)
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `CreateBranchDto` (`src/modules/branch/dto/create-branch.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `address`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `latitude`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsLatitude()`
- `longitude`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsLongitude()`
- `radius`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`

**5. Service:**
- Service method: `BranchService.create` (`src/modules/branch/branch.service.ts`)
- Kompaniya mavjudligini va branch nomining yagonaligini tekshiradi, so'ng yangi `Branch` yozuvini yaratadi. Yozuv radiusiga default qiymat sifatida 100 olinadi (agar kiritilmagan bo'lsa).

**6. Response:**
- Yaratilgan yangi `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Company not found") - Kompaniya topilmasa.
- `ConflictException` ("Branch name is required") - Branch nomi bo'sh jo'natilganda.
- `ConflictException` ("Branch name already exists in this company") - Shu kompaniyada bu nomli branch allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches`
- Controller class + method nomi: `BranchController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. (Query parametrlar)
- companyId: misol yo'q
- search: 'main'
- isActive: true
- page: 1
- limit: 10

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `BranchQueryDto` (`src/modules/branch/dto/branch-query.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `isActive`: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `BranchService.findAll` (`src/modules/branch/branch.service.ts`)
- DB'dan ko'rsatilgan filterlar (companyId, isActive, search) bo'yicha branch'lar ro'yxatini va jami sonini paginatsiya qilib o'qib keladi. `search` qiymati nomi va manzili bo'yicha izlanadi.

**6. Response:**
- Paginatsiya qilingan javob qaytadi:
  - `items`: Topilgan `Branch` obyektlari massivi
  - `total`: Umumiy elementlar soni (number)
  - `page`: Joriy sahifa (number)
  - `limit`: Sahifadagi limit (number)
  - `totalPages`: Jami sahifalar soni (number)

**7. Error case:**
- Alohida error tashlanmaydi (barcha query parametrlar ixtiyoriy). 

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO yo'q. Faqat route param `id` (`@Param('id', ParseUUIDPipe)`).

**5. Service:**
- Service method: `BranchService.findOne` (`src/modules/branch/branch.service.ts`)
- Berilgan UUID ID si bo'yicha branch ni izlaydi, agar foydalanuvchining ko'rishga ruxsati bo'lsa (scope tekshiruvidan o'tsa) javob sifatida qaytaradi.

**6. Response:**
- Topilgan bitta `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - ID orqali DB dan branch topilmaganda yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- name: 'Main Branch'
- address: 'Tashkent city, Chilonzor district'
- latitude: 41.2995
- longitude: 69.2401
- radius: 100

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `UpdateBranchDto` (`src/modules/branch/dto/update-branch.dto.ts`)
- Barcha `CreateBranchDto` maydonlari `PartialType` orqali ixtiyoriy (optional) bo'ladi.

**5. Service:**
- Service method: `BranchService.update` (`src/modules/branch/branch.service.ts`)
- Branche borligi tekshiriladi, berilgan ixtiyoriy field'larni avvalgilariga o'zgartiradi. Agar ismi yoki kompaniyasi o'zgarsa, yangi nomning unikal ligini tekshiradi va DB da saqlaydi.

**6. Response:**
- Yangilangan `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - Ko'rsatilgan ID bilan branch topilmasa.
- `NotFoundException` ("Company not found") - Agar companyId o'zgartirilmoqchi bo'lsa va bu company topilmasa.
- `ConflictException` ("Branch name is required") - Branch nomiga bo'sh satr jo'natilganda.
- `ConflictException` ("Branch name already exists in this company") - Shu kompaniyada bu yangi nomli branch allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/branches/:id/toggle-status
**Controller:** src/modules/branch/branch.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id/toggle-status`
- Controller class + method nomi: `BranchController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- isActive: false

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `ToggleBranchStatusDto` (`src/modules/branch/dto/toggle-branch-status.dto.ts`)
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Service method: `BranchService.toggleStatus` (`src/modules/branch/branch.service.ts`)
- ID bo'yicha filialni oladi. Agar status berilgan bo'lsa uni o'zlashtiradi, aks holda oldingisining teskarisi qilib yangilaydi (toggle).

**6. Response:**
- Yangilangan `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - Ko'rsatilgan ID bilan branch topilmasa yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO yo'q. Faqat route param `id` (`@Param('id', ParseUUIDPipe)`).

**5. Service:**
- Service method: `BranchService.delete` (`src/modules/branch/branch.service.ts`)
- ID bo'yicha DB'dan filial topiladi va tekshiriladi, ruxsat bo'lsa bu filial DB dan o'chirib tashlanadi (pastdagi "Relations" bandiga qarang — bu yerda CASCADE emas, balki SetNull ustunlik qiladi, ya'ni bog'liq yozuvlar o'chmaydi, faqat `branchId` ularda NULL bo'lib qoladi).

**6. Response:**
- JSON obyekt qaytadi:
  - `success`: `true`
  - `id`: o'chirilgan filialning id qiymati (string)

**7. Error case:**
- `NotFoundException` ("Branch not found") - ID orqali branch topilmasa yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (o'chiriladigan asosiy yozuv)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- **Relations / references — bu Branch modelining O'ZI qaysi modelga bog'liq:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Relations / references — Branch'ga qaysi modellar BOG'LANGAN (o'chirilganda ta'sirlanadi, barchasi `onDelete: SetNull`, ya'ni CASCADE emas — bog'liq qator o'chmaydi, faqat `branchId` NULL bo'ladi):**
  - `Department.branchId -> Branch.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
  - `Terminal.branchId -> Branch.id (onDelete: SetNull)`
  - `Attendance.branchId -> Branch.id (onDelete: SetNull)`
  - `Holiday.branchId -> Branch.id (onDelete: SetNull)`
  - `EmployeeLeave.branchId -> Branch.id (onDelete: SetNull)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

### Changes from commit d143c02 (order: 1)
- Service  updated: added default , uniqueness check for , new pagination in  (filters: companyId, search, isActive, page, limit).
- DTO  and  now include optional , , ,  with validation decorators.
- Controller  updated to reflect new query parameters and guards.
### Endpoint: POST /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/companies
- Controller class: CompanyController, method: create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
name: 'ZDES'
legalName: 'ZDES LLC'
phone: '+998901234567'
email: 'info@zdes.uz'
address: 'Tashkent city, Yunusobod district'
logoUrl: 'https://cdn.example.com/logos/zdes.png'

**3. Guard:**
- Class darajasida: `@Roles('superadmin')` (faqat superadmin ruxsat etilgan)
- Hech qanday `@Public()` qo'llanilmagan.

**4. DTO:**
- CreateCompanyDto (src/modules/company/dto/create-company.dto.ts)
- name: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- legalName: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- phone: string, `@IsOptional()`, `@IsString()`, `@MaxLength(50)`
- email: string, `@IsOptional()`, `@IsEmail()`, `@MaxLength(255)`
- address: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- logoUrl: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`

**5. Service:**
- CompanyService:create (src/modules/company/company.service.ts)
- Kompaniya nomini (name) normalizatsiya qilib (trimToNull orqali), uning yagonaligini (unique) tekshiradi va Prisma orqali bazaga yangi kompaniya yozuvini yaratadi.

**6. Response:**
- Yaratilgan Company obyekti to'liq qaytariladi.
- id: string
- name: string
- legalName: string | null
- phone: string | null
- email: string | null
- address: string | null
- logoUrl: string | null
- isActive: boolean
- stoppedAt: Date | null
- createdAt: Date
- updatedAt: Date

**7. Error case:**
- `ConflictException`: Kompaniya nomi kiritilmagan bo'lsa ('Company name is required') yoki shu nomdagi kompaniya allaqachon mavjud bo'lsa ('Company name already exists') (409 Conflict).

**8. DB struktura:**
- Model: `Company`
- O'qiydigan/yozadigan maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - name: String, majburiy, `@unique`, `@db.VarChar(255)`
  - legalName: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - phone: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - email: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - address: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - logoUrl: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - isActive: Boolean, majburiy, `@default(true)`
  - stoppedAt: DateTime, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references: Company modelida boshqa modelga ishora qiluvchi FK (`@relation(fields: [...])`) yo'q. Ammo bu boshqa modellar uchun asosiy (parent) model hisoblanadi.

---

### Endpoint: GET /api/v1/companies
**Controller:** src/modules/company/company.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/companies
- Controller class: CompanyController, method: findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.
Query parametrlari uchun misollar (CompanyQueryDto):
search: 'zdes' (misol yo'q qismidan olingan ApiPropertyOptional example)
isActive: true
page: 1
limit: 10

**3. Guard:**
- Class darajasida: `@Roles('superadmin')` (faqat superadmin ruxsat etilgan)

**4. DTO:**
- CompanyQueryDto (src/modules/company/dto/company-query.dto.ts)
- search: string, `@IsOptional()`, `@IsString()`
- isActive: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- page: number = 1, `@IsOptional()`, `@Type`, `@IsInt()`, `@Min(1)`
- limit: number = 10, `@IsOptional()`, `@Type`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- CompanyService:findAll (src/modules/company/company.service.ts)
- Kompaniyalar ro'yxatini paginatsiya (page, limit) va filter (isActive, search) bilan bazadan olib beradi. `search` qidiruvi `name`, `legalName`, `phone`, va `email` bo'yicha ishlaydi.

**6. Response:**
- Paginatsiya shaklidagi ob'ekt:
  - items: Company[] (Kompaniyalar ro'yxati)
  - total: number
  - page: number
  - limit: number
  - totalPages: number

**7. Error case:**
- Maxsus biznes mantiqi xatolari yo'q. Noto'g'ri so'rov parametrlari berilsa (masalan limit = 0), 400 Bad Request validatsiya xatosi chiqishi mumkin.

**8. DB struktura:**
- Model: `Company`
- O'qiladigan maydonlar: Barcha maydonlar o'qiladi (id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt). Ularning tiplari yuqoridagi Endpoint POST /api/v1/companies bo'limida keltirilganidek.
- Indekslar: 
  - `@@index([isActive])` (findAll usulida filterlash tezligi uchun ishlaydi).
- Relations / references: Hech qanday bog'lanish (FK) ishlatilmaydi.

---

### Endpoint: GET /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/companies/:id
- Controller class: CompanyController, method: findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- DTO class ishlatilmagan. Parametrda `id: string` qabul qilinadi (`ParseUUIDPipe` orqali validatsiya qilinadi).

**5. Service:**
- CompanyService:findOne (src/modules/company/company.service.ts)
- Berilgan UUID yordamida bazadan aniq bitta kompaniyani qidirib topib beradi. Topilmasa exception tashlaydi.

**6. Response:**
- Bitta to'liq Company obyekti (id, name, legalName, phone, email, address, logoUrl, isActive, stoppedAt, createdAt, updatedAt) qaytariladi.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha kompaniya bazadan topilmasa ('Company not found') (404 Not Found).
- 400 Bad Request: ID to'g'ri UUID formatida bo'lmasa (`ParseUUIDPipe` orqali).

**8. DB struktura:**
- Model: `Company`
- O'qiladigan maydon: `id` String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id` (va kompaniyaning boshqa barcha maydonlari qaytariladi).
- Relations / references: Company o'zida tashqi modelga `@relation` (fields bilan) yo'q.

---

### Endpoint: PATCH /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/companies/:id
- Controller class: CompanyController, method: update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
*(UpdateCompanyDto CreateCompanyDto'ning PartialType versiyasi bo'lgani uchun barcha misol qiymatlar o'zgarishsiz o'tadi)*
name: 'ZDES'
legalName: 'ZDES LLC'
phone: '+998901234567'
email: 'info@zdes.uz'
address: 'Tashkent city, Yunusobod district'
logoUrl: 'https://cdn.example.com/logos/zdes.png'

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- UpdateCompanyDto (src/modules/company/dto/update-company.dto.ts)
- PartialType(CreateCompanyDto) (barcha name, legalName, phone, email, address, logoUrl maydonlari ixtiyoriy holatda).

**5. Service:**
- CompanyService:update (src/modules/company/company.service.ts)
- Kompaniyani ID orqali qidirib topadi, yuborilgan yangi maydonlarni (agar mavjud bo'lsa) normalizatsiya qilib bazada yangilaydi. `name` yuborilgan bo'lsa boshqa kompaniyalar ismlari bilan to'qnashmasligini tekshiradi.

**6. Response:**
- Yangilangan Company obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa ('Company not found') (404 Not Found).
- `ConflictException`: Yangi uzatilgan `name` boshqa kompaniyada allaqachon mavjud bo'lsa ('Company name already exists') (409 Conflict).

**8. DB struktura:**
- Model: `Company`
- Yoziladigan (o'zgartirilishi mumkin bo'lgan) maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id` (qidiruv uchun)
  - name: String, majburiy, `@unique`, `@db.VarChar(255)`
  - legalName: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - phone: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - email: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - address: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - logoUrl: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references: FK bog'lanish ishlatilmaydi.

---

### Endpoint: PATCH /api/v1/companies/:id/toggle-status
**Controller:** src/modules/company/company.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- PATCH /api/v1/companies/:id/toggle-status
- Controller class: CompanyController, method: toggleStatus

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- ToggleCompanyStatusDto (src/modules/company/dto/toggle-company-status.dto.ts)
- isActive: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- CompanyService:toggleStatus (src/modules/company/company.service.ts)
- Kompaniyaning holatini faol yoki nofaol holatga o'tkazadi (isActive). Agar isActive=false qilinsa, qo'shimcha tarzda `stoppedAt` maydoniga hozirgi vaqtni yozib qo'yadi.

**6. Response:**
- Holati o'zgargan (yangilangan) Company obyekti qaytariladi.

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa (404 Not Found).

**8. DB struktura:**
- Model: `Company`
- O'qiydigan va yozadigan maydonlar:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - isActive: Boolean, majburiy, `@default(true)`
  - stoppedAt: DateTime, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Indekslar: `@@index([isActive])` (holati bo'yicha filterlarni tezlatish uchun yozilgan).

---

### Endpoint: DELETE /api/v1/companies/:id
**Controller:** src/modules/company/company.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/companies/:id
- Controller class: CompanyController, method: delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Class darajasida: `@Roles('superadmin')`

**4. DTO:**
- DTO yo'q. Parametrda id: string (`ParseUUIDPipe`).

**5. Service:**
- CompanyService:delete (src/modules/company/company.service.ts)
- Kompaniyaning mavjudligini ID orqali tekshiradi va topilsa bazadan o'chiradi.

**6. Response:**
- O'chirilganligini tasdiqlovchi ob'ekt: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: Kompaniya topilmasa ('Company not found') (404 Not Found).

**8. DB struktura:**
- Model: `Company`
- O'chiriladigan asosiy yozuv ID si qidiriladi:
  - id: String, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
- **Relations / references:** (O'chirish operatsiyasida Company'ga qaram bo'lgan jadvallar to'liq ta'sir qiladi, chunki ular quyidagicha bog'langan):
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
  - `Department.companyId -> Company.id (onDelete: Cascade)`
  - `Position.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `Terminal.companyId -> Company.id (onDelete: Cascade)`
  - `Attendance.companyId -> Company.id (onDelete: Cascade)`
  - `RawAttendanceLog.companyId -> Company.id (onDelete: Cascade)`
  - `SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)`
  - `Advance.companyId -> Company.id (onDelete: Cascade)`
  - `Holiday.companyId -> Company.id (onDelete: Cascade)`
  - `EmployeeLeave.companyId -> Company.id (onDelete: Cascade)`
  - `Payroll.companyId -> Company.id (onDelete: Cascade)`
  - `Setting.companyId -> Company.id (onDelete: Cascade)`
  - `User.companyId -> Company.id (onDelete: SetNull)`
  (Bu degani kompaniya o'chganda User'larda companyId NULL bo'ladi, boshqa barcha bog'langan ma'lumotlar esa zanjirli tarzda to'liq o'chib ketadi.)
# Dashboard — backend tahlili

**Topilma (Claude Code, 2026-07-25, AGY'siz — bu shunchaki "yo'qligini
tasdiqlash", alohida tahlil talab qilmaydi):**

`zdes_backend`da **alohida `dashboard` moduli/controller yo'q**
(`grep -rln dashboard src --include="*.controller.ts"` — natija bo'sh,
`find src -iname "*dashboard*"` — natija bo'sh). Demak `/api/v1/dashboard`
kabi yagona endpoint mavjud emas.

`test-zdes-front/src/app/features/dashboard/pages/dashboard/dashboard.ts`
da hozircha hech qanday servis chaqiruvi yo'q (statik/mock ko'rinishda).

## Faza 2 uchun tavsiya

Dashboard sahifasi alohida backend endpointga emas, balki **allaqachon
tahlil qilingan modullarning mavjud `GET` (ro'yxat/statistika) endpointlariga
tayanishi kerak** — masalan:

- `GET /api/v1/companies`, `GET /api/v1/branches`, `GET /api/v1/departments`,
  `GET /api/v1/positions` — umumiy sonlar (`total` maydoni paginatsiya
  javobida bor).
- `GET /api/v1/users` — xodimlar soni, `stats` maydoni (rol bo'yicha sanoq,
  `backend_crud_review/user.md` GET endpointida hujjatlangan).
- `GET /api/v1/attendance` — bugungi davomat statistikasi (filter: `date`).
- `GET /api/v1/payrolls`, `GET /api/v1/advances` — moliyaviy ko'rsatkichlar.
- `GET /api/v1/notifications` — so'nggi bildirishnomalar.

Agar Faza 2da dashboard uchun maxsus agregat endpoint kerak bo'lib qolsa
(masalan bitta so'rovda barcha statistikani qaytaruvchi `/api/v1/dashboard/
summary`) — bu **backendga yangi endpoint qo'shish** demak, ya'ni
`requirements.MD` 0-bo'limidagi "backend faqat o'qiladi, Fayzillo aniq
istisno bermaguncha" qoidasiga ko'ra alohida ruxsat so'ralishi shart.
# Department modulini backend tahlili

### Endpoint: POST /api/v1/departments
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `create`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/departments`
- Controller class + method nomi: `DepartmentController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `HR`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `CreateDepartmentDto` (`zdes_backend/src/modules/department/dto/create-department.dto.ts`)
- Har bir maydon:
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string | null`, `@IsOptional()`, `@IsUUID()`
  - `name`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Method: `DepartmentService.create` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Actor'ning ruxsat doirasi (scope) hamda tegishli company va branch mavjudligini tekshiradi. Ushbu nomdagi bo'lim allaqachon mavjud bo'lmasa, `Department` jadvaliga yangi yozuv (bo'lim) qo'shadi.

**6. Response:**
- Qaytariladigan javob: Yaratilgan `Department` obyekti (maydonlari: `id`, `companyId`, `branchId`, `name`, `isActive`, `createdAt`, `updatedAt`).

**7. Error case:**
- `NotFoundException`: Kiritilgan `companyId` yoki `branchId` topilmasa.
- `ConflictException`: Branch ushbu company'ga tegishli bo'lmasa, yoki xuddi shunday `name` bo'lgan bo'lim ushbu filial/kompaniyada allaqachon mavjud bo'lsa, yoxud `name` faqat bo'sh joylardan iborat bo'lsa.
- `ForbiddenException`: Obyekt yaratish ruxsat doirasidan (scope) tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department` (`prisma/schema.prisma` dan)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)` (fields: `[companyId]`)
  - `branch -> Branch.id (onDelete: SetNull)` (fields: `[branchId]`)
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/departments
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `findAll`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments`
- Controller class + method nomi: `DepartmentController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. (Query parametrlari uchun misollar: `search`: `hr`, `isActive`: `true`, `page`: `1`, `limit`: `10`)

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO (Query): `DepartmentQueryDto` (`zdes_backend/src/modules/department/dto/department-query.dto.ts`)
- Har bir maydon:
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `search`: `string`, `@IsOptional()`, `@IsString()`
  - `isActive`: `boolean`, `@IsOptional()`, `@Transform()`, `@IsBoolean()`
  - `page`: `number`, `@IsOptional()`, `@Type()`, `@IsInt()`, `@Min(1)`
  - `limit`: `number`, `@IsOptional()`, `@Type()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Method: `DepartmentService.findAll` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Foydalanuvchining ruxsat darajasiga qarab (scope) va filterlarga (`companyId`, `branchId`, `search`, `isActive`) mos keluvchi bo'limlar ro'yxatini va umumiy sonini ma'lumotlar bazasidan paginatsiya shaklida qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli (paginatsiya): `{ items: Department[], total: number, page: number, limit: number, totalPages: number }`

**7. Error case:**
- `ForbiddenException`: Scope yoki rol doirasida muammo bo'lsa (Access Token / Role).

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])` (Filter/search operatsiyalariga ta'sir qiluvchi indekslar)

---

### Endpoint: GET /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `findOne`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: Yo'q (Faqat Param orqali `id`, `ParseUUIDPipe` bilan olinadi).

**5. Service:**
- Method: `DepartmentService.findOne` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Berilgan UUID bo'yicha bo'limni ma'lumotlar bazasidan qidiradi, va so'rovchi ushbu bo'limni o'qishga (scope) haqli ekanini tasdiqlab, obyektni qaytaradi.

**6. Response:**
- Qaytariladigan javob: Topilgan `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: Topilgan bo'limga kirish actor'ning ruxsat doirasidan (scope) chetda bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `update`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `HR`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateDepartmentDto` (`zdes_backend/src/modules/department/dto/update-department.dto.ts`, `PartialType` bilan)
- Har bir maydon (barchasi ixtiyoriy):
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string | null`, `@IsOptional()`, `@IsUUID()`
  - `name`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Method: `DepartmentService.update` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Mavjud bo'limni tekshiradi, o'zgartirish doirasini ruxsat asosida tahlil qiladi (scope) va kiritilgan yangi ma'lumotlarni tekshirib (`name` va h.k.), `Department` obyektini bazada yangilaydi.

**6. Response:**
- Qaytariladigan javob: Yangilangan `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim yoxud bog'langan yangi kompaniya topilmasa.
- `ConflictException`: Yangi `name` bazada takrorlansa (aynan shu kompaniya va filial ichida) yoki filial kompaniyaga tegishli bo'lmasa.
- `ForbiddenException`: Obyekt o'zgartirish ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/departments/:id/toggle-status
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `toggleStatus`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id/toggle-status`
- Controller class + method nomi: `DepartmentController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `isActive`: `false`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `ToggleDepartmentStatusDto` (`zdes_backend/src/modules/department/dto/toggle-department-status.dto.ts`)
- Har bir maydon:
  - `isActive`: `boolean`, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Method: `DepartmentService.toggleStatus` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Bo'lim holatini (`isActive`) agarda parametrda uzatilgan bo'lsa shunga, aks holda esa bazadagi teskari holatga (`!department.isActive`) o'zgartiradi.

**6. Response:**
- Qaytariladigan javob: Yangilangan holatdagi `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: Obyekt o'zgartirish ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])` (Aynan shu jarayon shu ustun bilan ishlaydi)

---

### Endpoint: DELETE /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `delete`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: Yo'q (Param orqali `id` `ParseUUIDPipe` yordamida olinadi).

**5. Service:**
- Method: `DepartmentService.delete` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Bo'limni bazadan qidirib, agar topsa va o'chirishga huquq bo'lsa (scope tekshiruvi orqali), uni butunlay o'chirib tashlaydi.

**6. Response:**
- Qaytariladigan javob: Muvaffaqiyatni bildiruvchi obyekti: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: O'chiriladigan bo'lim actor'ning ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi — o'chirishda ta'siri):
  - `Position.departmentId -> Department.id (onDelete: SetNull)` — Ya'ni, ushbu Department o'chirilganda unga aloqador Position'larning departmentId maydoni NULL bo'lib qoladi, jadvallar kaskad o'chmaydi.
  - `User.departmentId -> Department.id (onDelete: SetNull)` — Xuddi shunday, o'chirilgan bo'limdagi xodimlarning (User) departmentId maydoni NULL qiymatiga o'tadi.
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`
### Endpoint: POST /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar)

**4. DTO:**
- Request DTO: `CreateEmployeeLeaveDto` (src/modules/employee-leave/dto/create-employee-leave.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsUUID()`
- `type`: Tip - LeaveType (enum), Validatorlar - `@IsEnum(LeaveType)`
- `fromDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `toDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `days`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@IsBoolean()`
- `reason`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Service method: `create` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Xodimni, kompaniya va filiallarni tekshiradi, kunlarni hisoblaydi (agar berilmagan bo'lsa) va `EmployeeLeave` jadvaliga yangi ta'til yozuvini qo'shadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti (aniq maydonlar: `id` (String), `companyId` (String), `branchId` (String?), `employeeId` (String), `type` (LeaveType), `fromDate` (DateTime), `toDate` (DateTime), `days` (Int), `affectsSalary` (Boolean), `reason` (String?), `createdById` (String?), `updatedById` (String?), `createdAt` (DateTime), `updatedAt` (DateTime)).

**7. Error case:**
- `NotFoundException`: 'Company not found' (kompaniya topilmasa), 'Branch not found' (filial topilmasa), 'Employee not found' (xodim topilmasa).
- `ConflictException`: 'Branch does not belong to the selected company' (filial tegishli emas), 'Employee does not belong to the selected company' (xodim tegishli emas), 'Employee does not belong to the selected branch' (xodim filialga tegishli emas).
- `BadRequestException`: 'Leave end date must be after start date' (sana xato bo'lsa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q (Boshqa modellar ushbu modelga ishora qilmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `type`: `vacation`
  - `affectsSalary`: `false`
  - `search`: `medical`
  - `dateFrom`: `2026-06-01`
  - `dateTo`: `2026-06-30`
  - `page`: `1`
  - `limit`: `10`
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `EmployeeLeaveQueryDto` (src/modules/employee-leave/dto/employee-leave-query.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `type`: Tip - LeaveType, Validatorlar - `@IsOptional()`, `@IsEnum(LeaveType)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- `search`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateFrom`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateTo`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `page`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `findAll` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Filterlar (kompaniya, xodim, filial, sana) bo'yicha ruxsat doirasida xodimlar ta'tillari ro'yxatini va paginatsiyani bazadan olib keladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
  - `items`: EmployeeLeave obyektlari massivi (Array)
  - `total`: Umumiy miqdor (Number)
  - `page`: Joriy sahifa (Number)
  - `limit`: Sahifadagi limit (Number)
  - `totalPages`: Jami sahifalar soni (Number)

**7. Error case:**
- Maxsus xatolik tashlamaydi (bazaviy exception'lar bo'lishi mumkin xolos).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string sifatida olinadi).

**5. Service:**
- Service method: `findOne` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Berilgan ID yordamida bitta ta'til yozuvini oladi va foydalanuvchining unga ruxsati borligini (scope) tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti.

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (berilgan id dagi ta'til topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: PATCH /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
(CreateEmployeeLeaveDto dan meros orqali olingan PartialType)
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateEmployeeLeaveDto` (src/modules/employee-leave/dto/update-employee-leave.dto.ts) - `PartialType(CreateEmployeeLeaveDto)`
- Maydonlar tip va validatorlari CreateEmployeeLeaveDto kabi, faqat barchasi ixtiyoriy bo'ladi.

**5. Service:**
- Service method: `update` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Mavjud ta'tilni topib tekshiradi va uzatilgan yangi ma'lumotlar bilan ma'lumotlar bazasida yozuvni yangilaydi (shuningdek sana oralig'ini qayta hisoblaydi).

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `EmployeeLeave` obyekti.

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (ta'til obyektini yoki kompaniya, xodim filialni topa olmasa).
- `ConflictException`: Kompaniya va filiallar mos tushmaganda.
- `BadRequestException`: 'Leave end date must be after start date' (Sana noto'g'ri bo'lganda).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: DELETE /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string).

**5. Service:**
- Service method: `delete` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Ta'til obyekti ID bo'yicha topiladi, scope orqali tekshiriladi va xavfsiz holatda o'chiriladi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: boolean, id: string }`

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (o'chirilishi kerak bo'lgan obyekt topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Kiruvchi reference'lar (ya'ni ushbu `EmployeeLeave` ni ko'rsatadigan boshqa modellar) butunlay YO'Q. (Yani EmployeeLeave o'chirilsa, hech qaysi boshqa jadvalga cascade yoki null qilib ta'sir ko'rsatmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`
### Endpoint: POST /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/holidays`
- Controller class + method nomi: `HolidayController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `Navruz holiday`
- `startDate`: `2026-03-21`
- `endDate`: `2026-03-22`
- `affectsSalary`: `false`
- `note`: `Official company holiday`

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `CreateHolidayDto` (src/modules/holiday/dto/create-holiday.dto.ts)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `startDate`: string, `@Type(() => String)`, `@IsDateString()`
- `endDate`: string, `@Type(() => String)`, `@IsDateString()`
- `affectsSalary`: boolean, `@IsOptional()`, `@IsBoolean()`
- `note`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Service method: `HolidayService.create` (src/modules/holiday/holiday.service.ts:create)
- Mantiq: Aktyor ruxsatlarini hisobga olgan holda kompaniya va (ixtiyoriy) filialni tekshiradi. Yozilgan sana oralig'ining to'g'riligini (endDate >= startDate) ham tekshiradi. Barcha shartlar bajarilganda, ma'lumotlar bazasida yangi Holiday (ta'til/bayram) yozuvini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan `Holiday` obyekti to'liq qaytariladi.
- Maydonlari: `id` (String), `companyId` (String), `branchId` (String, null bo'lishi mumkin), `name` (String), `startDate` (DateTime), `endDate` (DateTime), `affectsSalary` (Boolean), `note` (String, null bo'lishi mumkin), `createdById` (String), `updatedById` (String), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: "Company not found" - agar kompaniya topilmasa (404)
- `NotFoundException`: "Branch not found" - agar filial topilmasa (404)
- `ConflictException`: "Branch does not belong to the selected company" - agar filial boshqa kompaniyaga tegishli bo'lsa (409)
- `ConflictException`: "Holiday name is required" - agar nom bo'sh yoki faqat probellardan iborat bo'lsa (409)
- `BadRequestException`: "Holiday end date must be after start date" - agar tugash sanasi boshlanish sanasidan oldin bo'lsa (400)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif:
  - `id`: String, Majburiy, `@id`, `@default(uuid())`, `@db.Uuid`
  - `companyId`: String, Majburiy, `@db.Uuid`
  - `branchId`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `name`: String, Majburiy, `@db.VarChar(255)`
  - `startDate`: DateTime, Majburiy, `@db.Date`
  - `endDate`: DateTime, Majburiy, `@db.Date`
  - `affectsSalary`: Boolean, Majburiy, `@default(false)`
  - `note`: String, Ixtiyoriy (`?`)
  - `createdById`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: String, Ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `Company`: `companyId -> Company.id (onDelete: Cascade)`
  - `Branch`: `branchId -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - (Topilmadi - hech qaysi boshqa model Holiday modeliga ishora qilmaydi)
- Indekslar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([startDate])`
  - `@@index([endDate])`

---

### Endpoint: GET /api/v1/holidays
**Controller:** src/modules/holiday/holiday.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays`
- Controller class + method nomi: `HolidayController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (GET so'rovi bo'lgani uchun query parametrlar qabul qiladi).
- Query parametr misollari (`HolidayQueryDto` asosida):
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `search`: `navruz`
  - `affectsSalary`: `true`
  - `dateFrom`: `2026-03-01`
  - `dateTo`: `2026-03-31`
  - `page`: `1` (default: 1)
  - `limit`: `10` (default: 10)

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `HolidayQueryDto` (src/modules/holiday/dto/holiday-query.dto.ts)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `affectsSalary`: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- `dateFrom`: string, `@IsOptional()`, `@IsString()`
- `dateTo`: string, `@IsOptional()`, `@IsString()`
- `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `HolidayService.findAll` (src/modules/holiday/holiday.service.ts:findAll)
- Mantiq: Berilgan filtrlarga (qidiruv so'zi, companyId, branchId, affectsSalary, va sana oralig'i) va aktyor ruxsat doirasiga asoslanib `Holiday` modelidan ma'lumotlarni izlaydi. Paginatsiya qilingan (limit/page) qilib ro'yxat va umumiy sonini (`total`) qaytaradi. Sana bo'yicha filter qilinganda Date(dateFrom) va Date(dateTo) obyektlari asosida qoplanishlar tekshiriladi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya qilingan obyekt:
  - `items`: `Holiday` model obyektlar massivi
  - `total`: Topilgan barcha yozuvlar soni (Number)
  - `page`: Joriy sahifa raqami (Number)
  - `limit`: Bitta sahifadagi yozuvlar limiti (Number)
  - `totalPages`: Jami sahifalar soni (Number)

**7. Error case:**
- Boshqa maxsus xatolar ko'rsatilmagan (lekin avtorizatsiya va noto'g'ri so'rov xatoliklari bo'lishi mumkin).

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif (POST /api/v1/holidays dagi bilan bir xil).
- Relations / references (Chiquvchi va Kiruvchi) va Indekslar - yuqorida keltirilgandek bir xil. Paginatsiya va ro'yxat qidirish uchun `@@index([companyId])`, `@@index([branchId])`, `@@index([startDate])`, `@@index([endDate])` indekslar ishlatilishi nazarda tutilgan.

---

### Endpoint: GET /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. Faqat url ichida `id` parametri keladi.

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- DTO klassi yo'q. Parametr sifatida `id: string` (`ParseUUIDPipe` bilan) qabul qiladi.

**5. Service:**
- Service method: `HolidayService.findOne` (src/modules/holiday/holiday.service.ts:findOne)
- Mantiq: Berilgan `id` yordamida `Holiday` ni qidiradi va joriy foydalanuvchi (actor) uchun ushbu obyektga kirish ruxsati borligini tekshiradi (`assertWithinScope`). Topilsa qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Topilgan bitta `Holiday` obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: "Holiday not found" - agar ushbu `id` bilan yozuv topilmasa (404)
- `ForbiddenException`: "Access denied" (yoki `assertWithinScope` ichida otiladigan huquq etishmovchiligi xatosi, agar aktyor ushbu company/branch ga ruxsati bo'lmasa). (403 odatda)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif va bog'lanishlar - POST dagi kabi bir xil. Bitta obyekt bo'yicha ma'lumotlar olinadi.

---

### Endpoint: PATCH /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `UpdateHolidayDto` (CreateHolidayDto ning Partial ko'rinishi) quyidagi ehtimoliy qiymatlarga ega:
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `name`: `Navruz holiday`
  - `startDate`: `2026-03-21`
  - `endDate`: `2026-03-22`
  - `affectsSalary`: `false`
  - `note`: `Official company holiday`

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- Request DTO: `UpdateHolidayDto` (src/modules/holiday/dto/update-holiday.dto.ts) -> Bu `PartialType(CreateHolidayDto)` hisoblanadi.
- Barcha maydonlari (companyId, branchId, name, startDate, endDate, affectsSalary, note) ixtiyoriy (`@IsOptional()`). Validatsiya dekoratorlari xuddi `CreateHolidayDto` dagi kabi.

**5. Service:**
- Service method: `HolidayService.update` (src/modules/holiday/holiday.service.ts:update)
- Mantiq: Dastlab ko'rsatilgan `id` dagi holiday borligiga ishonch hosil qiladi va foydalanuvchining unga ruxsatini tekshiradi (`assertWithinScope`). So'ngra yangi kiritilgan ma'lumotlarga qarab tegishli `Company` va `Branch` larni bazada mavjudligini hamda aktyor ruxsatlarini qaytadan tekshiradi. Yana endDate >= startDate oraliq validatsiyasidan o'tadi va bazadagi ma'lumotni yangilaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Holiday` obyekti to'liq qaytariladi.

**7. Error case:**
- `NotFoundException`: "Holiday not found" - holiday topilmasa (404)
- (Yana `assertWithinScope` xatoligi ehtimoli)
- `NotFoundException`: "Company not found" (404)
- `NotFoundException`: "Branch not found" (404)
- `ConflictException`: "Branch does not belong to the selected company" (409)
- `ConflictException`: "Holiday name is required" (409)
- `BadRequestException`: "Holiday end date must be after start date" (400)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif, Relations va Indekslar POST bo'limidagi bilan aynan bir xil.

---

### Endpoint: DELETE /api/v1/holidays/:id
**Controller:** src/modules/holiday/holiday.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/holidays/:id`
- Controller class + method nomi: `HolidayController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@ApiBearerAuth()` orqali himoyalangan.
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar).

**4. DTO:**
- DTO klassi yo'q. URL ichidan `id` parametri `ParseUUIDPipe` orqali keladi.

**5. Service:**
- Service method: `HolidayService.delete` (src/modules/holiday/holiday.service.ts:delete)
- Mantiq: Yozuvni qidirib topadi, foydalanuvchining huquqlarini tekshiradi (`assertWithinScope`) va `Holiday` jadvalidan to'liq o'chirib yuboradi (hard delete). 

**6. Response:**
- Qaytariladigan javob shakli: `success` (Boolean) true qiymati va o'chirilgan holidayning `id` si qatnashgan obyekt: `{ success: true, id: string }`.

**7. Error case:**
- `NotFoundException`: "Holiday not found" (404)
- Ruxsat etishmovchiligi xatosi (`assertWithinScope` orqali) (403)

**8. DB struktura:**
- Tegishli Prisma model nomi: `Holiday` (`prisma/schema.prisma`)
- Har bir maydon uchun ta'rif (POST bilan bir xil).
- Relations / references (Chiquvchi):
  - `Company`: `companyId -> Company.id (onDelete: Cascade)`
  - `Branch`: `branchId -> Branch.id (onDelete: SetNull)`
- **Relations / references (Kiruvchi - O'chirilganda nima bo'ladi):**
  - Hech qaysi boshqa model ushbu `Holiday` modeliga xorijiy kalit (Foreign Key) orqali ishora qilmaydi. Shuning uchun o'chirish hech qanday boshqa modellarda to'g'ridan-to'g'ri o'zgarishga (masalan SetNull yoki Cascade delete) sabab bo'lmaydi. Xavfsiz o'chirish mumkin.
- Indekslar: yuqoridagi bo'limlardagidek.
### Endpoint: POST /api/v1/notifications
**Controller:** src/modules/notification/notification.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/notifications`
- Controller class + method nomi: `NotificationController` + `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: misol yo'q
title: 'Payroll ready'
message: 'June payroll has been prepared'
icon: NotificationIcon.money
isRead: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Request DTO: `CreateNotificationDto` (src/modules/notification/dto/create-notification.dto.ts)
- `userId`: `string`, `@IsOptional()`, `@IsUUID()`
- `title`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `message`: `string`, `@IsString()`, `@MinLength(1)`
- `icon`: `NotificationIcon`, `@IsOptional()`, `@IsEnum(NotificationIcon)`
- `isRead`: `boolean`, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Service method: `NotificationService.create` (src/modules/notification/notification.service.ts)
- Yangi bildirishnoma yaratadi (`Notification` jadvaliga yozadi). Agar actor superadmin bo'lmasa, `userId` bo'lishini talab qiladi va tegishli ruxsat (scope)larni tekshiradi.

**6. Response:**
- Yaratilgan `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `ForbiddenException`: 'userId is required for non-superadmin actors' (HTTP 403) - superadmin bo'lmaganlar uchun `userId` yo'q bo'lsa.
- `NotFoundException`: 'User not found' (HTTP 404) - kiritilgan `userId` mavjud bo'lmasa.
- `ForbiddenException` (HTTP 403) - kiritilgan user actor'ning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).
- `ConflictException`: 'Notification title is required' / 'Notification message is required' (HTTP 409) - bo'sh matn kiritilsa (`normalizeRequired` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: GET /api/v1/notifications
**Controller:** src/modules/notification/notification.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/notifications`
- Controller class + method nomi: `NotificationController` + `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Query parametrlari misollari:
userId: misol yo'q
icon: misol yo'q
isRead: false
search: 'payroll'
page: 1
limit: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Query DTO: `NotificationQueryDto` (src/modules/notification/dto/notification-query.dto.ts)
- `userId`: `string`, `@IsOptional()`, `@IsUUID()`
- `icon`: `NotificationIcon`, `@IsOptional()`, `@IsEnum(NotificationIcon)`
- `isRead`: `boolean`, `@IsOptional()`, `@IsBoolean()`
- `search`: `string`, `@IsOptional()`, `@IsString()`
- `page`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`
- `limit`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `NotificationService.findAll` (src/modules/notification/notification.service.ts)
- Bildirishnomalarni o'qiydi. Foydalanuvchining (actorning) companyId/branchId scope'iga qarab filtrlaydi, qidiruv va paginatsiya ishlatadi.

**6. Response:**
- Paginatsiya qilingan obyekt qaytaradi:
  - `items`: `Notification[]` massivi
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Maxsus xatolar ko'rsatilmagan (faqat default DTO validation xatoliklari bo'lishi mumkin).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: GET /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- DTO yo'q, faqat ID parametr: `@Param('id', ParseUUIDPipe) id: string`

**5. Service:**
- Service method: `NotificationService.findOne` (src/modules/notification/notification.service.ts)
- Berilgan ID bo'yicha bitta bildirishnomani bazadan o'qiydi va agar foydalanuvchiga tegishli (scope'iga mos) bo'lsa uni qaytaradi.

**6. Response:**
- Topilgan bitta `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403) - superadmin bo'lmagan shaxs `userId` si bo'lmagan xabarni ko'rmoqchi bo'lsa.
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: PATCH /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: misol yo'q
title: 'Payroll ready'
message: 'June payroll has been prepared'
icon: NotificationIcon.money
isRead: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Request DTO: `UpdateNotificationDto` (src/modules/notification/dto/update-notification.dto.ts, `CreateNotificationDto` ning Partial ko'rinishi)
- Hamma maydonlar ixtiyoriy.

**5. Service:**
- Service method: `NotificationService.update` (src/modules/notification/notification.service.ts)
- ID orqali bildirishnomani topib, uning qiymatlarini yangilaydi (faqat joriy foydalanuvchiga ruxsat etilgan scope'da ekanini tekshirib). `userId` o'zgarsa, uni ham scope bilan tekshiradi.

**6. Response:**
- Yangilangan bitta `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403).
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).
- `NotFoundException`: 'User not found' (HTTP 404) - yangi kiritilgan `userId` topilmasa.
- `ConflictException`: 'Notification title is required' / 'Notification message is required' (HTTP 409) - bo'sh matn kiritilsa.

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: DELETE /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- DTO yo'q, faqat ID parametr: `@Param('id', ParseUUIDPipe) id: string`

**5. Service:**
- Service method: `NotificationService.delete` (src/modules/notification/notification.service.ts)
- ID orqali bildirishnomani topadi, unga ruxsat etilganini tekshiradi va bazadan butunlay o'chirib tashlaydi.

**6. Response:**
- O'chirish bajarilgani to'g'risida success obyekti qaytariladi:
  - `{ success: true, id: <o'chirilgan id> }`

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403).
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`
### Endpoint: POST /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/payrolls
- PayrollController create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- month: 2026-06
- baseSalary: 4000000
- totalBonus: 500000
- totalPenalty: 100000
- totalAdvance: 200000
- netSalary: 4200000
- status: draft
- paidAt: 2026-06-30T10:00:00.000Z
- paidById: misol yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- CreatePayrollDto src/modules/payroll/dto/create-payroll.dto.ts
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- month: string, @IsString()
- baseSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalBonus: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalPenalty: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalAdvance: number, @IsOptional(), @Type(() => Number), @IsNumber()
- netSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- paidAt: string, @IsOptional(), @IsDateString()
- paidById: string, @IsOptional(), @IsUUID()

**5. Service:**
- create src/modules/payroll/payroll.service.ts
- Yaratilish jarayonida ruxsatlarni tekshiradi, company va employee borligini tekshiradi, shu oydagi xodimga tegishli payroll yo'qligini tekshirib keyin bazaga Payroll yozadi.

**6. Response:**
- Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Company not found' - company topilmasa
- NotFoundException: 'Employee not found' - employee topilmasa
- ConflictException: 'Employee does not belong to the selected company' - employee va company mos kelmasa
- ConflictException: 'Payroll month is required' - month probel bo'lsa
- NotFoundException: 'Paid by user not found' - to'lovchi foydalanuvchi topilmasa
- ConflictException: 'Payroll already exists for this employee and month' - unique constraint buzilsa (shu oydagi ishhaqi qilingan bo'lsa)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: GET /api/v1/payrolls
**Controller:** src/modules/payroll/payroll.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/payrolls
- PayrollController findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- PayrollQueryDto src/modules/payroll/dto/payroll-query.dto.ts
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsOptional(), @IsUUID()
- month: string, @IsOptional(), @IsString()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- page: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1)
- limit: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1), @Max(100)

**5. Service:**
- findAll src/modules/payroll/payroll.service.ts
- Ruxsat etilgan scope bo'yicha filterlab, page va limit yordamida ro'yxatni paginatsiya bilan qaytaradi.

**6. Response:**
- Paginatsiya qilingan javob qaytaradi:
  - items: Payroll[] (massiv)
  - total: number
  - page: number
  - limit: number
  - totalPages: number

**7. Error case:**
- (Ochiq tashlanadigan alohida Exception yo'q, default validation exception)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: GET /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/payrolls/:id
- PayrollController findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- (Request DTO yo'q, faqat ParseUUIDPipe)

**5. Service:**
- findOne src/modules/payroll/payroll.service.ts
- Id bo'yicha bazadan izlaydi va ruxsatlarini tekshirib obyektni qaytaradi.

**6. Response:**
- Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id li yozuv topilmasa

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: PATCH /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/payrolls/:id
- PayrollController update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- month: 2026-06
- baseSalary: 4000000
- totalBonus: 500000
- totalPenalty: 100000
- totalAdvance: 200000
- netSalary: 4200000
- status: draft
- paidAt: 2026-06-30T10:00:00.000Z
- paidById: misol yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- UpdatePayrollDto src/modules/payroll/dto/update-payroll.dto.ts (PartialType)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- month: string, @IsString()
- baseSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalBonus: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalPenalty: number, @IsOptional(), @Type(() => Number), @IsNumber()
- totalAdvance: number, @IsOptional(), @Type(() => Number), @IsNumber()
- netSalary: number, @IsOptional(), @Type(() => Number), @IsNumber()
- status: PayrollStatus, @IsOptional(), @IsEnum(PayrollStatus)
- paidAt: string, @IsOptional(), @IsDateString()
- paidById: string, @IsOptional(), @IsUUID()

**5. Service:**
- update src/modules/payroll/payroll.service.ts
- Mavjud yozuvni topib, ma'lumotlarini ruxsatlar bilan tahrirlaydi (jumladan unique payroll bor-yo'qligini employee va oy bo'yicha tekshiradi).

**6. Response:**
- Yangilangan Payroll obyektini qaytaradi (id, companyId, employeeId, month, baseSalary, totalBonus, totalPenalty, totalAdvance, netSalary, status, paidAt, paidById, createdById, updatedById, createdAt, updatedAt)

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id bo'yicha ishhaqi topilmasa
- NotFoundException: 'Company not found' - company topilmasa
- NotFoundException: 'Employee not found' - employee topilmasa
- ConflictException: 'Employee does not belong to the selected company' - employee va company mos kelmasa
- ConflictException: 'Payroll month is required' - month probel bo'lsa
- NotFoundException: 'Paid by user not found' - to'lovchi foydalanuvchi topilmasa
- ConflictException: 'Payroll already exists for this employee and month' - unique constraint buzilsa (boshqa id li)

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])

### Endpoint: DELETE /api/v1/payrolls/:id
**Controller:** src/modules/payroll/payroll.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/payrolls/:id
- PayrollController delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- (Request DTO yo'q, faqat ParseUUIDPipe)

**5. Service:**
- delete src/modules/payroll/payroll.service.ts
- Bazadan yozuvni izlaydi va o'chirib tashlaydi.

**6. Response:**
- `{ success: true, id: string }`

**7. Error case:**
- NotFoundException: 'Payroll not found' - berilgan id bo'yicha ishhaqi topilmasa

**8. DB struktura:**
- Model: Payroll
- id: String @id @default(uuid()) @db.Uuid
- companyId: String @db.Uuid
- employeeId: String @db.Uuid
- month: String @db.VarChar(7)
- baseSalary: Decimal @default(0) @db.Decimal(15, 2)
- totalBonus: Decimal @default(0) @db.Decimal(15, 2)
- totalPenalty: Decimal @default(0) @db.Decimal(15, 2)
- totalAdvance: Decimal @default(0) @db.Decimal(15, 2)
- netSalary: Decimal @default(0) @db.Decimal(15, 2)
- status: PayrollStatus @default(draft)
- paidAt: DateTime? @db.Timestamptz(6)
- paidById: String? @db.Uuid
- createdById: String? @db.Uuid
- updatedById: String? @db.Uuid
- createdAt: DateTime @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime @updatedAt @db.Timestamptz(6)
- Chiquvchi:
  - Company.companyId -> Company.id (onDelete: Cascade)
  - User.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi:
  - (Yo'q)
- Index/Unique:
  - @@unique([employeeId, month])
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([status])
### Endpoint: POST /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/positions`
- Controller class + method nomi: `PositionController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
departmentId: 'uuid-department-id'
name: 'Backend Developer'

**3. Guard:**
- Qo'llangan guard'lar: Metodda emas, Controller darajasida `@ApiBearerAuth()` va `@Roles(...)` qo'llangan.
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `CreatePositionDto` (`src/modules/position/dto/create-position.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `departmentId`: string, `@IsOptional()`, `@IsUUID()`
  - `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.create` (`src/modules/position/position.service.ts`)
- Mantiq: Foydalanuvchi roli asosida (masalan manager uchun majburiy departmentId tekshiruvi bilan) ruxsatlarni aniqlaydi. Ko'rsatilgan nom, kompaniya va departament bo'yicha unikallikni ta'minlaydi va yangi `Position` yozuvini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan `Position` obyekti. (Maydonlari: `id` (String), `companyId` (String), `departmentId` (String?), `name` (String), `isActive` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime)).

**7. Error case:**
- `NotFoundException`: 'Company not found' yoki 'Department not found'
- `ForbiddenException`: 'departmentId is required to create a position within your branch' yoki "You cannot access another branch's department"
- `ConflictException`: 'Department does not belong to the selected company', 'Position name already exists for this company and department', yoki 'Position name is required'

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi (bu model → boshqa model):
     - `Company`: `fields: [companyId]`, `references: [id]`, `onDelete: Cascade`
     - `Department`: `fields: [departmentId]`, `references: [id]`, `onDelete: SetNull`
  2. Kiruvchi (boshqa modellar → bu model):
     - `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar:
  - `@@unique([companyId, departmentId, name])`
  - `@@index([companyId])`
  - `@@index([departmentId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions`
- Controller class + method nomi: `PositionController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Qidiruv parametrlari uchun misollar (Query DTO):
search: 'developer'
isActive: true
page: 1
limit: 10
companyId: misol yo'q
departmentId: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `PositionQueryDto` (`src/modules/position/dto/position-query.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `departmentId`: string, `@IsOptional()`, `@IsUUID()`
  - `search`: string, `@IsOptional()`, `@IsString()`
  - `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`, `@Transform` qilingan
  - `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
  - `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.findAll` (`src/modules/position/position.service.ts`)
- Mantiq: Foydalanuvchining filiali va kompaniyasini inobatga olgan holda ro'yxatni filtrlaydi. Qidiruv kalit so'zi (`search`) va `isActive` bo'yicha filterlarni qo'llaydi, hamda ma'lumotlarni paginatsiya (skip, take) qilib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya obyekti.
  - `items`: `Position` obyektlari massivi
  - `total`: jami soni (Int)
  - `page`: joriy sahifa (Int)
  - `limit`: sahifa sig'imi (Int)
  - `totalPages`: jami sahifalar soni (Int)

**7. Error case:**
- Validatsiya (class-validator) xatolaridan tashqari to'g'ridan-to'g'ri exceptionlar tashlanmaydi, lekin guard'lar tomonidan ruxsat berilmagan xatolar (Forbidden) ehtimoli mavjud.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: (yuqoridagi kabi, barcha qidiriladigan va qaytadigan maydonlar `Position` modeliga tegishli).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Company` (Cascade), `Department` (SetNull)
  2. Kiruvchi: `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar: `@@index([companyId])`, `@@index([departmentId])`, `@@index([isActive])`, hamda qidiruv uchun qulaylik.

---

### Endpoint: GET /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Param: `id` (UUID)

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Alohida DTO klassi yo'q, `ParseUUIDPipe` orqali id qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.findOne` (`src/modules/position/position.service.ts`)
- Mantiq: Berilgan ID asosida bazadan pozitsiyani izlaydi. Foydalanuvchining tegishli kompaniya va filialga doir ma'lumotlarini tekshiradi (manager faqat o'z filialidagi pozitsiyalarni ko'ra oladi).

**6. Response:**
- Qaytariladigan javob shakli: Topilgan `Position` obyekti (faqat bitta).

**7. Error case:**
- `NotFoundException`: 'Position not found' (agar topilmasa)
- `ForbiddenException`: 'You cannot access a position outside your branch' yoki "You cannot access another branch's data" (manager o'z vakolatidan chetga chiqsa). Va `assertWithinScope` orqali umuman kompaniyaga kirish ruxsati tekshiriladi.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi, Relations va Indekslar `POST` va `GET` holatlaridagi bilan aynan bir xil. (Kiruvchi relation o'chirish yoki o'zgartirish bo'lmagani uchun to'g'ridan-to'g'ri ta'sir etmaydi, lekin model ta'rifining bir qismidir).

---

### Endpoint: PATCH /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id' (ixtiyoriy, UpdatePositionDto orqali)
departmentId: 'uuid-department-id' (ixtiyoriy)
name: 'Backend Developer' (ixtiyoriy)

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `UpdatePositionDto` (`src/modules/position/dto/update-position.dto.ts`) (CreatePositionDto dan meros olingan).
- Maydonlar: Barcha maydonlar (`companyId`, `departmentId`, `name`) `PartialType` bo'lgani uchun ixtiyoriy hisoblanadi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.update` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiyani topadi va unga tegishli ruxsatlarni tekshiradi. Yuborilgan qiymatlar (masalan nom o'zgarganda) asosida yangi ismning kompaniya/departament miqyosida ochiq (band emasligini) tekshiradi va pozitsiyani yangilaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Position` obyekti.

**7. Error case:**
- `NotFoundException`: 'Position not found' yoki 'Company not found' yoki 'Department not found'
- `ForbiddenException`: 'departmentId is required to keep a position within your branch', yoki ruxsat qilinmagan hududdagi ma'lumotga kirishda
- `ConflictException`: 'Position name already exists for this company and department', 'Position name is required', 'Department does not belong to the selected company'

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: (Oldingi endpointlar bilan aynan bir xil).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Company` (Cascade), `Department` (SetNull)
  2. Kiruvchi: `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar: `@@unique([companyId, departmentId, name])` (tahrirlashda nom takroriyligi shu orqali baholanadi).

---

### Endpoint: PATCH /api/v1/positions/:id/toggle-status
**Controller:** src/modules/position/position.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id/toggle-status`
- Controller class + method nomi: `PositionController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `TogglePositionStatusDto` (`src/modules/position/dto/toggle-position-status.dto.ts`)
- Maydonlar:
  - `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.toggleStatus` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiyaning mavjud holatini tekshiradi, ruxsatlari mos bo'lsa `isActive` qiymatini kiritilgan holatga (yoki teskarisiga) o'zgartiradi va saqlaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Position` obyekti (o'zgartirilgan `isActive` statusi bilan).

**7. Error case:**
- `NotFoundException`: 'Position not found'
- `ForbiddenException`: O'z filialidan/vakolatidan tashqaridagi ma'lumotga ta'sir qilishda.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: Asosan `isActive` maydoniga yoziladi.
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - boshqalari: (yuqoridagi kabi)
- Relations / references: (yuqoridagi kabi).
- Tegishli indekslar: `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Alohida DTO klassi yo'q, faqat ID parametr `ParseUUIDPipe` orqali yuboriladi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.delete` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiya obyektini avval izlab topib (va foydalanuvchining unga ruxsati borligiga ishonch hosil qilib), undan so'ng bazadan o'chiradi.

**6. Response:**
- Qaytariladigan javob shakli: Muvaffaqiyat (success obyekti): `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: 'Position not found'
- `ForbiddenException`: "You cannot access another branch's data" (ruxsati bo'lmagan branch).

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: Barcha maydonlar o'chib ketadi (id: String...).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi (bu model → boshqa model):
     - `Company`: `fields: [companyId]`, `references: [id]`, `onDelete: Cascade`
     - `Department`: `fields: [departmentId]`, `references: [id]`, `onDelete: SetNull`
  2. Kiruvchi (boshqa modellar → bu model) — MAJBURIY o'chirish harakati natijasi:
     - `User.positionId -> Position.id (onDelete: SetNull)`
       (Bu degani: Position o'chirilganda, shu pozitsiyada ishlagan foydalanuvchilar (`User`) o'chib ketmaydi, faqatgina ularning `positionId` maydoni `NULL` qiymat qabul qiladi.)
- Tegishli indekslar: Unikallik uchun bo'lgan barcha indekslar.
# SalaryAdjustment modulini backend tahlili

### Endpoint: POST /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/salary-adjustments
- SalaryAdjustmentController create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- type: AdjustmentType.bonus
- category: AdjustmentCategory.manual
- amount: 150000
- date: 2026-06-08
- month: 2026-06
- reason: Manual bonus

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: CreateSalaryAdjustmentDto (src/modules/salary-adjustment/dto/create-salary-adjustment.dto.ts)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- type: AdjustmentType, @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- amount: number, @Type(() => Number), @IsNumber()
- date: string, @IsDateString()
- month: string, @IsOptional(), @IsString()
- reason: string, @IsOptional(), @IsString(), @MaxLength(1000)

**5. Service:**
- Service method: salaryAdjustmentService.create (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Kiritilgan ma'lumotlarga asosan yangi oylik tuzatish (salary adjustment) yozuvini `SalaryAdjustment` jadvaliga saqlaydi. Bunga qadar kompaniya va xodimning berilgan doira (scope) ichida ekanligini tekshiradi (ensureCompanyExists, ensureEmployeeInScope).

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan oylik tuzatish obyekti (aniq qaytadigan tiplar prisma modelidagi tiplardir)
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Company not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Employee not found' (shart bajarilmasa, HTTP 404)
- ConflictException: 'Employee does not belong to the selected company' (shart bajarilmasa, HTTP 409)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: GET /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/salary-adjustments
- SalaryAdjustmentController findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q
- companyId: misol yo'q
- employeeId: misol yo'q
- type: misol yo'q
- category: misol yo'q
- month: 2026-06
- search: bonus
- dateFrom: 2026-06-01
- dateTo: 2026-06-30
- page: 1
- limit: 10

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: SalaryAdjustmentQueryDto (src/modules/salary-adjustment/dto/salary-adjustment-query.dto.ts)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsOptional(), @IsUUID()
- type: AdjustmentType, @IsOptional(), @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- month: string, @IsOptional(), @IsString()
- search: string, @IsOptional(), @IsString()
- dateFrom: string, @IsOptional(), @IsString()
- dateTo: string, @IsOptional(), @IsString()
- page: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1)
- limit: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1), @Max(100)

**5. Service:**
- Service method: salaryAdjustmentService.findAll (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Mavjud oylik tuzatishlarni filtrlar, qidiruv va paginatsiya orqali `SalaryAdjustment` jadvalidan o'qib keladi. Natijalarni ro'yxat va jami soni bilan qaytaradi.

**6. Response:**
- Paginatsiya obyekti qaytadi:
  - items: SalaryAdjustment[] (oylik tuzatishlar massivi)
  - total: number (jami yozuvlar soni)
  - page: number (joriy sahifa)
  - limit: number (sahifadagi yozuvlar chegarasi)
  - totalPages: number (jami sahifalar soni)

**7. Error case:**
- ForbiddenException: Agar scope dan tashqarida bo'lsa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: GET /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/salary-adjustments/:id
- SalaryAdjustmentController findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO yo'q
- @Param('id') id: string, ParseUUIDPipe

**5. Service:**
- Service method: salaryAdjustmentService.findOne (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Bitta aniq ID ga ega oylik tuzatishni topadi va foydalanuvchining huquq doirasidaligini tekshirib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Topilgan oylik tuzatish obyekti
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (agar topilmasa, HTTP 404)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: PATCH /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/salary-adjustments/:id
- SalaryAdjustmentController update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- type: AdjustmentType.bonus
- category: AdjustmentCategory.manual
- amount: 150000
- date: 2026-06-08
- month: 2026-06
- reason: Manual bonus

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: UpdateSalaryAdjustmentDto (src/modules/salary-adjustment/dto/update-salary-adjustment.dto.ts) (PartialType of CreateSalaryAdjustmentDto)
- Barcha maydonlar ixtiyoriy:
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- type: AdjustmentType, @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- amount: number, @Type(() => Number), @IsNumber()
- date: string, @IsDateString()
- month: string, @IsOptional(), @IsString()
- reason: string, @IsOptional(), @IsString(), @MaxLength(1000)

**5. Service:**
- Service method: salaryAdjustmentService.update (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Mavjud oylik tuzatish yozuvini yangilaydi, agar kompaniya yoki xodim ID o'zgarsa yana huquq va mavjudlikni tekshiradi, keyin o'zgarishlarni ma'lumotlar bazasida `SalaryAdjustment` modeliga saqlaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan oylik tuzatish obyekti
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Company not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Employee not found' (shart bajarilmasa, HTTP 404)
- ConflictException: 'Employee does not belong to the selected company' (shart bajarilmasa, HTTP 409)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: DELETE /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/salary-adjustments/:id
- SalaryAdjustmentController delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO yo'q
- @Param('id') id: string, ParseUUIDPipe

**5. Service:**
- Service method: salaryAdjustmentService.delete (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Berilgan ID ga mos oylik tuzatish yozuvini bazadan o'chiradi, avval uning huquq doirasidaligini tekshiradi.

**6. Response:**
- Obyekt qaytadi:
  - success: boolean (true)
  - id: string (o'chirilgan yozuv id si)

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (shart bajarilmasa, HTTP 404)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q (bu o'chirilganda boshqa hech narsa o'chmaydi yoki ta'sirlanmaydi)
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])
### Endpoint: POST /api/v1/settings
**Controller:** src/modules/setting/setting.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/settings
- SettingController.create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `key`: attendance_kpi_template
- `value`: { "latePenaltyPerMinute": 1000 }

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `CreateSettingDto` (src/modules/setting/dto/create-setting.dto.ts)
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `key`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `value`: `Record<string, unknown>`, `@IsOptional()`, `@IsObject()`

**5. Service:**
- `SettingService.create` (src/modules/setting/setting.service.ts)
- Yangi sozlamani (Setting) yaratadi. Avval company mavjudligi tekshiriladi, so'ngra shu kompaniya uchun xuddi shu `key` (kalit) bilan boshqa sozlama yo'qligi tekshiriladi (yagona bo'lishi kerak). So'ng bazaga yoziladi.

**6. Response:**
- `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Company not found" (Agar company topilmasa, HTTP 404)
- `ConflictException`: "Setting key is required" (Agar key bo'sh yoki probellardan iborat bo'lsa, HTTP 409)
- `ConflictException`: "Setting key already exists for this company" (Agar key takrorlansa, HTTP 409)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q (Boshqa modellar `Setting`ga bog'lanmagan)
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: GET /api/v1/settings
**Controller:** src/modules/setting/setting.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/settings
- SettingController.findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `SettingQueryDto` (src/modules/setting/dto/setting-query.dto.ts)
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `search`: `string`, `@IsOptional()`, `@IsString()` (misol: 'attendance')
- `page`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)` (misol: 1)
- `limit`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)` (misol: 10)

**5. Service:**
- `SettingService.findAll` (src/modules/setting/setting.service.ts)
- Sozlamalarni filter (search `key` bo'yicha) va kompaniya doirasida (`companyId`) paginatsiya bilan qaytaradi.

**6. Response:**
- Paginatsiya obyekti:
  - `items`: `Setting` qatorlari massivi
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Xatoliklar tashlanmaydi (Faqat validatsiya xatolari bo'lishi mumkin)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: GET /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/settings/:id
- SettingController.findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- Request body DTO yo'q, URL param `id`: `string`, `ParseUUIDPipe` bilan tasdiqlanadi.

**5. Service:**
- `SettingService.findOne` (src/modules/setting/setting.service.ts)
- Berilgan ID ga ko'ra sozlamani qidiradi va joriy foydalanuvchining ko'rish huquqini (scope) tekshiradi.

**6. Response:**
- `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali chiqishi mumkin)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: PATCH /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/settings/:id
- SettingController.update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `key`: attendance_kpi_template
- `value`: { "latePenaltyPerMinute": 1000 }

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `UpdateSettingDto` (src/modules/setting/dto/update-setting.dto.ts) -> `PartialType(CreateSettingDto)`
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `key`: `string`, `@IsOptional()`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `value`: `Record<string, unknown>`, `@IsOptional()`, `@IsObject()`

**5. Service:**
- `SettingService.update` (src/modules/setting/setting.service.ts)
- Sozlamani id bo'yicha yangilaydi. Agar `key` yoki `companyId` o'zgarayotgan bo'lsa, ularning bazada unikalligi (`ensureUniqueKey`) va company mavjudligi (`ensureCompanyExists`) tekshiriladi.

**6. Response:**
- Yangilangan `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- `NotFoundException`: "Company not found" (Agar companyId yuborilgan bo'lsa va topilmasa, HTTP 404)
- `ConflictException`: "Setting key is required" (Agar key bo'sh bo'lib qolsa, HTTP 409)
- `ConflictException`: "Setting key already exists for this company" (Agar yangi key takrorlansa, HTTP 409)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: DELETE /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/settings/:id
- SettingController.delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- Request body DTO yo'q, URL param `id`: `string`, `ParseUUIDPipe` bilan tasdiqlanadi.

**5. Service:**
- `SettingService.delete` (src/modules/setting/setting.service.ts)
- Sozlamani id bo'yicha qidirib, foydalanuvchi scope-da ekanligini tekshiradi va bazadan o'chirib yuboradi.

**6. Response:**
- Ob'ekt qaytariladi: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`
# Terminal Moduli Backend Tahlili

### Endpoint: POST /api/v1/terminals
**Controller:** src/modules/terminal/terminal.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/terminals` (API global prefix qo'shilishi hisobga olingan holda)
- Controller class + method nomi: `TerminalController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- branchId: misol yo'q
- name: 'Main gate terminal'
- serialNumber: 'TRN-001'
- ipAddress: '192.168.1.100'
- port: 4370
- type: TerminalType.zkteco_face
- status: TerminalStatus.active
- connectionConfig: { username: 'admin', password: '12345' }
- lastSyncAt: '2026-06-08T10:00:00.000Z'

**3. Guard:**
- Class darajasida qo'llanilgan Guard'lar yo'q lekin dekoratorlar mavjud:
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `CreateTerminalDto` (`src/modules/terminal/dto/create-terminal.dto.ts`)
- companyId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- branchId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- name: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- serialNumber: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- ipAddress: `string | undefined`, `@IsOptional()`, `@IsIP()`
- port: `number | undefined`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(65535)`
- type: `TerminalType | undefined`, `@IsOptional()`, `@IsEnum(TerminalType)`
- status: `TerminalStatus | undefined`, `@IsOptional()`, `@IsEnum(TerminalStatus)`
- connectionConfig: `Record<string, unknown> | undefined`, `@IsOptional()`, `@IsObject()`
- lastSyncAt: `string | undefined`, `@IsOptional()`, `@IsString()`

**5. Service:**
- Service method: `TerminalService.create` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Yuborilgan `companyId` va `branchId` asosida joriy foydalanuvchining (actor) vakolatlari tekshiriladi (resolveCompanyBranchScope). Ko'rsatilgan company va branch mavjudligi hamda branch berilgan company'ga tegishliligi tasdiqlanadi. Serial raqami tizimda takrorlanmasligi tekshirib, xatosiz holatda yangi Terminal bazada yaratiladi.

**6. Response:**
- Qaytariladigan javob: Yangi yaratilgan `Terminal` obyekti to'liqligicha qaytariladi. Maydonlar: `id`, `companyId`, `branchId`, `name`, `serialNumber`, `ipAddress`, `port`, `type`, `status`, `connectionConfig`, `lastSyncAt`, `createdAt`, `updatedAt`.

**7. Error case:**
- `NotFoundException('Company not found')`: Agar berilgan companyId bo'yicha kompaniya topilmasa.
- `NotFoundException('Branch not found')`: Agar berilgan branchId bo'yicha filial topilmasa.
- `ConflictException('Branch does not belong to the selected company')`: Agar tanlangan filial ko'rsatilgan kompaniyaga tegishli bo'lmasa.
- `ConflictException('Terminal name is required')`: Agar nom probellardan iborat bo'lsa yoki noto'g'ri bo'lsa (400 Bad Request validatsiyadan tashqari).
- `ConflictException('Serial number is required')`: Agar serial raqami bo'sh bo'lsa.
- `ConflictException('Terminal serial number already exists')`: Agar xuddi shu serial raqamli terminal bazada allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi:
  - `id`: `String`, majburiy, `@id`, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `serialNumber`: `String`, majburiy, `@unique`, `@db.VarChar(255)`
  - `ipAddress`: `String`, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `port`: `Int`, ixtiyoriy (`?`)
  - `type`: `TerminalType`, majburiy, `@default(zkteco_face)`
  - `status`: `TerminalStatus`, majburiy, `@default(active)`
  - `connectionConfig`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `lastSyncAt`: `DateTime`, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  - **Chiquvchi:**
    - `Company.id` ga ishora qiluvchi maydon: `company -> Company` (`fields: [companyId]`, `references: [id]`, `onDelete: Cascade`)
    - `Branch.id` ga ishora qiluvchi maydon: `branch -> Branch` (`fields: [branchId]`, `references: [id]`, `onDelete: SetNull`)
  - **Kiruvchi:**
    - `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`
    - `RawAttendanceLog.terminalId -> Terminal.id (onDelete: Cascade)`
- Indexlar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([status])`

---

### Endpoint: GET /api/v1/terminals
**Controller:** src/modules/terminal/terminal.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/terminals`
- Controller class + method nomi: `TerminalController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query qabul qiladi)
- search: 'TRN-001'
- page: 1
- limit: 10
- companyId: misol yo'q
- branchId: misol yo'q
- type: misol yo'q (Swaggerda type ko'rsatilmagan enumdan tashqari)
- status: misol yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `TerminalQueryDto` (`src/modules/terminal/dto/terminal-query.dto.ts`)
- companyId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- branchId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- type: `TerminalType | undefined`, `@IsOptional()`, `@IsEnum(TerminalType)`
- status: `TerminalStatus | undefined`, `@IsOptional()`, `@IsEnum(TerminalStatus)`
- search: `string | undefined`, `@IsOptional()`, `@IsString()`
- page: `number | undefined`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- limit: `number | undefined`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `TerminalService.findAll` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Kiritilgan query parametrlari bo'yicha filtirlash, qidirish (`name` va `serialNumber` orqali case-insensitive izlash), actor ruxsatlarini inobatga olgan holda terminallarni va ularning umumiy miqdorini bazadan oladi (Paginatsiya bilan).

**6. Response:**
- Qaytariladigan javob: Paginatsiya obyekti
  - `items`: `Terminal[]` (Terminal modeliga mos array)
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Maxsus xatolar service tomonidan tashlanmaydi (validatsiya xatolarini hisobga olmasa). Malumot topilmasa ochiq holda bo'sh ro'yxat va total 0 qaytadi.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: `POST /api/v1/terminals` dagi kabi barchasi aynan bir xil.
- Relations / references: `POST /api/v1/terminals` dagi kabi barchasi aynan bir xil.
- Indexlar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([status])`
  - *Izoh*: `search` qidiruvi uchun maxsus indeks (`name` yoki `serialNumber` da) yo'q, lekin `serialNumber` fieldda `@unique` borligi qisman samarali ishlashiga imkon beradi.

---

### Endpoint: GET /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. Faqat URL Parametric Data olinadi: `id` parametri `ParseUUIDPipe` orqali `string` ko'rinishida.

**5. Service:**
- Service method: `TerminalService.findOne` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Berilgan `id` yordamida terminal bazadan izlanadi. Topilgandan so'ng, ushbu terminalga foydalanuvchining (actor) ruxsati bor-yo'qligi (`assertWithinScope`) tekshiriladi.

**6. Response:**
- Qaytariladigan javob: Topilgan `Terminal` obyekti to'liq maydonlari bilan.

**7. Error case:**
- `NotFoundException('Terminal not found')`: Agar berilgan `id` bilan terminal bazadan topilmasa.
- (Ehtimolli scope exception): `assertWithinScope` dan kirishga ruxsat yo'q degan xato kelib chiqishi mumkin (Forbidden).

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagi barcha maydonlar bilan bir xil.
- Relations / references: `POST /api/v1/terminals` bilan bir xil.
- Indexlar: `id` `@id` orqali indexlangan.

---

### Endpoint: PATCH /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `UpdateTerminalDto` obyekti qabul qilinadi, partial bo'lgani sababli `CreateTerminalDto` namunalari bilan bir xil, lekin barchasi ixtiyoriy:
  - name: 'Main gate terminal' (misol, Optional)
  - serialNumber: 'TRN-001' (misol, Optional)
  - ipAddress: '192.168.1.100' (misol, Optional)
  - port: 4370 (misol, Optional)
  - type: TerminalType.zkteco_face (misol, Optional)
  - status: TerminalStatus.active (misol, Optional)
  - connectionConfig: { username: 'admin', password: '12345' } (misol, Optional)
  - lastSyncAt: '2026-06-08T10:00:00.000Z' (misol, Optional)

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `UpdateTerminalDto` (`src/modules/terminal/dto/update-terminal.dto.ts`), `CreateTerminalDto`ning Partial ko'rinishi.
- `id` param qismi: URL dagi parametr, `ParseUUIDPipe` orqali olinadi.

**5. Service:**
- Service method: `TerminalService.update` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Bazadagi mavjud terminal topiladi. Foydalanuvchining unga ruxsati tekshiriladi. Agar `companyId` yoki `branchId` o'zgartirilayotgan bo'lsa ularning haqiqiyligi tekshiriladi. Agar `serialNumber` yangilanayotgan bo'lsa, tizimda takrorlanmasligi qayta tekshiriladi. Shundan so'ng, faqat yangilangan ma'lumotlar bazada yangilanadi (update operation).

**6. Response:**
- Qaytariladigan javob: Yangilangan `Terminal` obyekti to'liq ko'rinishda.

**7. Error case:**
- `NotFoundException('Terminal not found')`: O'zgartirilayotgan terminal topilmasa.
- `NotFoundException('Company not found')`: Yangi companyId bo'yicha kompaniya bo'lmasa.
- `NotFoundException('Branch not found')`: Yangi branchId bo'yicha filial bo'lmasa.
- `ConflictException('Branch does not belong to the selected company')`: Filial ko'rsatilgan kompaniyaga mos kelmasa.
- `ConflictException('Terminal serial number already exists')`: Yangi kiritilayotgan seriya raqami band bo'lsa.
- `ConflictException('Terminal name is required')`: Ism maydoni uzatilib uning qiymati bosh bo'shliq yoki null ga trim bo'lsa.
- `ConflictException('Serial number is required')`: Seriya raqamiga shunday xato holat kelsa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagidek `Terminal` barcha maydonlari mavjud.
- Relations / references: Yuqoridagidek barcha relatsiyalar amalda bir xil ishlatiladi.

---

### Endpoint: DELETE /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `id` URL'dan olinadi `ParseUUIDPipe` yordamida.

**5. Service:**
- Service method: `TerminalService.delete` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Id bo'yicha terminalni topadi, ruxsatini (scope) tekshiradi va keyin `delete` so'rovini bazaga jo'natib obyektni to'liq o'chiradi.

**6. Response:**
- Qaytariladigan javob: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException('Terminal not found')`: Agar o'chirilayotgan ID'ga ega terminal topilmasa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagilar kabi.
- Relations / references (O'chirish operatsiyasi uchun muhim):
  - **Chiquvchi:**
    - Terminal o'chirilganda u bog'langan Company yoki Branch larga ta'sir qilmaydi (Faqatgina ichki reference foreign key si uziladi).
  - **Kiruvchi (BU JUDA MUHIM):**
    - `Attendance.terminalId -> Terminal.id (onDelete: SetNull)` : Terminal o'chirilganda shu terminalda tekshiruvdan o'tgan attendance (davomat) yozuvlari **o'chirilmaydi**, balki ularning `terminalId` ustuni `NULL` qilib qo'yiladi.
    - `RawAttendanceLog.terminalId -> Terminal.id (onDelete: Cascade)` : Terminal o'chirilganda shu terminalga tegishli bo'lgan barcha asl xom davomat loglari (`RawAttendanceLog` dagi ma'lumotlar) **birgalikda butunlay o'chib ketadi**.
- Indexlar: `id` obyekti o'chiriladi va uning barcha bog'liqliklari triggerlar asosida ishlaydi.

### Changes from commit d143c02 (order: 1)
-  updated: added MIME type validation and size limit checks for uploaded images.
# User Moduli Backend Tahlili

### Endpoint: POST /api/v1/users
**Controller:** src/modules/user/user.controller.ts:`create`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/users`
- Controller class + method nomi: `UserController` `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
login: 'john.doe'
password: 'StrongPass123'
role: 'employee'
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
departmentId: 'uuid-department-id'
positionId: 'uuid-position-id'
managerId: 'uuid-manager-id'
workScheduleId: 'uuid-work-schedule-id'
employeeNo: 'EMP-001'
firstName: 'John'
lastName: 'Doe'
middleName: 'Michael'
phone: '+998901234567'
email: 'john@example.com'
address: 'Tashkent, Yunusobod'
passportSerial: 'AA1234567'
dateOfBirth: '1990-05-15'
avatarUrl: 'https://cdn.example.com/avatars/john.png'
baseSalary: 5000000

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `CreateUserDto` (`src/modules/user/dto/create-user.dto.ts`)
- `login`: string, `@IsString()`, `@MinLength(3)`, `@MaxLength(255)`
- `password`: string, `@IsString()`, `@MinLength(6)`, `@MaxLength(255)`
- `role`: UserRole, `@IsOptional()`, `@IsEnum(UserRole)`
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `departmentId`: string, `@IsOptional()`, `@IsUUID()`
- `positionId`: string, `@IsOptional()`, `@IsUUID()`
- `managerId`: string, `@IsOptional()`, `@IsUUID()`
- `workScheduleId`: string, `@IsOptional()`, `@IsUUID()`
- `employeeNo`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
- `firstName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `lastName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `middleName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `phone`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(50)`
- `email`: string, `@IsOptional()`, `@IsEmail()`, `@MaxLength(255)`
- `address`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `passportSerial`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
- `dateOfBirth`: string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `avatarUrl`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `baseSalary`: number, `@IsOptional()`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`

**5. Service:**
- `UserService.create` (`src/modules/user/user.service.ts`)
- Yangi foydalanuvchini yaratadi. Parolni hashlash, unikal maydonlarni va bog'lanishlarni tekshirish kabi ishlarni bajarib, User modeliga yozadi.

**6. Response:**
Foydalanuvchi obyekti qaytariladi:
- `id`: string
- `login`: string
- `role`: enum
- `companyId`: string
- `branchId`: string
- `departmentId`: string
- `positionId`: string
- `managerId`: string
- `workScheduleId`: string
- `employeeNo`: string
- `firstName`: string
- `lastName`: string
- `middleName`: string
- `phone`: string
- `email`: string
- `address`: string
- `passportSerial`: string
- `dateOfBirth`: date
- `avatarUrl`: string
- `faceDeviceUserId`: string
- `faceImageUrl`: string
- `baseSalary`: decimal
- `isActive`: boolean
- `isBlocked`: boolean
- `createdAt`: date
- `updatedAt`: date

**7. Error case:**
- `ForbiddenException` (superadmin yaratilayotganda)
- `ConflictException` (login req bo'lganda, login yoki email bazada bo'lganda)
- `NotFoundException` (company, branch, department, position, manager, work schedule topilmaganda)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/users
**Controller:** src/modules/user/user.controller.ts:`findAll`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/users`
- Controller class + method nomi: `UserController` `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

Query parametrlar:
companyId: misol yo'q
branchId: misol yo'q
departmentId: misol yo'q
positionId: misol yo'q
role: misol yo'q
isActive: true
isBlocked: false
search: 'john'
page: 1
limit: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UserQueryDto` (`src/modules/user/dto/user-query.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `departmentId`: string, `@IsOptional()`, `@IsUUID()`
- `positionId`: string, `@IsOptional()`, `@IsUUID()`
- `role`: UserRole, `@IsOptional()`, `@IsEnum(UserRole)`
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`
- `isBlocked`: boolean, `@IsOptional()`, `@IsBoolean()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `page`: number, `@IsOptional()`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- `UserService.findAll` (`src/modules/user/user.service.ts`)
- Query parametrlariga ko'ra foydalanuvchilar (User) ro'yxatini filtrlash, qidirish va paginatsiya bilan o'qiydi. Shuningdek har bir rol bo'yicha statistika qaytaradi.

**6. Response:**
Paginatsiya qilingan javob obyekti:
- `items`: Foydalanuvchilar massivi (har birida id, login, role, companyId va hk `USER_SELECT` bo'yicha)
- `total`: number
- `page`: number
- `limit`: number
- `totalPages`: number
- `stats`: Object (har bir rol bo'yicha sanoq)

**7. Error case:**
Odatda tashlanmaydi, auth va ruxsat xatolari bo'lishi mumkin (`ForbiddenException`, `UnauthorizedException`).


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`findOne`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/users/:id`
- Controller class + method nomi: `UserController` `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ID (param)` (`yo'q`)
Request DTO class yo'q, faqat `@Param('id', ParseUUIDPipe) id: string` qabul qiladi.

**5. Service:**
- `UserService.findOne` (`src/modules/user/user.service.ts`)
- Berilgan ID orqali bitta User'ni o'qiydi, so'rov yuborgan actorning (superadmin/admin/manager) ko'rish doirasiga kirishini tekshiradi.

**6. Response:**
Bitta foydalanuvchi obyekti (`USER_SELECT` dagi maydonlar bilan: `id`, `login`, `role`, `companyId` va h.k.)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Foydalanuvchi actorning ko'rish doirasidan tashqarida bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/me
**Controller:** src/modules/user/user.controller.ts:`updateOwnProfile`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/me`
- Controller class + method nomi: `UserController` `updateOwnProfile`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
firstName: 'John'
lastName: 'Doe'
middleName: 'Michael'
phone: '+998901234567'
email: 'john@example.com'
address: 'Tashkent, Yunusobod'
passportSerial: 'AA1234567'
dateOfBirth: '1990-05-15'
avatarUrl: 'https://cdn.example.com/avatars/john.png'

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UpdateOwnProfileDto` (`src/modules/user/dto/update-own-profile.dto.ts`)
- Barcha maydonlar `CreateUserDto` dan olingan ixtiyoriy (optional) maydonlar:
- `firstName`: string
- `lastName`: string
- `middleName`: string
- `phone`: string
- `email`: string
- `address`: string
- `passportSerial`: string
- `dateOfBirth`: string
- `avatarUrl`: string

**5. Service:**
- `UserService.updateOwnProfile` (`src/modules/user/user.service.ts`)
- Joriy foydalanuvchining o'z profil ma'lumotlarini (User modeli) yangilaydi. Email kiritilsa band emasligini tekshiradi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (Joriy foydalanuvchi bazadan topilmasa)
- `ConflictException` (Email allaqachon band bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`update`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id`
- Controller class + method nomi: `UserController` `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Barcha maydonlar `CreateUserDto` ga o'xshaydi (`password` dan tashqari), hech biriga specific example qayta yozilmagan. 
Misollar `CreateUserDto` dagi misollar bilan bir xil, barchasi optional.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UpdateUserDto` (`src/modules/user/dto/update-user.dto.ts`)
`CreateUserDto` dan `password` maydonini olib tashlab, qolgan barcha maydonlarni `PartialType` qilingan versiyasi. Barcha maydonlar ixtiyoriy (optional).

**5. Service:**
- `UserService.update` (`src/modules/user/user.service.ts`)
- Berilgan ID dagi User obyektini yangilaydi. Administrator/manager huquqlari va ko'rish doirasini tekshiradi, noyob maydonlar band emasligini tekshiradi, va yozadi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa yoki relation modellar topilmasa)
- `ForbiddenException` (Huquq yetarli bo'lmasa yoki boshqa kompaniya ma'lumoti o'zgartirilayotgan bo'lsa)
- `ConflictException` (Login, email yoki employeeNo band bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/toggle-status
**Controller:** src/modules/user/user.controller.ts:`toggleStatus`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/toggle-status`
- Controller class + method nomi: `UserController` `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ToggleUserStatusDto` (`src/modules/user/dto/toggle-user-status.dto.ts`)
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- `UserService.toggleStatus` (`src/modules/user/user.service.ts`)
- Foydalanuvchining aktivlik holatini (`isActive`) teskarisiga yoki berilgan qiymatga o'zgartiradi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/toggle-blocked
**Controller:** src/modules/user/user.controller.ts:`toggleBlocked`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/toggle-blocked`
- Controller class + method nomi: `UserController` `toggleBlocked`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isBlocked: true

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ToggleUserBlockedDto` (`src/modules/user/dto/toggle-user-blocked.dto.ts`)
- `isBlocked`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- `UserService.toggleBlocked` (`src/modules/user/user.service.ts`)
- Foydalanuvchini bloklangan yoki blokdan chiqarilgan holatga (`isBlocked`) o'tkazadi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/change-password
**Controller:** src/modules/user/user.controller.ts:`changePassword`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/change-password`
- Controller class + method nomi: `UserController` `changePassword`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
newPassword: 'NewStrongPass123'

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ChangePasswordDto` (`src/modules/user/dto/change-password.dto.ts`)
- `newPassword`: string, `@IsString()`, `@MinLength(6)`, `@MaxLength(255)`

**5. Service:**
- `UserService.changePassword` (`src/modules/user/user.service.ts`)
- Foydalanuvchining parolini yangilaydi (heshlaydi va saqlaydi).

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa yoki admin superadmin parolini o'zgartirmoqchi bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`delete`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/users/:id`
- Controller class + method nomi: `UserController` `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ID (param)` (`yo'q`)
Request DTO class yo'q, faqat `@Param('id', ParseUUIDPipe) id: string` qabul qiladi.

**5. Service:**
- `UserService.delete` (`src/modules/user/user.service.ts`)
- Berilgan ID ga ega User yozuvini bazadan butunlay o'chirib tashlaydi.

**6. Response:**
O'chirish holati: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa, yoxud admin superadminni o'chirmoqchi bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/work-schedules
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/work-schedules
- WorkScheduleController class + findAll method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida qo'llangan)

**4. DTO:**
- Request DTO: WorkScheduleQueryDto, src/modules/work-schedule/dto/work-schedule-query.dto.ts
- companyId: string, `@IsOptional()`, `@IsUUID()`
- branchId: string, `@IsOptional()`, `@IsUUID()`
- search: string, `@IsOptional()`, `@IsString()`
- isDefault: boolean, `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- isActive: boolean, `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- page: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- limit: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- findAll, src/modules/work-schedule/work-schedule.service.ts
- Kiritilgan query parametrlari va aktiyor (actor) ruxsatlariga qarab ish grafiklari ro'yxatini filtrlash va paginatsiya qilib bazadan o'qib qaytarish vazifasini bajaradi.

**6. Response:**
- Paginatsiya qilingan ob'ekt: `{ items: WorkSchedule[], total: number, page: number, limit: number, totalPages: number }` shaklida.

**7. Error case:**
- `ForbiddenException` (ruxsat bo'lmasa, Guard'dan keladi)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: GET /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/work-schedules/:id
- WorkScheduleController class + findOne method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: ID parametr sifatida olinadi (`@Param('id', ParseUUIDPipe) id: string`), alohida DTO yo'q.

**5. Service:**
- findOne, src/modules/work-schedule/work-schedule.service.ts
- ID bo'yicha bazadan tegishli ish grafigini izlaydi va topilsa foydalanuvchi (actor) ko'rishga ruxsati borligini (`scope`) tekshirib qaytaradi.

**6. Response:**
- Topilgan `WorkSchedule` obyekti (paginatsiyasiz, oddiy ob'ekt).

**7. Error case:**
- `NotFoundException` (Work schedule not found)
- `ForbiddenException` yoki `UnauthorizedException` (actor ruxsati bo'lmasa)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: POST /api/v1/work-schedules
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/work-schedules
- WorkScheduleController class + create method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
name: 'Standart ish kuni'
startTime: '09:00'
endTime: '18:00'
workDays: [1, 2, 3, 4, 5]
graceMinutes: 15
isDefault: false
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: CreateWorkScheduleDto, src/modules/work-schedule/dto/create-work-schedule.dto.ts
- companyId: string, `@IsOptional()`, `@IsUUID()`
- branchId: string, `@IsOptional()`, `@IsUUID()`
- name: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- startTime: string, `@IsString()`, `@Matches(/^\d{2}:\d{2}$/, { message: 'startTime must be in HH:mm format' })`
- endTime: string, `@IsString()`, `@Matches(/^\d{2}:\d{2}$/, { message: 'endTime must be in HH:mm format' })`
- workDays: number[], `@IsArray()`, `@ArrayMinSize(1)`, `@ArrayMaxSize(7)`, `@IsInt({ each: true })`, `@Min(1, { each: true })`, `@Max(7, { each: true })`
- graceMinutes: number, `@IsOptional()`, `@IsInt()`, `@Min(0)`, `@Max(120)`
- isDefault: boolean, `@IsOptional()`, `@IsBoolean()`
- userId: string, `@IsOptional()`, `@IsUUID()`

**5. Service:**
- create, src/modules/work-schedule/work-schedule.service.ts
- Yangi ish grafigini (WorkSchedule) yaratadi. Kiritilgan ma'lumotlarni validatsiya qilib (kompaniya, filial, nom takrorlanmasligi), jadvallarga yozadi va agar `userId` berilgan bo'lsa, foydalanuvchiga biriktiradi.

**6. Response:**
- Yaratilgan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Company not found, Branch not found, User not found)
- `ConflictException` (User does not belong to the selected company, Branch does not belong to the selected company, Work schedule name already exists for this company, Work schedule name is required)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id
- WorkScheduleController class + update method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
name: 'Standart ish kuni'
startTime: '09:00'
endTime: '18:00'
workDays: [1, 2, 3, 4, 5]
graceMinutes: 15
isDefault: false
userId: 'uuid-user-id'

*(Izoh: `UpdateWorkScheduleDto` `CreateWorkScheduleDto` dan PartialType qilib olingan, barcha fieldlar va example'lar saqlanadi.)*

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: UpdateWorkScheduleDto, src/modules/work-schedule/dto/update-work-schedule.dto.ts
- Barcha `CreateWorkScheduleDto` maydonlari `@IsOptional()` shaklida meros olinadi.

**5. Service:**
- update, src/modules/work-schedule/work-schedule.service.ts
- Belgilangan ish grafigining maydonlarini o'zgartiradi (update). ID orqali borligini tekshiradi, agar yangi isDefault berilsa boshqalarinikini tozalaydi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Work schedule not found, Company not found, Branch not found)
- `ConflictException` (Branch does not belong to the selected company, Work schedule name already exists for this company, Work schedule name is required)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/toggle-status
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/toggle-status
- WorkScheduleController class + toggleStatus method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: ToggleWorkScheduleStatusDto, src/modules/work-schedule/dto/toggle-work-schedule-status.dto.ts
- isActive: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- toggleStatus, src/modules/work-schedule/work-schedule.service.ts
- Ish grafigining `isActive` holatini teskarisiga (yoki ko'rsatilgan qiymatga) o'zgartiradi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/set-default
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:setDefault

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/set-default
- WorkScheduleController class + setDefault method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Body qabul qilmaydi. ID parametrdan (ParseUUIDPipe) olinadi.

**5. Service:**
- setDefault, src/modules/work-schedule/work-schedule.service.ts
- Berilgan ish grafigini standart (`isDefault = true`) qilib belgilaydi va shu kompaniyaning boshqa barcha standart grafiklarining `isDefault` qiymatini `false` qilib bekor qiladi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti (isDefault: true bilan).

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/assign-user
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:assignUser

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/assign-user
- WorkScheduleController class + assignUser method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: AssignUserDto, src/modules/work-schedule/dto/assign-user.dto.ts
- userId: string, `@IsUUID()`

**5. Service:**
- assignUser, src/modules/work-schedule/work-schedule.service.ts
- Berilgan jadvalni (WorkSchedule) foydalanuvchiga (User) biriktiradi. User va WorkSchedule bitta kompaniyaga tegishliligini tekshiradi, keyin `User.workScheduleId` ni o'zgartiradi.

**6. Response:**
- Yangilangan `User` obyektining bir qismi: `{ id: string, login: string, companyId: string | null, workScheduleId: string | null }`

**7. Error case:**
- `NotFoundException` (Work schedule not found, User not found)
- `ConflictException` (Work schedule does not belong to the user's company)

**8. DB struktura:**
- Model: `WorkSchedule` va `User` ga ta'sir qiladi.
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/unassign-user
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:unassignUser

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/unassign-user
- WorkScheduleController class + unassignUser method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: AssignUserDto, src/modules/work-schedule/dto/assign-user.dto.ts
- userId: string, `@IsUUID()`

**5. Service:**
- unassignUser, src/modules/work-schedule/work-schedule.service.ts
- Foydalanuvchidan (User) berilgan ish grafigini (WorkSchedule) olib tashlaydi (`User.workScheduleId` ni null ga aylantiradi).

**6. Response:**
- Yangilangan `User` obyektining bir qismi: `{ id: string, login: string, companyId: string | null, workScheduleId: string | null }`

**7. Error case:**
- `NotFoundException` (Work schedule not found, User not found)

**8. DB struktura:**
- Model: `WorkSchedule` va `User` (asosan User modifikatsiya qilinadi).
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/work-schedules/:id
- WorkScheduleController class + delete method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Body DTO yo'q. Faqat ID (ParseUUIDPipe).

**5. Service:**
- delete, src/modules/work-schedule/work-schedule.service.ts
- Ish grafigini bazadan butunlay o'chirib yuboradi (`delete`).

**6. Response:**
- Ob'ekt: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)` (o'chirilganda foydalanuvchilarning workScheduleId null bo'lib qoladi, chunki onDelete: SetNull)
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/work-schedule.md`

### Endpoint: GET /api/v1/work-schedules
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/work-schedules
- WorkScheduleController class + findAll method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida qo'llangan)

**4. DTO:**
- Request DTO: WorkScheduleQueryDto, src/modules/work-schedule/dto/work-schedule-query.dto.ts
- companyId: string, `@IsOptional()`, `@IsUUID()`
- branchId: string, `@IsOptional()`, `@IsUUID()`
- search: string, `@IsOptional()`, `@IsString()`
- isDefault: boolean, `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- isActive: boolean, `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- page: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- limit: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- findAll, src/modules/work-schedule/work-schedule.service.ts
- Kiritilgan query parametrlari va aktiyor (actor) ruxsatlariga qarab ish grafiklari ro'yxatini filtrlash va paginatsiya qilib bazadan o'qib qaytarish vazifasini bajaradi.

**6. Response:**
- Paginatsiya qilingan ob'ekt: `{ items: WorkSchedule[], total: number, page: number, limit: number, totalPages: number }` shaklida.

**7. Error case:**
- `ForbiddenException` (ruxsat bo'lmasa, Guard'dan keladi)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: GET /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/work-schedules/:id
- WorkScheduleController class + findOne method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: ID parametr sifatida olinadi (`@Param('id', ParseUUIDPipe) id: string`), alohida DTO yo'q.

**5. Service:**
- findOne, src/modules/work-schedule/work-schedule.service.ts
- ID bo'yicha bazadan tegishli ish grafigini izlaydi va topilsa foydalanuvchi (actor) ko'rishga ruxsati borligini (`scope`) tekshirib qaytaradi.

**6. Response:**
- Topilgan `WorkSchedule` obyekti (paginatsiyasiz, oddiy ob'ekt).

**7. Error case:**
- `NotFoundException` (Work schedule not found)
- `ForbiddenException` yoki `UnauthorizedException` (actor ruxsati bo'lmasa)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: POST /api/v1/work-schedules
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/work-schedules
- WorkScheduleController class + create method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
name: 'Standart ish kuni'
startTime: '09:00'
endTime: '18:00'
workDays: [1, 2, 3, 4, 5]
graceMinutes: 15
isDefault: false
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: CreateWorkScheduleDto, src/modules/work-schedule/dto/create-work-schedule.dto.ts
- companyId: string, `@IsOptional()`, `@IsUUID()`
- branchId: string, `@IsOptional()`, `@IsUUID()`
- name: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- startTime: string, `@IsString()`, `@Matches(/^\d{2}:\d{2}$/, { message: 'startTime must be in HH:mm format' })`
- endTime: string, `@IsString()`, `@Matches(/^\d{2}:\d{2}$/, { message: 'endTime must be in HH:mm format' })`
- workDays: number[], `@IsArray()`, `@ArrayMinSize(1)`, `@ArrayMaxSize(7)`, `@IsInt({ each: true })`, `@Min(1, { each: true })`, `@Max(7, { each: true })`
- graceMinutes: number, `@IsOptional()`, `@IsInt()`, `@Min(0)`, `@Max(120)`
- isDefault: boolean, `@IsOptional()`, `@IsBoolean()`
- userId: string, `@IsOptional()`, `@IsUUID()`

**5. Service:**
- create, src/modules/work-schedule/work-schedule.service.ts
- Yangi ish grafigini (WorkSchedule) yaratadi. Kiritilgan ma'lumotlarni validatsiya qilib (kompaniya, filial, nom takrorlanmasligi), jadvallarga yozadi va agar `userId` berilgan bo'lsa, foydalanuvchiga biriktiradi.

**6. Response:**
- Yaratilgan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Company not found, Branch not found, User not found)
- `ConflictException` (User does not belong to the selected company, Branch does not belong to the selected company, Work schedule name already exists for this company, Work schedule name is required)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id
- WorkScheduleController class + update method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
name: 'Standart ish kuni'
startTime: '09:00'
endTime: '18:00'
workDays: [1, 2, 3, 4, 5]
graceMinutes: 15
isDefault: false
userId: 'uuid-user-id'

*(Izoh: `UpdateWorkScheduleDto` `CreateWorkScheduleDto` dan PartialType qilib olingan, barcha fieldlar va example'lar saqlanadi.)*

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: UpdateWorkScheduleDto, src/modules/work-schedule/dto/update-work-schedule.dto.ts
- Barcha `CreateWorkScheduleDto` maydonlari `@IsOptional()` shaklida meros olinadi.

**5. Service:**
- update, src/modules/work-schedule/work-schedule.service.ts
- Belgilangan ish grafigining maydonlarini o'zgartiradi (update). ID orqali borligini tekshiradi, agar yangi isDefault berilsa boshqalarinikini tozalaydi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Work schedule not found, Company not found, Branch not found)
- `ConflictException` (Branch does not belong to the selected company, Work schedule name already exists for this company, Work schedule name is required)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/toggle-status
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/toggle-status
- WorkScheduleController class + toggleStatus method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: ToggleWorkScheduleStatusDto, src/modules/work-schedule/dto/toggle-work-schedule-status.dto.ts
- isActive: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- toggleStatus, src/modules/work-schedule/work-schedule.service.ts
- Ish grafigining `isActive` holatini teskarisiga (yoki ko'rsatilgan qiymatga) o'zgartiradi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti.

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/set-default
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:setDefault

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/set-default
- WorkScheduleController class + setDefault method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Body qabul qilmaydi. ID parametrdan (ParseUUIDPipe) olinadi.

**5. Service:**
- setDefault, src/modules/work-schedule/work-schedule.service.ts
- Berilgan ish grafigini standart (`isDefault = true`) qilib belgilaydi va shu kompaniyaning boshqa barcha standart grafiklarining `isDefault` qiymatini `false` qilib bekor qiladi.

**6. Response:**
- Yangilangan `WorkSchedule` obyekti (isDefault: true bilan).

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/assign-user
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:assignUser

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/assign-user
- WorkScheduleController class + assignUser method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: AssignUserDto, src/modules/work-schedule/dto/assign-user.dto.ts
- userId: string, `@IsUUID()`

**5. Service:**
- assignUser, src/modules/work-schedule/work-schedule.service.ts
- Berilgan jadvalni (WorkSchedule) foydalanuvchiga (User) biriktiradi. User va WorkSchedule bitta kompaniyaga tegishliligini tekshiradi, keyin `User.workScheduleId` ni o'zgartiradi.

**6. Response:**
- Yangilangan `User` obyektining bir qismi: `{ id: string, login: string, companyId: string | null, workScheduleId: string | null }`

**7. Error case:**
- `NotFoundException` (Work schedule not found, User not found)
- `ConflictException` (Work schedule does not belong to the user's company)

**8. DB struktura:**
- Model: `WorkSchedule` va `User` ga ta'sir qiladi.
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/work-schedules/:id/unassign-user
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:unassignUser

**1. Point (yo'nalish):**
- PATCH /api/v1/work-schedules/:id/unassign-user
- WorkScheduleController class + unassignUser method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: 'uuid-user-id'

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Request DTO: AssignUserDto, src/modules/work-schedule/dto/assign-user.dto.ts
- userId: string, `@IsUUID()`

**5. Service:**
- unassignUser, src/modules/work-schedule/work-schedule.service.ts
- Foydalanuvchidan (User) berilgan ish grafigini (WorkSchedule) olib tashlaydi (`User.workScheduleId` ni null ga aylantiradi).

**6. Response:**
- Yangilangan `User` obyektining bir qismi: `{ id: string, login: string, companyId: string | null, workScheduleId: string | null }`

**7. Error case:**
- `NotFoundException` (Work schedule not found, User not found)

**8. DB struktura:**
- Model: `WorkSchedule` va `User` (asosan User modifikatsiya qilinadi).
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/work-schedules/:id
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/work-schedules/:id
- WorkScheduleController class + delete method

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')` (class darajasida)

**4. DTO:**
- Body DTO yo'q. Faqat ID (ParseUUIDPipe).

**5. Service:**
- delete, src/modules/work-schedule/work-schedule.service.ts
- Ish grafigini bazadan butunlay o'chirib yuboradi (`delete`).

**6. Response:**
- Ob'ekt: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException` (Work schedule not found)

**8. DB struktura:**
- Model: `WorkSchedule`
- id: String, majburiy, `@default(uuid())`, `@db.Uuid`
- companyId: String, majburiy, `@db.Uuid`
- branchId: String, ixtiyoriy (`?`), `@db.Uuid`
- name: String, majburiy, `@db.VarChar(255)`
- startTime: String, majburiy, `@db.VarChar(10)`
- endTime: String, majburiy, `@db.VarChar(10)`
- workDays: Json, majburiy, `@db.Json`
- graceMinutes: Int, majburiy, `@default(0)`
- isDefault: Boolean, majburiy, `@default(false)`
- isActive: Boolean, majburiy, `@default(true)`
- createdAt: DateTime, majburiy, `@default(now())`, `@db.Timestamptz(6)`
- updatedAt: DateTime, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Chiquvchi relations:
  - `WorkSchedule.companyId -> Company.id (onDelete: Cascade)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
- Kiruvchi relations:
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)` (o'chirilganda foydalanuvchilarning workScheduleId null bo'lib qoladi, chunki onDelete: SetNull)
- Indekslar: `@@unique([companyId, name])`, `@@index([companyId])`, `@@index([branchId])`, `@@index([isDefault])`, `@@index([isActive])`


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/employee-leave.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

### Endpoint: POST /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar)

**4. DTO:**
- Request DTO: `CreateEmployeeLeaveDto` (src/modules/employee-leave/dto/create-employee-leave.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsUUID()`
- `type`: Tip - LeaveType (enum), Validatorlar - `@IsEnum(LeaveType)`
- `fromDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `toDate`: Tip - String, Validatorlar - `@Type(() => String)`, `@IsDateString()`
- `days`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@IsBoolean()`
- `reason`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`, `@MaxLength(1000)`

**5. Service:**
- Service method: `create` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Xodimni, kompaniya va filiallarni tekshiradi, kunlarni hisoblaydi (agar berilmagan bo'lsa) va `EmployeeLeave` jadvaliga yangi ta'til yozuvini qo'shadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti (aniq maydonlar: `id` (String), `companyId` (String), `branchId` (String?), `employeeId` (String), `type` (LeaveType), `fromDate` (DateTime), `toDate` (DateTime), `days` (Int), `affectsSalary` (Boolean), `reason` (String?), `createdById` (String?), `updatedById` (String?), `createdAt` (DateTime), `updatedAt` (DateTime)).

**7. Error case:**
- `NotFoundException`: 'Company not found' (kompaniya topilmasa), 'Branch not found' (filial topilmasa), 'Employee not found' (xodim topilmasa).
- `ConflictException`: 'Branch does not belong to the selected company' (filial tegishli emas), 'Employee does not belong to the selected company' (xodim tegishli emas), 'Employee does not belong to the selected branch' (xodim filialga tegishli emas).
- `BadRequestException`: 'Leave end date must be after start date' (sana xato bo'lsa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q (Boshqa modellar ushbu modelga ishora qilmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves`
- Controller class + method nomi: `EmployeeLeaveController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `type`: `vacation`
  - `affectsSalary`: `false`
  - `search`: `medical`
  - `dateFrom`: `2026-06-01`
  - `dateTo`: `2026-06-30`
  - `page`: `1`
  - `limit`: `10`
  - `companyId`: misol yo'q
  - `branchId`: misol yo'q
  - `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `EmployeeLeaveQueryDto` (src/modules/employee-leave/dto/employee-leave-query.dto.ts)
- `companyId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `branchId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `employeeId`: Tip - String, Validatorlar - `@IsOptional()`, `@IsUUID()`
- `type`: Tip - LeaveType, Validatorlar - `@IsOptional()`, `@IsEnum(LeaveType)`
- `affectsSalary`: Tip - Boolean, Validatorlar - `@IsOptional()`, `@Transform(...)`, `@IsBoolean()`
- `search`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateFrom`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `dateTo`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `page`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `findAll` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Filterlar (kompaniya, xodim, filial, sana) bo'yicha ruxsat doirasida xodimlar ta'tillari ro'yxatini va paginatsiyani bazadan olib keladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
  - `items`: EmployeeLeave obyektlari massivi (Array)
  - `total`: Umumiy miqdor (Number)
  - `page`: Joriy sahifa (Number)
  - `limit`: Sahifadagi limit (Number)
  - `totalPages`: Jami sahifalar soni (Number)

**7. Error case:**
- Maxsus xatolik tashlamaydi (bazaviy exception'lar bo'lishi mumkin xolos).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: GET /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string sifatida olinadi).

**5. Service:**
- Service method: `findOne` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Berilgan ID yordamida bitta ta'til yozuvini oladi va foydalanuvchining unga ruxsati borligini (scope) tekshiradi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `EmployeeLeave` obyekti.

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (berilgan id dagi ta'til topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: PATCH /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
(CreateEmployeeLeaveDto dan meros orqali olingan PartialType)
- `type`: `vacation`
- `fromDate`: `2026-06-10`
- `toDate`: `2026-06-12`
- `days`: `3`
- `affectsSalary`: `false`
- `reason`: `Medical leave`
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `employeeId`: misol yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateEmployeeLeaveDto` (src/modules/employee-leave/dto/update-employee-leave.dto.ts) - `PartialType(CreateEmployeeLeaveDto)`
- Maydonlar tip va validatorlari CreateEmployeeLeaveDto kabi, faqat barchasi ixtiyoriy bo'ladi.

**5. Service:**
- Service method: `update` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Mavjud ta'tilni topib tekshiradi va uzatilgan yangi ma'lumotlar bilan ma'lumotlar bazasida yozuvni yangilaydi (shuningdek sana oralig'ini qayta hisoblaydi).

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `EmployeeLeave` obyekti.

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (ta'til obyektini yoki kompaniya, xodim filialni topa olmasa).
- `ConflictException`: Kompaniya va filiallar mos tushmaganda.
- `BadRequestException`: 'Leave end date must be after start date' (Sana noto'g'ri bo'lganda).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`

---

### Endpoint: DELETE /api/v1/employee-leaves/:id
**Controller:** src/modules/employee-leave/employee-leave.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/employee-leaves/:id`
- Controller class + method nomi: `EmployeeLeaveController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string).

**5. Service:**
- Service method: `delete` (src/modules/employee-leave/employee-leave.service.ts)
- Tavsifi: Ta'til obyekti ID bo'yicha topiladi, scope orqali tekshiriladi va xavfsiz holatda o'chiriladi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: boolean, id: string }`

**7. Error case:**
- `NotFoundException`: 'Employee leave not found' (o'chirilishi kerak bo'lgan obyekt topilmasa).

**8. DB struktura:**
- Prisma modeli: `EmployeeLeave` (prisma/schema.prisma)
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeId`: `String`, majburiy, `@db.Uuid`
  - `type`: `LeaveType`, majburiy, `@default(vacation)`
  - `fromDate`: `DateTime`, majburiy, `@db.Date`
  - `toDate`: `DateTime`, majburiy, `@db.Date`
  - `days`: `Int`, majburiy
  - `affectsSalary`: `Boolean`, majburiy, `@default(false)`
  - `reason`: `String`, ixtiyoriy (`?`)
  - `createdById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `updatedById`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi):
  - `companyId -> Company.id (onDelete: Cascade)`
  - `branchId -> Branch.id (onDelete: SetNull)`
  - `employeeId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Kiruvchi reference'lar (ya'ni ushbu `EmployeeLeave` ni ko'rsatadigan boshqa modellar) butunlay YO'Q. (Yani EmployeeLeave o'chirilsa, hech qaysi boshqa jadvalga cascade yoki null qilib ta'sir ko'rsatmaydi).
- Indekslar: 
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([employeeId])`
  - `@@index([fromDate])`
  - `@@index([toDate])`


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/position.md`

### Endpoint: POST /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/positions`
- Controller class + method nomi: `PositionController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: `105a743b-8e71-4e87-aaff-131f27837a22`
- `departmentId`: `653b8aae-5091-4d50-b14c-258e30b5873b` (ixtiyoriy)
- `name`: `Backend Developer`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `CreatePositionDto`
- `companyId`: Optional, UUID
- `departmentId`: Optional, UUID
- `name`: Required, String (min: 1, max: 255)

**5. Service:**
- Service method: `create`
- Tavsifi: Superadmin yoki admin (o'z kompaniyasi bo'yicha) lavozim yarata oladi. Manager esa faqat o'z filiali doirasida yarata oladi. Ism takrorlanmasligini tekshiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "54c388e2-3e62-4e74-8bea-afd7947ada74",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "departmentId": null,
    "name": "Test Position",
    "isActive": true,
    "createdAt": "2026-08-22T16:36:53.622Z",
    "updatedAt": "2026-08-22T16:36:53.622Z"
  },
  "path": "/api/v1/positions",
  "timestamp": "2026-08-22T16:36:53.628Z"
}
```

**7. Error case:**
- `404 Not Found`: "Company not found", "Department not found".
- `403 Forbidden`: "departmentId is required to create a position within your branch".
- `409 Conflict`: "Department does not belong to the selected company", "Position name already exists for this company and department".

**8. DB struktura:**
- Prisma modeli: `Position`
- `id`: `String`, `@id @default(uuid()) @db.Uuid`
- `companyId`: `String`, `@db.Uuid`
- `departmentId`: `String?`, `@db.Uuid`
- `name`: `String`, `@db.VarChar(255)`
- `isActive`: `Boolean`, `@default(true)`
- `createdAt`, `updatedAt`
- Relations: `companyId` -> `Company`, `departmentId` -> `Department`
- Unique: `@@unique([companyId, departmentId, name])`

**cURL Misoli:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"companyId":"105a743b-8e71-4e87-aaff-131f27837a22", "name":"Test Position"}' \
  http://localhost:4000/api/v1/positions
```

---

### Endpoint: GET /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions`
- Controller class + method nomi: `PositionController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Query parametrlari orqali ma'lumot keladi.
- `companyId`: `105a743b...`
- `departmentId`: `653b8aae...`
- `search`: `Backend`
- `isActive`: `true`
- `page`: `1`
- `limit`: `10`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `PositionQueryDto`
- Query parametrlar: `companyId`, `departmentId`, `search`, `isActive`, `page`, `limit`.

**5. Service:**
- Service method: `findAll`
- Tavsifi: Ruxsat berilgan lavozimlarni sahifalab ro'yxatini qaytaradi (superadmin hammasini, admin o'z kompaniyasidagilarni, manager faqat o'z filialidagi). Izlash imkoniyati bor.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "1fcdfc24-c786-47cc-91d8-77bea0966171",
        "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
        "departmentId": "653b8aae-5091-4d50-b14c-258e30b5873b",
        "name": "Operator — Bosh Ofis",
        "isActive": true,
        "createdAt": "2026-08-07T14:01:48.793Z",
        "updatedAt": "2026-08-07T14:01:48.793Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/positions",
  "timestamp": "2026-08-22T16:36:41.117Z"
}
```

**7. Error case:**
- Maxsus xatolik tashlamaydi.

**8. DB struktura:**
- Prisma modeli: `Position` (POST bilan bir xil)

**cURL Misoli:**
```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "http://localhost:4000/api/v1/positions?page=1&limit=10"
```

---

### Endpoint: GET /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions/:id`
- Controller class + method nomi: `PositionController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat param `id` beriladi.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO yo'q. Parametr string.

**5. Service:**
- Service method: `findOne`
- Tavsifi: `id` bo'yicha bitta lavozimni olish, lavozim ushbu actorning ruxsat doirasida ekanligi tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "54c388e2-3e62-4e74-8bea-afd7947ada74",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "departmentId": null,
    "name": "Test Position",
    "isActive": true,
    "createdAt": "2026-08-22T16:36:53.622Z",
    "updatedAt": "2026-08-22T16:36:53.622Z",
    "company": {
      "id": "105a743b-8e71-4e87-aaff-131f27837a22",
      "name": "TexnoSoft Uzbekistan",
      "branches": [
        {
          "id": "626572f8-e317-43a3-94e0-9e851a741f59",
          "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
          "name": "TexnoSoft Uzbekistan — Bosh Ofis",
          "isActive": true
        }
      ]
    },
    "department": null
  },
  "path": "/api/v1/positions/54c388e2-3e62-4e74-8bea-afd7947ada74",
  "timestamp": "2026-08-22T16:37:03.894Z"
}
```

**7. Error case:**
- `404 Not Found`: "Position not found".
- `403 Forbidden`: "You cannot access a position outside your branch".

**8. DB struktura:**
- Prisma modeli: `Position` (POST bilan bir xil)

**cURL Misoli:**
```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "http://localhost:4000/api/v1/positions/<id>"
```

---

### Endpoint: PATCH /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id`
- Controller class + method nomi: `PositionController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `Updated Backend Developer`
- `departmentId`: `653b8aae-5091-4d50-b14c-258e30b5873b`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `UpdatePositionDto` (CreatePositionDto ning ixtiyoriy shakli).

**5. Service:**
- Service method: `update`
- Tavsifi: Mavjud lavozimni yangilaydi. Ism yagona bo'lishi hamda filial/kompaniya doirasida ekanligi tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "54c388e2-3e62-4e74-8bea-afd7947ada74",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "departmentId": null,
    "name": "Updated Test Position",
    "isActive": true,
    "createdAt": "2026-08-22T16:36:53.622Z",
    "updatedAt": "2026-08-22T16:37:09.691Z"
  },
  "path": "/api/v1/positions/54c388e2-3e62-4e74-8bea-afd7947ada74",
  "timestamp": "2026-08-22T16:37:09.695Z"
}
```

**7. Error case:**
- `404 Not Found`: "Position not found", "Department not found".
- `409 Conflict`: "Position name already exists for this company and department".

**8. DB struktura:**
- Prisma modeli: `Position` (POST bilan bir xil)

**cURL Misoli:**
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Test Position"}' \
  http://localhost:4000/api/v1/positions/<id>
```

---

### Endpoint: PATCH /api/v1/positions/:id/toggle-status
**Controller:** src/modules/position/position.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id/toggle-status`
- Controller class + method nomi: `PositionController` -> `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `isActive`: `false`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO: `TogglePositionStatusDto`
- `isActive`: Optional, Boolean

**5. Service:**
- Service method: `toggleStatus`
- Tavsifi: Lavozimning `isActive` holatini teskarisiga o'zgartirish yoki berilgan holatga o'zgartirish. Ruxsatlar qat'iy tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "54c388e2-3e62-4e74-8bea-afd7947ada74",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "departmentId": null,
    "name": "Updated Test Position",
    "isActive": false,
    "createdAt": "2026-08-22T16:36:53.622Z",
    "updatedAt": "2026-08-22T16:37:16.088Z"
  },
  "path": "/api/v1/positions/54c388e2-3e62-4e74-8bea-afd7947ada74/toggle-status",
  "timestamp": "2026-08-22T16:37:16.093Z"
}
```

**7. Error case:**
- `404 Not Found`: "Position not found".
- `403 Forbidden`: Ruxsatsiz filial yoki kompaniya uchun.

**8. DB struktura:**
- Prisma modeli: `Position` (POST bilan bir xil)

**cURL Misoli:**
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"isActive":false}' \
  http://localhost:4000/api/v1/positions/<id>/toggle-status
```

---

### Endpoint: DELETE /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/positions/:id`
- Controller class + method nomi: `PositionController` -> `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- `@ApiBearerAuth()`

**4. DTO:**
- Request DTO yo'q, faqat ID parametr.

**5. Service:**
- Service method: `delete`
- Tavsifi: Lavozimni butunlay o'chirib yuborish. Ruxsat doirasida ekanligi tekshiriladi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "54c388e2-3e62-4e74-8bea-afd7947ada74"
  },
  "path": "/api/v1/positions/54c388e2-3e62-4e74-8bea-afd7947ada74",
  "timestamp": "2026-08-22T16:38:08.598Z"
}
```

**7. Error case:**
- `404 Not Found`: "Position not found".
- `403 Forbidden`: Ruxsatsiz o'chirishga urinish.

**8. DB struktura:**
- Prisma modeli: `Position` (POST bilan bir xil)

**cURL Misoli:**
```bash
curl -s -X DELETE \
  -H "Authorization: Bearer <TOKEN>" \
  http://localhost:4000/api/v1/positions/<id>
```


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/department.md`

# Department modulini backend tahlili

### Endpoint: POST /api/v1/departments
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `create`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/departments`
- Controller class + method nomi: `DepartmentController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `HR`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `CreateDepartmentDto` (`zdes_backend/src/modules/department/dto/create-department.dto.ts`)
- Har bir maydon:
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string | null`, `@IsOptional()`, `@IsUUID()`
  - `name`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Method: `DepartmentService.create` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Actor'ning ruxsat doirasi (scope) hamda tegishli company va branch mavjudligini tekshiradi. Ushbu nomdagi bo'lim allaqachon mavjud bo'lmasa, `Department` jadvaliga yangi yozuv (bo'lim) qo'shadi.

**6. Response:**
- Qaytariladigan javob: Yaratilgan `Department` obyekti (maydonlari: `id`, `companyId`, `branchId`, `name`, `isActive`, `createdAt`, `updatedAt`).

**7. Error case:**
- `NotFoundException`: Kiritilgan `companyId` yoki `branchId` topilmasa.
- `ConflictException`: Branch ushbu company'ga tegishli bo'lmasa, yoki xuddi shunday `name` bo'lgan bo'lim ushbu filial/kompaniyada allaqachon mavjud bo'lsa, yoxud `name` faqat bo'sh joylardan iborat bo'lsa.
- `ForbiddenException`: Obyekt yaratish ruxsat doirasidan (scope) tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department` (`prisma/schema.prisma` dan)
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)` (fields: `[companyId]`)
  - `branch -> Branch.id (onDelete: SetNull)` (fields: `[branchId]`)
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/departments
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `findAll`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments`
- Controller class + method nomi: `DepartmentController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. (Query parametrlari uchun misollar: `search`: `hr`, `isActive`: `true`, `page`: `1`, `limit`: `10`)

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO (Query): `DepartmentQueryDto` (`zdes_backend/src/modules/department/dto/department-query.dto.ts`)
- Har bir maydon:
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `search`: `string`, `@IsOptional()`, `@IsString()`
  - `isActive`: `boolean`, `@IsOptional()`, `@Transform()`, `@IsBoolean()`
  - `page`: `number`, `@IsOptional()`, `@Type()`, `@IsInt()`, `@Min(1)`
  - `limit`: `number`, `@IsOptional()`, `@Type()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Method: `DepartmentService.findAll` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Foydalanuvchining ruxsat darajasiga qarab (scope) va filterlarga (`companyId`, `branchId`, `search`, `isActive`) mos keluvchi bo'limlar ro'yxatini va umumiy sonini ma'lumotlar bazasidan paginatsiya shaklida qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli (paginatsiya): `{ items: Department[], total: number, page: number, limit: number, totalPages: number }`

**7. Error case:**
- `ForbiddenException`: Scope yoki rol doirasida muammo bo'lsa (Access Token / Role).

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])` (Filter/search operatsiyalariga ta'sir qiluvchi indekslar)

---

### Endpoint: GET /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `findOne`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: Yo'q (Faqat Param orqali `id`, `ParseUUIDPipe` bilan olinadi).

**5. Service:**
- Method: `DepartmentService.findOne` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Berilgan UUID bo'yicha bo'limni ma'lumotlar bazasidan qidiradi, va so'rovchi ushbu bo'limni o'qishga (scope) haqli ekanini tasdiqlab, obyektni qaytaradi.

**6. Response:**
- Qaytariladigan javob: Topilgan `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: Topilgan bo'limga kirish actor'ning ruxsat doirasidan (scope) chetda bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `update`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `branchId`: misol yo'q
- `name`: `HR`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateDepartmentDto` (`zdes_backend/src/modules/department/dto/update-department.dto.ts`, `PartialType` bilan)
- Har bir maydon (barchasi ixtiyoriy):
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string | null`, `@IsOptional()`, `@IsUUID()`
  - `name`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Method: `DepartmentService.update` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Mavjud bo'limni tekshiradi, o'zgartirish doirasini ruxsat asosida tahlil qiladi (scope) va kiritilgan yangi ma'lumotlarni tekshirib (`name` va h.k.), `Department` obyektini bazada yangilaydi.

**6. Response:**
- Qaytariladigan javob: Yangilangan `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim yoxud bog'langan yangi kompaniya topilmasa.
- `ConflictException`: Yangi `name` bazada takrorlansa (aynan shu kompaniya va filial ichida) yoki filial kompaniyaga tegishli bo'lmasa.
- `ForbiddenException`: Obyekt o'zgartirish ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/departments/:id/toggle-status
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `toggleStatus`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/departments/:id/toggle-status`
- Controller class + method nomi: `DepartmentController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `isActive`: `false`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: `ToggleDepartmentStatusDto` (`zdes_backend/src/modules/department/dto/toggle-department-status.dto.ts`)
- Har bir maydon:
  - `isActive`: `boolean`, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Method: `DepartmentService.toggleStatus` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Bo'lim holatini (`isActive`) agarda parametrda uzatilgan bo'lsa shunga, aks holda esa bazadagi teskari holatga (`!department.isActive`) o'zgartiradi.

**6. Response:**
- Qaytariladigan javob: Yangilangan holatdagi `Department` obyekti.

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: Obyekt o'zgartirish ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi):
  - `Position.departmentId -> Department.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])` (Aynan shu jarayon shu ustun bilan ishlaydi)

---

### Endpoint: DELETE /api/v1/departments/:id
**Controller:** `zdes_backend/src/modules/department/department.controller.ts` : `delete`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/departments/:id`
- Controller class + method nomi: `DepartmentController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)
- `@ApiBearerAuth()` / AccessTokenGuard (Controller darajasida)

**4. DTO:**
- Request DTO: Yo'q (Param orqali `id` `ParseUUIDPipe` yordamida olinadi).

**5. Service:**
- Method: `DepartmentService.delete` (`zdes_backend/src/modules/department/department.service.ts`)
- Mantiq: Bo'limni bazadan qidirib, agar topsa va o'chirishga huquq bo'lsa (scope tekshiruvi orqali), uni butunlay o'chirib tashlaydi.

**6. Response:**
- Qaytariladigan javob: Muvaffaqiyatni bildiruvchi obyekti: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: Berilgan ID bo'yicha bo'lim topilmasa.
- `ForbiddenException`: O'chiriladigan bo'lim actor'ning ruxsat doirasidan tashqarida bo'lsa.

**8. DB struktura:**
- Prisma modeli: `Department`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references (Chiquvchi):
  - `company -> Company.id (onDelete: Cascade)`
  - `branch -> Branch.id (onDelete: SetNull)`
- Relations / references (Kiruvchi — o'chirishda ta'siri):
  - `Position.departmentId -> Department.id (onDelete: SetNull)` — Ya'ni, ushbu Department o'chirilganda unga aloqador Position'larning departmentId maydoni NULL bo'lib qoladi, jadvallar kaskad o'chmaydi.
  - `User.departmentId -> Department.id (onDelete: SetNull)` — Xuddi shunday, o'chirilgan bo'limdagi xodimlarning (User) departmentId maydoni NULL qiymatiga o'tadi.
- Indexes:
  - `@@unique([companyId, branchId, name])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([isActive])`


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/user.md`

# User Moduli Backend Tahlili

### Endpoint: POST /api/v1/users
**Controller:** src/modules/user/user.controller.ts:`create`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/users`
- Controller class + method nomi: `UserController` `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
login: 'john.doe'
password: 'StrongPass123'
role: 'employee'
companyId: 'uuid-company-id'
branchId: 'uuid-branch-id'
departmentId: 'uuid-department-id'
positionId: 'uuid-position-id'
managerId: 'uuid-manager-id'
workScheduleId: 'uuid-work-schedule-id'
employeeNo: 'EMP-001'
firstName: 'John'
lastName: 'Doe'
middleName: 'Michael'
phone: '+998901234567'
email: 'john@example.com'
address: 'Tashkent, Yunusobod'
passportSerial: 'AA1234567'
dateOfBirth: '1990-05-15'
avatarUrl: 'https://cdn.example.com/avatars/john.png'
baseSalary: 5000000

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `CreateUserDto` (`src/modules/user/dto/create-user.dto.ts`)
- `login`: string, `@IsString()`, `@MinLength(3)`, `@MaxLength(255)`
- `password`: string, `@IsString()`, `@MinLength(6)`, `@MaxLength(255)`
- `role`: UserRole, `@IsOptional()`, `@IsEnum(UserRole)`
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `departmentId`: string, `@IsOptional()`, `@IsUUID()`
- `positionId`: string, `@IsOptional()`, `@IsUUID()`
- `managerId`: string, `@IsOptional()`, `@IsUUID()`
- `workScheduleId`: string, `@IsOptional()`, `@IsUUID()`
- `employeeNo`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
- `firstName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `lastName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `middleName`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(255)`
- `phone`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(50)`
- `email`: string, `@IsOptional()`, `@IsEmail()`, `@MaxLength(255)`
- `address`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `passportSerial`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(100)`
- `dateOfBirth`: string, `@IsOptional()`, `@IsISO8601({ strict: true })`
- `avatarUrl`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `baseSalary`: number, `@IsOptional()`, `@IsNumber({ maxDecimalPlaces: 2 })`, `@Min(0)`

**5. Service:**
- `UserService.create` (`src/modules/user/user.service.ts`)
- Yangi foydalanuvchini yaratadi. Parolni hashlash, unikal maydonlarni va bog'lanishlarni tekshirish kabi ishlarni bajarib, User modeliga yozadi.

**6. Response:**
Foydalanuvchi obyekti qaytariladi:
- `id`: string
- `login`: string
- `role`: enum
- `companyId`: string
- `branchId`: string
- `departmentId`: string
- `positionId`: string
- `managerId`: string
- `workScheduleId`: string
- `employeeNo`: string
- `firstName`: string
- `lastName`: string
- `middleName`: string
- `phone`: string
- `email`: string
- `address`: string
- `passportSerial`: string
- `dateOfBirth`: date
- `avatarUrl`: string
- `faceDeviceUserId`: string
- `faceImageUrl`: string
- `baseSalary`: decimal
- `isActive`: boolean
- `isBlocked`: boolean
- `createdAt`: date
- `updatedAt`: date

**7. Error case:**
- `ForbiddenException` (superadmin yaratilayotganda)
- `ConflictException` (login req bo'lganda, login yoki email bazada bo'lganda)
- `NotFoundException` (company, branch, department, position, manager, work schedule topilmaganda)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/users
**Controller:** src/modules/user/user.controller.ts:`findAll`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/users`
- Controller class + method nomi: `UserController` `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

Query parametrlar:
companyId: misol yo'q
branchId: misol yo'q
departmentId: misol yo'q
positionId: misol yo'q
role: misol yo'q
isActive: true
isBlocked: false
search: 'john'
page: 1
limit: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UserQueryDto` (`src/modules/user/dto/user-query.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `branchId`: string, `@IsOptional()`, `@IsUUID()`
- `departmentId`: string, `@IsOptional()`, `@IsUUID()`
- `positionId`: string, `@IsOptional()`, `@IsUUID()`
- `role`: UserRole, `@IsOptional()`, `@IsEnum(UserRole)`
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`
- `isBlocked`: boolean, `@IsOptional()`, `@IsBoolean()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `page`: number, `@IsOptional()`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- `UserService.findAll` (`src/modules/user/user.service.ts`)
- Query parametrlariga ko'ra foydalanuvchilar (User) ro'yxatini filtrlash, qidirish va paginatsiya bilan o'qiydi. Shuningdek har bir rol bo'yicha statistika qaytaradi.

**6. Response:**
Paginatsiya qilingan javob obyekti:
- `items`: Foydalanuvchilar massivi (har birida id, login, role, companyId va hk `USER_SELECT` bo'yicha)
- `total`: number
- `page`: number
- `limit`: number
- `totalPages`: number
- `stats`: Object (har bir rol bo'yicha sanoq)

**7. Error case:**
Odatda tashlanmaydi, auth va ruxsat xatolari bo'lishi mumkin (`ForbiddenException`, `UnauthorizedException`).


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`findOne`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/users/:id`
- Controller class + method nomi: `UserController` `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ID (param)` (`yo'q`)
Request DTO class yo'q, faqat `@Param('id', ParseUUIDPipe) id: string` qabul qiladi.

**5. Service:**
- `UserService.findOne` (`src/modules/user/user.service.ts`)
- Berilgan ID orqali bitta User'ni o'qiydi, so'rov yuborgan actorning (superadmin/admin/manager) ko'rish doirasiga kirishini tekshiradi.

**6. Response:**
Bitta foydalanuvchi obyekti (`USER_SELECT` dagi maydonlar bilan: `id`, `login`, `role`, `companyId` va h.k.)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Foydalanuvchi actorning ko'rish doirasidan tashqarida bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/me
**Controller:** src/modules/user/user.controller.ts:`updateOwnProfile`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/me`
- Controller class + method nomi: `UserController` `updateOwnProfile`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
firstName: 'John'
lastName: 'Doe'
middleName: 'Michael'
phone: '+998901234567'
email: 'john@example.com'
address: 'Tashkent, Yunusobod'
passportSerial: 'AA1234567'
dateOfBirth: '1990-05-15'
avatarUrl: 'https://cdn.example.com/avatars/john.png'

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UpdateOwnProfileDto` (`src/modules/user/dto/update-own-profile.dto.ts`)
- Barcha maydonlar `CreateUserDto` dan olingan ixtiyoriy (optional) maydonlar:
- `firstName`: string
- `lastName`: string
- `middleName`: string
- `phone`: string
- `email`: string
- `address`: string
- `passportSerial`: string
- `dateOfBirth`: string
- `avatarUrl`: string

**5. Service:**
- `UserService.updateOwnProfile` (`src/modules/user/user.service.ts`)
- Joriy foydalanuvchining o'z profil ma'lumotlarini (User modeli) yangilaydi. Email kiritilsa band emasligini tekshiradi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (Joriy foydalanuvchi bazadan topilmasa)
- `ConflictException` (Email allaqachon band bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`update`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id`
- Controller class + method nomi: `UserController` `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Barcha maydonlar `CreateUserDto` ga o'xshaydi (`password` dan tashqari), hech biriga specific example qayta yozilmagan. 
Misollar `CreateUserDto` dagi misollar bilan bir xil, barchasi optional.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `UpdateUserDto` (`src/modules/user/dto/update-user.dto.ts`)
`CreateUserDto` dan `password` maydonini olib tashlab, qolgan barcha maydonlarni `PartialType` qilingan versiyasi. Barcha maydonlar ixtiyoriy (optional).

**5. Service:**
- `UserService.update` (`src/modules/user/user.service.ts`)
- Berilgan ID dagi User obyektini yangilaydi. Administrator/manager huquqlari va ko'rish doirasini tekshiradi, noyob maydonlar band emasligini tekshiradi, va yozadi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa yoki relation modellar topilmasa)
- `ForbiddenException` (Huquq yetarli bo'lmasa yoki boshqa kompaniya ma'lumoti o'zgartirilayotgan bo'lsa)
- `ConflictException` (Login, email yoki employeeNo band bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/toggle-status
**Controller:** src/modules/user/user.controller.ts:`toggleStatus`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/toggle-status`
- Controller class + method nomi: `UserController` `toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ToggleUserStatusDto` (`src/modules/user/dto/toggle-user-status.dto.ts`)
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- `UserService.toggleStatus` (`src/modules/user/user.service.ts`)
- Foydalanuvchining aktivlik holatini (`isActive`) teskarisiga yoki berilgan qiymatga o'zgartiradi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/toggle-blocked
**Controller:** src/modules/user/user.controller.ts:`toggleBlocked`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/toggle-blocked`
- Controller class + method nomi: `UserController` `toggleBlocked`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isBlocked: true

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ToggleUserBlockedDto` (`src/modules/user/dto/toggle-user-blocked.dto.ts`)
- `isBlocked`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- `UserService.toggleBlocked` (`src/modules/user/user.service.ts`)
- Foydalanuvchini bloklangan yoki blokdan chiqarilgan holatga (`isBlocked`) o'tkazadi.

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/users/:id/change-password
**Controller:** src/modules/user/user.controller.ts:`changePassword`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/users/:id/change-password`
- Controller class + method nomi: `UserController` `changePassword`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
newPassword: 'NewStrongPass123'

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ChangePasswordDto` (`src/modules/user/dto/change-password.dto.ts`)
- `newPassword`: string, `@IsString()`, `@MinLength(6)`, `@MaxLength(255)`

**5. Service:**
- `UserService.changePassword` (`src/modules/user/user.service.ts`)
- Foydalanuvchining parolini yangilaydi (heshlaydi va saqlaydi).

**6. Response:**
Yangilangan bitta foydalanuvchi obyekti (`USER_SELECT` bo'yicha)

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa yoki admin superadmin parolini o'zgartirmoqchi bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/users/:id
**Controller:** src/modules/user/user.controller.ts:`delete`

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/users/:id`
- Controller class + method nomi: `UserController` `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q

**3. Guard:**
- `@Roles('superadmin', 'admin')`
- Yopiq endpoint (Bearer auth kutiladi)

**4. DTO:**
- Request DTO: `ID (param)` (`yo'q`)
Request DTO class yo'q, faqat `@Param('id', ParseUUIDPipe) id: string` qabul qiladi.

**5. Service:**
- `UserService.delete` (`src/modules/user/user.service.ts`)
- Berilgan ID ga ega User yozuvini bazadan butunlay o'chirib tashlaydi.

**6. Response:**
O'chirish holati: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException` (User topilmasa)
- `ForbiddenException` (Actorning ruxsati bo'lmasa, yoxud admin superadminni o'chirmoqchi bo'lsa)


**8. DB struktura:**
- Tegishli Prisma model: `User`
- Maydonlar ta'rifi (barchasi, `schema.prisma` bo'yicha):
  - `id`: String, majburiy, `@id @default(uuid()) @db.Uuid`
  - `login`: String, majburiy, `@unique @db.VarChar(255)`
  - `passwordHash`: String, majburiy, `@db.VarChar(255)`
  - `role`: UserRole (enum), majburiy, `@default(employee)`
  - `companyId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `branchId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `departmentId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `positionId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `managerId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `workScheduleId`: String, ixtiyoriy (`?`), `@db.Uuid`
  - `employeeNo`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `firstName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `lastName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `middleName`: String, ixtiyoriy (`?`), `@db.VarChar(255)`
  - `phone`: String, ixtiyoriy (`?`), `@db.VarChar(50)`
  - `email`: String, ixtiyoriy (`?`), `@unique @db.VarChar(255)`
  - `address`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `passportSerial`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `dateOfBirth`: DateTime, ixtiyoriy (`?`), `@db.Date`
  - `avatarUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `faceDeviceUserId`: String, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `faceDescriptor`: String, ixtiyoriy (`?`)
  - `faceImageUrl`: String, ixtiyoriy (`?`), `@db.VarChar(500)`
  - `baseSalary`: Decimal, ixtiyoriy (`?`), `@db.Decimal(15, 2)`
  - `isActive`: Boolean, majburiy, `@default(true)`
  - `isBlocked`: Boolean, majburiy, `@default(false)`
  - `createdAt`: DateTime, majburiy, `@default(now()) @db.Timestamptz(6)`
  - `updatedAt`: DateTime, majburiy, `@updatedAt @db.Timestamptz(6)`
- Chiquvchi relations (outgoing):
  - `User.companyId -> Company.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `User.departmentId -> Department.id (onDelete: SetNull)`
  - `User.positionId -> Position.id (onDelete: SetNull)`
  - `User.workScheduleId -> WorkSchedule.id (onDelete: SetNull)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Kiruvchi relations (incoming):
  - `Attendance.employeeId -> User.id (onDelete: Cascade)`
  - `RawAttendanceLog.employeeId -> User.id (onDelete: SetNull)`
  - `SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)`
  - `Advance.employeeId -> User.id (onDelete: Cascade)`
  - `EmployeeLeave.employeeId -> User.id (onDelete: Cascade)`
  - `Payroll.employeeId -> User.id (onDelete: Cascade)`
  - `Notification.userId -> User.id (onDelete: Cascade)`
  - `PushToken.userId -> User.id (onDelete: Cascade)`
  - `RefreshToken.userId -> User.id (onDelete: Cascade)`
  - `User.managerId -> User.id (onDelete: SetNull)`
- Model index/unique:
  - `@@unique([companyId, employeeNo])`
  - `@@unique([companyId, faceDeviceUserId])`
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([departmentId])`
  - `@@index([positionId])`
  - `@@index([managerId])`
  - `@@index([role])`
  - `@@index([isActive])`

---


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/auth.md`

# Auth Module API Documentation

Bu hujjat `auth` modulining backend qismini tahlil qilgan holda, mavjud endpointlar, ularning ishlash mantig'i, ma'lumotlar bazasi va cURL orqali sinovdan o'tgan real JSON javoblarini o'z ichiga oladi. Asosiy URL: `http://localhost:4000/api/v1`

---

### Endpoint: POST /api/v1/auth/login
**Controller:** src/modules/auth/auth.controller.ts:login

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/login`
- Controller class + method nomi: `AuthController` -> `login`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "login": "admin",
  "password": "password123",
  "deviceType": "web",
  "deviceName": "Chrome",
  "pushToken": "fcm-test"
}
```

**3. Guard:**
- Public (Ochiq endpoint)

**4. DTO:**
- Request DTO: `LoginDto` (src/modules/auth/dto/login.dto.ts)
- `login`: Tip - String, Validatorlar - `@IsString()`, `@IsNotEmpty()`
- `password`: Tip - String, Validatorlar - `@IsString()`, `@MinLength(1)`
- `deviceType`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `deviceName`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `pushToken`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`

**5. Service:**
- Service method: `login` (src/modules/auth/auth.service.ts)
- Tavsifi: Foydalanuvchini `login` yoki `email` orqali bazadan qidiradi. Parolni solishtiradi. Foydalanuvchining statusini tekshiradi va Access, Refresh tokenlarni yaratadi. Refresh va push tokenlar bazaga saqlanadi.

**6. Response:**
- Qaytariladigan javob shakli: Auth obyekt (Tokenlar va user obyekti).
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "tokenType": "Bearer",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
    "refreshToken": "refresh.1787416416.1789144416.bmrdL23rRGsDnhmw...",
    "expiresIn": 1728000,
    "user": {
      "id": "c1d0f9e5-ff89-403d-9568-d670e72aac9c",
      "login": "admin",
      "role": "admin",
      "companyId": null,
      "branchId": null,
      "departmentId": null,
      "positionId": null,
      "firstName": "admin",
      "lastName": "Seed",
      "middleName": null,
      "phone": null,
      "email": null,
      "employeeNo": null,
      "faceDeviceUserId": null,
      "isActive": true,
      "isBlocked": false
    }
  },
  "path": "/api/v1/auth/login",
  "timestamp": "2026-08-22T16:33:36.472Z"
}
```

**7. Error case:**
- `401 Unauthorized`: "Login and password are required", "Invalid login or password"
- `403 Forbidden`: "You do not have access to login", "User is inactive", "User is blocked"

**8. DB struktura:**
- Prisma modellari: `User`, `RefreshToken`, `PushToken` (prisma/schema.prisma)
- `User`: `id` (Uuid), `login` (String, unique), `passwordHash` (String), `role` (Enum), `isActive` (Boolean), `isBlocked` (Boolean).
- `RefreshToken`: `id` (Uuid), `userId` (Uuid), `token` (String), `expiresAt` (DateTime).
- `PushToken`: `id` (Uuid), `userId` (Uuid), `token` (String, unique).

**cURL Misol:**
```bash
curl -s -X POST http://localhost:4000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"login":"admin","password":"password123","deviceType":"web","deviceName":"Chrome"}'
```

---

### Endpoint: POST /api/v1/auth/refresh
**Controller:** src/modules/auth/auth.controller.ts:refresh

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/refresh`
- Controller class + method nomi: `AuthController` -> `refresh`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "refreshToken": "refresh.1787416416.1789144416.bmrdL23r...",
  "deviceType": "web",
  "deviceName": "Chrome",
  "pushToken": "fcm-test-2"
}
```

**3. Guard:**
- Public (Ochiq endpoint)

**4. DTO:**
- Request DTO: `RefreshTokenDto` (src/modules/auth/dto/refresh-token.dto.ts)
- `refreshToken`: Tip - String, Validatorlar - `@IsString()`, `@IsNotEmpty()`
- `deviceType`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `deviceName`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`
- `pushToken`: Tip - String, Validatorlar - `@IsOptional()`, `@IsString()`

**5. Service:**
- Service method: `refresh` (src/modules/auth/auth.service.ts)
- Tavsifi: Jo'natilgan refresh tokenni bazadan tekshiradi, amal qilish muddatini ko'radi. Agar token yaroqli bo'lsa, yangi access va refresh tokenlarni yaratadi va foydalanuvchiga qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Auth obyekt (Yangi tokenlar va user obyekti).
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "tokenType": "Bearer",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC...",
    "expiresIn": 1728000,
    "user": {
      "id": "c1d0f9e5-ff89-403d-9568-d670e72aac9c",
      "login": "admin",
      "role": "admin",
      "isActive": true,
      "isBlocked": false
    }
  },
  "path": "/api/v1/auth/refresh",
  "timestamp": "2026-08-22T16:33:48.837Z"
}
```

**7. Error case:**
- `401 Unauthorized`: "Refresh token is required", "Refresh token is invalid", "Refresh token expired"
- `403 Forbidden`: "User is inactive", "User is blocked"

**8. DB struktura:**
- Prisma modellari: `User`, `RefreshToken`, `PushToken` (prisma/schema.prisma)
- Xuddi shu modellar ishlatiladi.

**cURL Misol:**
```bash
curl -s -X POST http://localhost:4000/api/v1/auth/refresh \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"your_refresh_token_here"}'
```

---

### Endpoint: POST /api/v1/auth/logout
**Controller:** src/modules/auth/auth.controller.ts:logout

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/logout`
- Controller class + method nomi: `AuthController` -> `logout`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "refreshToken": "refresh.1787416416.1789144416.bmrdL23r...",
  "pushToken": "fcm-test-2"
}
```

**3. Guard:**
- Public (Ochiq endpoint)

**4. DTO:**
- Request DTO: `RefreshTokenDto` (src/modules/auth/dto/refresh-token.dto.ts)

**5. Service:**
- Service method: `logout` (src/modules/auth/auth.service.ts)
- Tavsifi: `refreshToken` ni bazadan o'chiradi. Agar `pushToken` mavjud bo'lsa, uni ham o'chirib yuboradi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: true }`
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true
  },
  "path": "/api/v1/auth/logout",
  "timestamp": "2026-08-22T16:33:53.396Z"
}
```

**7. Error case:**
- Maxsus xatolik tashlamaydi.

**8. DB struktura:**
- Prisma modellari: `RefreshToken`, `PushToken` (prisma/schema.prisma)
- Ushbu jadvallardan mos yozuvlar o'chiriladi.

**cURL Misol:**
```bash
curl -s -X POST http://localhost:4000/api/v1/auth/logout \
  -H 'Content-Type: application/json' \
  -d '{"refreshToken":"your_refresh_token_here"}'
```

---

### Endpoint: GET /api/v1/auth/me
**Controller:** src/modules/auth/auth.controller.ts:getMe

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/auth/me`
- Controller class + method nomi: `AuthController` -> `getMe`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `Bearer Token` auth.
- Rollar: `superadmin`, `admin`, `manager`, `employee`

**4. DTO:**
- Request DTO yo'q (Headerdan olinadi).

**5. Service:**
- Service method: `getMe` (src/modules/auth/auth.service.ts)
- Tavsifi: Access tokenning payload qismidagi foydalanuvchi IDsi bo'yicha user ma'lumotlarini bazadan oladi.

**6. Response:**
- Qaytariladigan javob shakli: Foydalanuvchi ma'lumotlari.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "c1d0f9e5-ff89-403d-9568-d670e72aac9c",
    "login": "admin",
    "role": "admin",
    "companyId": null,
    "branchId": null,
    "departmentId": null,
    "positionId": null,
    "firstName": "admin",
    "lastName": "Seed",
    "middleName": null,
    "phone": null,
    "email": null,
    "employeeNo": null,
    "faceDeviceUserId": null,
    "isActive": true,
    "isBlocked": false
  },
  "path": "/api/v1/auth/me",
  "timestamp": "2026-08-22T16:33:44.148Z"
}
```

**7. Error case:**
- `401 Unauthorized`: "Invalid token signature", "User not found"
- `403 Forbidden`: "You do not have access to login", "User is inactive", "User is blocked"

**8. DB struktura:**
- Prisma modeli: `User` (prisma/schema.prisma)

**cURL Misol:**
```bash
curl -s -X GET http://localhost:4000/api/v1/auth/me \
  -H 'Authorization: Bearer your_access_token_here'
```


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/branch.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

### Endpoint: POST /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/branches`
- Controller class + method nomi: `BranchController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- name: 'Main Branch'
- address: 'Tashkent city, Chilonzor district'
- latitude: 41.2995
- longitude: 69.2401
- radius: 100

**3. Guard:**
- Token talab qilinadi (`@ApiBearerAuth()` va `@CurrentUser()` dekoratorlari yordamida `AccessTokenPayload` kutiladi)
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `CreateBranchDto` (`src/modules/branch/dto/create-branch.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `address`: string, `@IsOptional()`, `@IsString()`, `@MaxLength(500)`
- `latitude`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsLatitude()`
- `longitude`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsLongitude()`
- `radius`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`

**5. Service:**
- Service method: `BranchService.create` (`src/modules/branch/branch.service.ts`)
- Kompaniya mavjudligini va branch nomining yagonaligini tekshiradi, so'ng yangi `Branch` yozuvini yaratadi. Yozuv radiusiga default qiymat sifatida 100 olinadi (agar kiritilmagan bo'lsa).

**6. Response:**
- Yaratilgan yangi `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Company not found") - Kompaniya topilmasa.
- `ConflictException` ("Branch name is required") - Branch nomi bo'sh jo'natilganda.
- `ConflictException` ("Branch name already exists in this company") - Shu kompaniyada bu nomli branch allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/branches
**Controller:** src/modules/branch/branch.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches`
- Controller class + method nomi: `BranchController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q. (Query parametrlar)
- companyId: misol yo'q
- search: 'main'
- isActive: true
- page: 1
- limit: 10

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `BranchQueryDto` (`src/modules/branch/dto/branch-query.dto.ts`)
- `companyId`: string, `@IsOptional()`, `@IsUUID()`
- `search`: string, `@IsOptional()`, `@IsString()`
- `isActive`: boolean, `@IsOptional()`, `@Transform`, `@IsBoolean()`
- `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `BranchService.findAll` (`src/modules/branch/branch.service.ts`)
- DB'dan ko'rsatilgan filterlar (companyId, isActive, search) bo'yicha branch'lar ro'yxatini va jami sonini paginatsiya qilib o'qib keladi. `search` qiymati nomi va manzili bo'yicha izlanadi.

**6. Response:**
- Paginatsiya qilingan javob qaytadi:
  - `items`: Topilgan `Branch` obyektlari massivi
  - `total`: Umumiy elementlar soni (number)
  - `page`: Joriy sahifa (number)
  - `limit`: Sahifadagi limit (number)
  - `totalPages`: Jami sahifalar soni (number)

**7. Error case:**
- Alohida error tashlanmaydi (barcha query parametrlar ixtiyoriy). 

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO yo'q. Faqat route param `id` (`@Param('id', ParseUUIDPipe)`).

**5. Service:**
- Service method: `BranchService.findOne` (`src/modules/branch/branch.service.ts`)
- Berilgan UUID ID si bo'yicha branch ni izlaydi, agar foydalanuvchining ko'rishga ruxsati bo'lsa (scope tekshiruvidan o'tsa) javob sifatida qaytaradi.

**6. Response:**
- Topilgan bitta `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - ID orqali DB dan branch topilmaganda yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- name: 'Main Branch'
- address: 'Tashkent city, Chilonzor district'
- latitude: 41.2995
- longitude: 69.2401
- radius: 100

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `UpdateBranchDto` (`src/modules/branch/dto/update-branch.dto.ts`)
- Barcha `CreateBranchDto` maydonlari `PartialType` orqali ixtiyoriy (optional) bo'ladi.

**5. Service:**
- Service method: `BranchService.update` (`src/modules/branch/branch.service.ts`)
- Branche borligi tekshiriladi, berilgan ixtiyoriy field'larni avvalgilariga o'zgartiradi. Agar ismi yoki kompaniyasi o'zgarsa, yangi nomning unikal ligini tekshiradi va DB da saqlaydi.

**6. Response:**
- Yangilangan `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - Ko'rsatilgan ID bilan branch topilmasa.
- `NotFoundException` ("Company not found") - Agar companyId o'zgartirilmoqchi bo'lsa va bu company topilmasa.
- `ConflictException` ("Branch name is required") - Branch nomiga bo'sh satr jo'natilganda.
- `ConflictException` ("Branch name already exists in this company") - Shu kompaniyada bu yangi nomli branch allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: PATCH /api/v1/branches/:id/toggle-status
**Controller:** src/modules/branch/branch.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/branches/:id/toggle-status`
- Controller class + method nomi: `BranchController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- isActive: false

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO: `ToggleBranchStatusDto` (`src/modules/branch/dto/toggle-branch-status.dto.ts`)
- `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Service method: `BranchService.toggleStatus` (`src/modules/branch/branch.service.ts`)
- ID bo'yicha filialni oladi. Agar status berilgan bo'lsa uni o'zlashtiradi, aks holda oldingisining teskarisi qilib yangilaydi (toggle).

**6. Response:**
- Yangilangan `Branch` obyekti to'liq qaytariladi.
- Maydonlar: id, companyId, name, address, latitude, longitude, radius, isActive, createdAt, updatedAt.

**7. Error case:**
- `NotFoundException` ("Branch not found") - Ko'rsatilgan ID bilan branch topilmasa yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (va aloqador modellar)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- `companyId`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.Uuid`
- `name`: String, Majburiy, `@@unique([companyId, name])` da qatnashadi, `@db.VarChar(255)`
- `address`: String, Ixtiyoriy (`?`), `@db.VarChar(500)`
- `latitude`: Float, Ixtiyoriy (`?`)
- `longitude`: Float, Ixtiyoriy (`?`)
- `radius`: Int, Ixtiyoriy (`?`), `@default(100)`
- `isActive`: Boolean, Majburiy, `@default(true)`
- `createdAt`: DateTime, Majburiy, `@default(now())`, `@db.Timestamptz(6)`
- `updatedAt`: DateTime, Majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- **Relations / references:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/branches/:id
**Controller:** src/modules/branch/branch.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/branches/:id`
- Controller class + method nomi: `BranchController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- Token talab qilinadi
- `@Roles('superadmin', 'admin')` ruxsat etilgan.

**4. DTO:**
- Request DTO yo'q. Faqat route param `id` (`@Param('id', ParseUUIDPipe)`).

**5. Service:**
- Service method: `BranchService.delete` (`src/modules/branch/branch.service.ts`)
- ID bo'yicha DB'dan filial topiladi va tekshiriladi, ruxsat bo'lsa bu filial DB dan o'chirib tashlanadi (pastdagi "Relations" bandiga qarang — bu yerda CASCADE emas, balki SetNull ustunlik qiladi, ya'ni bog'liq yozuvlar o'chmaydi, faqat `branchId` ularda NULL bo'lib qoladi).

**6. Response:**
- JSON obyekt qaytadi:
  - `success`: `true`
  - `id`: o'chirilgan filialning id qiymati (string)

**7. Error case:**
- `NotFoundException` ("Branch not found") - ID orqali branch topilmasa yuzaga keladi.

**8. DB struktura:**
- Model: `Branch` (o'chiriladigan asosiy yozuv)
- `id`: String, Majburiy, `@default(uuid())`, `@db.Uuid`
- **Relations / references — bu Branch modelining O'ZI qaysi modelga bog'liq:**
  - `Branch.companyId -> Company.id (onDelete: Cascade)`
- **Relations / references — Branch'ga qaysi modellar BOG'LANGAN (o'chirilganda ta'sirlanadi, barchasi `onDelete: SetNull`, ya'ni CASCADE emas — bog'liq qator o'chmaydi, faqat `branchId` NULL bo'ladi):**
  - `Department.branchId -> Branch.id (onDelete: SetNull)`
  - `User.branchId -> Branch.id (onDelete: SetNull)`
  - `WorkSchedule.branchId -> Branch.id (onDelete: SetNull)`
  - `Terminal.branchId -> Branch.id (onDelete: SetNull)`
  - `Attendance.branchId -> Branch.id (onDelete: SetNull)`
  - `Holiday.branchId -> Branch.id (onDelete: SetNull)`
  - `EmployeeLeave.branchId -> Branch.id (onDelete: SetNull)`
- **Indexes:**
  - `@@unique([companyId, name])`
  - `@@index([companyId])`
  - `@@index([isActive])`

### Changes from commit d143c02 (order: 1)
- Service  updated: added default , uniqueness check for , new pagination in  (filters: companyId, search, isActive, page, limit).
- DTO  and  now include optional , , ,  with validation decorators.
- Controller  updated to reflect new query parameters and guards.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/attendance.md`

# Attendance Module API Documentation

Bu hujjat `attendance` modulining barcha endpointlarini tavsiflaydi.

---

### Endpoint: GET /api/v1/attendance/kpi-template/:companyId
**Controller:** src/modules/attendance/attendance.controller.ts:getKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/kpi-template/:companyId`
- Controller class + method nomi: `AttendanceController` -> `getKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- URL parametrlari:
  - `companyId` (UUID) - Kompaniya ID si. Masalan: `105a743b-8e71-4e87-aaff-131f27837a22`

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `companyId` majburiy).
- `companyId`: UUID formatida bo'lishi shart (`ParseUUIDPipe`).

**5. Service:**
- Service method: `getKpiTemplate` (src/modules/attendance/attendance.service.ts)
- Tavsifi: `companyId` ga biriktirilgan KPI sozlamalarini (`Setting` modelidan `ATTENDANCE_KPI` kaliti orqali) oladi. Ruxsat (Scope) tekshiriladi. Agar mavjud bo'lmasa, bo'sh obyekt qaytaradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "latePenaltyPerMinute": 0,
    "earlyLeavePenaltyPerMinute": 0,
    "overtimeBonusPerMinute": 0,
    "faceSimilarityThreshold": 90
  },
  "path": "/api/v1/attendance/kpi-template/105a743b-8e71-4e87-aaff-131f27837a22",
  "timestamp": "2026-08-22T16:38:59.448Z"
}
```

**7. Error case:**
- `UnauthorizedException`: `401` Noto'g'ri token.
- `ForbiddenException`: `403` Ruxsat etilmagan kompaniya ID (Scope error).
- `BadRequestException`: `400` Noto'g'ri UUID formati.

**8. DB struktura:**
- Prisma modeli: `Setting`
- `Setting` modeliga `companyId` va `key="ATTENDANCE_KPI"` sifatida JSON formatida saqlanadi.

**cURL misol:**
```bash
curl -s -X GET "http://localhost:4000/api/v1/attendance/kpi-template/105a743b-8e71-4e87-aaff-131f27837a22" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PUT /api/v1/attendance/kpi-template
**Controller:** src/modules/attendance/attendance.controller.ts:upsertKpiTemplate

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PUT /api/v1/attendance/kpi-template`
- Controller class + method nomi: `AttendanceController` -> `upsertKpiTemplate`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
  "latePenaltyPerMinute": 1000,
  "earlyLeavePenaltyPerMinute": 500,
  "overtimeBonusPerMinute": 2000,
  "faceSimilarityThreshold": 95
}
```

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin')`

**4. DTO:**
- Request DTO: `AttendanceKpiTemplateDto`
  - `companyId` (UUID, ixtiyoriy, superadmin uchun majburiy)
  - `latePenaltyPerMinute` (Number, ixtiyoriy, min: 0)
  - `earlyLeavePenaltyPerMinute` (Number, ixtiyoriy, min: 0)
  - `overtimeBonusPerMinute` (Number, ixtiyoriy, min: 0)
  - `faceSimilarityThreshold` (Number, ixtiyoriy, min: 0, max: 100)

**5. Service:**
- Service method: `upsertKpiTemplate` (src/modules/attendance/attendance.service.ts)
- Tavsifi: `upsertKpiTemplate` orqali `Setting` jadvaliga yozadi. Yoki yangilaydi (upsert).

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "latePenaltyPerMinute": 1000,
    "earlyLeavePenaltyPerMinute": 500,
    "overtimeBonusPerMinute": 2000,
    "faceSimilarityThreshold": 95
  },
  "path": "/api/v1/attendance/kpi-template",
  "timestamp": "2026-08-22T16:39:06.133Z"
}
```

**7. Error case:**
- `UnauthorizedException`: `401` Token yaroqsiz.
- `ForbiddenException`: `403` Boshqa kompaniyaga o'zgartirish kiritish taqiqlangan.

**8. DB struktura:**
- Prisma modeli: `Setting`
- `Setting` modelida `value` (JSON) da qiymatlar saqlanadi.

**cURL misol:**
```bash
curl -s -X PUT "http://localhost:4000/api/v1/attendance/kpi-template" \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"companyId": "105a743b-8e71-4e87-aaff-131f27837a22", "latePenaltyPerMinute": 1000, "faceSimilarityThreshold": 95}'
```

---

### Endpoint: POST /api/v1/attendance/check-in
**Controller:** src/modules/attendance/attendance.controller.ts:checkIn

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-in`
- Controller class + method nomi: `AttendanceController` -> `checkIn`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0",
  "imageBase64": "data:image/jpeg;base64,...",
  "eventTime": "2026-06-08T09:05:00.000Z",
  "contentType": "image/jpeg"
}
```

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckInDto`
  - `employeeId` (UUID, majburiy)
  - `terminalId` (UUID, ixtiyoriy)
  - `imageBase64` (String, min 10 belgi, majburiy)
  - `contentType` (String, ixtiyoriy)
  - `eventTime` (ISO8601, ixtiyoriy)
  - `notes` (String, ixtiyoriy)

**5. Service:**
- Service method: `checkIn` (src/modules/attendance/attendance.service.ts)
- Tavsifi: AWS Rekognition yordamida `imageBase64` yuz tasviri bilan xodimning saqlangan yuz tasvirini solishtiradi. `faceSimilarityThreshold` ga asosan tasdiqlanadi. S3 ga rasmni yuklab URL ni qaytaradi. `Attendance` yozuvini yaratadi yoki yangilaydi. `checkIn` maydonini belgilaydi. Ish vaqtlari (lateMinutes) hisob-kitob qilinadi.

**6. Response:**
```json
{
  "statusCode": 500,
  "error": "Internal Server Error",
  "message": "AWS Rekognition face verification failed: The security token included in the request is invalid.",
  "path": "/api/v1/attendance/check-in",
  "timestamp": "2026-08-22T16:39:20.794Z"
}
```
*(AWS konfiguratsiyasi local muhitda bo'lmagani uchun Internal error қайтмоқда. Muvaqqiyatli bo'lsa `Attendance` obyektini qaytaradi)*

**7. Error case:**
- `BadRequestException`: `400` Validatsiya xatolari yoki tasvir noto'g'ri.
- `NotFoundException`: `404` Xodim topilmadi.
- `ConflictException`: `409` Tasvir mos kelmadi yoki allaqachon check-in qilingan.
- `InternalServerErrorException`: `500` AWS Rekognition xatosi.

**8. DB struktura:**
- Prisma modeli: `Attendance`
- `checkIn` (DateTime), `lateMinutes` (Int), `checkInImageUrl` (String) maydonlariga ma'lumotlar yoziladi.

**cURL misol:**
```bash
curl -s -X POST "http://localhost:4000/api/v1/attendance/check-in" \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0", "imageBase64": "data:image/jpeg;base64,..."}'
```

---

### Endpoint: POST /api/v1/attendance/check-out
**Controller:** src/modules/attendance/attendance.controller.ts:checkOut

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/check-out`
- Controller class + method nomi: `AttendanceController` -> `checkOut`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0",
  "imageBase64": "data:image/jpeg;base64,...",
  "eventTime": "2026-06-08T18:05:00.000Z",
  "contentType": "image/jpeg"
}
```

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceCheckOutDto` (check-in bilan bir xil).
  - `employeeId` (UUID, majburiy)
  - `terminalId` (UUID, ixtiyoriy)
  - `imageBase64` (String, min 10 belgi, majburiy)
  - `contentType` (String, ixtiyoriy)
  - `eventTime` (ISO8601, ixtiyoriy)
  - `notes` (String, ixtiyoriy)

**5. Service:**
- Service method: `checkOut` (src/modules/attendance/attendance.service.ts)
- Tavsifi: AWS orqali yuz tasdiqlanadi. Bugungi sanaga oid `Attendance` yozuviga `checkOut` sanasini qo'shadi. `workedMinutes`, `earlyLeaveMinutes`, `overtimeMinutes` kabilarni hisoblab chiqadi va saqlaydi.

**6. Response:**
```json
{
  "statusCode": 500,
  "error": "Internal Server Error",
  "message": "AWS Rekognition face verification failed: The security token included in the request is invalid.",
  "path": "/api/v1/attendance/check-out",
  "timestamp": "2026-08-22T16:39:20.794Z"
}
```
*(AWS integratsiyasi ishlamagani uchun xuddi Check-In kabi error qaytaradi yoki muvaffaqiyatli attendance obyektini qaytaradi)*

**7. Error case:**
- Check-in bilan bir xil xatolar qaytarishi mumkin.
- `BadRequestException`: `400` Validatsiya xatolari yoki tasvir noto'g'ri.
- `NotFoundException`: `404` Xodim topilmadi.
- `ConflictException`: `409` Tasvir mos kelmadi yoki allaqachon check-out qilingan.

**8. DB struktura:**
- Prisma modeli: `Attendance`
- `checkOut`, `workedMinutes`, `earlyLeaveMinutes`, `overtimeMinutes`, `checkOutImageUrl` yangilanadi.

**cURL misol:**
```bash
curl -s -X POST "http://localhost:4000/api/v1/attendance/check-out" \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0", "imageBase64": "data:image/jpeg;base64,..."}'
```

---

### Endpoint: GET /api/v1/attendance
**Controller:** src/modules/attendance/attendance.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance`
- Controller class + method nomi: `AttendanceController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- URL Query parametrlar:
  - `companyId` (UUID)
  - `branchId` (UUID)
  - `employeeId` (UUID)
  - `terminalId` (UUID)
  - `status` (Enum: present, absent, etc)
  - `dateFrom` (ISO8601, masalan: 2026-06-01)
  - `dateTo` (ISO8601)
  - `page` (Number, default: 1)
  - `limit` (Number, default: 10)

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `AttendanceQueryDto` da ko'rsatilgan sanalar ISO8601 qat'iy formatida (strict: true) kutiladi. Limit eng ko'pi bilan 100.

**5. Service:**
- Service method: `findAll` (src/modules/attendance/attendance.service.ts)
- Tavsifi: `findAll` orqali berilgan parametrlarga mos keluvchi attendance jadvallarini DB dan oladi, foydalanuvchining rollariga qarab scope chegaralaydi (faqat o'z kompaniyasi/filialiga ruxsat).

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "data": [
      {
        "id": "f4408a17-44ca-4024-a590-b59c24e67a56",
        "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
        "branchId": null,
        "employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0",
        "terminalId": null,
        "date": "2026-08-06T00:00:00.000Z",
        "checkIn": "2026-08-06T04:00:00.000Z",
        "checkOut": "2026-08-06T13:00:00.000Z",
        "status": "present",
        "source": "terminal",
        "workStartTime": "09:00",
        "workEndTime": "18:00",
        "workedMinutes": 540,
        "lateMinutes": 0,
        "earlyLeaveMinutes": 0,
        "overtimeMinutes": 0,
        "checkInImageUrl": null,
        "checkOutImageUrl": null,
        "notes": null,
        "appliedAdjustments": [],
        "createdAt": "2026-08-07T14:16:35.275Z",
        "updatedAt": "2026-08-07T14:16:35.275Z"
      }
    ],
    "total": 66000,
    "page": 1,
    "limit": 10,
    "totalPages": 6600
  },
  "path": "/api/v1/attendance",
  "timestamp": "2026-08-22T16:38:45.313Z"
}
```

**7. Error case:**
- `BadRequestException`: `400` Filter formati xato.
- `UnauthorizedException`: `401` Token yaroqsiz.

**8. DB struktura:**
- Prisma modeli: `Attendance`

**cURL misol:**
```bash
curl -s -X GET "http://localhost:4000/api/v1/attendance?page=1&limit=10" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/attendance/:id
**Controller:** src/modules/attendance/attendance.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/:id`
- Controller class + method nomi: `AttendanceController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- URL parametr: `id` (UUID). Masalan: `f4408a17-44ca-4024-a590-b59c24e67a56`

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: yo'q. `id` parametrigacha `ParseUUIDPipe` qollanilgan.

**5. Service:**
- Service method: `findOne` (src/modules/attendance/attendance.service.ts)
- Tavsifi: Prisma orqali bitta elementni izlab qaytaradi. Boshqa filial/kompaniya ma'lumotini o'qishga harakat qilsa ruxsat bermaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "f4408a17-44ca-4024-a590-b59c24e67a56",
    "companyId": "105a743b-8e71-4e87-aaff-131f27837a22",
    "branchId": null,
    "employeeId": "0fc03f71-85e4-4699-9b37-ee5437afa5c0",
    "terminalId": null,
    "date": "2026-08-06T00:00:00.000Z",
    "checkIn": "2026-08-06T04:00:00.000Z",
    "checkOut": "2026-08-06T13:00:00.000Z",
    "status": "present",
    "source": "terminal",
    "workStartTime": "09:00",
    "workEndTime": "18:00",
    "workedMinutes": 540,
    "lateMinutes": 0,
    "earlyLeaveMinutes": 0,
    "overtimeMinutes": 0,
    "checkInImageUrl": null,
    "checkOutImageUrl": null,
    "notes": null,
    "appliedAdjustments": [],
    "createdAt": "2026-08-07T14:16:35.275Z",
    "updatedAt": "2026-08-07T14:16:35.275Z"
  },
  "path": "/api/v1/attendance/f4408a17-44ca-4024-a590-b59c24e67a56",
  "timestamp": "2026-08-22T16:38:51.747Z"
}
```

**7. Error case:**
- `BadRequestException`: `400` Noto'g'ri UUID format.
- `NotFoundException`: `404` Topilmadi.

**8. DB struktura:**
- Prisma modeli: `Attendance`

**cURL misol:**
```bash
curl -s -X GET "http://localhost:4000/api/v1/attendance/f4408a17-44ca-4024-a590-b59c24e67a56" \
-H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: POST /api/v1/attendance/self/check-in
**Controller:** src/modules/attendance/attendance.controller.ts:selfCheckIn

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/self/check-in`
- Controller class + method nomi: `AttendanceController` -> `selfCheckIn`

**2. ApiBody / Misollar:**
- `multipart/form-data` formatida:
  - `notes` (string, optional) — Izoh, max 1000 belgi
  - `file` (binary, optional) — Yuz rasmi (AWS face verification uchun)

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('employee')` — faqat xodimlar uchun

**4. DTO:**
- `SelfAttendanceCheckInDto`:
  - `notes?: string` — ixtiyoriy, max 1000 belgi

**5. Service:**
- Service method: `selfCheckIn` (src/modules/attendance/services/attendance.service.ts)
- Tavsifi: Xodim o'zi app orqali kirishini qayd etadi. AWS yuz verifikatsiyasi amalga oshiriladi. Token'dagi `sub` orqali xodim aniqlanadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "uuid",
    "employeeId": "uuid",
    "date": "2026-08-22",
    "checkIn": "2026-08-22T09:05:00.000Z",
    "checkOut": null,
    "status": "present",
    "source": "self",
    "lateMinutes": 5,
    "checkInImageUrl": "https://s3.amazonaws.com/..."
  }
}
```

**7. Error case:**
- `401` — Noto'g'ri token
- `403` — Role `employee` emas
- `409` — Bugun allaqachon check-in qilingan

**8. DB struktura:**
- Prisma modeli: `Attendance` (source: `self`)

**cURL misol:**
```bash
curl -s -X POST "http://localhost:4000/api/v1/attendance/self/check-in" \
-H "Authorization: Bearer <TOKEN>" \
-F "notes=Ishga keldim"
```

---

### Endpoint: POST /api/v1/attendance/self/check-out
**Controller:** src/modules/attendance/attendance.controller.ts:selfCheckOut

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/attendance/self/check-out`
- Controller class + method nomi: `AttendanceController` -> `selfCheckOut`

**2. ApiBody / Misollar:**
- `multipart/form-data` formatida:
  - `notes` (string, optional) — Izoh, max 1000 belgi
  - `file` (binary, optional) — Yuz rasmi (AWS face verification uchun)

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('employee')` — faqat xodimlar uchun

**4. DTO:**
- `SelfAttendanceCheckOutDto`:
  - `notes?: string` — ixtiyoriy, max 1000 belgi

**5. Service:**
- Service method: `selfCheckOut` (src/modules/attendance/services/attendance.service.ts)
- Tavsifi: Xodim o'zi app orqali chiqishini qayd etadi. AWS yuz verifikatsiyasi amalga oshiriladi. Ishlangan vaqt, `workedMinutes`, `earlyLeaveMinutes`, `overtimeMinutes` hisoblanadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "uuid",
    "employeeId": "uuid",
    "date": "2026-08-22",
    "checkIn": "2026-08-22T09:05:00.000Z",
    "checkOut": "2026-08-22T18:10:00.000Z",
    "status": "present",
    "source": "self",
    "workedMinutes": 545,
    "earlyLeaveMinutes": 0,
    "overtimeMinutes": 10,
    "checkOutImageUrl": "https://s3.amazonaws.com/..."
  }
}
```

**7. Error case:**
- `401` — Noto'g'ri token
- `403` — Role `employee` emas
- `404` — Bugungi check-in topilmadi (avval check-in qilinmagan)

**8. DB struktura:**
- Prisma modeli: `Attendance` — `checkOut`, `workedMinutes`, `overtimeMinutes` yangilanadi

**cURL misol:**
```bash
curl -s -X POST "http://localhost:4000/api/v1/attendance/self/check-out" \
-H "Authorization: Bearer <TOKEN>" \
-F "notes=Ishdan ketdim"
```

---

### Endpoint: GET /api/v1/attendance/self/sessions
**Controller:** src/modules/attendance/attendance.controller.ts:selfListSessions

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/attendance/self/sessions`
- Controller class + method nomi: `AttendanceController` -> `selfListSessions`

**2. ApiBody / Misollar (Query params):**
- `dateFrom` (ISO8601, optional) — Boshlanish sanasi. Masalan: `2026-08-01`
- `dateTo` (ISO8601, optional) — Tugash sanasi. Masalan: `2026-08-31`
- `page` (int, default: 1) — Sahifa raqami
- `limit` (int, default: 10, max: 100) — Sahifadagi elementlar soni

**3. Guard:**
- Auth: `Bearer Token`
- Roles: `@Roles('employee')` — faqat o'z sessiyalarini ko'radi

**4. DTO:**
- `AttendanceSessionQueryDto`:
  - `dateFrom?: string` — ISO8601
  - `dateTo?: string` — ISO8601
  - `page?: number` — min: 1
  - `limit?: number` — min: 1, max: 100

**5. Service:**
- Service method: `selfListSessions` (src/modules/attendance/services/attendance.service.ts)
- Tavsifi: Xodim o'zining check-in/check-out sessiyalarini ko'radi. Token'dagi `sub` orqali `employeeId` aniqlanadi, boshqa xodimlar ko'rinmaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "date": "2026-08-22",
        "checkIn": "2026-08-22T09:05:00.000Z",
        "checkOut": "2026-08-22T18:10:00.000Z",
        "status": "present",
        "workedMinutes": 545,
        "lateMinutes": 5,
        "overtimeMinutes": 10
      }
    ],
    "total": 22,
    "page": 1,
    "limit": 10
  }
}
```

**7. Error case:**
- `401` — Noto'g'ri token
- `403` — Role `employee` emas

**8. DB struktura:**
- Prisma modeli: `Attendance` — `employeeId` = current user, sana oralig'i filter

**cURL misol:**
```bash
curl -s -X GET "http://localhost:4000/api/v1/attendance/self/sessions?dateFrom=2026-08-01&dateTo=2026-08-31&page=1&limit=10" \
-H "Authorization: Bearer <TOKEN>"
```


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ummat******illlo@gmail.com/apiproperty_example_yozish.md`

# ApiProperty example yozish

### 👤 Foydalanuvchi:

Salom 

BUnga  ApiPrperty example yozib ber

### 🤖 ChatGPT:

Salom 🙂  

`@ApiProperty` dekoratori **NestJS Swagger** uchun ishlatiladi. U model (DTO) ichidagi property haqida hujjatlash (docs) yaratadi va `example` qo‘shish orqali Swagger UI’da namunaviy qiymat ko‘rsatish mumkin.  

Masalan:  

```ts
import { ApiProperty } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({
    example: 'john_doe',
    description: 'Unique username of the user',
  })
  username: string;

  @ApiProperty({
    example: 'John',
    description: 'First name of the user',
  })
  firstName: string;

  @ApiProperty({
    example: 'Doe',
    description: 'Last name of the user',
  })
  lastName: string;

  @ApiProperty({
    example: 'john@example.com',
    description: 'Email address of the user',
  })
  email: string;

  @ApiProperty({
    example: 'strongPassword123!',
    description: 'Password for account login',
  })
  password: string;
}
```

👉 Shunda Swagger UI’da har bir field yonida **example** qiymatlar chiqib turadi.  

Aytchi, sening DTO’ing qanaqa fieldlardan iborat? Shu bo‘yicha moslab `ApiProperty` yozib beraymi?

---


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/setting.md`

### Endpoint: POST /api/v1/settings
**Controller:** src/modules/setting/setting.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/settings
- SettingController.create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `key`: attendance_kpi_template
- `value`: { "latePenaltyPerMinute": 1000 }

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `CreateSettingDto` (src/modules/setting/dto/create-setting.dto.ts)
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `key`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `value`: `Record<string, unknown>`, `@IsOptional()`, `@IsObject()`

**5. Service:**
- `SettingService.create` (src/modules/setting/setting.service.ts)
- Yangi sozlamani (Setting) yaratadi. Avval company mavjudligi tekshiriladi, so'ngra shu kompaniya uchun xuddi shu `key` (kalit) bilan boshqa sozlama yo'qligi tekshiriladi (yagona bo'lishi kerak). So'ng bazaga yoziladi.

**6. Response:**
- `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Company not found" (Agar company topilmasa, HTTP 404)
- `ConflictException`: "Setting key is required" (Agar key bo'sh yoki probellardan iborat bo'lsa, HTTP 409)
- `ConflictException`: "Setting key already exists for this company" (Agar key takrorlansa, HTTP 409)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q (Boshqa modellar `Setting`ga bog'lanmagan)
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: GET /api/v1/settings
**Controller:** src/modules/setting/setting.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/settings
- SettingController.findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `SettingQueryDto` (src/modules/setting/dto/setting-query.dto.ts)
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `search`: `string`, `@IsOptional()`, `@IsString()` (misol: 'attendance')
- `page`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)` (misol: 1)
- `limit`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)` (misol: 10)

**5. Service:**
- `SettingService.findAll` (src/modules/setting/setting.service.ts)
- Sozlamalarni filter (search `key` bo'yicha) va kompaniya doirasida (`companyId`) paginatsiya bilan qaytaradi.

**6. Response:**
- Paginatsiya obyekti:
  - `items`: `Setting` qatorlari massivi
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Xatoliklar tashlanmaydi (Faqat validatsiya xatolari bo'lishi mumkin)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: GET /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/settings/:id
- SettingController.findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- Request body DTO yo'q, URL param `id`: `string`, `ParseUUIDPipe` bilan tasdiqlanadi.

**5. Service:**
- `SettingService.findOne` (src/modules/setting/setting.service.ts)
- Berilgan ID ga ko'ra sozlamani qidiradi va joriy foydalanuvchining ko'rish huquqini (scope) tekshiradi.

**6. Response:**
- `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali chiqishi mumkin)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: PATCH /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/settings/:id
- SettingController.update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `companyId`: misol yo'q
- `key`: attendance_kpi_template
- `value`: { "latePenaltyPerMinute": 1000 }

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- `UpdateSettingDto` (src/modules/setting/dto/update-setting.dto.ts) -> `PartialType(CreateSettingDto)`
- `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
- `key`: `string`, `@IsOptional()`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `value`: `Record<string, unknown>`, `@IsOptional()`, `@IsObject()`

**5. Service:**
- `SettingService.update` (src/modules/setting/setting.service.ts)
- Sozlamani id bo'yicha yangilaydi. Agar `key` yoki `companyId` o'zgarayotgan bo'lsa, ularning bazada unikalligi (`ensureUniqueKey`) va company mavjudligi (`ensureCompanyExists`) tekshiriladi.

**6. Response:**
- Yangilangan `Setting` obyekti:
  - `id`: `String`
  - `companyId`: `String`
  - `key`: `String`
  - `value`: `Json` (yoki `null`)
  - `createdAt`: `DateTime`
  - `updatedAt`: `DateTime`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- `NotFoundException`: "Company not found" (Agar companyId yuborilgan bo'lsa va topilmasa, HTTP 404)
- `ConflictException`: "Setting key is required" (Agar key bo'sh bo'lib qolsa, HTTP 409)
- `ConflictException`: "Setting key already exists for this company" (Agar yangi key takrorlansa, HTTP 409)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`

### Endpoint: DELETE /api/v1/settings/:id
**Controller:** src/modules/setting/setting.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/settings/:id
- SettingController.delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin')` class-darajasida

**4. DTO:**
- Request body DTO yo'q, URL param `id`: `string`, `ParseUUIDPipe` bilan tasdiqlanadi.

**5. Service:**
- `SettingService.delete` (src/modules/setting/setting.service.ts)
- Sozlamani id bo'yicha qidirib, foydalanuvchi scope-da ekanligini tekshiradi va bazadan o'chirib yuboradi.

**6. Response:**
- Ob'ekt qaytariladi: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: "Setting not found" (Agar sozlama topilmasa, HTTP 404)
- (Yashirin xatolik) `ForbiddenException` ruxsat etilmagan scope xatoligi (`assertWithinScope` orqali)

**8. DB struktura:**
- Prisma modeli: `Setting`
- Ustunlar:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`, `@id`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `key`: `String`, majburiy, `@db.VarChar(255)`
  - `value`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Setting.companyId -> Company.id (onDelete: Cascade)`
  2. Kiruvchi: Yo'q
- Indexes / Uniques:
  - `@@unique([companyId, key])`
  - `@@index([companyId])`


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/terminal.md`

# Terminal Moduli Backend Tahlili

### Endpoint: POST /api/v1/terminals
**Controller:** src/modules/terminal/terminal.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/terminals` (API global prefix qo'shilishi hisobga olingan holda)
- Controller class + method nomi: `TerminalController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- branchId: misol yo'q
- name: 'Main gate terminal'
- serialNumber: 'TRN-001'
- ipAddress: '192.168.1.100'
- port: 4370
- type: TerminalType.zkteco_face
- status: TerminalStatus.active
- connectionConfig: { username: 'admin', password: '12345' }
- lastSyncAt: '2026-06-08T10:00:00.000Z'

**3. Guard:**
- Class darajasida qo'llanilgan Guard'lar yo'q lekin dekoratorlar mavjud:
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `CreateTerminalDto` (`src/modules/terminal/dto/create-terminal.dto.ts`)
- companyId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- branchId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- name: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- serialNumber: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- ipAddress: `string | undefined`, `@IsOptional()`, `@IsIP()`
- port: `number | undefined`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(65535)`
- type: `TerminalType | undefined`, `@IsOptional()`, `@IsEnum(TerminalType)`
- status: `TerminalStatus | undefined`, `@IsOptional()`, `@IsEnum(TerminalStatus)`
- connectionConfig: `Record<string, unknown> | undefined`, `@IsOptional()`, `@IsObject()`
- lastSyncAt: `string | undefined`, `@IsOptional()`, `@IsString()`

**5. Service:**
- Service method: `TerminalService.create` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Yuborilgan `companyId` va `branchId` asosida joriy foydalanuvchining (actor) vakolatlari tekshiriladi (resolveCompanyBranchScope). Ko'rsatilgan company va branch mavjudligi hamda branch berilgan company'ga tegishliligi tasdiqlanadi. Serial raqami tizimda takrorlanmasligi tekshirib, xatosiz holatda yangi Terminal bazada yaratiladi.

**6. Response:**
- Qaytariladigan javob: Yangi yaratilgan `Terminal` obyekti to'liqligicha qaytariladi. Maydonlar: `id`, `companyId`, `branchId`, `name`, `serialNumber`, `ipAddress`, `port`, `type`, `status`, `connectionConfig`, `lastSyncAt`, `createdAt`, `updatedAt`.

**7. Error case:**
- `NotFoundException('Company not found')`: Agar berilgan companyId bo'yicha kompaniya topilmasa.
- `NotFoundException('Branch not found')`: Agar berilgan branchId bo'yicha filial topilmasa.
- `ConflictException('Branch does not belong to the selected company')`: Agar tanlangan filial ko'rsatilgan kompaniyaga tegishli bo'lmasa.
- `ConflictException('Terminal name is required')`: Agar nom probellardan iborat bo'lsa yoki noto'g'ri bo'lsa (400 Bad Request validatsiyadan tashqari).
- `ConflictException('Serial number is required')`: Agar serial raqami bo'sh bo'lsa.
- `ConflictException('Terminal serial number already exists')`: Agar xuddi shu serial raqamli terminal bazada allaqachon mavjud bo'lsa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi:
  - `id`: `String`, majburiy, `@id`, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `branchId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `serialNumber`: `String`, majburiy, `@unique`, `@db.VarChar(255)`
  - `ipAddress`: `String`, ixtiyoriy (`?`), `@db.VarChar(100)`
  - `port`: `Int`, ixtiyoriy (`?`)
  - `type`: `TerminalType`, majburiy, `@default(zkteco_face)`
  - `status`: `TerminalStatus`, majburiy, `@default(active)`
  - `connectionConfig`: `Json`, ixtiyoriy (`?`), `@db.Json`
  - `lastSyncAt`: `DateTime`, ixtiyoriy (`?`), `@db.Timestamptz(6)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  - **Chiquvchi:**
    - `Company.id` ga ishora qiluvchi maydon: `company -> Company` (`fields: [companyId]`, `references: [id]`, `onDelete: Cascade`)
    - `Branch.id` ga ishora qiluvchi maydon: `branch -> Branch` (`fields: [branchId]`, `references: [id]`, `onDelete: SetNull`)
  - **Kiruvchi:**
    - `Attendance.terminalId -> Terminal.id (onDelete: SetNull)`
    - `RawAttendanceLog.terminalId -> Terminal.id (onDelete: Cascade)`
- Indexlar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([status])`

---

### Endpoint: GET /api/v1/terminals
**Controller:** src/modules/terminal/terminal.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/terminals`
- Controller class + method nomi: `TerminalController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query qabul qiladi)
- search: 'TRN-001'
- page: 1
- limit: 10
- companyId: misol yo'q
- branchId: misol yo'q
- type: misol yo'q (Swaggerda type ko'rsatilmagan enumdan tashqari)
- status: misol yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `TerminalQueryDto` (`src/modules/terminal/dto/terminal-query.dto.ts`)
- companyId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- branchId: `string | undefined`, `@IsOptional()`, `@IsUUID()`
- type: `TerminalType | undefined`, `@IsOptional()`, `@IsEnum(TerminalType)`
- status: `TerminalStatus | undefined`, `@IsOptional()`, `@IsEnum(TerminalStatus)`
- search: `string | undefined`, `@IsOptional()`, `@IsString()`
- page: `number | undefined`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- limit: `number | undefined`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `TerminalService.findAll` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Kiritilgan query parametrlari bo'yicha filtirlash, qidirish (`name` va `serialNumber` orqali case-insensitive izlash), actor ruxsatlarini inobatga olgan holda terminallarni va ularning umumiy miqdorini bazadan oladi (Paginatsiya bilan).

**6. Response:**
- Qaytariladigan javob: Paginatsiya obyekti
  - `items`: `Terminal[]` (Terminal modeliga mos array)
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Maxsus xatolar service tomonidan tashlanmaydi (validatsiya xatolarini hisobga olmasa). Malumot topilmasa ochiq holda bo'sh ro'yxat va total 0 qaytadi.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: `POST /api/v1/terminals` dagi kabi barchasi aynan bir xil.
- Relations / references: `POST /api/v1/terminals` dagi kabi barchasi aynan bir xil.
- Indexlar:
  - `@@index([companyId])`
  - `@@index([branchId])`
  - `@@index([status])`
  - *Izoh*: `search` qidiruvi uchun maxsus indeks (`name` yoki `serialNumber` da) yo'q, lekin `serialNumber` fieldda `@unique` borligi qisman samarali ishlashiga imkon beradi.

---

### Endpoint: GET /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. Faqat URL Parametric Data olinadi: `id` parametri `ParseUUIDPipe` orqali `string` ko'rinishida.

**5. Service:**
- Service method: `TerminalService.findOne` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Berilgan `id` yordamida terminal bazadan izlanadi. Topilgandan so'ng, ushbu terminalga foydalanuvchining (actor) ruxsati bor-yo'qligi (`assertWithinScope`) tekshiriladi.

**6. Response:**
- Qaytariladigan javob: Topilgan `Terminal` obyekti to'liq maydonlari bilan.

**7. Error case:**
- `NotFoundException('Terminal not found')`: Agar berilgan `id` bilan terminal bazadan topilmasa.
- (Ehtimolli scope exception): `assertWithinScope` dan kirishga ruxsat yo'q degan xato kelib chiqishi mumkin (Forbidden).

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagi barcha maydonlar bilan bir xil.
- Relations / references: `POST /api/v1/terminals` bilan bir xil.
- Indexlar: `id` `@id` orqali indexlangan.

---

### Endpoint: PATCH /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `UpdateTerminalDto` obyekti qabul qilinadi, partial bo'lgani sababli `CreateTerminalDto` namunalari bilan bir xil, lekin barchasi ixtiyoriy:
  - name: 'Main gate terminal' (misol, Optional)
  - serialNumber: 'TRN-001' (misol, Optional)
  - ipAddress: '192.168.1.100' (misol, Optional)
  - port: 4370 (misol, Optional)
  - type: TerminalType.zkteco_face (misol, Optional)
  - status: TerminalStatus.active (misol, Optional)
  - connectionConfig: { username: 'admin', password: '12345' } (misol, Optional)
  - lastSyncAt: '2026-06-08T10:00:00.000Z' (misol, Optional)

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `UpdateTerminalDto` (`src/modules/terminal/dto/update-terminal.dto.ts`), `CreateTerminalDto`ning Partial ko'rinishi.
- `id` param qismi: URL dagi parametr, `ParseUUIDPipe` orqali olinadi.

**5. Service:**
- Service method: `TerminalService.update` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Bazadagi mavjud terminal topiladi. Foydalanuvchining unga ruxsati tekshiriladi. Agar `companyId` yoki `branchId` o'zgartirilayotgan bo'lsa ularning haqiqiyligi tekshiriladi. Agar `serialNumber` yangilanayotgan bo'lsa, tizimda takrorlanmasligi qayta tekshiriladi. Shundan so'ng, faqat yangilangan ma'lumotlar bazada yangilanadi (update operation).

**6. Response:**
- Qaytariladigan javob: Yangilangan `Terminal` obyekti to'liq ko'rinishda.

**7. Error case:**
- `NotFoundException('Terminal not found')`: O'zgartirilayotgan terminal topilmasa.
- `NotFoundException('Company not found')`: Yangi companyId bo'yicha kompaniya bo'lmasa.
- `NotFoundException('Branch not found')`: Yangi branchId bo'yicha filial bo'lmasa.
- `ConflictException('Branch does not belong to the selected company')`: Filial ko'rsatilgan kompaniyaga mos kelmasa.
- `ConflictException('Terminal serial number already exists')`: Yangi kiritilayotgan seriya raqami band bo'lsa.
- `ConflictException('Terminal name is required')`: Ism maydoni uzatilib uning qiymati bosh bo'shliq yoki null ga trim bo'lsa.
- `ConflictException('Serial number is required')`: Seriya raqamiga shunday xato holat kelsa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagidek `Terminal` barcha maydonlari mavjud.
- Relations / references: Yuqoridagidek barcha relatsiyalar amalda bir xil ishlatiladi.

---

### Endpoint: DELETE /api/v1/terminals/:id
**Controller:** src/modules/terminal/terminal.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/terminals/:id`
- Controller class + method nomi: `TerminalController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.

**3. Guard:**
- `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- DTO yo'q. `id` URL'dan olinadi `ParseUUIDPipe` yordamida.

**5. Service:**
- Service method: `TerminalService.delete` (`src/modules/terminal/terminal.service.ts`)
- Mantiq: Id bo'yicha terminalni topadi, ruxsatini (scope) tekshiradi va keyin `delete` so'rovini bazaga jo'natib obyektni to'liq o'chiradi.

**6. Response:**
- Qaytariladigan javob: `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException('Terminal not found')`: Agar o'chirilayotgan ID'ga ega terminal topilmasa.

**8. DB struktura:**
- Model nomi: `Terminal` (`prisma/schema.prisma`)
- Maydonlar ta'rifi: Yuqoridagilar kabi.
- Relations / references (O'chirish operatsiyasi uchun muhim):
  - **Chiquvchi:**
    - Terminal o'chirilganda u bog'langan Company yoki Branch larga ta'sir qilmaydi (Faqatgina ichki reference foreign key si uziladi).
  - **Kiruvchi (BU JUDA MUHIM):**
    - `Attendance.terminalId -> Terminal.id (onDelete: SetNull)` : Terminal o'chirilganda shu terminalda tekshiruvdan o'tgan attendance (davomat) yozuvlari **o'chirilmaydi**, balki ularning `terminalId` ustuni `NULL` qilib qo'yiladi.
    - `RawAttendanceLog.terminalId -> Terminal.id (onDelete: Cascade)` : Terminal o'chirilganda shu terminalga tegishli bo'lgan barcha asl xom davomat loglari (`RawAttendanceLog` dagi ma'lumotlar) **birgalikda butunlay o'chib ketadi**.
- Indexlar: `id` obyekti o'chiriladi va uning barcha bog'liqliklari triggerlar asosida ishlaydi.


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/auth.md`

### Endpoint: POST /api/v1/auth/login
**Controller:** src/modules/auth/controllers/auth.controller.ts:login

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/login`
- Controller class + method nomi: `AuthController.login`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- login: 'admin'
- password: '1234'
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `LoginDto` (`src/modules/auth/dto/login.dto.ts`)
- Har bir maydon:
  - `login`: `string`, `@IsString()`
  - `password`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.login` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Baza bo'yicha `login` yoki `email` orqali foydalanuvchini izlaydi va parolni tekshiradi (faqat superadmin, admin, manager ruxsat etilgan). Muvaffaqiyatli bo'lsa yangi refresh token yaratib bazaga (`RefreshToken` modeliga) yozadi va JWT access token hamda foydalanuvchi ma'lumotlarini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `tokenType`: `string` ('Bearer')
  - `accessToken`: `string`
  - `refreshToken`: `string`
  - `expiresIn`: `number`
  - `user`: ob'ekt (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('Login and password are required') - login yoki parol jo'natilmasa.
- `UnauthorizedException` ('Invalid login or password') - foydalanuvchi topilmasa yoki parol noto'g'ri bo'lsa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login. Employee users authenticate through turnstile integration.') - foydalanuvchi roli ruxsat etilmagan bo'lsa.
- `ForbiddenException` ('User is inactive') - foydalanuvchi faol bo'lmasa.
- `ForbiddenException` ('User is blocked') - foydalanuvchi bloklangan bo'lsa.

**8. DB struktura:**
- `User` modeli (o'qish):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `login`: `String @unique @db.VarChar(255)`
  - `email`: `String? @unique @db.VarChar(255)` (ixtiyoriy, `login` bo'yicha topilmasa shu orqali ham qidiriladi)
  - `passwordHash`: `String @db.VarChar(255)`
  - `role`: `UserRole @default(employee)` (enum)
  - `isActive`: `Boolean @default(true)`
  - `isBlocked`: `Boolean @default(false)`
  - `companyId`, `branchId`, `departmentId`, `positionId`: hammasi `String? @db.Uuid` (ixtiyoriy FK)
  - `firstName`, `lastName`, `middleName`, `phone`: `String? @db.VarChar(...)` (ixtiyoriy)
  - `employeeNo`: `String? @db.VarChar(100)`
  - `faceDeviceUserId`: `String? @db.VarChar(100)`
- **Relations (User):**
  - `User.companyId -> Company.id` (`onDelete: SetNull`)
  - `User.branchId -> Branch.id` (`onDelete: SetNull`)
  - `User.departmentId -> Department.id` (`onDelete: SetNull`)
  - `User.positionId -> Position.id` (`onDelete: SetNull`)
- `RefreshToken` modeli (yozish/create):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `userId`: `String @db.Uuid` (majburiy FK)
  - `token`: `String` (xeshlangan refresh token qiymati)
  - `expiresAt`: `DateTime @db.Timestamptz(6)` (majburiy)
  - `deviceType`: `String? @db.VarChar(100)` (ixtiyoriy)
  - `deviceName`: `String? @db.VarChar(255)` (ixtiyoriy)
  - `userAgent`: `String?` (ixtiyoriy)
  - `ipAddress`: `String? @db.VarChar(100)` (ixtiyoriy)
  - `lastUsedAt`: `DateTime? @db.Timestamptz(6)` (bu yozuvda `new Date()` bilan to'ldiriladi)
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade` — user o'chirilsa uning barcha refresh tokenlari ham o'chadi)
- **Indexlar:** `@@index([userId])`, `@@index([expiresAt])` (`RefreshToken`); `User.login`/`User.email` `@unique`.


### Endpoint: POST /api/v1/auth/refresh
**Controller:** src/modules/auth/controllers/auth.controller.ts:refresh

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/refresh`
- Controller class + method nomi: `AuthController.refresh`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- refreshToken: misol yo'q (`@ApiProperty()` — example ko'rsatilmagan)
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `RefreshTokenDto` (`src/modules/auth/dto/refresh-token.dto.ts`)
- Har bir maydon:
  - `refreshToken`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.refresh` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Berilgan refresh tokenni xeshlangan holatda bazadan qidiradi va amal qilish muddati o'tmaganligini tekshiradi. Muddat o'tgan bo'lsa, tokenni o'chiradi; agar amal qilsa `RefreshToken` ni so'nggi ishlatilgan vaqti va meta-ma'lumotlarini yangilaydi hamda yangi access token qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `tokenType`: `string` ('Bearer')
  - `accessToken`: `string`
  - `refreshToken`: mavjud emas (undefined)
  - `expiresIn`: `number`
  - `user`: ob'ekt (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('Refresh token is required') - refresh token jo'natilmasa.
- `UnauthorizedException` ('Refresh token is invalid') - token bazadan topilmasa.
- `UnauthorizedException` ('Refresh token expired') - tokenning amal qilish muddati tugagan bo'lsa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login...') - topilgan foydalanuvchi roli noto'g'ri bo'lsa.
- `ForbiddenException` ('User is inactive' / 'User is blocked') - foydalanuvchi bloklangan yoki faol bo'lmasa.

**8. DB struktura:**
- `RefreshToken` modeli (o'qish + yangilash):
  - `id`: `String @id @default(uuid()) @db.Uuid`
  - `userId`: `String @db.Uuid` (majburiy FK)
  - `token`: `String` (xeshlangan qiymat bo'yicha qidiriladi, `findFirst`)
  - `expiresAt`: `DateTime @db.Timestamptz(6)` — muddat tekshiriladi, o'tgan bo'lsa yozuv o'chiriladi (`delete`)
  - `deviceType`, `deviceName`: `String? @db.VarChar(...)` (yangilanadi, `update`)
  - `userAgent`: `String?`, `ipAddress`: `String? @db.VarChar(100)` (yangilanadi)
  - `lastUsedAt`: `DateTime? @db.Timestamptz(6)` (yangilanadi, `new Date()`)
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade`) — `include: { user: true }` bilan birga o'qiladi
- `User` modeli (o'qish, `RefreshToken.user` orqali):
  - `id`, `login`, `role` (`UserRole`), `isActive` (`Boolean`), `isBlocked` (`Boolean`) — `ensureUserCanLogin` tekshiruvi uchun
  - `companyId`, `branchId`, `departmentId`, `positionId`: `String? @db.Uuid` — javobga qaytariladi
- **Relations (User, javobga qaytarilganda):**
  - `User.companyId -> Company.id`, `User.branchId -> Branch.id`,
    `User.departmentId -> Department.id`, `User.positionId -> Position.id`
    (barchasi `onDelete: SetNull`)
- **Indexlar:** `@@index([userId])`, `@@index([expiresAt])`.


### Endpoint: POST /api/v1/auth/logout
**Controller:** src/modules/auth/controllers/auth.controller.ts:logout

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/auth/logout`
- Controller class + method nomi: `AuthController.logout`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- refreshToken: misol yo'q (`@ApiProperty()` — example ko'rsatilmagan)
- deviceType: 'web' (ixtiyoriy, misol bor)
- deviceName: 'Chrome on Windows' (ixtiyoriy, misol bor)

**3. Guard:**
- Qo'llangan guard'lar: `@Public()` (bu endpoint authentication talab qilmaydi)

**4. DTO:**
- Request DTO class nomi + fayl yo'li: `RefreshTokenDto` (`src/modules/auth/dto/refresh-token.dto.ts`)
- Har bir maydon:
  - `refreshToken`: `string`, `@IsString()`, `@MinLength(1)`
  - `deviceType`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`
  - `deviceName`: `string` (ixtiyoriy), `@IsOptional()`, `@IsString()`

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.logout` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Berilgan refresh tokenni xeshlangan holatda bazadan izlaydi va mos keluvchi yozuvlarni `RefreshToken` jadvalidan o'chiradi. Token bo'sh bo'lsa, xato bermasdan muvaffaqiyat holatini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - `success`: `boolean` (`true`)

**7. Error case:**
- Ushbu endpoint to'g'ridan-to'g'ri xatolik (Exception) tashlamaydi. Noto'g'ri yoki bo'sh token yuborilsa ham `{ success: true }` qaytaradi.

**8. DB struktura:**
- `RefreshToken` modeli (o'chirish, `deleteMany`):
  - `token`: `String` — xeshlangan qiymat bo'yicha mos yozuvlar qidiriladi va o'chiriladi (`where: { token: ... }`)
  - Boshqa maydonlarga (`userId`, `expiresAt`, va h.k.) bu operatsiyada tegilmaydi, faqat `token` shart sifatida ishlatiladi.
- **Relations (RefreshToken):**
  - `RefreshToken.userId -> User.id` (`onDelete: Cascade`) — bu endpointda ishlatilmaydi (foydalanuvchi o'qilmaydi), lekin modelning o'zida mavjud.


### Endpoint: GET /api/v1/auth/me
**Controller:** src/modules/auth/controllers/auth.controller.ts:me

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/auth/me`
- Controller class + method nomi: `AuthController.me`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (GET so'rov, DTO ishlatilmaydi).

**3. Guard:**
- Qo'llangan guard'lar: Metod darajasida `@Roles('superadmin', 'admin', 'manager')`.
- Qaysi rollar ruxsat etilgan: `superadmin`, `admin`, `manager`

**4. DTO:**
- Request DTO class nomi + fayl yo'li: Body qabul qilinmaydi, faqat tokendan kirgan user payloadi ishlatiladi (DTO yo'q, `@CurrentUser() user: AccessTokenPayload` ishlatilgan).

**5. Service:**
- Chaqirilayotgan service method nomi + fayl yo'li: `AuthService.getCurrentUser` (`src/modules/auth/services/auth.service.ts`)
- Mantiq tavsifi: Token orqali olingan foydalanuvchi id'si bo'yicha `User` jadvalidan ma'lumotlarni qidiradi. Uning faolligini tekshiradi va ruxsat berilgan bo'lsa, foydalanuvchining ochiq profil ma'lumotlarini qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli:
  - Foydalanuvchi ob'ekti (`id`, `login`, `role`, `companyId`, `branchId`, `departmentId`, `positionId`, `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`, `isActive`, `isBlocked`)

**7. Error case:**
- `UnauthorizedException` ('User not found') - bazadan foydalanuvchi topilmasa.
- `ForbiddenException` ('Only superadmin, admin, and manager users can login...') - topilgan foydalanuvchi roli noto'g'ri bo'lsa.
- `ForbiddenException` ('User is inactive') - foydalanuvchi faol bo'lmasa.
- `ForbiddenException` ('User is blocked') - foydalanuvchi bloklangan bo'lsa.

**8. DB struktura:**
- `User` modeli (o'qish, `findUnique({ where: { id } })`):
  - `id`: `String @id @default(uuid()) @db.Uuid` (token payload'dagi `sub` bilan qidiriladi)
  - `login`, `role` (`UserRole`), `isActive` (`Boolean`), `isBlocked` (`Boolean`) — `ensureUserCanLogin` tekshiruvi uchun
  - `companyId`, `branchId`, `departmentId`, `positionId`: `String? @db.Uuid`
  - `firstName`, `lastName`, `middleName`, `phone`, `email`, `employeeNo`, `faceDeviceUserId`: javobga qaytariladi
- **Relations (User):**
  - `User.companyId -> Company.id` (`onDelete: SetNull`)
  - `User.branchId -> Branch.id` (`onDelete: SetNull`)
  - `User.departmentId -> Department.id` (`onDelete: SetNull`)
  - `User.positionId -> Position.id` (`onDelete: SetNull`)
- **Indexlar:** `User.id` — `@id` (birlamchi kalit, qo'shimcha indeks shart emas).


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/notification.md`

### Endpoint: POST /api/v1/notifications
**Controller:** src/modules/notification/notification.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/notifications`
- Controller class + method nomi: `NotificationController` + `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: misol yo'q
title: 'Payroll ready'
message: 'June payroll has been prepared'
icon: NotificationIcon.money
isRead: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Request DTO: `CreateNotificationDto` (src/modules/notification/dto/create-notification.dto.ts)
- `userId`: `string`, `@IsOptional()`, `@IsUUID()`
- `title`: `string`, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`
- `message`: `string`, `@IsString()`, `@MinLength(1)`
- `icon`: `NotificationIcon`, `@IsOptional()`, `@IsEnum(NotificationIcon)`
- `isRead`: `boolean`, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Service method: `NotificationService.create` (src/modules/notification/notification.service.ts)
- Yangi bildirishnoma yaratadi (`Notification` jadvaliga yozadi). Agar actor superadmin bo'lmasa, `userId` bo'lishini talab qiladi va tegishli ruxsat (scope)larni tekshiradi.

**6. Response:**
- Yaratilgan `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `ForbiddenException`: 'userId is required for non-superadmin actors' (HTTP 403) - superadmin bo'lmaganlar uchun `userId` yo'q bo'lsa.
- `NotFoundException`: 'User not found' (HTTP 404) - kiritilgan `userId` mavjud bo'lmasa.
- `ForbiddenException` (HTTP 403) - kiritilgan user actor'ning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).
- `ConflictException`: 'Notification title is required' / 'Notification message is required' (HTTP 409) - bo'sh matn kiritilsa (`normalizeRequired` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: GET /api/v1/notifications
**Controller:** src/modules/notification/notification.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/notifications`
- Controller class + method nomi: `NotificationController` + `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Query parametrlari misollari:
userId: misol yo'q
icon: misol yo'q
isRead: false
search: 'payroll'
page: 1
limit: 10

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Query DTO: `NotificationQueryDto` (src/modules/notification/dto/notification-query.dto.ts)
- `userId`: `string`, `@IsOptional()`, `@IsUUID()`
- `icon`: `NotificationIcon`, `@IsOptional()`, `@IsEnum(NotificationIcon)`
- `isRead`: `boolean`, `@IsOptional()`, `@IsBoolean()`
- `search`: `string`, `@IsOptional()`, `@IsString()`
- `page`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`
- `limit`: `number`, `@IsOptional()`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `NotificationService.findAll` (src/modules/notification/notification.service.ts)
- Bildirishnomalarni o'qiydi. Foydalanuvchining (actorning) companyId/branchId scope'iga qarab filtrlaydi, qidiruv va paginatsiya ishlatadi.

**6. Response:**
- Paginatsiya qilingan obyekt qaytaradi:
  - `items`: `Notification[]` massivi
  - `total`: `number`
  - `page`: `number`
  - `limit`: `number`
  - `totalPages`: `number`

**7. Error case:**
- Maxsus xatolar ko'rsatilmagan (faqat default DTO validation xatoliklari bo'lishi mumkin).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: GET /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- DTO yo'q, faqat ID parametr: `@Param('id', ParseUUIDPipe) id: string`

**5. Service:**
- Service method: `NotificationService.findOne` (src/modules/notification/notification.service.ts)
- Berilgan ID bo'yicha bitta bildirishnomani bazadan o'qiydi va agar foydalanuvchiga tegishli (scope'iga mos) bo'lsa uni qaytaradi.

**6. Response:**
- Topilgan bitta `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403) - superadmin bo'lmagan shaxs `userId` si bo'lmagan xabarni ko'rmoqchi bo'lsa.
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: PATCH /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
userId: misol yo'q
title: 'Payroll ready'
message: 'June payroll has been prepared'
icon: NotificationIcon.money
isRead: false

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- Request DTO: `UpdateNotificationDto` (src/modules/notification/dto/update-notification.dto.ts, `CreateNotificationDto` ning Partial ko'rinishi)
- Hamma maydonlar ixtiyoriy.

**5. Service:**
- Service method: `NotificationService.update` (src/modules/notification/notification.service.ts)
- ID orqali bildirishnomani topib, uning qiymatlarini yangilaydi (faqat joriy foydalanuvchiga ruxsat etilgan scope'da ekanini tekshirib). `userId` o'zgarsa, uni ham scope bilan tekshiradi.

**6. Response:**
- Yangilangan bitta `Notification` obyekti qaytariladi.
- Maydonlari: `id` (String), `userId` (String?), `title` (String), `message` (String), `icon` (NotificationIcon?), `isRead` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime).

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403).
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).
- `NotFoundException`: 'User not found' (HTTP 404) - yangi kiritilgan `userId` topilmasa.
- `ConflictException`: 'Notification title is required' / 'Notification message is required' (HTTP 409) - bo'sh matn kiritilsa.

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`

---

### Endpoint: DELETE /api/v1/notifications/:id
**Controller:** src/modules/notification/notification.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/notifications/:id`
- Controller class + method nomi: `NotificationController` + `delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (controller darajasida)

**4. DTO:**
- DTO yo'q, faqat ID parametr: `@Param('id', ParseUUIDPipe) id: string`

**5. Service:**
- Service method: `NotificationService.delete` (src/modules/notification/notification.service.ts)
- ID orqali bildirishnomani topadi, unga ruxsat etilganini tekshiradi va bazadan butunlay o'chirib tashlaydi.

**6. Response:**
- O'chirish bajarilgani to'g'risida success obyekti qaytariladi:
  - `{ success: true, id: <o'chirilgan id> }`

**7. Error case:**
- `NotFoundException`: 'Notification not found' (HTTP 404) - ko'rsatilgan ID bilan yozuv topilmasa.
- `ForbiddenException`: 'Only superadmin can access global notifications' (HTTP 403).
- `ForbiddenException` (HTTP 403) - bildirishnoma actorning scope'iga to'g'ri kelmasa (`assertWithinScope` orqali).

**8. DB struktura:**
- Tegishli model: `Notification`
- `id`: `String` / majburiy / `@default(uuid())` / `@db.Uuid`
- `userId`: `String` / ixtiyoriy (`?`) / `@db.Uuid`
- `title`: `String` / majburiy / `@db.VarChar(255)`
- `message`: `String` / majburiy
- `icon`: `NotificationIcon` / ixtiyoriy (`?`)
- `isRead`: `Boolean` / majburiy / `@default(false)`
- `createdAt`: `DateTime` / majburiy / `@default(now())` / `@db.Timestamptz(6)`
- `updatedAt`: `DateTime` / majburiy / `@updatedAt` / `@db.Timestamptz(6)`
- Chiquvchi (bu model → boshqa model):
  - `user -> User.id (onDelete: Cascade)`
- Kiruvchi (boshqa modellar → bu model):
  - (Yo'q)
- Index/Unique:
  - `@@index([userId])`
  - `@@index([isRead])`


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/push-token.md`

# Push Token API Docs

### Endpoint: POST /api/v1/push-tokens
**Controller:** src/modules/push-token/push-token.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/push-tokens`
- Controller class + method nomi: `PushTokenController` -> `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "userId": "ffbf3676-4428-415b-9e6b-0833f249072d",
  "token": "ExponentPushToken[xxxx]",
  "platform": "android",
  "deviceId": "device-001",
  "deviceName": "Samsung A55",
  "lastSeenAt": "2026-06-08T10:00:00.000Z"
}
```

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `CreatePushTokenDto`
- `userId`: Tip - UUID, Validatorlar - Required
- `token`: Tip - String, Validatorlar - Required, MinLength: 1
- `platform`: Tip - String, Validatorlar - Optional, MaxLength: 50
- `deviceId`: Tip - String, Validatorlar - Optional, MaxLength: 255
- `deviceName`: Tip - String, Validatorlar - Optional, MaxLength: 255
- `lastSeenAt`: Tip - DateString, Validatorlar - Optional

**5. Service:**
- Service method: `create`
- Tavsifi: `ensureUserInScope` orqali userId joriy foydalanuvchi scope-ida ekanligini tekshiradi. `ensureUniqueToken` orqali token avval mavjud emasligiga ishonch hosil qiladi. DB da yangi `PushToken` yozuvini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `PushToken` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "7fa85f64-5717-4562-b3fc-2c963f66afa6",
    "userId": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "token": "ExponentPushToken[xxxx]",
    "platform": "android",
    "deviceId": "device-001",
    "deviceName": "Samsung A55",
    "lastSeenAt": "2026-06-08T10:00:00.000Z",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:00:00.000Z"
  }
}
```

**7. Error case:**
- `BadRequestException`: 400 Bad Request (DTO validatsiya xatosi).
- `UnauthorizedException`: 401 Unauthorized (Token yaroqsiz).
- `NotFoundException`: 404 Not Found ('User not found').
- `ConflictException`: 409 Conflict ('Push token is required' yoki 'Push token already exists').

**8. DB struktura:**
- Prisma modeli: `PushToken`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `userId`: `String`, majburiy, `@db.Uuid`
  - `token`: `String`, majburiy, `@unique`
  - `platform`: `String`, ixtiyoriy (`?`)
  - `deviceId`: `String`, ixtiyoriy (`?`)
  - `deviceName`: `String`, ixtiyoriy (`?`)
  - `lastSeenAt`: `DateTime`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`
- Relations (Chiquvchi):
  - `userId -> User.id (onDelete: Cascade)`
- Relations (Kiruvchi): Yo'q.
- Indekslar: Yo'q

**cURL misoli:**
```bash
curl -X POST http://localhost:4000/api/v1/push-tokens \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"ffbf3676-4428-415b-9e6b-0833f249072d", "token":"ExponentPushToken[xxxx]"}'
```

---

### Endpoint: GET /api/v1/push-tokens
**Controller:** src/modules/push-token/push-token.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/push-tokens`
- Controller class + method nomi: `PushTokenController` -> `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `userId`: `ffbf3676-4428-415b-9e6b-0833f249072d`
  - `platform`: `android`
  - `search`: `Exponent`
  - `page`: `1`
  - `limit`: `10`

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `PushTokenQueryDto`
- `userId`: Tip - UUID, Validatorlar - Optional
- `platform`: Tip - String, Validatorlar - Optional
- `search`: Tip - String, Validatorlar - Optional
- `page`: Tip - Number, Validatorlar - Min: 1, Default: 1
- `limit`: Tip - Number, Validatorlar - Min: 1, Max: 100, Default: 10

**5. Service:**
- Service method: `findAll`
- Tavsifi: Joriy userning `companyId` va `branchId` scope-iga asoslanib DB dan tokenlarni filtrlaydi. `search` qidiruv parametri orqali `token`, `deviceName`, `deviceId` ustunlari bo'yicha qidiradi (mode: insensitive). Natijani paginatsiya qilib qaytaradi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "7fa85f64-5717-4562-b3fc-2c963f66afa6",
        "userId": "ffbf3676-4428-415b-9e6b-0833f249072d",
        "token": "ExponentPushToken[xxxx]",
        "platform": "android",
        "deviceId": "device-001",
        "deviceName": "Samsung A55",
        "lastSeenAt": "2026-06-08T10:00:00.000Z",
        "createdAt": "2026-08-22T17:00:00.000Z",
        "updatedAt": "2026-08-22T17:00:00.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  }
}
```

**7. Error case:**
- `BadRequestException`: 400 Bad Request (Validatsiya xatosi).
- `UnauthorizedException`: 401 Unauthorized (Token yaroqsiz).

**8. DB struktura:**
- (Yuqoridagi model bilan bir xil)

**cURL misoli:**
```bash
curl -X GET 'http://localhost:4000/api/v1/push-tokens?page=1&limit=10' \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/push-tokens/:id
**Controller:** src/modules/push-token/push-token.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/push-tokens/:id`
- Controller class + method nomi: `PushTokenController` -> `findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat URL parametr: `:id` (UUID formatida)

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Yo'q (Faqat Param `id` `ParseUUIDPipe` orqali olinadi)

**5. Service:**
- Service method: `findOne`
- Tavsifi: Push tokenni DB dan qidiradi (`findPushTokenByIdOrThrow`). Topilgan tokenni joriy foydalanuvchi scope-ida ekanligini tasdiqlaydi (`assertPushTokenInScope`).

**6. Response:**
- Qaytariladigan javob shakli: Prisma `PushToken` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7fa85f64-5717-4562-b3fc-2c963f66afa6",
    "userId": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "token": "ExponentPushToken[xxxx]",
    "platform": "android",
    "deviceId": "device-001",
    "deviceName": "Samsung A55",
    "lastSeenAt": "2026-06-08T10:00:00.000Z",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:00:00.000Z"
  }
}
```

**7. Error case:**
- `BadRequestException`: 400 Bad Request (UUID formati noto'g'ri).
- `UnauthorizedException`: 401 Unauthorized (Token yaroqsiz).
- `ForbiddenException`: 403 Forbidden (Userning scope-idan tashqarida bo'lsa).
- `NotFoundException`: 404 Not Found ('Push token not found').

**8. DB struktura:**
- (Yuqoridagi model bilan bir xil)

**cURL misoli:**
```bash
curl -X GET http://localhost:4000/api/v1/push-tokens/7fa85f64-5717-4562-b3fc-2c963f66afa6 \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/push-tokens/:id
**Controller:** src/modules/push-token/push-token.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/push-tokens/:id`
- Controller class + method nomi: `PushTokenController` -> `update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "platform": "ios",
  "deviceName": "iPhone 13"
}
```

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `UpdatePushTokenDto` (`CreatePushTokenDto` ning Partial formati)

**5. Service:**
- Service method: `update`
- Tavsifi: DB dan eski yozuvni olib tekshiradi, scope bo'yicha ruxsat etilganini aniqlaydi. Agar yangi `userId` kelsa, uning ham scope doirasidaligini tekshiradi. Agar yangi `token` kelsa, ushbu id-dan tashqari boshqa tokenlar orasida bor-yo'qligini tekshirib (unique) xato qaytaradi. DB da token yozuvini yangilaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `PushToken` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7fa85f64-5717-4562-b3fc-2c963f66afa6",
    "userId": "ffbf3676-4428-415b-9e6b-0833f249072d",
    "token": "ExponentPushToken[xxxx]",
    "platform": "ios",
    "deviceId": "device-001",
    "deviceName": "iPhone 13",
    "lastSeenAt": "2026-06-08T10:00:00.000Z",
    "createdAt": "2026-08-22T17:00:00.000Z",
    "updatedAt": "2026-08-22T17:05:00.000Z"
  }
}
```

**7. Error case:**
- `BadRequestException`: 400 Bad Request (DTO yoki UUID xato).
- `UnauthorizedException`: 401 Unauthorized.
- `ForbiddenException`: 403 Forbidden (Boshqa kompaniya tokenini yangilashga urinish).
- `NotFoundException`: 404 Not Found ('Push token not found' yoki 'User not found').
- `ConflictException`: 409 Conflict ('Push token already exists').

**8. DB struktura:**
- (Yuqoridagi model bilan bir xil)

**cURL misoli:**
```bash
curl -X PATCH http://localhost:4000/api/v1/push-tokens/7fa85f64-5717-4562-b3fc-2c963f66afa6 \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"platform": "ios"}'
```

---

### Endpoint: DELETE /api/v1/push-tokens/:id
**Controller:** src/modules/push-token/push-token.controller.ts:remove

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/push-tokens/:id`
- Controller class + method nomi: `PushTokenController` -> `remove`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat URL parametr: `:id` (UUID formatida)

**3. Guard:**
- `@ApiBearerAuth()`
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Yo'q (Faqat Param `id` `ParseUUIDPipe` orqali olinadi)

**5. Service:**
- Service method: `remove`
- Tavsifi: Push tokenni DB dan qidiradi (`findPushTokenByIdOrThrow`). Topilgan tokenni joriy foydalanuvchi scope-ida ekanligini tasdiqlaydi (`assertPushTokenInScope`). DB dan tokenni o'chiradi.

**6. Response:**
- Qaytariladigan javob shakli: O'chirish holati.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "7fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
}
```

**7. Error case:**
- `BadRequestException`: 400 Bad Request (UUID formati noto'g'ri).
- `UnauthorizedException`: 401 Unauthorized.
- `ForbiddenException`: 403 Forbidden.
- `NotFoundException`: 404 Not Found ('Push token not found').

**8. DB struktura:**
- (Yuqoridagi model bilan bir xil)

**cURL misoli:**
```bash
curl -X DELETE http://localhost:4000/api/v1/push-tokens/7fa85f64-5717-4562-b3fc-2c963f66afa6 \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/position.md` _(takroriy nusxa — asosiy manbaga qarang, duplicates-report.md)_

### Endpoint: POST /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/positions`
- Controller class + method nomi: `PositionController.create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id'
departmentId: 'uuid-department-id'
name: 'Backend Developer'

**3. Guard:**
- Qo'llangan guard'lar: Metodda emas, Controller darajasida `@ApiBearerAuth()` va `@Roles(...)` qo'llangan.
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `CreatePositionDto` (`src/modules/position/dto/create-position.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `departmentId`: string, `@IsOptional()`, `@IsUUID()`
  - `name`: string, `@IsString()`, `@MinLength(1)`, `@MaxLength(255)`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.create` (`src/modules/position/position.service.ts`)
- Mantiq: Foydalanuvchi roli asosida (masalan manager uchun majburiy departmentId tekshiruvi bilan) ruxsatlarni aniqlaydi. Ko'rsatilgan nom, kompaniya va departament bo'yicha unikallikni ta'minlaydi va yangi `Position` yozuvini yaratadi.

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan `Position` obyekti. (Maydonlari: `id` (String), `companyId` (String), `departmentId` (String?), `name` (String), `isActive` (Boolean), `createdAt` (DateTime), `updatedAt` (DateTime)).

**7. Error case:**
- `NotFoundException`: 'Company not found' yoki 'Department not found'
- `ForbiddenException`: 'departmentId is required to create a position within your branch' yoki "You cannot access another branch's department"
- `ConflictException`: 'Department does not belong to the selected company', 'Position name already exists for this company and department', yoki 'Position name is required'

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi (bu model → boshqa model):
     - `Company`: `fields: [companyId]`, `references: [id]`, `onDelete: Cascade`
     - `Department`: `fields: [departmentId]`, `references: [id]`, `onDelete: SetNull`
  2. Kiruvchi (boshqa modellar → bu model):
     - `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar:
  - `@@unique([companyId, departmentId, name])`
  - `@@index([companyId])`
  - `@@index([departmentId])`
  - `@@index([isActive])`

---

### Endpoint: GET /api/v1/positions
**Controller:** src/modules/position/position.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions`
- Controller class + method nomi: `PositionController.findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Qidiruv parametrlari uchun misollar (Query DTO):
search: 'developer'
isActive: true
page: 1
limit: 10
companyId: misol yo'q
departmentId: misol yo'q

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `PositionQueryDto` (`src/modules/position/dto/position-query.dto.ts`)
- Maydonlar:
  - `companyId`: string, `@IsOptional()`, `@IsUUID()`
  - `departmentId`: string, `@IsOptional()`, `@IsUUID()`
  - `search`: string, `@IsOptional()`, `@IsString()`
  - `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`, `@Transform` qilingan
  - `page`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
  - `limit`: number, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.findAll` (`src/modules/position/position.service.ts`)
- Mantiq: Foydalanuvchining filiali va kompaniyasini inobatga olgan holda ro'yxatni filtrlaydi. Qidiruv kalit so'zi (`search`) va `isActive` bo'yicha filterlarni qo'llaydi, hamda ma'lumotlarni paginatsiya (skip, take) qilib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Paginatsiya obyekti.
  - `items`: `Position` obyektlari massivi
  - `total`: jami soni (Int)
  - `page`: joriy sahifa (Int)
  - `limit`: sahifa sig'imi (Int)
  - `totalPages`: jami sahifalar soni (Int)

**7. Error case:**
- Validatsiya (class-validator) xatolaridan tashqari to'g'ridan-to'g'ri exceptionlar tashlanmaydi, lekin guard'lar tomonidan ruxsat berilmagan xatolar (Forbidden) ehtimoli mavjud.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: (yuqoridagi kabi, barcha qidiriladigan va qaytadigan maydonlar `Position` modeliga tegishli).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Company` (Cascade), `Department` (SetNull)
  2. Kiruvchi: `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar: `@@index([companyId])`, `@@index([departmentId])`, `@@index([isActive])`, hamda qidiruv uchun qulaylik.

---

### Endpoint: GET /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.findOne`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q. Param: `id` (UUID)

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Alohida DTO klassi yo'q, `ParseUUIDPipe` orqali id qabul qilinadi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.findOne` (`src/modules/position/position.service.ts`)
- Mantiq: Berilgan ID asosida bazadan pozitsiyani izlaydi. Foydalanuvchining tegishli kompaniya va filialga doir ma'lumotlarini tekshiradi (manager faqat o'z filialidagi pozitsiyalarni ko'ra oladi).

**6. Response:**
- Qaytariladigan javob shakli: Topilgan `Position` obyekti (faqat bitta).

**7. Error case:**
- `NotFoundException`: 'Position not found' (agar topilmasa)
- `ForbiddenException`: 'You cannot access a position outside your branch' yoki "You cannot access another branch's data" (manager o'z vakolatidan chetga chiqsa). Va `assertWithinScope` orqali umuman kompaniyaga kirish ruxsati tekshiriladi.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi, Relations va Indekslar `POST` va `GET` holatlaridagi bilan aynan bir xil. (Kiruvchi relation o'chirish yoki o'zgartirish bo'lmagani uchun to'g'ridan-to'g'ri ta'sir etmaydi, lekin model ta'rifining bir qismidir).

---

### Endpoint: PATCH /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.update`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
companyId: 'uuid-company-id' (ixtiyoriy, UpdatePositionDto orqali)
departmentId: 'uuid-department-id' (ixtiyoriy)
name: 'Backend Developer' (ixtiyoriy)

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `UpdatePositionDto` (`src/modules/position/dto/update-position.dto.ts`) (CreatePositionDto dan meros olingan).
- Maydonlar: Barcha maydonlar (`companyId`, `departmentId`, `name`) `PartialType` bo'lgani uchun ixtiyoriy hisoblanadi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.update` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiyani topadi va unga tegishli ruxsatlarni tekshiradi. Yuborilgan qiymatlar (masalan nom o'zgarganda) asosida yangi ismning kompaniya/departament miqyosida ochiq (band emasligini) tekshiradi va pozitsiyani yangilaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Position` obyekti.

**7. Error case:**
- `NotFoundException`: 'Position not found' yoki 'Company not found' yoki 'Department not found'
- `ForbiddenException`: 'departmentId is required to keep a position within your branch', yoki ruxsat qilinmagan hududdagi ma'lumotga kirishda
- `ConflictException`: 'Position name already exists for this company and department', 'Position name is required', 'Department does not belong to the selected company'

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: (Oldingi endpointlar bilan aynan bir xil).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi: `Company` (Cascade), `Department` (SetNull)
  2. Kiruvchi: `User.positionId -> Position.id (onDelete: SetNull)`
- Tegishli indekslar: `@@unique([companyId, departmentId, name])` (tahrirlashda nom takroriyligi shu orqali baholanadi).

---

### Endpoint: PATCH /api/v1/positions/:id/toggle-status
**Controller:** src/modules/position/position.controller.ts:toggleStatus

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/positions/:id/toggle-status`
- Controller class + method nomi: `PositionController.toggleStatus`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
isActive: false

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO class nomi: `TogglePositionStatusDto` (`src/modules/position/dto/toggle-position-status.dto.ts`)
- Maydonlar:
  - `isActive`: boolean, `@IsOptional()`, `@IsBoolean()`

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.toggleStatus` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiyaning mavjud holatini tekshiradi, ruxsatlari mos bo'lsa `isActive` qiymatini kiritilgan holatga (yoki teskarisiga) o'zgartiradi va saqlaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan `Position` obyekti (o'zgartirilgan `isActive` statusi bilan).

**7. Error case:**
- `NotFoundException`: 'Position not found'
- `ForbiddenException`: O'z filialidan/vakolatidan tashqaridagi ma'lumotga ta'sir qilishda.

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: Asosan `isActive` maydoniga yoziladi.
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - boshqalari: (yuqoridagi kabi)
- Relations / references: (yuqoridagi kabi).
- Tegishli indekslar: `@@index([isActive])`

---

### Endpoint: DELETE /api/v1/positions/:id
**Controller:** src/modules/position/position.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/positions/:id`
- Controller class + method nomi: `PositionController.delete`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
Body yo'q.

**3. Guard:**
- Qo'llangan guard'lar: Controller darajasida `@ApiBearerAuth()`
- Rollar: `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: Alohida DTO klassi yo'q, faqat ID parametr `ParseUUIDPipe` orqali yuboriladi.

**5. Service:**
- Chaqirilayotgan service method nomi: `PositionService.delete` (`src/modules/position/position.service.ts`)
- Mantiq: Pozitsiya obyektini avval izlab topib (va foydalanuvchining unga ruxsati borligiga ishonch hosil qilib), undan so'ng bazadan o'chiradi.

**6. Response:**
- Qaytariladigan javob shakli: Muvaffaqiyat (success obyekti): `{ success: true, id: string }`

**7. Error case:**
- `NotFoundException`: 'Position not found'
- `ForbiddenException`: "You cannot access another branch's data" (ruxsati bo'lmagan branch).

**8. DB struktura:**
- Prisma modeli: `Position`
- Maydonlar ta'rifi: Barcha maydonlar o'chib ketadi (id: String...).
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `companyId`: `String`, majburiy, `@db.Uuid`
  - `departmentId`: `String`, ixtiyoriy (`?`), `@db.Uuid`
  - `name`: `String`, majburiy, `@db.VarChar(255)`
  - `isActive`: `Boolean`, majburiy, `@default(true)`
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations / references:
  1. Chiquvchi (bu model → boshqa model):
     - `Company`: `fields: [companyId]`, `references: [id]`, `onDelete: Cascade`
     - `Department`: `fields: [departmentId]`, `references: [id]`, `onDelete: SetNull`
  2. Kiruvchi (boshqa modellar → bu model) — MAJBURIY o'chirish harakati natijasi:
     - `User.positionId -> Position.id (onDelete: SetNull)`
       (Bu degani: Position o'chirilganda, shu pozitsiyada ishlagan foydalanuvchilar (`User`) o'chib ketmaydi, faqatgina ularning `positionId` maydoni `NULL` qiymat qabul qiladi.)
- Tegishli indekslar: Unikallik uchun bo'lgan barcha indekslar.


## Manba: `zdes_archive_docs/raw_history/backend_crud_review/salary-adjustment.md`

# SalaryAdjustment modulini backend tahlili

### Endpoint: POST /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:create

**1. Point (yo'nalish):**
- POST /api/v1/salary-adjustments
- SalaryAdjustmentController create

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- type: AdjustmentType.bonus
- category: AdjustmentCategory.manual
- amount: 150000
- date: 2026-06-08
- month: 2026-06
- reason: Manual bonus

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: CreateSalaryAdjustmentDto (src/modules/salary-adjustment/dto/create-salary-adjustment.dto.ts)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- type: AdjustmentType, @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- amount: number, @Type(() => Number), @IsNumber()
- date: string, @IsDateString()
- month: string, @IsOptional(), @IsString()
- reason: string, @IsOptional(), @IsString(), @MaxLength(1000)

**5. Service:**
- Service method: salaryAdjustmentService.create (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Kiritilgan ma'lumotlarga asosan yangi oylik tuzatish (salary adjustment) yozuvini `SalaryAdjustment` jadvaliga saqlaydi. Bunga qadar kompaniya va xodimning berilgan doira (scope) ichida ekanligini tekshiradi (ensureCompanyExists, ensureEmployeeInScope).

**6. Response:**
- Qaytariladigan javob shakli: Yaratilgan oylik tuzatish obyekti (aniq qaytadigan tiplar prisma modelidagi tiplardir)
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Company not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Employee not found' (shart bajarilmasa, HTTP 404)
- ConflictException: 'Employee does not belong to the selected company' (shart bajarilmasa, HTTP 409)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: GET /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findAll

**1. Point (yo'nalish):**
- GET /api/v1/salary-adjustments
- SalaryAdjustmentController findAll

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q
- companyId: misol yo'q
- employeeId: misol yo'q
- type: misol yo'q
- category: misol yo'q
- month: 2026-06
- search: bonus
- dateFrom: 2026-06-01
- dateTo: 2026-06-30
- page: 1
- limit: 10

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: SalaryAdjustmentQueryDto (src/modules/salary-adjustment/dto/salary-adjustment-query.dto.ts)
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsOptional(), @IsUUID()
- type: AdjustmentType, @IsOptional(), @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- month: string, @IsOptional(), @IsString()
- search: string, @IsOptional(), @IsString()
- dateFrom: string, @IsOptional(), @IsString()
- dateTo: string, @IsOptional(), @IsString()
- page: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1)
- limit: number, @IsOptional(), @Type(() => Number), @IsInt(), @Min(1), @Max(100)

**5. Service:**
- Service method: salaryAdjustmentService.findAll (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Mavjud oylik tuzatishlarni filtrlar, qidiruv va paginatsiya orqali `SalaryAdjustment` jadvalidan o'qib keladi. Natijalarni ro'yxat va jami soni bilan qaytaradi.

**6. Response:**
- Paginatsiya obyekti qaytadi:
  - items: SalaryAdjustment[] (oylik tuzatishlar massivi)
  - total: number (jami yozuvlar soni)
  - page: number (joriy sahifa)
  - limit: number (sahifadagi yozuvlar chegarasi)
  - totalPages: number (jami sahifalar soni)

**7. Error case:**
- ForbiddenException: Agar scope dan tashqarida bo'lsa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: GET /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findOne

**1. Point (yo'nalish):**
- GET /api/v1/salary-adjustments/:id
- SalaryAdjustmentController findOne

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO yo'q
- @Param('id') id: string, ParseUUIDPipe

**5. Service:**
- Service method: salaryAdjustmentService.findOne (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Bitta aniq ID ga ega oylik tuzatishni topadi va foydalanuvchining huquq doirasidaligini tekshirib qaytaradi.

**6. Response:**
- Qaytariladigan javob shakli: Topilgan oylik tuzatish obyekti
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (agar topilmasa, HTTP 404)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: PATCH /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:update

**1. Point (yo'nalish):**
- PATCH /api/v1/salary-adjustments/:id
- SalaryAdjustmentController update

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- companyId: misol yo'q
- employeeId: misol yo'q
- type: AdjustmentType.bonus
- category: AdjustmentCategory.manual
- amount: 150000
- date: 2026-06-08
- month: 2026-06
- reason: Manual bonus

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO: UpdateSalaryAdjustmentDto (src/modules/salary-adjustment/dto/update-salary-adjustment.dto.ts) (PartialType of CreateSalaryAdjustmentDto)
- Barcha maydonlar ixtiyoriy:
- companyId: string, @IsOptional(), @IsUUID()
- employeeId: string, @IsUUID()
- type: AdjustmentType, @IsEnum(AdjustmentType)
- category: AdjustmentCategory, @IsOptional(), @IsEnum(AdjustmentCategory)
- amount: number, @Type(() => Number), @IsNumber()
- date: string, @IsDateString()
- month: string, @IsOptional(), @IsString()
- reason: string, @IsOptional(), @IsString(), @MaxLength(1000)

**5. Service:**
- Service method: salaryAdjustmentService.update (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Mavjud oylik tuzatish yozuvini yangilaydi, agar kompaniya yoki xodim ID o'zgarsa yana huquq va mavjudlikni tekshiradi, keyin o'zgarishlarni ma'lumotlar bazasida `SalaryAdjustment` modeliga saqlaydi.

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan oylik tuzatish obyekti
- id: string
- companyId: string
- employeeId: string
- type: enum
- category: enum
- amount: number
- date: date
- month: string
- reason: string
- createdById: string
- updatedById: string
- createdAt: datetime
- updatedAt: datetime

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Company not found' (shart bajarilmasa, HTTP 404)
- NotFoundException: 'Employee not found' (shart bajarilmasa, HTTP 404)
- ConflictException: 'Employee does not belong to the selected company' (shart bajarilmasa, HTTP 409)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


### Endpoint: DELETE /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:delete

**1. Point (yo'nalish):**
- DELETE /api/v1/salary-adjustments/:id
- SalaryAdjustmentController delete

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q

**3. Guard:**
- @ApiBearerAuth()
- @Roles('superadmin', 'admin', 'manager')

**4. DTO:**
- Request DTO yo'q
- @Param('id') id: string, ParseUUIDPipe

**5. Service:**
- Service method: salaryAdjustmentService.delete (src/modules/salary-adjustment/salary-adjustment.service.ts)
- Berilgan ID ga mos oylik tuzatish yozuvini bazadan o'chiradi, avval uning huquq doirasidaligini tekshiradi.

**6. Response:**
- Obyekt qaytadi:
  - success: boolean (true)
  - id: string (o'chirilgan yozuv id si)

**7. Error case:**
- NotFoundException: 'Salary adjustment not found' (shart bajarilmasa, HTTP 404)
- ForbiddenException: Agar record actor doirasida (scope) bo'lmasa (HTTP 403)

**8. DB struktura:**
- Tegishli model: SalaryAdjustment
- id: String (Majburiy) @default(uuid()) @db.Uuid
- companyId: String (Majburiy) @db.Uuid
- employeeId: String (Majburiy) @db.Uuid
- type: AdjustmentType (Majburiy)
- category: AdjustmentCategory (Majburiy) @default(manual)
- amount: Decimal (Majburiy) @db.Decimal(15, 2)
- date: DateTime (Majburiy) @db.Date
- month: String (Majburiy) @db.VarChar(7)
- reason: String? (Ixtiyoriy)
- createdById: String? (Ixtiyoriy) @db.Uuid
- updatedById: String? (Ixtiyoriy) @db.Uuid
- createdAt: DateTime (Majburiy) @default(now()) @db.Timestamptz(6)
- updatedAt: DateTime (Majburiy) @updatedAt @db.Timestamptz(6)
- Chiquvchi relations:
  - SalaryAdjustment.companyId -> Company.id (onDelete: Cascade)
  - SalaryAdjustment.employeeId -> User.id (onDelete: Cascade)
- Kiruvchi relations: Yo'q (bu o'chirilganda boshqa hech narsa o'chmaydi yoki ta'sirlanmaydi)
- Indexes:
  - @@index([companyId])
  - @@index([employeeId])
  - @@index([month])
  - @@index([type])
  - @@index([category])


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/salary-adjustment.md`

### Endpoint: POST /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/salary-adjustments`
- Controller class + method nomi: `SalaryAdjustmentController` -> `create`
- Tavsif: Yangi oylik maosh o'zgarishini (bonus yoki jarima) qo'shish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
  "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
  "type": "bonus",
  "category": "manual",
  "amount": 10000,
  "date": "2026-08-22",
  "month": "2026-08",
  "reason": "Test bonus"
}
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida ruxsat etilgan rollar)

**4. DTO:**
- Request DTO: `CreateSalaryAdjustmentDto`
- `companyId` (ixtiyoriy, UUID) - Superadmin uchun majburiy, boshqalar uchun avto to'ldiriladi.
- `employeeId` (majburiy, UUID)
- `type` (majburiy, Enum: AdjustmentType)
- `category` (ixtiyoriy, Enum: AdjustmentCategory)
- `amount` (majburiy, Raqam)
- `date` (majburiy, ISO Date String)
- `month` (ixtiyoriy, String)
- `reason` (ixtiyoriy, String, max: 1000)

**5. Service:**
- Service method: `create`
- Tavsifi: Kompaniya va xodim mavjudligi hamda ruxsat doirasi (scope) tekshiriladi. Xodim tanlangan kompaniyaga tegishlimi degan tekshiruv bor. Kiritilgan ma'lumotlar bilan `SalaryAdjustment` yozuvi yaratiladi. Xodimga `notificationTemplates.adjustmentApplied` orqali xabarnoma (notification) yuboriladi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `SalaryAdjustment` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "37de1f29-77ee-44df-8016-755a60693519",
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
    "type": "bonus",
    "category": "manual",
    "amount": "10000",
    "date": "2026-08-22T00:00:00.000Z",
    "month": "2026-08",
    "reason": "Test bonus",
    "createdById": "6af2bec4-91c9-4935-bacc-718bd4531ec8",
    "updatedById": "6af2bec4-91c9-4935-bacc-718bd4531ec8",
    "createdAt": "2026-08-22T17:26:59.371Z",
    "updatedAt": "2026-08-22T17:26:59.371Z"
  },
  "path": "/api/v1/salary-adjustments",
  "timestamp": "2026-08-22T17:26:59.412Z"
}
```

**7. Error case:**
- `BadRequestException`: Validatsiya xatosi.
- `UnauthorizedException`: Token yaroqsiz yoki mavjud emas.
- `ForbiddenException`: Ruxsat etilmagan rol.
- `NotFoundException`: 'Company not found' yoki 'Employee not found'.
- `ConflictException`: 'Employee does not belong to the selected company'.

**8. DB struktura:**
- Prisma modeli: `SalaryAdjustment`
- Ustun ta'riflari:
  - `id`: UUID (Primary Key)
  - `companyId`: UUID (Kompaniya bilan bog'liqlik)
  - `employeeId`: UUID (Xodim bilan bog'liqlik)
  - `type`: Enum (AdjustmentType)
  - `category`: Enum (AdjustmentCategory, default: manual)
  - `amount`: Decimal(15, 2)
  - `date`: Date
  - `month`: VarChar(7)
  - `reason`: String?
  - `createdById`: UUID?
  - `updatedById`: UUID?
  - `createdAt`: DateTime
  - `updatedAt`: DateTime

**cURL misol:**
```bash
curl -X POST "http://localhost:4000/api/v1/salary-adjustments" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
    "type": "bonus",
    "category": "manual",
    "amount": 10000,
    "date": "2026-08-22",
    "month": "2026-08",
    "reason": "Test bonus"
  }'
```

---

### Endpoint: GET /api/v1/salary-adjustments
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/salary-adjustments`
- Controller class + method nomi: `SalaryAdjustmentController` -> `findAll`
- Tavsif: Oylik maosh o'zgarishlari ro'yxatini va jami sonini qaytaradi (sahifalab).

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q.
- Query parametr misollari:
  - `page`: 1
  - `limit`: 10
  - `companyId`, `employeeId`, `type`, `category`, `month`, `search`, `dateFrom`, `dateTo`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `SalaryAdjustmentQueryDto`
- `page` (Int, min 1)
- `limit` (Int, min 1, max 100)
- Boshqa maydonlar (String, UUID, Enum) orqali filtrlash.

**5. Service:**
- Service method: `findAll`
- Tavsifi: Foydalanuvchi roli ruxsat beruvchi doira (scope) asosida `where` obyektini tuzadi (masalan, faqat o'z kompaniyasi yoki filiali xodimlarini ko'rishi mumkin). `reason` bo'yicha qidiruv (`search`) hamda muddatlar orqali filtrlashlarni qo'llab, bazadan ma'lumotlarni tortib oladi.

**6. Response:**
- Paginatsiya shaklidagi obyekt:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "3d128590-762c-4aca-a3f4-6182c7581831",
        "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
        "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
        "type": "penalty",
        "category": "late",
        "amount": "55371.03",
        "date": "2026-08-06T00:00:00.000Z",
        "month": "2026-08",
        "reason": "Late arrival penalty",
        "createdById": null,
        "updatedById": null,
        "createdAt": "2026-08-07T14:16:35.082Z",
        "updatedAt": "2026-08-07T14:16:35.082Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/salary-adjustments",
  "timestamp": "2026-08-22T17:26:32.888Z"
}
```

**7. Error case:**
- `BadRequestException`: Noto'g'ri so'rov parametrlari.
- `UnauthorizedException`
- `ForbiddenException`

**8. DB struktura:**
- Prisma modeli: `SalaryAdjustment` (yuqorida ko'rsatilgandek).

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/salary-adjustments?limit=10&page=1" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/salary-adjustments/:id`
- Controller class + method nomi: `SalaryAdjustmentController` -> `findOne`
- Tavsif: ID bo'yicha bitta maosh o'zgarishi haqidagi ma'lumotni olish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q
- URL Params: `id` - UUID formati.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (`ParseUUIDPipe` orqali tekshiriladi).

**5. Service:**
- Service method: `findOne`
- Tavsifi: Obyektni bazadan oladi, topilmasa NotFound xatosi qaytadi. `assertRecordInScope` yordamida obyektni joriy foydalanuvchiga tegishliligi (ko'rish huquqi) tekshiriladi.

**6. Response:**
- Qaytariladigan javob shakli: Prisma `SalaryAdjustment` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "3d128590-762c-4aca-a3f4-6182c7581831",
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
    "type": "penalty",
    "category": "late",
    "amount": "55371.03",
    "date": "2026-08-06T00:00:00.000Z",
    "month": "2026-08",
    "reason": "Late arrival penalty",
    "createdById": null,
    "updatedById": null,
    "createdAt": "2026-08-07T14:16:35.082Z",
    "updatedAt": "2026-08-07T14:16:35.082Z"
  },
  "path": "/api/v1/salary-adjustments/3d128590-762c-4aca-a3f4-6182c7581831",
  "timestamp": "2026-08-22T17:26:52.526Z"
}
```

**7. Error case:**
- `BadRequestException`: Noto'g'ri UUID yuborilganda.
- `NotFoundException`: 'Salary adjustment not found'
- `UnauthorizedException`
- `ForbiddenException`

**8. DB struktura:**
- Prisma modeli: `SalaryAdjustment` (yuqorida ko'rsatilgandek).

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/salary-adjustments/3d128590-762c-4aca-a3f4-6182c7581831" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/salary-adjustments/:id`
- Controller class + method nomi: `SalaryAdjustmentController` -> `update`
- Tavsif: Mavjud maosh o'zgarishini qisman tahrirlash.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
```json
{
  "amount": 15000,
  "reason": "Updated test bonus"
}
```

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO: `UpdateSalaryAdjustmentDto` (`CreateSalaryAdjustmentDto`ning `PartialType` holati).

**5. Service:**
- Service method: `update`
- Tavsifi: Mavjud yozuvni topib, foydalanuvchida uni tahrirlashga huquqi borligini tekshiradi. Kiritilgan ma'lumotlar bilan yozuvni yangilaydi (shu jumladan yangi oydagi ma'lumot kiritilsa, shu bo'yicha oyni ham yangilaydi).

**6. Response:**
- Qaytariladigan javob shakli: Yangilangan Prisma `SalaryAdjustment` obyekti.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "37de1f29-77ee-44df-8016-755a60693519",
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "employeeId": "021d58a1-98b7-4331-bc1e-1e45728d9408",
    "type": "bonus",
    "category": "manual",
    "amount": "15000",
    "date": "2026-08-22T00:00:00.000Z",
    "month": "2026-08",
    "reason": "Updated test bonus",
    "createdById": "6af2bec4-91c9-4935-bacc-718bd4531ec8",
    "updatedById": "6af2bec4-91c9-4935-bacc-718bd4531ec8",
    "createdAt": "2026-08-22T17:26:59.371Z",
    "updatedAt": "2026-08-22T17:27:04.432Z"
  },
  "path": "/api/v1/salary-adjustments/37de1f29-77ee-44df-8016-755a60693519",
  "timestamp": "2026-08-22T17:27:04.447Z"
}
```

**7. Error case:**
- `BadRequestException`: Validatsiya muammosi yoki yaroqsiz UUID.
- `NotFoundException`: Obyekt topilmasa.
- `UnauthorizedException`
- `ForbiddenException`
- `ConflictException`: Xodim tanlangan kompaniyada emasligi sababli ruxsatsizlik bo'lsa.

**8. DB struktura:**
- Prisma modeli: `SalaryAdjustment` (yuqorida ko'rsatilgandek).

**cURL misol:**
```bash
curl -X PATCH "http://localhost:4000/api/v1/salary-adjustments/37de1f29-77ee-44df-8016-755a60693519" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 15000,
    "reason": "Updated test bonus"
  }'
```

---

### Endpoint: DELETE /api/v1/salary-adjustments/:id
**Controller:** src/modules/salary-adjustment/salary-adjustment.controller.ts:delete

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/salary-adjustments/:id`
- Controller class + method nomi: `SalaryAdjustmentController` -> `delete`
- Tavsif: Maosh o'zgarishini o'chirish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q
- URL Params: `id` - UUID

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')` (Controller darajasida)

**4. DTO:**
- Request DTO qo'llanilmagan (`ParseUUIDPipe` orqali tekshiriladi).

**5. Service:**
- Service method: `delete`
- Tavsifi: Mavjud yozuvni topib, scope (ruxsat) tekshiriladi. So'ngra yozuv ma'lumotlar bazasidan olib tashlanadi.

**6. Response:**
- Qaytariladigan javob shakli: `{ success: boolean, id: string }`
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "37de1f29-77ee-44df-8016-755a60693519"
  },
  "path": "/api/v1/salary-adjustments/37de1f29-77ee-44df-8016-755a60693519",
  "timestamp": "2026-08-22T17:27:09.595Z"
}
```

**7. Error case:**
- `BadRequestException`: Noto'g'ri UUID.
- `NotFoundException`: Yozuv topilmadi.
- `UnauthorizedException`
- `ForbiddenException`

**8. DB struktura:**
- Prisma modeli: `SalaryAdjustment` (yuqorida ko'rsatilgandek).

**cURL misol:**
```bash
curl -X DELETE "http://localhost:4000/api/v1/salary-adjustments/37de1f29-77ee-44df-8016-755a60693519" \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/app-version.md`

### Endpoint: POST /api/v1/app-versions
**Controller:** src/modules/app-version/app-version.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/app-versions`
- Controller class + method nomi: `AppVersionController` -> `create`
- Tavsif: Yangi app versiyasini yaratish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `android`: `{ "latest": "1.0.0", "minRequired": "1.0.0" }`
- `ios`: `{ "latest": "1.0.0", "minRequired": "1.0.0" }`

**3. Guard:**
- `@Roles('superadmin', 'admin')` (Controller darajasida)
- Bearer Token

**4. DTO:**
- Request DTO: `CreateAppVersionDto`
- `android`: Tip - Record<string, unknown>, Validatorlar - `@IsOptional()`, `@IsObject()`
- `ios`: Tip - Record<string, unknown>, Validatorlar - `@IsOptional()`, `@IsObject()`

**5. Service:**
- Service method: `create`
- Tavsifi: PrismaService orqali yangi AppVersion rekordini bazaga qo'shadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Success",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "android": {
      "latest": "1.0.0",
      "minRequired": "1.0.0"
    },
    "ios": {
      "latest": "1.0.0",
      "minRequired": "1.0.0"
    },
    "createdAt": "2026-08-22T16:36:58.759Z",
    "updatedAt": "2026-08-22T16:36:58.759Z"
  },
  "path": "/api/v1/app-versions",
  "timestamp": "2026-08-22T16:36:58.759Z"
}
```

**7. Error case:**
- `UnauthorizedException`: 'Yaroqsiz token' (401)
- `ForbiddenException`: 'Ruxsat etilmagan rol' (403)

**8. DB struktura:**
- Prisma modeli: `AppVersion`
- Ustun ta'riflari:
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `android`: `Json`, ixtiyoriy (`?`)
  - `ios`: `Json`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi): Yo'q
- Relations (Kiruvchi): Yo'q
- Indekslar: Yo'q

**cURL misol:**
```bash
curl -X POST http://localhost:4000/api/v1/app-versions \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"android": {"latest": "1.0.0", "minRequired": "1.0.0"}, "ios": {"latest": "1.0.0", "minRequired": "1.0.0"}}'
```

---

### Endpoint: GET /api/v1/app-versions
**Controller:** src/modules/app-version/app-version.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/app-versions`
- Controller class + method nomi: `AppVersionController` -> `findAll`
- Tavsif: Barcha app versiyalarini sahifalab olish (pagination).

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q (Query parametrlari orqali ma'lumot keladi).
- Query parametr misollari:
  - `page`: `1`
  - `limit`: `10`

**3. Guard:**
- `@Roles('superadmin', 'admin')` (Controller darajasida)
- Bearer Token

**4. DTO:**
- Request DTO: `AppVersionQueryDto`
- `page`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
- `limit`: Tip - Number, Validatorlar - `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `findAll`
- Tavsifi: PrismaService yordamida bazadagi barcha yozuvlarni createdAt bo'yicha kamayish tartibida qaytaradi va umumiy sonini hisoblaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "android": {
          "latest": "1.0.0",
          "minRequired": "1.0.0"
        },
        "ios": {
          "latest": "1.0.0",
          "minRequired": "1.0.0"
        },
        "createdAt": "2026-08-22T16:36:58.759Z",
        "updatedAt": "2026-08-22T16:36:58.759Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/app-versions?page=1&limit=10",
  "timestamp": "2026-08-22T16:36:58.759Z"
}
```

**7. Error case:**
- `UnauthorizedException`: 'Yaroqsiz token' (401)
- `ForbiddenException`: 'Ruxsat etilmagan rol' (403)

**8. DB struktura:**
- Prisma modeli: `AppVersion`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `android`: `Json`, ixtiyoriy (`?`)
  - `ios`: `Json`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi): Yo'q
- Relations (Kiruvchi): Yo'q
- Indekslar: Yo'q

**cURL misol:**
```bash
curl -X GET "http://localhost:4000/api/v1/app-versions?page=1&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: GET /api/v1/app-versions/:id
**Controller:** src/modules/app-version/app-version.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/app-versions/:id`
- Controller class + method nomi: `AppVersionController` -> `findOne`
- Tavsif: ID orqali bitta app versiyasi ma'lumotini olish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat `:id` parametri qabul qilinadi.

**3. Guard:**
- `@Roles('superadmin', 'admin')` (Controller darajasida)
- Bearer Token

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string sifatida olinadi, ParseUUIDPipe yordamida).

**5. Service:**
- Service method: `findOne`
- Tavsifi: ID orqali mos rekordni qidiradi, topilmasa xatolik qaytaradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "android": {
      "latest": "1.0.0",
      "minRequired": "1.0.0"
    },
    "ios": {
      "latest": "1.0.0",
      "minRequired": "1.0.0"
    },
    "createdAt": "2026-08-22T16:36:58.759Z",
    "updatedAt": "2026-08-22T16:36:58.759Z"
  },
  "path": "/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2026-08-22T16:36:58.759Z"
}
```

**7. Error case:**
- `UnauthorizedException`: 'Yaroqsiz token' (401)
- `ForbiddenException`: 'Ruxsat etilmagan rol' (403)
- `NotFoundException`: 'App version not found' (404)

**8. DB struktura:**
- Prisma modeli: `AppVersion`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `android`: `Json`, ixtiyoriy (`?`)
  - `ios`: `Json`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi): Yo'q
- Relations (Kiruvchi): Yo'q
- Indekslar: Yo'q

**cURL misol:**
```bash
curl -X GET http://localhost:4000/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer <TOKEN>"
```

---

### Endpoint: PATCH /api/v1/app-versions/:id
**Controller:** src/modules/app-version/app-version.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/app-versions/:id`
- Controller class + method nomi: `AppVersionController` -> `update`
- Tavsif: App versiyasi ma'lumotlarini qisman yangilash.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `android`: `{ "latest": "1.1.0", "minRequired": "1.0.0" }`

**3. Guard:**
- `@Roles('superadmin', 'admin')` (Controller darajasida)
- Bearer Token

**4. DTO:**
- Request DTO: `UpdateAppVersionDto` (CreateAppVersionDto ning barcha maydonlari ixtiyoriy shaklda)
- Param: `id` (ParseUUIDPipe)

**5. Service:**
- Service method: `update`
- Tavsifi: ID orqali bazadan izlaydi, agar mavjud bo'lsa faqat kiritilgan maydonlarni (android yoki ios) yangilaydi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "android": {
      "latest": "1.1.0",
      "minRequired": "1.0.0"
    },
    "ios": {
      "latest": "1.0.0",
      "minRequired": "1.0.0"
    },
    "createdAt": "2026-08-22T16:36:58.759Z",
    "updatedAt": "2026-08-22T16:37:10.000Z"
  },
  "path": "/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2026-08-22T16:37:10.000Z"
}
```

**7. Error case:**
- `UnauthorizedException`: 'Yaroqsiz token' (401)
- `ForbiddenException`: 'Ruxsat etilmagan rol' (403)
- `NotFoundException`: 'App version not found' (404)

**8. DB struktura:**
- Prisma modeli: `AppVersion`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `android`: `Json`, ixtiyoriy (`?`)
  - `ios`: `Json`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi): Yo'q
- Relations (Kiruvchi): Yo'q
- Indekslar: Yo'q

**cURL misol:**
```bash
curl -X PATCH http://localhost:4000/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"android": {"latest": "1.1.0", "minRequired": "1.0.0"}}'
```

---

### Endpoint: DELETE /api/v1/app-versions/:id
**Controller:** src/modules/app-version/app-version.controller.ts:remove

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/app-versions/:id`
- Controller class + method nomi: `AppVersionController` -> `remove`
- Tavsif: App versiyasini o'chirish.

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, faqat `:id` parametri qabul qilinadi.

**3. Guard:**
- `@Roles('superadmin', 'admin')` (Controller darajasida)
- Bearer Token

**4. DTO:**
- Request DTO qo'llanilmagan (Faqat Param `id` string, ParseUUIDPipe yordamida).

**5. Service:**
- Service method: `remove`
- Tavsifi: Mavjudligini tekshiradi va rekordni o'chiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Success",
  "data": {
    "success": true,
    "id": "123e4567-e89b-12d3-a456-426614174000"
  },
  "path": "/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2026-08-22T16:37:10.000Z"
}
```

**7. Error case:**
- `UnauthorizedException`: 'Yaroqsiz token' (401)
- `ForbiddenException`: 'Ruxsat etilmagan rol' (403)
- `NotFoundException`: 'App version not found' (404)

**8. DB struktura:**
- Prisma modeli: `AppVersion`
- Ustun ta'riflari: (POST bilan bir xil)
  - `id`: `String`, majburiy, `@default(uuid())`, `@db.Uuid`
  - `android`: `Json`, ixtiyoriy (`?`)
  - `ios`: `Json`, ixtiyoriy (`?`)
  - `createdAt`: `DateTime`, majburiy, `@default(now())`, `@db.Timestamptz(6)`
  - `updatedAt`: `DateTime`, majburiy, `@updatedAt`, `@db.Timestamptz(6)`
- Relations (Chiquvchi): Yo'q
- Relations (Kiruvchi): Yo'q
- Indekslar: Yo'q

**cURL misol:**
```bash
curl -X DELETE http://localhost:4000/api/v1/app-versions/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer <TOKEN>"
```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/api/work-schedule.md`

### Endpoint: POST /api/v1/work-schedules
```bash
curl -X POST http://localhost:3000/api/v1/work-schedules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Shift",
    "startTime": "08:00",
    "endTime": "17:00",
    "breakDuration": 60,
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "branchId": "b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b"
}'
```
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:create

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `POST /api/v1/work-schedules`
- Controller class + method nomi: `WorkScheduleController` → `create`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- `name`: `Morning Shift`
- `startTime`: `08:00`
- `endTime`: `17:00`
- `breakDuration`: `60` (minutes)
- `companyId`: `c5f2c7c8-40eb-4091-b066-b3e4e245b962`
- `branchId`: `b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- Request DTO: `CreateWorkScheduleDto` (src/modules/work-schedule/dto/create-work-schedule.dto.ts)
  - `name`: `string`, `@IsString()`, `@MaxLength(100)`
  - `startTime`: `string`, `@Matches(/^([01]\d|2[0-3]):([0-5]\d)$/)`
  - `endTime`: `string`, `@Matches(/^([01]\d|2[0-3]):([0-5]\d)$/)`
  - `breakDuration`: `number`, `@IsInt()`, `@Min(0)`
  - `companyId`: `string`, `@IsUUID()`
  - `branchId`: `string`, `@IsOptional()`, `@IsUUID()`

**5. Service:**
- Service method: `create` (src/modules/work-schedule/work-schedule.service.ts)
- Tavsifi: Kompaniya, filial tekshiriladi, yangi `WorkSchedule` yozuvi yaratadi.

**6. Response:**
- Yaratilgan `WorkSchedule` obyekti.
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Work schedule created",
  "data": {
    "id": "d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
    "name": "Morning Shift",
    "startTime": "08:00",
    "endTime": "17:00",
    "breakDuration": 60,
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "branchId": "b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b",
    "createdAt": "2026-08-22T12:00:00.000Z",
    "updatedAt": "2026-08-22T12:00:00.000Z"
  },
  "path": "/api/v1/work-schedules",
  "timestamp": "2026-08-22T12:00:00.000Z"
}
```

**7. Error case:**
- `BadRequestException`: Invalid time range (`endTime` must be after `startTime`).
- `ConflictException`: Duplicate schedule name within same company/branch.

**8. DB struktura:**
- Prisma modeli: `WorkSchedule` (prisma/schema.prisma)
- Ustunlar:
  - `id`: `String` @default(uuid()) @db.Uuid
  - `name`: `String`
  - `startTime`: `String`
  - `endTime`: `String`
  - `breakDuration`: `Int`
  - `companyId`: `String` @db.Uuid
  - `branchId`: `String?` @db.Uuid
  - `createdAt`: `DateTime` @default(now()) @db.Timestamptz(6)
  - `updatedAt`: `DateTime` @updatedAt @db.Timestamptz(6)
- Relations: `companyId -> Company.id (onDelete: Cascade)`, `branchId -> Branch.id (onDelete: SetNull)`

---

### Endpoint: GET /api/v1/work-schedules
```bash
curl -X GET "http://localhost:3000/api/v1/work-schedules?companyId=c5f2c7c8-40eb-4091-b066-b3e4e245b962&branchId=b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b&page=1&limit=10"
```
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findAll

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/work-schedules`
- Controller class + method nomi: `WorkScheduleController` → `findAll`

**2. ApiBody / Misollar (Swagger example qiymatlar):**
- Body yo'q, query parametrlari orqali filterlar:
  - `companyId`: `c5f2c7c8-40eb-4091-b066-b3e4e245b962`
  - `branchId`: `b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b`
  - `page`: `1`
  - `limit`: `10`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager', 'employee')`

**4. DTO:**
- Query DTO: `WorkScheduleQueryDto`
  - `companyId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `branchId`: `string`, `@IsOptional()`, `@IsUUID()`
  - `page`: `number`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`
  - `limit`: `number`, `@IsOptional()`, `@Type(() => Number)`, `@IsInt()`, `@Min(1)`, `@Max(100)`

**5. Service:**
- Service method: `findAll` (src/modules/work-schedule/work-schedule.service.ts)
- Tavsifi: Filterlangan jadvaldan `WorkSchedule` ro'yxatini paginatsiyalab qaytaradi.

**6. Response:**
- Paginatsiyalangan obyekt.
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Work schedules fetched",
  "data": {
    "items": [
      {
        "id": "d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
        "name": "Morning Shift",
        "startTime": "08:00",
        "endTime": "17:00",
        "breakDuration": 60,
        "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
        "branchId": "b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b",
        "createdAt": "2026-08-22T12:00:00.000Z",
        "updatedAt": "2026-08-22T12:00:00.000Z"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1
  },
  "path": "/api/v1/work-schedules",
  "timestamp": "2026-08-22T12:05:00.000Z"
}
```

**7. Error case:**
- `BadRequestException`: Invalid pagination parameters.

**8. DB struktura:** Same as POST description.

---

### Endpoint: GET /api/v1/work-schedules/:id
```bash
curl -X GET "http://localhost:3000/api/v1/work-schedules/<<schedule-id>>"
```
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:findOne

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `GET /api/v1/work-schedules/:id`
- Controller class + method nomi: `WorkScheduleController` → `findOne`

**2. ApiBody / Misollar:**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager', 'employee')`

**4. DTO:**
- Param `id`: `string`, `@IsUUID()`

**5. Service:**
- Service method: `findOne` (src/modules/work-schedule/work-schedule.service.ts)
- Tavsifi: ID bo'yicha bitta `WorkSchedule` obyektini topadi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Work schedule fetched",
  "data": {
    "id": "d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
    "name": "Morning Shift",
    "startTime": "08:00",
    "endTime": "17:00",
    "breakDuration": 60,
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "branchId": "b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b",
    "createdAt": "2026-08-22T12:00:00.000Z",
    "updatedAt": "2026-08-22T12:00:00.000Z"
  },
  "path": "/api/v1/work-schedules/d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
  "timestamp": "2026-08-22T12:10:00.000Z"
}
```

**7. Error case:**
- `NotFoundException`: `Work schedule not found`.

**8. DB struktura:** Same as above.

---

### Endpoint: PATCH /api/v1/work-schedules/:id
```bash
curl -X PATCH "http://localhost:3000/api/v1/work-schedules/<schedule-id>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Evening Shift",
    "startTime": "14:00",
    "endTime": "22:00",
    "breakDuration": 45
  }'
```

**Controller:** src/modules/work-schedule/work-schedule.controller.ts:update

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `PATCH /api/v1/work-schedules/:id`
- Controller class + method nomi: `WorkScheduleController` → `update`

**2. ApiBody / Misollar (PartialType of Create DTO):**
- `name`: `Evening Shift`
- `startTime`: `14:00`
- `endTime`: `22:00`
- `breakDuration`: `45`

**3. Guard:**
- `@Roles('superadmin', 'admin', 'manager')`

**4. DTO:**
- `UpdateWorkScheduleDto` extends `PartialType(CreateWorkScheduleDto)`

**5. Service:**
- Service method: `update` (src/modules/work-schedule/work-schedule.service.ts)
- Tavsifi: Mavjud jadvalni yangilaydi, vaqt oralig'ini qayta tekshiradi.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Work schedule updated",
  "data": {
    "id": "d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
    "name": "Evening Shift",
    "startTime": "14:00",
    "endTime": "22:00",
    "breakDuration": 45,
    "companyId": "c5f2c7c8-40eb-4091-b066-b3e4e245b962",
    "branchId": "b3a1d5e2-9c2f-4f6a-8a1b-2e7c5d9f0a1b",
    "createdAt": "2026-08-22T12:00:00.000Z",
    "updatedAt": "2026-08-22T12:15:00.000Z"
  },
  "path": "/api/v1/work-schedules/d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
  "timestamp": "2026-08-22T12:15:00.000Z"
}
```

**7. Error case:**
- `NotFoundException`: `Work schedule not found`.
- `BadRequestException`: Invalid time range.

**8. DB struktura:** Same as POST.

---

### Endpoint: DELETE /api/v1/work-schedules/:id
```bash
curl -X DELETE "http://localhost:3000/api/v1/work-schedules/<schedule-id>"
```
**Controller:** src/modules/work-schedule/work-schedule.controller.ts:remove

**1. Point (yo'nalish):**
- HTTP metod + to'liq yo'l: `DELETE /api/v1/work-schedules/:id`
- Controller class + method nomi: `WorkScheduleController` → `remove`

**2. ApiBody / Misollar:**
- Body yo'q.

**3. Guard:**
- `@Roles('superadmin', 'admin')`

**4. DTO:**
- Param `id`: `string`, `@IsUUID()`

**5. Service:**
- Service method: `remove` (src/modules/work-schedule/work-schedule.service.ts)
- Tavsifi: Jadvalni ID bo'yicha o'chiradi, bog'langan xodimlar uchun foreign key `SET NULL`.

**6. Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Work schedule deleted",
  "data": { "id": "d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f" },
  "path": "/api/v1/work-schedules/d3f2a9c4-7b5e-4c2a-9a8f-1e2b3c4d5e6f",
  "timestamp": "2026-08-22T12:20:00.000Z"
}
```

**7. Error case:**
- `NotFoundException`: `Work schedule not found`.

**8. DB struktura:** Same as POST.

---

**cURL examples** (for each endpoint, omitted here for brevity but can be added similarly).

*Note: All timestamps are examples.*

---

## Manba: bot_post_using/docs/telegram-id-string-db-architecture.md

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
