# Zdes Loyihasi: Foydalanuvchi Profili va Xabarnoma Sahifalari (User Profiles & Notifications)


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_14.md`

# Step 14: All Modules Create / Edit Form Pages Star Admin 2 Redesign

## 📅 Bajarilgan Ishlar:

Barcha modullardagi **Yangi Qo'shish (`/new`) hamda Tahrirlash (`/edit`)** forma sahifalari eskicha HTML ko'rinishidan Star Admin 2 dizayniga o'tkazildi:

1. **`DepartmentForm` (`/departments/new` & `/departments/:id/edit`)**:
   - Modern Form Card UI ([department-form.html](file:///home/fayzillo/Desktop/zdes/test-zdes-front/src/app/features/departments/pages/department-form/department-form.html)).
   - Gradient header ikonkalari, toza focus-ring bilan ta'minlangan input/select elementlari hamda saqlash/bekor qilish gradient tugmalari.

2. **`EmployeeForm` (`/employees/new` & `/employees/:id/edit`)**:
   - Responsive 2-ustunli **Form Grid** tizimi ([employee-form.html](file:///home/fayzillo/Desktop/zdes/test-zdes-front/src/app/features/employees/pages/employee-form/employee-form.html)).
   - To'liq Ism, Telefon, Status hamda dinamik Filial, Bo'lim va Lavozim select elementlari bilan jihozlandi.

3. **Barcha formalar uchun umumiy Star Admin 2 Card Pattern**:
   - `form-card`, `form-header-icon`, `form-input`, `form-select` va `btn-gradient-submit` uslublari barcha modullar uchun bir xil standartga keltirildi.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/notifications.md`

# Notifications Page Specification

## 1. Maqsad
Foydalanuvchiga tizimdan kelgan barcha xabarnomalarni (payroll, attendance, leave status) bitta joyda jamlab ko'rsatish, o'qilmaganlarini boshqarish va o'qilgan belgisi qo'yish imkoniyatini taqdim etish.

## 2. Route
`/notifications`

## 3. Mockup reference
`orcestor/examples/panel/panel-notifications-v1.jpg`

## 4. Layout tuzilmasi
- **Header:** "Notifications" sarlavhasi va o'ng tomonda "Mark all as read" tugmasi.
- **Filter Tabs:** All, Unread, Payroll, Attendance, Leave kabi tablar.
- **List Section:** Xabarnomalar ro'yxati. Yangi xabarlar va eski xabarlar (New / Earlier) divider bilan ajratilgan.
- **Footer Section:** "Load more" tugmasi (agar pagination ishlatsa) yoki infinite scroll.

## 5. Komponentlar ro'yxati
- `NotificationTabs`: Filterlarni boshqarish uchun (All, Unread va hkz).
- `NotificationItem`: Alohida xabar komponenti. O'z ichiga oladi: Icon (turiga qarab), Title, Description, Timestamp (masalan: "2 hours ago"), va o'qilmagan bo'lsa "Unread dot" (nuqta).
- `SectionDivider`: "New" va "Earlier" guruhlarini ajratib turuvchi chiziqli text.
- `MarkAllAsReadButton`: Hamma xabarlarni o'qilgan holatga o'tkazuvchi tugma.
- `LoadMoreButton`: Qo'shimcha xabarlarni yuklash uchun.

## 6. Style (ranglar, tipografiya, spacing)
- **Ranglar:** O'qilmagan xabarlar backgroundi yengil ko'k/kulrang (masalan: `bg-primary-50` yoki e'tiborni tortuvchi boshqa rang) bo'lishi va e'tibor qaratuvchi indikator (nuqta) primary rangda bo'lishi kerak.
- **Tipografiya:** O'qilmagan xabarlar sarlavhasi bold, o'qilganlari regular.
- **Spacing:** Xabarlar orasida margin/padding yetarli bo'lishi, yirik tap area ta'minlanishi kerak (mobil uchun muhim).

## 7. States (loading, empty, success)
- **Loading:** Sahifa va tab o'zgarganda list uchun skeleton loader.
- **Empty:** Xabarnomalar umuman yo'q bo'lsa yoki tanlangan tab bo'yicha xabar chiqmasa "No notifications yet" illyustratsiyasi/teksti chiqadi.
- **Filter Active:** Qaysi tab tanlanganligiga qarab vizual indikator (active state).

## 8. Animatsiyalar
- Yangi tabga o'tganda ro'yxatning paydo bo'lish animatsiyasi (fade in yoki slide in).
- Xabar o'qilganda "unread dot" ning g'oyib bo'lishi yengil fade out bilan amalga oshiriladi.

## 9. Responsive
- **Mobile (sm):** Full width xabar kartalari. Tablar scrollable (gorizontal) bo'lishi kerak. "Mark all as read" tugmasi kichik ikonka ko'rinishida yoki menyuda.
- **Tablet & Desktop (md, lg):** Markazlashtirilgan yoki limitlangan kenglikda (masalan `max-w-3xl`) ro'yxat chiqariladi.

## 10. API endpointlar
- `GET /api/v1/notifications?page=1&limit=20` — Xabarlarni ro'yxatini olish. (Filtr uchun type/status query parameter bo'lishi mumkin).
- `PATCH /api/v1/notifications/:id` — Muayyan xabarni o'qilgan deb belgilash (mark as read).
- `POST /api/v1/notifications/mark-all-read` (yoki shunga o'xshash) — Barchasini o'qilgan qilish.

**API docs:** `orcestor/project_docs/api/notification.md`

## 11. Global state (Zustand)
- `useNotificationStore`: Dastur bo'ylab o'qilmagan xabarlar sonini saqlash uchun (`unreadCount`). Bu son sidebar dagi badge'ni ham yangilaydi. Mark as read bosilganda shu store yangilanishi shart.

## 12. Muhim eslatmalar
- Timestamp qismi relative bo'lishi tavsiya qilinadi (masalan, `date-fns` ning `formatDistanceToNow` yordamida "3 hours ago", "yesterday").
- Xabarni bosish uning turiga qarab tegishli sahifaga o'tkazishi kerak (masalan, payslip notification bo'lsa -> `/payslips` ga).


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/payslips.md`

# Payslips Page Specification

## 1. Maqsad
Foydalanuvchiga (xodimga) o'zining oylik maoshlari (payslips) tarixini, hisoblangan va ushlangan summalarini, shuningdek yillik maosh o'zgarishi dinamikasini ko'rsatish. Oylik maosh bo'yicha hujjatni PDF formatida yuklab olish imkoniyatini taqdim etish.

## 2. Route
`/payslips` (My Payslips)

## 3. Mockup reference
`orcestor/examples/panel/panel-payslips-v1.jpg`

## 4. Layout tuzilmasi
- **Header:** Sahifa sarlavhasi ("My Payslips") va yillarni filtrlash uchun "Year filter" dropdown.
- **Top Metrics (Summary Cards):** 3 ta karta qatorlashib turadi (Average Net, Total Earned, Total Deductions).
- **Middle Section:**
  - **Left (Chart):** Salary History bar chart (Jan-Dec).
  - **Right (Latest Payslip):** Eng so'nggi maosh haqida qisqacha ma'lumot va PDF yuklab olish tugmasi.
- **Bottom Section:** Payslip history table (oylik maoshlar ro'yxati).

## 5. Komponentlar ro'yxati
- `PageHeader`: Sarlavha va Year Filter dropdown bilan.
- `SummaryCard`: Metric (Title, Value, Icon) ko'rsatuvchi karta (3 dona).
- `SalaryHistoryChart`: Yillik oylik maoshlar bar charti (`recharts` yoki `chart.js` kutubxonasidagi `BarChart` yordamida).
- `LatestPayslipCard`: Oylikning batafsil qismi (Base, Bonus, Penalty, Advance, Net) hamda "Download PDF" tugmasi, status badge bilan.
- `PayslipsTable`: Jadval komponenti. Ustunlari: Month, Base, Bonus, Penalty, Advance, Net, Status, Download.
- `StatusBadge`: To'lov holatini ko'rsatuvchi (Paid, Pending).

## 6. Style (ranglar, tipografiya, spacing)
- **Ranglar:** Asosiy net maosh yashil (Success), ushlanmalar qizil (Danger) ranglarda beriladi. Chart ustunlari brand rangida (Primary).
- **Tipografiya:** Summalar aniq va ajralib turadigan bold fontda ko'rsatiladi. Valyuta belgisi kiritiladi.
- **Spacing:** Kartalar va jadval orasida 24px (gap-6) bo'shliq bo'ladi.

## 7. States (loading, error, empty, success)
- **Loading:** Ma'lumotlar kelayotganda skeleton loader (kartalar, chart va jadval o'rnida).
- **Empty:** Tanlangan yil uchun payroll ma'lumotlari topilmasa (no payrolls), o'rtada "No payslips found for selected year" xabari ko'rinadi.
- **Error:** API dan xatolik kelsa, error state va qayta yuklash tugmasi.

## 8. Animatsiyalar
- Chart ustunlarining pastdan tepaga o'sish animatsiyasi (Chart.js/Recharts default).
- "Download PDF" bosilganda tugma loading (spinner) holatiga o'tadi.
- Jadval qatorlari hover qilinganda yengil background o'zgarishi.

## 9. Responsive
- **Mobile (sm):** Summary kartalar ustma-ust (1-column). Chart va Latest Payslip ustma-ust tushadi. Jadval gorizontal scroll bo'ladi yoki card view ga aylanadi.
- **Tablet (md):** Summary kartalar 2x2 grid. Chart va Latest Payslip 1-column bo'lib tushadi.
- **Desktop (lg, xl):** Summary kartalar 3-column. Chart katta qismni (masalan 2/3), Latest Payslip qolgan (1/3) qismni egallaydi.

## 10. API endpointlar
- `GET /api/v1/payrolls?employeeId=me&year=2026` — Barcha (yoki filtrlangan) payrollarni olish.
- `GET /api/v1/payrolls/:id` — Bitta payrollning batafsil (detail) ma'lumotlarini olish (PDF yaratish yoki latest card uchun).

**API docs:** `orcestor/project_docs/api/payroll.md`

## 11. Global state (Zustand)
- Faqat local state (tanlangan `year`) kerak bo'ladi, global state shart emas. Agar user auth ma'lumotlari kerak bo'lsa `useAuthStore` dan olinadi.

## 12. Muhim eslatmalar
- Chart kutubxonasi loyiha bo'ylab standartlashtirilishi kerak (`recharts` afzalroq, chunki React bilan yaxshi ishlaydi).
- PDF yuklab olish jarayonida kutilmagan kechikish bo'lishi mumkinligi sababli tugma animatsiyasida feedback (loading spinner) bo'lishi shart.
- "Net" summa hamma vaqt asosiy ajralib turuvchi (highlight) qism bo'lishi kerak.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/landing/features.md`

# Features Page Specification

## 1. Maqsad

Mahsulotning barcha asosiy funksiyalarini batafsil ko'rsatish sahifasi. Potensial mijozlarga har bir modul nima qila olishini tushuntirish, vizual kartalar orqali xususiyatlarni taqdim etish va sahifa oxirida CTA banner orqali konversiyaga undash.

---

## 2. Route

```
/features
```

---

## 3. Mockup reference

```
orcestor/examples/landing/features-page-v1.jpg
```

> Mockupda: Navbar, page hero (heading + subtitle), 2×3 feature cards grid, pastda CTA banner ko'rsatilgan.

---

## 4. Layout tuzilmasi

```
<RootLayout>
  └── <LandingLayout>
        ├── <Navbar />
        ├── <main>
        │     ├── <PageHero />           ← heading + subtitle (centered)
        │     ├── <FeaturesGrid />       ← 6 ta karta, 2×3 yoki 3×2 grid
        │     └── <CTABanner />          ← pastki call-to-action bloki
        └── <Footer />
```

**Page wrapper:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

---

## 5. Komponentlar ro'yxati

### 5.1 `<PageHero />` (Features variant)

| Element   | Mazmun                                                                    |
|-----------|---------------------------------------------------------------------------|
| Badge     | `"Platform Features"` — small pill/chip, indigo rang                      |
| Heading   | `"Everything your HR team needs"` — H1, centered                         |
| Subtitle  | `"Powerful tools to manage attendance, payroll, and more — all in one place"` |
| Background| Gradient yoki subtle pattern                                              |

```tsx
<PageHero
  badge="Platform Features"
  heading="Everything your HR team needs"
  subtitle="Powerful tools to manage attendance, payroll, and more — all in one place"
/>
```

---

### 5.2 `<FeaturesGrid />` — 6 ta Feature Card

Layout: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8`

#### Feature kartalar ma'lumotlari:

| # | Title               | Description                                                                   | Icon         | Color accent |
|---|---------------------|-------------------------------------------------------------------------------|--------------|--------------|
| 1 | Attendance Tracking | Real-time attendance monitoring with check-in/out logs and biometric support  | `Clock`      | indigo       |
| 2 | Leave Management    | Streamlined leave requests, multi-level approvals and leave balance tracking   | `Calendar`   | emerald      |
| 3 | Payroll Processing  | Automated salary calculations, tax deductions and payslip generation           | `DollarSign` | amber        |
| 4 | Employee Directory  | Centralized employee profiles, department structure and org chart view         | `Users`      | blue         |
| 5 | Terminal Access     | Secure CLI-based management interface for power users and system admins        | `Terminal`   | violet       |
| 6 | Analytics & Reports | Visual dashboards, custom reports, workforce insights and data export          | `BarChart2`  | rose         |

#### Static data strukturasi:

```tsx
const FEATURES = [
  {
    id: 'attendance',
    title: 'Attendance Tracking',
    description: 'Real-time attendance monitoring with check-in/out logs, late tracking, and biometric support.',
    icon: Clock,
    accent: 'indigo',
  },
  {
    id: 'leave',
    title: 'Leave Management',
    description: 'Streamlined leave requests, multi-level approvals, leave balance tracking and calendar view.',
    icon: Calendar,
    accent: 'emerald',
  },
  {
    id: 'payroll',
    title: 'Payroll Processing',
    description: 'Automated salary calculations, tax deductions, payslip generation and bank transfer integration.',
    icon: DollarSign,
    accent: 'amber',
  },
  {
    id: 'employee',
    title: 'Employee Directory',
    description: 'Centralized employee profiles, department structure, role management and org chart view.',
    icon: Users,
    accent: 'blue',
  },
  {
    id: 'terminal',
    title: 'Terminal Access',
    description: 'Secure CLI-based management interface for power users and system administrators.',
    icon: Terminal,
    accent: 'violet',
  },
  {
    id: 'analytics',
    title: 'Analytics & Reports',
    description: 'Visual dashboards, custom reports, workforce insights and data export capabilities.',
    icon: BarChart2,
    accent: 'rose',
  },
] as const;
```

---

### 5.3 `<FeatureCard />` komponenti

```tsx
interface FeatureCardProps {
  title:       string;
  description: string;
  icon:        LucideIcon;
  accent:      'indigo' | 'emerald' | 'amber' | 'blue' | 'violet' | 'rose';
}
```

**Card tuzilmasi:**

```tsx
<article className="group relative rounded-2xl border border-gray-100 bg-white p-8
                    shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
  {/* Icon container */}
  <div className={`mb-4 inline-flex rounded-xl p-3 bg-${accent}-50
                   group-hover:bg-${accent}-500 transition-colors duration-300`}>
    <Icon className={`h-6 w-6 text-${accent}-600
                      group-hover:text-white transition-colors duration-300`} />
  </div>

  {/* Content */}
  <h3 className="mb-2 text-xl font-semibold text-gray-900">{title}</h3>
  <p  className="text-gray-500 leading-relaxed">{description}</p>

  {/* Hover arrow indicator */}
  <div className="mt-4 flex items-center text-sm font-medium text-indigo-600
                  opacity-0 group-hover:opacity-100 transition-opacity duration-200">
    Learn more <ArrowRight className="ml-1 h-4 w-4" />
  </div>
</article>
```

> **Eslatma:** Tailwind JIT uchun dinamik `bg-${accent}-50` klass safelist-ga qo'shilishi kerak (quyida ko'rsatilgan).

**tailwind.config.ts safelist:**

```ts
safelist: [
  'bg-indigo-50',  'bg-indigo-500',  'text-indigo-600',
  'bg-emerald-50', 'bg-emerald-500', 'text-emerald-600',
  'bg-amber-50',   'bg-amber-500',   'text-amber-600',
  'bg-blue-50',    'bg-blue-500',    'text-blue-600',
  'bg-violet-50',  'bg-violet-500',  'text-violet-600',
  'bg-rose-50',    'bg-rose-500',    'text-rose-600',
],
```

---

### 5.4 `<CTABanner />`

| Element       | Mazmun                                          |
|---------------|-------------------------------------------------|
| Background    | Gradient: `from-indigo-600 to-violet-600`       |
| Heading       | `"Ready to transform your workforce?"` — H2, white |
| Subtitle      | `"Join 50+ companies already using our platform"` |
| Primary CTA   | `"Get Started Free"` → `/sign-in`              |
| Secondary CTA | `"Contact Sales"` → `mailto:sales@zdes.uz`     |
| Layout        | Centered, padding `py-20`                       |

```tsx
<section className="bg-gradient-to-r from-indigo-600 to-violet-600 py-20">
  <div className="max-w-3xl mx-auto text-center px-4">
    <h2 className="text-3xl font-bold text-white mb-4">
      Ready to transform your workforce?
    </h2>
    <p className="text-indigo-100 mb-8">
      Join 50+ companies already using our platform
    </p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center">
      <Link to="/sign-in" className="btn-primary-white">Get Started Free</Link>
      <a href="mailto:sales@zdes.uz" className="btn-ghost-white">Contact Sales</a>
    </div>
  </div>
</section>
```

---

## 6. Style (ranglar, tipografiya, spacing)

### Ranglar

```css
/* Karta accent ranglari */
--accent-indigo:  #6366f1;
--accent-emerald: #10b981;
--accent-amber:   #f59e0b;
--accent-blue:    #3b82f6;
--accent-violet:  #8b5cf6;
--accent-rose:    #f43f5e;

/* Background */
--bg-page:   #f9fafb;    /* gray-50 */
--bg-card:   #ffffff;
--bg-banner: linear-gradient(135deg, #6366f1, #8b5cf6);
```

### Tipografiya

| Element        | Size    | Weight | Color      |
|----------------|---------|--------|------------|
| Page H1        | 3xl–4xl | 700    | gray-900   |
| Badge          | xs–sm   | 600    | indigo-700 |
| Card title H3  | xl      | 600    | gray-900   |
| Card body      | base    | 400    | gray-500   |
| CTA heading H2 | 2xl–3xl | 700    | white      |
| CTA subtitle   | lg      | 400    | indigo-100 |

### Spacing

- Page hero padding: `py-20`
- Features grid section padding: `py-16`
- Card internal padding: `p-8`
- Grid gap: `gap-8`
- CTA banner padding: `py-20 px-4`

---

## 7. States

| State   | Tavsif                                                                      |
|---------|-----------------------------------------------------------------------------|
| Default | Statik render — kartalar ko'rinadi                                         |
| Hover   | Karta `translateY(-4px)`, shadow kuchayadi, icon rangi o'zgaradi, "Learn more" paydo bo'ladi |
| Focus   | Keyboard nav: `focus-visible:ring-2 ring-indigo-500 ring-offset-2`         |
| Loading | Yo'q (statik sahifa)                                                        |
| Error   | Yo'q (API yo'q)                                                             |

---

## 8. Animatsiyalar

### Kartalar hover animatsiyasi

```css
.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
}
```

**Framer Motion varianti:**

```tsx
<motion.article
  whileHover={{ y: -4 }}
  transition={{ type: 'spring', stiffness: 300, damping: 20 }}
>
```

### Scroll reveal (stagger)

```tsx
{FEATURES.map((feature, index) => (
  <motion.div
    key={feature.id}
    initial={{ opacity: 0, y: 40 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, amount: 0.1 }}
    transition={{ duration: 0.5, delay: index * 0.08 }}
  >
    <FeatureCard {...feature} />
  </motion.div>
))}
```

### Page Hero entrance

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6 }}
>
```

---

## 9. Responsive

| Breakpoint    | Grid layout  | Xatti-harakat                            |
|---------------|--------------|------------------------------------------|
| `xs` (<640px) | 1 column     | Kartalar to'liq kenglikda, vertikal      |
| `sm` (640px+) | 2 columns    | Kartalar 2 ustun                         |
| `lg` (1024px+)| 3 columns    | To'liq 3×2 grid                          |
| `xl` (1280px+)| 3 columns    | Container max-width cheklangan           |

**CTA Banner responsive:**

- Mobile: Tugmalar `flex-col gap-3 w-full`
- Desktop: Tugmalar `flex-row gap-4 justify-center`

---

## 10. API endpointlar

```
Hech qanday API chaqiruv yo'q — sahifa to'liq statik.
Feature ma'lumotlari frontend konstantasida saqlangan (yuqoridagi FEATURES array).
```

---

## 11. Global state (Zustand)

```
Bu sahifada global state ishlatilmaydi.
Local state ham yo'q — hover animatsiyalar CSS/Framer Motion orqali.
```

---

## 12. Muhim eslatmalar

1. **Icon library:** `import { Clock, Calendar, DollarSign, Users, Terminal, BarChart2, ArrowRight } from 'lucide-react'`
2. **Tailwind dynamic classes:** `bg-${accent}-50` kabi dinamik class-lar uchun `tailwind.config.ts`-da safelist o'rnating (yuqorida namuna bor).
3. **Accessibility:** Kartalar `<article>` tegi; grid `role="list"`, kartalar `role="listitem"`.
4. **SEO:** `<title>Features — Zdes</title>`, `<meta name="description">` barcha 6 modul nomlarini qamrab olsin.
5. **CTA Banner kontrast:** Oq matn kontrast nisbati WCAG AA ≥ 4.5:1 bo'lishi kerak — indigo-600 ustida oq rang OK.
6. **Card anchor links:** Kelajakda `href="#feature-id"` anchor link detail section-larga scroll qilishi uchun qoldiring.
7. **Reusability:** `<PageHero>`, `<CTABanner>` komponentlari boshqa landing sahifalarida ham ishlatiladi — ularni `components/landing/` papkasiga qo'ying.


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_review_12.md`

# Star Admin Inspired UI Redesign & Profile Modal Tasks

## 📌 Qadamlar Ro'yxati (12 Steps)

### Step 1: Dastlabki Reja va Arxitekturani Belgilash
- [x] Star Admin dizayn tamoyillarini va talablarni o'rganish
- [x] `zdes/review/tasks/step_review_12.md` va subagentlar vazifalarini taqsimlash

### Step 2: SVG Icon Tizimini O'rnatish va Sidebar Navigation ni Boyitish
- [ ] Sidebar uchun har bir menyu bandiga (Dashboard, Employees, Branches, Departments, Positions, Attendance, Terminals, Payroll, Leaves va h.k.) mos SVG ikonkalarni o'rnatish

### Step 3: Sidebar Zamonaviy Scroll va Gradient Buttonlar Dizayni
- [ ] Sidebar scrollbar'ini zamonaviy custom scrollbar (slim, rounded thumb) ko mezoniga o'tkazish
- [ ] Menyu faol va hover tugmalariga premium Star Admin uslubidagi gradient va glasmorfik background UI berish

### Step 4: Header User Profile & Avatar Button Qo'shish
- [ ] Headerda foydalanuvchi ismi oldiga Avatar avatar belgisi va Profile tugmasini joylashtirish
- [ ] Chiqish va Profile tugmalariga mos SVG ikonkalarni qo'shish

### Step 5: User Name display Name mapping (ID o'rniga ism ko'rsatish)
- [ ] `Header` hamda `Auth` servislarida `currentUser()?.firstName` / `lastName` bo'sh bo'lganda `login` ko'rsatish, UUID / numeric ID chiqqan joylarni to'g'rilash

### Step 6: User Profile Modal Component (Ko'rish Modal) Yaratish
- [ ] `UserProfileModal` komponentini standalone Angular komponenti sifatida yaratish
- [ ] Star Admin dizaynida modal UI, avatar, rol, login, email, telefon ma'lumotlarini taqdim etish

### Step 7: Profile Edit Modal Component (Tahrirlash Modal) Yaratish
- [ ] `ProfileEditModal` komponentini yaratish (Ism, familiya, email, telefon, parol o'zgartirish)
- [ ] ReactiveForm va validationlarni o'rnatish

### Step 8: User Profile API integration (`PATCH /users/me`)
- [ ] Backend NestJS `UserController` da `PATCH /users/me` endpointi bilan profilni yangilash integratsiyasini ulash

### Step 9: Jadvallar va Cards Star Admin Gradient & Shadows UI
- [ ] Barcha jadvallarga Star Admin clean modern card, subtle border radius va shadowlarni qo'llash
- [ ] Hover effektlari va micro-interactionlarni kuchaytirish

### Step 10: Global Buttons & Form Controls Modernization
- [ ] Barcha primary/secondary tugmalarni gradient (indigo to purple/blue) ko'rinishga o'tkazish
- [ ] Input va Select elementlariga focus-ring va modern border radius berish

### Step 11: Dark / Light Mode Harmonization Across All Components
- [ ] Star Admin Dark Theme rang palitrasiga barcha modullarni to'liq integratsiya qilish
- [ ] Matn va sarlavhalardagi kontrastni tekshirib to'g'rilash

### Step 12: Final Build, Subagent Synthesis & Verification
- [ ] Production / Dev build va UI sinovlarini o'tkazish
- [ ] Barcha 12 qadamni hujjatlashtirish va yakuniy hisobotni taqdim etish


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/T-043-response.md`

# T-043: 7 ta "A tizimi" modulini `/employees` ("B tizimi") page-header/table uslubiga o'tkazish

## Bajarilish jarayoni:

- [x] T-042 audit natijalarini o'qish va tushunish.
- [x] `positions` moduli (HTML va CSS yangilandi).
- [x] `departments` moduli.
- [x] `advances` moduli.
- [x] `terminals` moduli.
- [x] `payroll` moduli (Tugma mavjud emas, shunga ko'ra faqat header va table o'zgartirildi).
- [x] `holidays` moduli.
- [x] `salary-adjustments` moduli.
- [x] Barcha `.page-header-card` `linear-gradient` dizayniga o'tkazildi.
- [x] `h2` teglar `h1` teglariga aylantirildi.
- [x] Tugma sinflari `btn btn-gradient-add` yoki `btn-gradient-add`dan `.btn-add-new` ga o'zgartirildi.
- [x] Barcha ikonkalarning o'lchami `22x22` qilib belgilandi.
- [x] `npm run build` muvaffaqiyatli o'tmoqda.

## O'zgargan fayllar
| Fayl yo'li | O'zgarish turi | Sabab |
|---|---|---|
| `src/app/features/positions/pages/position-list/position-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/positions/pages/position-list/position-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/departments/pages/department-list/department-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/departments/pages/department-list/department-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/advances/pages/advance-list/advance-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/advances/pages/advance-list/advance-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/terminals/pages/terminal-list/terminal-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/terminals/pages/terminal-list/terminal-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/payroll/pages/payroll-list/payroll-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/payroll/pages/payroll-list/payroll-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/holidays/pages/holiday-list/holiday-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/holidays/pages/holiday-list/holiday-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/salary-adjustments/pages/adjustment-list/adjustment-list.css` | O'zgartirish | "B tizimi" uslubini tatbiq etish |
| `src/app/features/salary-adjustments/pages/adjustment-list/adjustment-list.html` | O'zgartirish | "B tizimi" uslubini tatbiq etish |

## Yakuniy Xulosa
Barcha 7 ta nishon moduli `employees` modulida qo'llanilgan yagona vizual stilga (ko'k gradient banner, neytral orqa fonli icon-badge, bir xil table card shadow/border o'zgarishlari) o'tkazildi. `notifications` moduliga tegib ketilmadi, chunki u aralash tizim hisoblanadi. Tashqi kutubxona qo'shilmadi. Barcha cheklovlar to'liq bajarildi.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/landing/pricing.md`

# Pricing Page Specification

## 1. Maqsad

Narx rejalarini foydalanuvchiga shaffof va aniq taqdim etish. Monthly/Annual switching, 3 ta narx rejasi va FAQ accordion orqali potensial mijozning savollariga javob berish va konversiyaga undash. To'liq statik sahifa — hech qanday API chaqiruv yo'q.

---

## 2. Route

```
/pricing
```

---

## 3. Mockup reference

```
orcestor/examples/landing/pricing-page-v1.jpg
```

> Mockupda: Navbar, page hero, monthly/annual toggle, 3 ta pricing card (Starter, Professional, Enterprise), pastda FAQ accordion ko'rsatilgan.

---

## 4. Layout tuzilmasi

```
<RootLayout>
  └── <LandingLayout>
        ├── <Navbar />
        ├── <main>
        │     ├── <PageHero />              ← heading + subtitle
        │     ├── <BillingToggle />         ← Monthly / Annual switch
        │     ├── <PricingGrid />           ← 3 ta pricing karta
        │     └── <FAQSection />            ← Accordion FAQ
        └── <Footer />
```

**Page wrapper:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

---

## 5. Komponentlar ro'yxati

### 5.1 `<PageHero />` (Pricing variant)

| Element  | Mazmun                                                        |
|----------|---------------------------------------------------------------|
| Badge    | `"Simple Pricing"` — pill/chip                               |
| Heading  | `"Choose the plan that fits your team"` — H1                 |
| Subtitle | `"Start free, scale as you grow. No hidden fees."` — muted   |

---

### 5.2 `<BillingToggle />`

Foydalanuvchi monthly yoki annual billing tanlaydi.

**State:**

```tsx
const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');
```

**UI tuzilmasi:**

```tsx
<div className="flex items-center justify-center gap-4">
  <span className={billingCycle === 'monthly' ? 'text-gray-900 font-semibold' : 'text-gray-400'}>
    Monthly
  </span>

  {/* Toggle switch */}
  <button
    role="switch"
    aria-checked={billingCycle === 'annual'}
    onClick={() => setBillingCycle(prev => prev === 'monthly' ? 'annual' : 'monthly')}
    className={`relative inline-flex h-6 w-11 rounded-full transition-colors
                ${billingCycle === 'annual' ? 'bg-indigo-600' : 'bg-gray-200'}`}
  >
    <span className={`inline-block h-4 w-4 rounded-full bg-white shadow
                      transform transition-transform mt-1
                      ${billingCycle === 'annual' ? 'translate-x-6' : 'translate-x-1'}`} />
  </button>

  <span className={billingCycle === 'annual' ? 'text-gray-900 font-semibold' : 'text-gray-400'}>
    Annual
    <span className="ml-2 text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-medium">
      Save 20%
    </span>
  </span>
</div>
```

**Narx hisoblash:**

```tsx
const getPrice = (monthlyPrice: number) => {
  if (billingCycle === 'annual') {
    return Math.round(monthlyPrice * 0.8); // 20% discount
  }
  return monthlyPrice;
};
```

---

### 5.3 `<PricingGrid />` — 3 ta Pricing Card

Layout: `grid grid-cols-1 md:grid-cols-3 gap-8 items-start`

#### Narx rejalari:

| #  | Plan         | Monthly Price | Annual Price | Target          | Highlighted |
|----|--------------|---------------|--------------|-----------------|-------------|
| 1  | Starter      | $29/mo        | $23/mo       | Small teams     | No          |
| 2  | Professional | $79/mo        | $63/mo       | Growing companies | **Yes** (featured) |
| 3  | Enterprise   | Custom        | Custom       | Large orgs      | No          |

#### Starter plan features:

```
✓ Up to 20 employees
✓ Attendance tracking
✓ Leave management
✓ Basic reports
✓ Email support
✗ Payroll processing
✗ Advanced analytics
✗ API access
```

#### Professional plan features:

```
✓ Up to 200 employees
✓ Attendance tracking
✓ Leave management
✓ Payroll processing
✓ Advanced analytics
✓ API access
✓ Priority support
✓ Custom integrations
✗ Dedicated account manager
```

#### Enterprise plan features:

```
✓ Unlimited employees
✓ All Professional features
✓ Dedicated account manager
✓ SLA guarantee (99.9%)
✓ Custom onboarding
✓ SSO / SAML
✓ Audit logs
✓ On-premise option
```

---

### 5.4 `<PricingCard />` komponenti

```tsx
interface PricingCardProps {
  plan:         string;            // "Starter" | "Professional" | "Enterprise"
  price:        number | 'custom'; // monthly narx (number) yoki custom
  billingCycle: 'monthly' | 'annual';
  features:     string[];
  isHighlighted?: boolean;         // Professional — featured card
  ctaLabel:     string;            // "Get Started" | "Start Free Trial" | "Contact Sales"
  ctaHref:      string;            // "/sign-in" | "/contact"
}
```

**Card tuzilmasi:**

```tsx
<div className={`relative rounded-2xl p-8 border
  ${isHighlighted
    ? 'bg-indigo-600 border-indigo-600 shadow-2xl scale-105 text-white'
    : 'bg-white border-gray-200 shadow-sm text-gray-900'
  }`}>

  {/* Popular badge */}
  {isHighlighted && (
    <div className="absolute -top-4 left-1/2 -translate-x-1/2">
      <span className="bg-amber-400 text-amber-900 text-xs font-bold
                       px-4 py-1 rounded-full uppercase tracking-wide">
        Most Popular
      </span>
    </div>
  )}

  {/* Plan name */}
  <h3 className="text-xl font-bold mb-2">{plan}</h3>

  {/* Price */}
  <div className="mb-6">
    {price === 'custom' ? (
      <span className="text-4xl font-bold">Custom</span>
    ) : (
      <>
        <span className="text-4xl font-bold">
          ${billingCycle === 'annual' ? Math.round(price * 0.8) : price}
        </span>
        <span className="text-sm opacity-70">/mo</span>
        {billingCycle === 'annual' && (
          <p className="text-sm opacity-70 mt-1">billed annually</p>
        )}
      </>
    )}
  </div>

  {/* Features list */}
  <ul className="space-y-3 mb-8">
    {features.map((f, i) => (
      <li key={i} className="flex items-center gap-2 text-sm">
        {f.startsWith('✓')
          ? <Check className="h-4 w-4 text-emerald-400 shrink-0" />
          : <X    className="h-4 w-4 opacity-30 shrink-0" />
        }
        {f.replace(/^[✓✗] /, '')}
      </li>
    ))}
  </ul>

  {/* CTA Button */}
  <Link to={ctaHref}
    className={`block w-full text-center py-3 px-6 rounded-xl font-semibold
      ${isHighlighted
        ? 'bg-white text-indigo-600 hover:bg-indigo-50'
        : 'bg-indigo-600 text-white hover:bg-indigo-700'
      } transition-colors`}>
    {ctaLabel}
  </Link>
</div>
```

---

### 5.5 `<FAQSection />` — Accordion

FAQ elementlari (static data):

```tsx
const FAQ_ITEMS = [
  {
    question: 'Can I change my plan later?',
    answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately and billing is prorated.',
  },
  {
    question: 'Is there a free trial?',
    answer: 'Yes! The Professional plan comes with a 14-day free trial. No credit card required to get started.',
  },
  {
    question: 'How does the annual billing work?',
    answer: 'Annual billing means you pay for 12 months upfront and get a 20% discount compared to monthly billing.',
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards (Visa, Mastercard, Amex), bank transfers, and PayPal.',
  },
  {
    question: 'Can I add more employees to my plan?',
    answer: 'Yes, you can add employees at any time. If you exceed your plan limit, we will notify you to upgrade.',
  },
  {
    question: 'Is my data secure?',
    answer: 'Absolutely. We use AES-256 encryption, SOC 2 Type II certified infrastructure, and regular security audits.',
  },
];
```

**Accordion state:**

```tsx
const [openIndex, setOpenIndex] = useState<number | null>(null);

const toggle = (index: number) => {
  setOpenIndex(prev => prev === index ? null : index);
};
```

**Accordion item tuzilmasi:**

```tsx
<div className="border-b border-gray-200">
  <button
    onClick={() => toggle(index)}
    className="flex w-full items-center justify-between py-5 text-left"
    aria-expanded={openIndex === index}
  >
    <span className="font-medium text-gray-900">{item.question}</span>
    <ChevronDown
      className={`h-5 w-5 text-gray-400 transition-transform duration-200
                  ${openIndex === index ? 'rotate-180' : ''}`}
    />
  </button>

  {/* Animated collapse */}
  <div className={`overflow-hidden transition-all duration-300
                   ${openIndex === index ? 'max-h-96 pb-5' : 'max-h-0'}`}>
    <p className="text-gray-500">{item.answer}</p>
  </div>
</div>
```

---

## 6. Style (ranglar, tipografiya, spacing)

### Ranglar

```css
/* Cards */
--card-default:      #ffffff;
--card-featured:     #6366f1;   /* indigo-600 */
--card-border:       #e5e7eb;   /* gray-200 */

/* Badge */
--badge-popular:     #fbbf24;   /* amber-400 */
--badge-save:        #d1fae5;   /* emerald-100 */

/* Toggle */
--toggle-on:  #6366f1;
--toggle-off: #e5e7eb;

/* Check icon */
--check-color: #34d399;   /* emerald-400 */
```

### Tipografiya

| Element        | Size    | Weight | Color        |
|----------------|---------|--------|--------------|
| H1 (Page)      | 3xl–4xl | 700    | gray-900     |
| Plan name H3   | xl      | 700    | gray-900/white |
| Price value    | 4xl     | 700    | gray-900/white |
| Feature item   | sm      | 400    | gray-700/white |
| FAQ question   | base    | 500    | gray-900     |
| FAQ answer     | base    | 400    | gray-500     |

### Spacing

- Hero padding: `py-20`
- Toggle margin: `my-10`
- Grid padding: `pb-20`
- Card padding: `p-8`
- FAQ section padding: `py-16`

---

## 7. States

| State           | Tavsif                                                              |
|-----------------|---------------------------------------------------------------------|
| Monthly (default)| Monthly narxlar ko'rsatiladi                                       |
| Annual          | Annual narxlar (20% off) ko'rsatiladi, toggle active               |
| FAQ closed      | Accordion yopiq — faqat question ko'rinadi                         |
| FAQ open        | Accordion ochiq — answer `max-h-96` bilan animate paydo bo'ladi    |
| Card highlighted| Professional card — indigo bg, scale-105, "Most Popular" badge     |
| Loading         | Yo'q (statik sahifa)                                               |
| Error           | Yo'q (API yo'q)                                                    |

---

## 8. Animatsiyalar

### Billing toggle narx o'zgarishi

```tsx
// Narx o'zgarganda fade animatsiya
<motion.span
  key={`${plan}-${billingCycle}`}  // key o'zgarganda re-animate
  initial={{ opacity: 0, y: -8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.2 }}
>
  ${price}
</motion.span>
```

### FAQ accordion

```tsx
<AnimatePresence>
  {openIndex === index && (
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{ height: 'auto', opacity: 1 }}
      exit={{ height: 0, opacity: 0 }}
      transition={{ duration: 0.25 }}
    >
      <p className="text-gray-500 pb-5">{item.answer}</p>
    </motion.div>
  )}
</AnimatePresence>
```

### Scroll reveal (pricing cards)

```tsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.5, delay: index * 0.1 }}
>
```

---

## 9. Responsive

| Breakpoint    | Grid         | Xatti-harakat                                      |
|---------------|--------------|----------------------------------------------------|
| `xs` (<640px) | 1 column     | Kartalar vertikal, Professional card scale-105 yo'q |
| `md` (768px+) | 3 columns    | Professional card scale-105 bilan featured         |
| `lg` (1024px+)| 3 columns    | Full layout, max-width container                    |

**Toggle responsive:** Centered, `flex-wrap` bilan kichik ekranlarda ham to'g'ri ko'rinadi.

**Card responsive:** Mobile-da `scale-105` olib tashlanadi (`md:scale-105`).

---

## 10. API endpointlar

```
Hech qanday API chaqiruv yo'q — sahifa to'liq statik.
Narxlar va features frontend konstantasida saqlangan.
```

---

## 11. Global state (Zustand)

```
Bu sahifada global Zustand state ishlatilmaydi.
```

**Local state:**

```tsx
const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');
const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(null);
```

---

## 12. Muhim eslatmalar

1. **Pricing data boshqaruvi:** Narxlar hozircha hardcoded — kelajakda CMS yoki env variable orqali boshqarilishi mumkin.
2. **Enterprise CTA:** Enterprise karta CTA-si `/sign-in` emas, `mailto:sales@zdes.uz` yoki `/contact` sahifasiga borilsin.
3. **Annual savings badge:** Toggle annual-ga o'tganda "Save 20%" badge ko'rinsin.
4. **Professional card z-index:** Scale-105 bilan adjacent kartalar ustidan chiqmasligi uchun `z-10` qo'shing.
5. **FAQ SEO:** FAQ items `<script type="application/ld+json">` FAQPage schema bilan markup qilinsin.
6. **Accessibility:** Toggle `role="switch"`, `aria-checked`; Accordion items `aria-expanded`, `aria-controls` atributlari.
7. **Currency:** Hozircha USD — kelajakda i18n bilan lokalizatsiya qilinishi mumkin.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/attendance.md`

# Attendance Page Specification

## 1. Maqsad

"My Attendance" sahifasi xodimning shaxsiy davomat tarixini ko'rish, filter qilish va export qilish uchun mo'ljallangan. Oy bo'yicha kalendar ko'rinishida va jadval (table) ko'rinishida ma'lumotlar taqdim etiladi.

---

## 2. Route

```
/attendance
```

Protected route. Autentifikatsiya talab qilinadi.

---

## 3. Mockup Reference

```
orcestor/examples/panel/panel-attendance-v1.jpg
```

---

## 4. Layout Tuzilmasi

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR (fixed left, 240px)                                │
├─────────────────────────────────────────────────────────────┤
│  TOPBAR (sticky, 64px)                                      │
├─────────────────────────────────────────────────────────────┤
│  MAIN CONTENT                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Page Header: "My Attendance" + Month Switcher       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │Present │ │ Late   │ │Absent  │ │ Total  │               │
│  │  Days  │ │Arrivals│ │  Days  │ │  Hrs   │               │
│  └────────┘ └────────┘ └────────┘ └────────┘               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Full-width Attendance Calendar (monthly)            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Attendance Log Table                                │   │
│  │  [Date][Check In][Check Out][Worked Hours][Status]   │   │
│  │  [Notes]                                             │   │
│  │  Pagination                                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Komponentlar Ro'yxati

### 5.1 Page Header

```tsx
<PageHeader
  title="My Attendance"
  subtitle="Track your daily attendance records"
/>
```

### 5.2 Month Switcher

```tsx
<MonthSwitcher
  currentMonth={queryState.month}   // "2026-08"
  onPrev={handlePrevMonth}
  onNext={handleNextMonth}
  disableNext={isCurrentMonth}      // kelajakka o'tib bo'lmaydi
/>
```

**Ko'rinish:**
```
[<] August 2026 [>]
```

- `<` tugma: oldingi oyga o'tish
- `>` tugma: keyingi oyga o'tish, lekin joriy oydan o'tib ketmaydi
- Format: `MMMM yyyy` (`date-fns/format`)

---

### 5.3 Summary Cards (4 ta)

| # | Title | Hisob-kitob | Icon | Color |
|---|-------|-------------|------|-------|
| 1 | Present Days | sessions filter `status !== 'absent'` count | `UserCheck` | Green |
| 2 | Late Arrivals | sessions filter `status === 'late'` count | `Clock` | Orange |
| 3 | Absent Days | sessions filter `status === 'absent'` count | `UserX` | Red |
| 4 | Total Worked Hours | sum of `workedMinutes / 60`, format: "142h 30m" | `Timer` | Blue |

```tsx
<StatCard
  title="Present Days"
  value={presentDays}
  unit="days"
  icon={UserCheckIcon}
  accentColor="green"
  loading={isLoading}
/>
```

---

### 5.4 Full-width Attendance Calendar

```tsx
<AttendanceCalendarFull
  month={queryState.month}           // "2026-08"
  sessions={sessions}
  loading={isLoadingCalendar}
  onDayClick={handleDayClick}       // → scroll to table row yoki modal
/>
```

**Color coding:**
```
present  → bg-green-100  text-green-800   border-l-4 border-green-500
late     → bg-orange-100 text-orange-800  border-l-4 border-orange-500
absent   → bg-red-100    text-red-800     border-l-4 border-red-500
weekend  → bg-gray-50    text-gray-400
holiday  → bg-purple-50  text-purple-600
today    → ring-2 ring-blue-400
future   → text-gray-300 (grayed out, no data)
```

**Kalendar grid:**
- 7 ustun (Sun-Sat yoki Mon-Sun, konfigga qarab)
- Har bir cell ichida: kun raqami + status dot/badge
- Hover tooltip: "Check In: 09:05 | Check Out: 18:02 | Worked: 8h 57m"

**Legend (kalendar ostida):**
```
● Present  ● Late  ● Absent  ● Weekend  ● No Data
```

---

### 5.5 Attendance Log Table

```tsx
<AttendanceTable
  sessions={sessions}
  loading={isLoadingTable}
  pagination={pagination}
  onPageChange={handlePageChange}
/>
```

**Columns:**

| Column | Type | Misol |
|--------|------|-------|
| Date | `MMM d, yyyy (EEEE)` | "Aug 22, 2026 (Friday)" |
| Check In | `hh:mm a` | "09:05 AM" |
| Check Out | `hh:mm a` yoki "—" | "06:02 PM" |
| Worked Hours | "8h 57m" yoki "—" | |
| Status | Badge | `Present / Late / Absent` |
| Notes | truncate 30 chars | "Left early for..." |

**Status badge ranglari:**
```
present → bg-green-100 text-green-700 ring-green-600/20
late    → bg-orange-100 text-orange-700 ring-orange-600/20
absent  → bg-red-100 text-red-700 ring-red-600/20
```

**Row hover:** `hover:bg-gray-50`

**Absent row:** butun qator `bg-red-50/30` yoki faqat status cell highlighted

---

### 5.6 Pagination

```tsx
<Pagination
  currentPage={queryState.page}
  totalPages={Math.ceil(total / queryState.limit)}
  onPageChange={setPage}
  limit={queryState.limit}
  totalItems={total}
/>
```

- Page size options: 10, 20, 50
- Ko'rinish: `"Showing 1-20 of 47 records"` + `[< 1 2 3 >]`

---

## 6. Style (Ranglar, Tipografiya, Spacing)

### Ranglar
```
Page bg:           bg-gray-50
Card/Table bg:     bg-white
Border:            border-gray-200
Table header bg:   bg-gray-50
Table row hover:   bg-gray-50
Divider:           border-gray-100

Status Present:    bg-green-100 text-green-700
Status Late:       bg-orange-100 text-orange-700
Status Absent:     bg-red-100 text-red-700
```

### Tipografiya
```
Page title:        text-2xl font-bold text-gray-900
Month display:     text-xl font-semibold text-gray-700
Table header:      text-xs font-semibold text-gray-500 uppercase tracking-wide
Table cell:        text-sm text-gray-700
Status badge:      text-xs font-medium
Pagination info:   text-sm text-gray-500
```

### Spacing
```
Page padding:      p-6
Card padding:      p-4 yoki p-5
Table padding:     px-6 py-4 (th), px-6 py-3 (td)
Section gap:       mb-6
```

---

## 7. States

### 7.1 Loading State
- Summary cards: skeleton placeholder (4 ta)
- Calendar: grid skeleton — 35 ta cell, har biri `h-12 bg-gray-100 animate-pulse`
- Table: 10 ta skeleton row

### 7.2 Empty State (no records)
```tsx
<EmptyState
  icon={CalendarOff}
  title="No attendance records"
  description="No records found for this month."
/>
```

### 7.3 Month Filter State
- Month o'zgarganda: `isLoading = true`, yangi ma'lumot kelguncha skeleton
- URL query param sifatida saqlash: `?month=2026-08&page=1`

### 7.4 Error State
```tsx
<ErrorState
  message="Failed to load attendance data"
  onRetry={refetch}
/>
```

---

## 8. Animatsiyalar

```
Month switch:      fade transition (calendar va table birga)
                   animate-out: opacity 0, 150ms
                   animate-in:  opacity 1, 150ms
Calendar day hover: bg-color transition 100ms
Table row hover:   bg transition 100ms
Skeleton:          animate-pulse
Page load:         staggered fade-in (cards first, then calendar, then table)
```

---

## 9. Responsive

| Breakpoint | Layout |
|-----------|--------|
| `< 640px` | Summary cards: 2x2 grid. Calendar: simplified (dots only per day). Table: card-style (stacked rows). |
| `640px–1024px` | Summary cards: 4 column. Calendar: full grid. Table: horizontal scroll if needed. |
| `>= 1024px` | Full layout as designed. |

```tsx
// Cards
<div className="grid grid-cols-2 sm:grid-cols-4 gap-4">

// Calendar
<div className="overflow-x-auto">
  <AttendanceCalendarFull />
</div>

// Table
<div className="overflow-x-auto">
  <table className="min-w-full">
```

---

## 10. API Endpointlar

### 10.1 Attendance Sessions (asosiy)
```
GET /api/v1/attendance/self/sessions
Authorization: Bearer {token}

Query params:
  dateFrom:  string  "2026-08-01"     (oy boshi)
  dateTo:    string  "2026-08-31"     (oy oxiri)
  page:      number  1
  limit:     number  20

Response 200:
{
  data: [
    {
      id:            string,
      date:          "2026-08-22",
      checkIn:       "2026-08-22T09:05:00.000Z" | null,
      checkOut:      "2026-08-22T18:02:00.000Z" | null,
      workedMinutes: number | null,
      status:        "present" | "late" | "absent",
      notes:         string | null,
      fileUrl:       string | null
    }
  ],
  total:   number,
  page:    number,
  limit:   number,
  totalPages: number
}
```

**Eslatma:** Calendar uchun `limit=100` (yoki oy kunlari soni), jadval uchun `limit=20` + pagination. Ikki alohida query ishlatish yoki bitta katta query dan filter qilish mumkin.

---

### 10.2 Check In
```
POST /api/v1/attendance/self/check-in
Authorization: Bearer {token}
Content-Type: multipart/form-data

Body (FormData):
  notes:  string (optional)
  file:   File   (optional, rasm yoki hujjat)

Response 201:
{
  id:       string,
  checkIn:  "2026-08-23T09:05:00.000Z",
  status:   "present" | "late"
}

Errors:
  400 - Already checked in today
  422 - Validation error
```

---

### 10.3 Check Out
```
POST /api/v1/attendance/self/check-out
Authorization: Bearer {token}

Response 200:
{
  id:            string,
  checkOut:      "2026-08-23T18:02:00.000Z",
  workedMinutes: number
}

Errors:
  400 - Not checked in yet
  400 - Already checked out
```

Ref: `orcestor/project_docs/api/attendance.md`

---

## 11. Global State (Zustand)

### `useAttendanceStore`
```ts
interface AttendanceStore {
  // Data
  sessions:      AttendanceSession[];
  todaySession:  AttendanceSession | null;
  total:         number;

  // Loading/Error
  isLoading:     boolean;
  isCheckingIn:  boolean;
  isCheckingOut: boolean;
  error:         string | null;

  // Query state
  queryState: {
    month:  string;    // "YYYY-MM"
    page:   number;
    limit:  number;
  };

  // Actions
  fetchSessions:  (dateFrom: string, dateTo: string, page?: number) => Promise<void>;
  checkIn:        (notes?: string, file?: File) => Promise<void>;
  checkOut:       () => Promise<void>;
  setMonth:       (month: string) => void;
  setPage:        (page: number) => void;
}
```

**Query state URL sync:**
```ts
// TanStack Router search params bilan sinxronlash
const { month, page } = useSearch({ from: '/attendance' })
// yoki React Router searchParams
```

---

## 12. Muhim Eslatmalar

1. **Calendar va Table uchun bir xil data:** Calendar uchun oy davomidagi barcha sessionlar kerak (limit=100), table uchun paginated (limit=20). Ikki alohida state ishlatish yoki bir xil ma'lumotdan ikkalasi uchun ham foydalanish mumkin.

2. **Worked Hours hisoblash:**
   ```ts
   const formatWorkedTime = (minutes: number | null) => {
     if (!minutes) return '—'
     const h = Math.floor(minutes / 60)
     const m = minutes % 60
     return `${h}h ${m}m`
   }
   ```

3. **Total Worked Hours (stat card):**
   ```ts
   const totalMinutes = sessions.reduce((acc, s) => acc + (s.workedMinutes ?? 0), 0)
   ```

4. **Month boundary calculation:**
   ```ts
   import { startOfMonth, endOfMonth, format } from 'date-fns'
   const date = parse(queryState.month, 'yyyy-MM', new Date())
   const dateFrom = format(startOfMonth(date), 'yyyy-MM-dd')
   const dateTo = format(endOfMonth(date), 'yyyy-MM-dd')
   ```

5. **Future month prevention:**
   ```ts
   const isCurrentOrFuture = queryState.month >= format(new Date(), 'yyyy-MM')
   // disableNext={isCurrentOrFuture}
   ```

6. **URL search params:** `?month=2026-08&page=1` — sahifani yangilaganda ham holat saqlansin.

7. **Calendar day click:** Kun bosilganda table-da o'sha date ga scroll qiling yoki highlight qiling.

8. **Late determination:** Backend status qaytaradi. Agar frontend taraf kerak bo'lsa: check-in time > work schedule start time + grace period → "late".


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/T-031-response.md`

# T-031: Server-side pagination — API sirtini tayyorlash

## Bajarilgan ishlar:
1. `DataTableComponent`ga server-side pagination uchun tegishli input/output parametrlar qo'shildi (`serverSide`, `totalCount`, `serverPageChange`, `serverSortChange`, `serverFilterChange`).
2. Agar `serverSide` true bo'lsa komponent ma'lumotlarni o'zi filterlamaydi, sortlamaydi va sahifalamaydi (bular uchun maxsus eventlar chaqiriladi). `serverSide` false bo'lsa hozirgi holat qanday bo'lsa shundayligicha (client-side) ishlaydi.
3. Backend chegarasi: `pageSize` qiymati `@Max(100)` dan oshib ketmasligi uchun `Math.min(pageSize, 100)` validatsiyasi qo'shildi. 
4. HTML template'da sahifalash komponenti server-side rejim uchun ham to'g'ri ko'rinishi (ya'ni `processedData.length` emas `totalCount` hisobga olinishi) ta'minlandi.
5. `project_docs/api/README.md` fayliga server-side pagination haqida qisqacha ma'lumot qo'shildi.

## O'zgargan fayllar
| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `src/app/shared/components/ui/data-table/data-table.ts` | Tahrir | `serverSide` input va outputlarni ulash, API sirtini tayyorlash. `pageSize` 100 dan oshmasligi tekshirildi. |
| `src/app/shared/components/ui/data-table/data-table.html` | Tahrir | Sahifalash qismini `serverSide` ga moslashtirish, `showPagination` xossasi orqali. |
| `project_docs/api/README.md` | Tahrir | API bo'yicha hujjatda DataTable ning kelajakdagi imkoniyati haqida qisqa eslatma qo'shildi. |


## Manba: `zdes_archive_docs/raw_history/orcestor/analysis/T-042-header-style-audit.md`

# Barcha list-sahifalarning page-header/table uslubini `/employees` andozasiga solishtirish audit

## 1. Modullar bo'yicha tahlil natijalari

| Modul | Tizim | Aniq farqlar (agar bo'lsa) |
|---|---|---|
| positions | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| departments | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| branches | B tizimi | Yo'q |
| attendance | B tizimi | Yo'q |
| leaves | B tizimi | Yo'q |
| work-schedules | B tizimi | Yo'q |
| company | B tizimi | Yo'q |
| employees | B tizimi | Yo'q |
| advances | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| terminals | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| payroll | A tizimi | sarlavha: <h2>, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| holidays | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| salary-adjustments | A tizimi | sarlavha: <h2>, tugmada <span> bor, .page-header-card foni neytral, tugma klassi .btn-gradient-add |
| notifications | Aralash | Stillar to'liq A yoki B ga mos emas |

## 2. Umumiy statistika
- **A tizimi**: 7 ta modul (positions, departments, advances, terminals, payroll, holidays, salary-adjustments)
- **B tizimi**: 6 ta modul (branches, attendance, leaves, work-schedules, company, employees)
- **Aralash/Boshqa**: 1 ta modul (notifications)

## 3. `employees` (B tizimi)ga o'tish uchun nima o'zgartirilishi kerak (A tizimidagi modullar uchun)
Har bir A tizimidagi modullar uchun quyidagi CSS/HTML o'zgarishlari qilinishi kerak:
1. **`.page-header-card` CSS**: `background: var(--color-bg-primary); border: ...` olib tashlanib, `background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(37, 99, 235, 0.25);` ga almashtirilishi kerak.
2. **`.header-icon-badge` CSS**: Foni `rgba(255, 255, 255, 0.15)` qilinishi va box-shadow olib tashlanishi kerak. Icon o'lchami 22x22 qilinishi kerak.
3. **Sarlavha va matnlar CSS**: `.page-title` rangi `#fff`, `.page-subtitle` rangi `rgba(255, 255, 255, 0.7)` qilinishi kerak.
4. **HTML Sarlavha teg**: `<h2 class="page-title">` dan `<h1 class="page-title">` ga o'zgartirilishi kerak.\n5. **Tugma CSS va HTML**: `.btn-gradient-add` o'rniga `.btn-add-new` ishlatilishi kerak. Uning CSS foni `rgba(255, 255, 255, 0.15)`, `border: 1.5px solid rgba(255, 255, 255, 0.35);`, `color: #fff;` qilinishi kerak. HTMLda `<svg>... Y` matni `<span>` siz yozilishi kerak.

## 4. Dark-mode ta'siri haqida eslatma
B tizimidagi butun kartani qamrab oluvchi gradient (`linear-gradient`) dark va light rejimlarda mustaqil ravishda bir xil (ko'k) ko'rinadi. 
- **Ijobiy tomoni**: Gradient har doim chiroyli va diqqatni tortuvchi premium ko'rinish beradi (dark rejimda ham ajralib turadi).
- **Salbiy tomoni**: Agar ilova qat'iy quyuq (dark) ranglar tizimiga ega bo'lsa, bu yorqin ko'k karta juda yorqin bo'lib qolishi mumkin, chunki u CSS o'zgaruvchisiga (var(--color-bg...)) bog'lanmagan. Lekin hozirgi kunda `employees`ni reference qilib olganimiz uchun, bu kerakli natija hisoblanadi.


## Manba: `zdes_archive_docs/raw_history/orcestor/task_compliete/T-037-response.md`

# T-037 — Responsive Media Query (max-width: 480px) — Jonli Jurnal

**Boshlangan vaqt:** 2026-07-26T01:12  
**Holat:** 🔄 Jarayonda

---

## Reja

7 ta CSS faylning har biriga faylning OXIRIGA `@media (max-width: 480px)` blok qo'shish:
1. `department-form.css` — `.form-page` (padding: 1.5rem 0 → 12px), `.form-actions`
2. `advance-form.css` — `.advance-form-container` (padding: 20px → 12px), `.form-actions`
3. `work-schedule-form.css` — `.form-container` (padding: 20px → 12px), `.actions`
4. `terminal-form.css` — `.terminal-form-container` (padding: 20px → 12px), `.form-actions`
5. `leave-form.css` — `.leave-form-container` (padding: 20px → 12px), `.btn` (flex-wrap: wrap)
6. `holiday-form.css` — `.holiday-form-container` (padding: 24px → 12px), `.form-actions`
7. `adjustment-form.css` — `.form` (padding yo'q — padding: 0 12px qo'shiladi), `.actions`

---

## Bajarilgan qadamlar

### Qadam 1 — Barcha 7 ta faylni o'qish (✅ tugadi)
- `department-form.css`: 146 qator, `.form-page {padding: 1.5rem 0}`, `.form-actions` (98-103-qatorlar)
- `advance-form.css`: 62 qator, `.advance-form-container {padding: 20px}`, `.form-actions` (32-36-qatorlar)
- `work-schedule-form.css`: 46 qator, `.form-container {padding: 20px}`, `.actions` (22-26-qatorlar)
- `terminal-form.css`: 62 qator, `.terminal-form-container {padding: 20px}`, `.form-actions` (33-37-qatorlar)
- `leave-form.css`: 29 qator, `.leave-form-container {padding: 20px}`, `.btn` alohida (20-25-qatorlar)
- `holiday-form.css`: 102 qator, `.holiday-form-container {padding: 24px}`, `.form-actions` (55-59-qatorlar)
- `adjustment-form.css`: 15 qator, `.form {max-width: 400px; padding yo'q}`, `.actions` (11-14-qatorlar)

**Qaror:** `leave-form.css`da alohida `.form-actions` yo'q — `.btn`larning ota-elementiga `.leave-form-container`ga `display: flex; flex-wrap: wrap` qo'shish o'rniga, `.btn` uchun `display: block; width: 100%; margin-right: 0` ishlatiladi (task talabi: `.btn`larning ota-elementiga flex-wrap yoki shunga o'xshash).

**Qaror:** `adjustment-form.css`da padding yo'q — `padding: 0 12px` qo'shiladi (task ruxsat bergan).

### Qadam 2 — CSS fayllarni tahrirlash (✅ tugadi)

Har bir faylning oxiriga `@media (max-width: 480px)` bloki qo'shildi:

| # | Fayl | Konteyner | Padding o'zgarishi | Tugma qatori |
|---|------|-----------|-------------------|--------------|
| 1 | `department-form.css` | `.form-page` | `1.5rem 0` → `12px` | `.form-actions` → `flex-direction: column; align-items: stretch` |
| 2 | `advance-form.css` | `.advance-form-container` | `20px` → `12px` | `.form-actions` → `flex-direction: column; align-items: stretch` |
| 3 | `work-schedule-form.css` | `.form-container` | `20px` → `12px` | `.actions` → `flex-direction: column; align-items: stretch` |
| 4 | `terminal-form.css` | `.terminal-form-container` | `20px` → `12px` | `.form-actions` → `flex-direction: column; align-items: stretch` |
| 5 | `leave-form.css` | `.leave-form-container` | `20px` → `12px` | `.btn` → `display: block; width: 100%; margin-right: 0; margin-bottom: 8px` |
| 6 | `holiday-form.css` | `.holiday-form-container` | `24px` → `12px` | `.form-actions` → `flex-direction: column; align-items: stretch` |
| 7 | `adjustment-form.css` | `.form` | yo'q → `0 12px` | `.actions` → `flex-direction: column; align-items: stretch` |

**Maxsus qarorlar:**
- `leave-form.css`: alohida `.form-actions` yo'q. `.btn`ga `display: block; width: 100%` berish bilan tugmalar to'liq kenglikka chiqarildi — bu task talabidagi "ularning ota-elementiga flex-wrap yoki shunga o'xshash" ekvivalenti.
- `adjustment-form.css`: `.form`da padding qiymati yo'q edi. Task ruxsat berganidek `padding: 0 12px` qo'shildi (yon tomonlarga kichik bo'shliq).

### Qadam 3 — `npm run build` tekshiruvi (✅ tugadi)
- **Exit code: 0** — muvaffaqiyatli
- Ogohlantirishlar: `login.css budget` (T-037 bilan bog'liq emas, oldin ham mavjud), `axios ESM` (oldin ham mavjud)
- Yangi xato yo'q

### Qadam 4 — Fayllarni `task_compliete/` ga ko'chirish (✅ tugadi)
- `T-037.md` → `orcestor/task_compliete/T-037.md`
- `T-037-response.md` → `orcestor/task_compliete/T-037-response.md`

---

## Yakuniy Xulosa

T-037 to'liq bajarildi. 7 ta CSS faylning har birining oxiriga `@media (max-width: 480px)` bloki qo'shildi: konteyner padding'i kichraytirildi (20–24px dan 12px ga), tugma qatorlari kichik ekranda bir ustunga tushirildi. Mavjud qoidalar o'zgartirilmadi, `.html`/`.ts` fayllar tegmasilmadi. `npm run build` exit code 0 bilan muvaffaqiyatli tugadi.

**Definition of Done tekshiruvi:**
- ✅ Har bir faylning oxirida `@media (max-width: 480px)` bloki bor
- ✅ Konteyner padding kichraygan (20/24px → 12px yoki yo'q → `0 12px`)
- ✅ Tugma qatori kichik ekranda bir ustunga tushgan
- ✅ `npm run build` xatosiz o'tdi (exit code 0)

---

### O'zgargan fayllar

| Fayl | Turi | Qisqa sabab |
|---|---|---|
| `src/app/features/departments/pages/department-form/department-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.form-page` padding 12px, `.form-actions` bir ustun |
| `src/app/features/advances/pages/advance-form/advance-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.advance-form-container` padding 12px, `.form-actions` bir ustun |
| `src/app/features/work-schedules/pages/work-schedule-form/work-schedule-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.form-container` padding 12px, `.actions` bir ustun |
| `src/app/features/terminals/pages/terminal-form/terminal-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.terminal-form-container` padding 12px, `.form-actions` bir ustun |
| `src/app/features/leaves/pages/leave-form/leave-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.leave-form-container` padding 12px, `.btn` full-width blok |
| `src/app/features/holidays/pages/holiday-form/holiday-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.holiday-form-container` padding 12px, `.form-actions` bir ustun |
| `src/app/features/salary-adjustments/pages/adjustment-form/adjustment-form.css` | o'zgartirilgan | `@media (max-width: 480px)` qo'shildi: `.form` padding 0 12px, `.actions` bir ustun |


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/leaves.md`

# Leaves Page Specification

## 1. Maqsad

"My Leaves" sahifasi xodimning ta'til balansini ko'rish, ta'til so'rovlarini yuborish, mavjud so'rovlarni kuzatish va bekor qilish uchun mo'ljallangan. Foydalanuvchi turli turdagi ta'tillar (annual, sick, unpaid) bo'yicha ma'lumot olishi mumkin.

---

## 2. Route

```
/leaves
```

Protected route. Autentifikatsiya talab qilinadi.

---

## 3. Mockup Reference

```
orcestor/examples/panel/panel-leaves-v1.jpg
```

---

## 4. Layout Tuzilmasi

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR (fixed left, 240px)                                │
├─────────────────────────────────────────────────────────────┤
│  TOPBAR (sticky, 64px)                                      │
├─────────────────────────────────────────────────────────────┤
│  MAIN CONTENT                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Page Header: "My Leaves"   [Request Leave button]  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │Annual  │ │ Sick   │ │Unpaid  │ │  Used  │               │
│  │Balance │ │Balance │ │Balance │ │ This Yr│               │
│  └────────┘ └────────┘ └────────┘ └────────┘               │
│  ┌─────────────────────────────┐ ┌────────────────────────┐ │
│  │  My Leave Requests Table    │ │  Leave Calendar (mini) │ │
│  │  [Type][From][To][Days]     │ │                        │ │
│  │  [Status][Action]           │ │                        │ │
│  │  Pagination                 │ │                        │ │
│  └─────────────────────────────┘ └────────────────────────┘ │
│                                                              │
│  [Request Leave Modal/Drawer]                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Komponentlar Ro'yxati

### 5.1 Page Header

```tsx
<div className="flex items-center justify-between">
  <PageHeader title="My Leaves" subtitle="Manage your leave requests" />
  <Button onClick={() => setIsModalOpen(true)} icon={Plus}>
    Request Leave
  </Button>
</div>
```

---

### 5.2 Leave Balance Cards (4 ta)

| # | Title | Qiymat | Icon | Color |
|---|-------|--------|------|-------|
| 1 | Annual Leave | "12 days remaining" | `Sun` | Blue |
| 2 | Sick Leave | "5 days remaining" | `HeartPulse` | Red |
| 3 | Unpaid Leave | "Unlimited" | `Banknote` | Gray |
| 4 | Used This Year | "8 days" | `CalendarMinus` | Orange |

```tsx
<LeaveBalanceCard
  title="Annual Leave"
  remaining={12}
  total={20}
  used={8}
  icon={SunIcon}
  accentColor="blue"
  loading={isLoading}
/>
```

**Progress bar** (optional): used/total ratio
```tsx
<div className="mt-3">
  <div className="flex justify-between text-xs text-gray-500 mb-1">
    <span>{used} used</span>
    <span>{total} total</span>
  </div>
  <div className="h-1.5 bg-gray-100 rounded-full">
    <div
      className="h-1.5 bg-blue-500 rounded-full"
      style={{ width: `${(used / total) * 100}%` }}
    />
  </div>
</div>
```

---

### 5.3 My Leave Requests Table

```tsx
<LeaveRequestsTable
  leaves={leaves}
  loading={isLoadingLeaves}
  onCancel={handleCancelLeave}
  pagination={pagination}
  onPageChange={handlePageChange}
/>
```

**Columns:**

| Column | Type | Misol |
|--------|------|-------|
| Type | Badge | `Annual / Sick / Unpaid` |
| From | `MMM d, yyyy` | "Aug 10, 2026" |
| To | `MMM d, yyyy` | "Aug 12, 2026" |
| Days | number | "3 days" |
| Status | Colored Badge | `Pending / Approved / Rejected` |
| Action | Button | "Cancel" (faqat Pending) |

**Status badges:**
```
pending  → bg-yellow-100 text-yellow-800
approved → bg-green-100 text-green-800
rejected → bg-red-100 text-red-800
```

**Leave type badges:**
```
annual → bg-blue-100 text-blue-800
sick   → bg-red-100 text-red-800
unpaid → bg-gray-100 text-gray-700
```

**Cancel action:**
```tsx
// Faqat "pending" statusdagi leavelarda "Cancel" tugmasi ko'rinadi
{leave.status === 'pending' && (
  <Button
    variant="ghost"
    size="sm"
    className="text-red-600 hover:text-red-700"
    onClick={() => handleCancelLeave(leave.id)}
  >
    Cancel
  </Button>
)}
```

**Cancel confirmation dialog:**
```tsx
<ConfirmDialog
  isOpen={confirmDialogOpen}
  title="Cancel Leave Request"
  description="Are you sure you want to cancel this leave request? This action cannot be undone."
  onConfirm={confirmCancel}
  onClose={() => setConfirmDialogOpen(false)}
  confirmLabel="Yes, Cancel"
  confirmVariant="destructive"
/>
```

---

### 5.4 Leave Calendar (Mini)

```tsx
<LeaveCalendarMini
  month={currentMonth}
  leaves={approvedLeaves}
  loading={isLoadingCalendar}
/>
```

- Faqat approved ta'tillar ko'rsatiladi (rangli)
- Har bir ta'til kuni: `bg-blue-200` (annual), `bg-red-200` (sick), `bg-gray-200` (unpaid)
- Kichik format: mini-calendar (desktop o'ng tomonda)
- Mobile da yashirin yoki table ostida to'liq ko'rinadi

---

### 5.5 Request Leave Modal

```tsx
<RequestLeaveModal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  onSubmit={handleSubmitLeave}
  isSubmitting={isSubmitting}
  formErrors={formErrors}
/>
```

**Modal tarkibi:**

```
┌─────────────────────────────────────────┐
│  Request Leave              [X]          │
├─────────────────────────────────────────┤
│                                          │
│  Leave Type *                            │
│  [Annual Leave        ▼]                │
│                                          │
│  From Date *          To Date *          │
│  [2026-08-10 ▼]      [2026-08-12 ▼]   │
│                                          │
│  Duration: 3 working days                │
│                                          │
│  Reason *                                │
│  ┌──────────────────────────────────┐    │
│  │ Family event...                  │    │
│  └──────────────────────────────────┘    │
│  Min 10, max 500 characters              │
│                                          │
│  [Cancel]              [Submit Request]  │
└─────────────────────────────────────────┘
```

**Form fields:**
```ts
interface LeaveRequestForm {
  type:     'annual' | 'sick' | 'unpaid';
  fromDate: string;   // "YYYY-MM-DD"
  toDate:   string;   // "YYYY-MM-DD"
  reason:   string;   // min 10, max 500 chars
}
```

**Form validation:**
```ts
// react-hook-form + zod schema
const leaveSchema = z.object({
  type: z.enum(['annual', 'sick', 'unpaid'], {
    required_error: 'Please select leave type'
  }),
  fromDate: z.string().min(1, 'From date is required'),
  toDate: z.string().min(1, 'To date is required'),
  reason: z.string()
    .min(10, 'Reason must be at least 10 characters')
    .max(500, 'Reason must not exceed 500 characters'),
}).refine(data => data.toDate >= data.fromDate, {
  message: 'End date must be after start date',
  path: ['toDate']
})
```

**Duration hisoblash (real-time):**
```ts
// fromDate va toDate o'zgarganda avtomatik hisobla
const duration = differenceInBusinessDays(
  parseISO(toDate),
  parseISO(fromDate)
) + 1
```

---

## 6. Style (Ranglar, Tipografiya, Spacing)

### Ranglar
```
Page bg:             bg-gray-50
Card bg:             bg-white
Border:              border-gray-200
Modal overlay:       bg-black/50
Modal bg:            bg-white
Modal shadow:        shadow-xl

Leave type Annual:   bg-blue-100 text-blue-800
Leave type Sick:     bg-red-100 text-red-800
Leave type Unpaid:   bg-gray-100 text-gray-700

Status Pending:      bg-yellow-100 text-yellow-800
Status Approved:     bg-green-100 text-green-800
Status Rejected:     bg-red-100 text-red-800

Request button:      bg-blue-600 hover:bg-blue-700 text-white
Cancel action:       text-red-600 hover:text-red-700
```

### Tipografiya
```
Page title:          text-2xl font-bold text-gray-900
Card value:          text-2xl font-bold text-gray-900
Card subtitle:       text-sm text-gray-500
Table header:        text-xs font-semibold text-gray-500 uppercase
Table cell:          text-sm text-gray-700
Modal title:         text-lg font-semibold text-gray-900
Form label:          text-sm font-medium text-gray-700
Form error:          text-xs text-red-500 mt-1
```

### Spacing
```
Page padding:        p-6
Card padding:        p-5
Gap between cards:   gap-4
Modal padding:       p-6
Form field gap:      space-y-4
```

---

## 7. States

### 7.1 Loading State
- Balance cards: 4 ta skeleton
- Table: 5 ta row skeleton
- Calendar: mini skeleton grid

### 7.2 Empty State (no leaves)
```tsx
<EmptyState
  icon={CalendarOff}
  title="No leave requests yet"
  description="You haven't submitted any leave requests."
  action={
    <Button onClick={() => setIsModalOpen(true)}>
      Request Your First Leave
    </Button>
  }
/>
```

### 7.3 Form Validation Errors
```tsx
// Har bir field ostida xato xabari
{errors.type && (
  <p className="text-xs text-red-500 mt-1">{errors.type.message}</p>
)}
```

### 7.4 Submitting State
```tsx
<Button disabled={isSubmitting}>
  {isSubmitting ? <Spinner size="sm" /> : null}
  {isSubmitting ? 'Submitting...' : 'Submit Request'}
</Button>
```

### 7.5 Success State
- Modal yopiladi
- Toast: "Leave request submitted successfully!"
- Table refresh (invalidate query)

### 7.6 Cancel Confirmation State
- Confirm dialog ochiladi
- "Yes, Cancel" bosilganda: API call, loading, toast, refresh

---

## 8. Animatsiyalar

```
Modal open:       scale-95→100 opacity 0→1, 200ms ease-out
Modal close:      scale-100→95 opacity 1→0, 150ms ease-in
Overlay:          opacity 0→0.5, 200ms
Cancel confirm:   shake animation (optional, 300ms)
Toast:            slide-in + fade-out
Form errors:      fade-in (150ms) when validation triggers
```

---

## 9. Responsive

| Breakpoint | Layout |
|-----------|--------|
| `< 640px` | Balance cards: 2x2. Table: horizontal scroll. Calendar: hidden yoki below table. Modal: full-screen drawer. |
| `640px–1024px` | Balance cards: 4 col. Right layout: stacked. |
| `>= 1024px` | Full two-column layout (table + mini calendar). |

```tsx
// Balance cards
<div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

// Table + Calendar layout
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div className="lg:col-span-2"> {/* Table */} </div>
  <div className="lg:col-span-1"> {/* Mini Calendar */} </div>
</div>

// Modal on mobile: drawer from bottom
<Dialog className="sm:max-w-lg w-full fixed bottom-0 sm:relative sm:bottom-auto">
```

---

## 10. API Endpointlar

### 10.1 Get All Leaves
```
GET /api/v1/employee-leaves
Authorization: Bearer {token}

Query params:
  page:   number  1
  limit:  number  20

Response 200:
{
  data: [
    {
      id:         string,
      type:       "annual" | "sick" | "unpaid",
      fromDate:   "2026-08-10",
      toDate:     "2026-08-12",
      days:       3,
      status:     "pending" | "approved" | "rejected",
      reason:     string,
      createdAt:  string,
      updatedAt:  string
    }
  ],
  total:      number,
  page:       number,
  limit:      number,
  totalPages: number
}
```

**Leave balance aggregate (agar backend taqdim etsa):**
```
Response ichida yoki alohida endpoint:
{
  annual:  { total: 20, used: 8, remaining: 12 },
  sick:    { total: 10, used: 5, remaining: 5 },
  unpaid:  { total: null, used: 3, remaining: null }
}
```

---

### 10.2 Create Leave Request
```
POST /api/v1/employee-leaves
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  type:     "annual",
  fromDate: "2026-08-10",
  toDate:   "2026-08-12",
  reason:   "Family vacation"
}

Response 201:
{
  id:       string,
  type:     "annual",
  fromDate: "2026-08-10",
  toDate:   "2026-08-12",
  days:     3,
  status:   "pending",
  reason:   "Family vacation",
  createdAt: string
}

Errors:
  400 - Insufficient leave balance
  422 - Validation error
  409 - Overlapping leave request
```

---

### 10.3 Cancel Leave Request
```
DELETE /api/v1/employee-leaves/:id
Authorization: Bearer {token}

Condition: faqat status === "pending" bo'lganida

Response 200:
{
  message: "Leave request cancelled successfully"
}

Errors:
  404 - Leave not found
  403 - Cannot cancel approved/rejected leaves
```

Ref: `orcestor/project_docs/api/employee-leave.md`

---

## 11. Global State (Zustand)

### `useLeaveStore`
```ts
interface LeaveStore {
  // Data
  leaves:       Leave[];
  total:        number;
  leaveBalance: LeaveBalance | null;

  // Loading/Error
  isLoading:    boolean;
  isSubmitting: boolean;
  isCancelling: string | null;  // leave id (cancelling qaysi)
  error:        string | null;

  // Modal state
  isModalOpen:  boolean;
  formErrors:   Record<string, string>;

  // Actions
  fetchLeaves:       (params?: { page?: number; limit?: number }) => Promise<void>;
  submitLeaveRequest: (data: LeaveRequestForm) => Promise<void>;
  cancelLeave:       (id: string) => Promise<void>;
  openModal:         () => void;
  closeModal:        () => void;
}
```

---

## 12. Muhim Eslatmalar

1. **Balance kalkulyatsiya:** Agar backend `leaveBalance` endpointi taqdim etmasa, frontend `leaves` dan hisoblashi mumkin:
   ```ts
   const usedAnnual = leaves.filter(l =>
     l.type === 'annual' && l.status === 'approved'
   ).reduce((acc, l) => acc + l.days, 0)
   ```

2. **Date validation:** `fromDate` dan oldingi sanaga ta'til so'rash oldini olish:
   ```ts
   fromDate min: format(new Date(), 'yyyy-MM-dd')
   ```

3. **Weekend/holiday filter:** Duration hisoblaganda faqat ish kunlarini hisoblash (backend da yoki `date-fns/differenceInBusinessDays`).

4. **Optimistic update (ixtiyoriy):** Cancel bosilganda UI da darhol o'chirib, API xato bo'lsa rollback qilish UX ni yaxshilaydi.

5. **Modal reset:** Modal yopilganda form state tozalanishi kerak:
   ```ts
   onClose={() => {
     reset()           // react-hook-form
     setIsModalOpen(false)
   }}
   ```

6. **Confirm before cancel:** Delete action uchun har doim confirm dialog ko'rsating, tasodifiy o'chirishni oldini olish uchun.

7. **Table sort:** `createdAt:desc` default sort (eng yangi tepada).

8. **Leave type display names:**
   ```ts
   const leaveTypeLabels = {
     annual: 'Annual Leave',
     sick:   'Sick Leave',
     unpaid: 'Unpaid Leave'
   }
   ```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/profile.md`

# Profile Page Specification

## 1. Maqsad
Xodimning o'z ma'lumotlarini (shaxsiy va ishga oid), hujjatlarini ko'rishi, ish jadvali statistikasini kuzatishi, tahrirlashi hamda xavfsizlik (parolni o'zgartirish) sozlamalarini boshqarishi uchun markaziy sahifa.

## 2. Route
`/profile`

## 3. Mockup reference
`orcestor/examples/panel/panel-profile-v1.jpg`

## 4. Layout tuzilmasi
- **Ikki ustunli (Split) dizayn (Desktop uchun):**
  - **Chap ustun (Left Column - 1/3 qism):** 
    - Asosiy Profile Card (Avatar, ism, lavozim, bo'lim, filial, employee no, contact info) va "Edit Profile" tugmasi.
    - Security Card (Change Password tugmasi va Active Sessions ko'rinishi).
  - **O'ng ustun (Right Column - 2/3 qism):** 
    - Tablar bilan bo'lingan ma'lumotlar hududi (Personal Info | Work Info | Documents).

## 5. Komponentlar ro'yxati
- **Left Column:**
  - `ProfileOverviewCard`: Avatar yuklash imkoni, user qisqacha bio va roliga tegishli informatsiyalar.
  - `SecurityCard`: Parol o'zgartirish va faol qurilmalar ro'yxati.
- **Right Column Tabs:**
  - `Tabs` orqali quyidagi seksiyalarga o'tiladi:
    - `PersonalInfoTab`: Faqat o'qish uchun (read-only) grid form ko'rinishidagi ma'lumotlar (firstName, lastName, middleName, dob, phone, email, address, passport).
    - `WorkInfoTab`: Work Schedule (ish kunlari chiplari, vaqtlari), Quick stats (attendance, leave balance, last payroll).
    - `DocumentsTab`: Yuklangan va saqlanayotgan hujjatlar ro'yxati.
- **Modals:**
  - `EditProfileModal`: Formani tahrirlash (update) hududi.
  - `ChangePasswordModal`: Parol almashtirish formasi (oldPassword, newPassword, confirmPassword).

## 6. Style (ranglar, tipografiya, spacing)
- **Ranglar:** Avatar atrofi border (masalan statusga qarab: Active). Asosiy linklar/tahrir tugmalari Primary rangda. Parolni yangilashdagi warning/error xabarlar tegishli rangda.
- **Tipografiya:** Ma'lumot nomlari (Label) ochiqroq kulrang, ma'lumotning o'zi (Value) qoramtir va aniq yoziladi.
- **Spacing:** Chap va o'ng ustunlar orasida (gap-6 yoki gap-8). Form elementlari orasida 16px (gap-4).

## 7. States (loading, error, empty, success)
- **Loading:** Butun sahifa ma'lumotlari API dan kelgunicha Skeleton cardlar.
- **Form States (Modals):** `isEditing`, `isChangingPassword`, `formErrors` (validatsiya xatolari chiqqanda form tagida qizil tekst).
- **Success:** Parol yoki profil o'zgartirilganda "Toast notification" chiqadi (Success holati).

## 8. Animatsiyalar
- Tablar almashinishida cross-fade animatsiyasi.
- Modal ochilishi va yopilishi uchun yengil scale/opacity animatsiyasi (Dialog komponentiga kiritilgan standart).
- Ma'lumot yangilanganda (Save bosilganda) tugmada loading spinner.

## 9. Responsive
- **Mobile (sm):** Ustunlar ustma-ust tushadi. Avval Profile Overview va Security Card, keyin Tablar keladi. Modal to'liq ekranni (fullscreen) egallashi mumkin.
- **Tablet (md):** Xuddi shunday ustma-ust (1-column), lekin kartalar kattaroq padding va chetlari (margin) qisqarishi mumkin.
- **Desktop (lg, xl):** Izohlangandek Chap (1/3) va O'ng (2/3) grid strukturada joylashadi.

## 10. API endpointlar
- `GET /api/v1/auth/me` — Joriy user (o'zining) to'liq ma'lumotlarini olish.
- `PATCH /api/v1/users/me` — Profil ma'lumotlarini yangilash.
- `PATCH /api/v1/users/change-password` — Parolni almashtirish.
- `GET /api/v1/work-schedules/:id` — Foydalanuvchiga biriktirilgan work schedule tafsilotlarini olish.

**API docs:** `orcestor/project_docs/api/user.md`, `orcestor/project_docs/api/work-schedule.md`, `orcestor/project_docs/api/auth.md`

## 11. Global state (Zustand)
- `useAuthStore`: Yangilangan foydalanuvchi ma'lumotlarini dasturning boshqa joylarida (masalan Headerdagi avatar/ism) yangilanishi uchun, `updateUser` orqali store yangilanadi.

## 12. Muhim eslatmalar
- Modallarda form validatsiyasi Client side (Zod + React Hook Form) orqali yozilishi kerak. Server side errorlar (masalan "Old password incorrect") to'g'ri ushlanib, form tagida ko'rsatilishi kerak.
- Parolni almashtirganda, token invalidation kerak emas (agar API dan majburiy chiqarib yuborish ko'zda tutilmagan bo'lsa), lekin foydalanuvchini xabardor qilib Toast yuboriladi.
- Read-only form grid o'zgaruvchilar bo'sh (null) kelsa, o'rniga "N/A" yoki chiziqcha "-" qo'yilishi UX ni oshiradi.


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_13.md`

# Step 13: Departments Page Star Admin Redesign & Signal State Fix

## 📅 Bajarilgan Ishlar:

1. **`DepartmentList` Signal State Fix (`department-list.ts`)**:
   - `departments: Department[]` oddiy o'zgaruvchisi `departments = signal<Department[]>([])` o'tkazildi, shunda `ChangeDetectionStrategy.OnPush` bo'lgan komponentda ma'lumotlar kelgan zahoti darhol ekranga chiziladi.

2. **Star Admin 2 Redesign (`department-list.html` & `department-list.css`)**:
   - Oddiy HTML jadval o'rniga **Page Header Banner Card** (Sarlavha, SVG Ikonka, Subtitle va Gradient "Yangi Bo'lim" tugmasi) o'rnatildi.
   - **Modern Table**: Bo'limlar har biri uchun maxsus avatar harf badge'lari (`dept-avatar`), monospaced GUID badge'lari (`id-badge`) hamda hover interaktivliklari berildi.
   - **Modern Actions**: Tahrirlash hamda O'chirish tugmalariga translyutsiya effektli premium gradient va glass-borders berildi.
   - Bo'limlar mavjud bo'lmagan holat uchun chiroyli **Empty State** paneli tayyorlandi.


## Manba: `zdes_archive_docs/raw_history/review/tasks/step_8.md`

# Step 8: Star Admin Modern Redesign & User Profile Modal Implementation

## 📅 Bajarilgan Ishlar:

1. **Subagentlar Orkestratsiyasi**:
   - `Sidebar UI Designer Agent` va `Header & Profile Logic Agent` subagentlari chaqirilib, vizual va mantiqiy vazifalar taqsimlandi.

2. **Sidebar Star Admin 2 Redesign (`sidebar.html`, `sidebar.css`)**:
   - Har bir menyu bo'limiga (Dashboard, Employees, Branches, Departments, Positions, Attendance, Terminals, Payroll, Leaves, Settings) individual vektor SVG ikonkalari qo'shildi.
   - Sidebar menyu tugmalariga (`.nav-link`) gradient fon (`linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)`) hamda modern glasmorfik active/hover stil berildi.
   - Sidebar scrollbar-i zamonaviy 5px slim custom scrollbar'ga o'tkazildi.

3. **User Profile & Avatar Button (`header.html`, `header.css`)**:
   - ID o'rniga foydalanuvchining to'liq ismi (`firstName` / `lastName` yoki `login`) ko'rsatilishi yo'lga qo'yildi.
   - Headerda avatar circle (bosh harf bilan boyitilgan) va profile tugmasi hamda zamonaviy Chiqish tugmasi o'rnatildi.

4. **Profile Modal & Edit Profile Component (`ProfileModal`)**:
   - `ProfileModal` standalone Angular komponenti yaratildi ([profile-modal.ts](file:///home/fayzillo/Desktop/zdes/test-zdes-front/src/app/shared/components/profile-modal/profile-modal.ts), `profile-modal.html`, `profile-modal.css`).
   - Modal Star Admin dizaynida tayyorlandi. Foydalanuvchi ma'lumotlarini ko'rish (Login, Ism, Familiya, Email, Rol) hamda **Profilni Tahrirlash** (`PATCH /users/me`) imkoniyati qo'shildi.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/landing/landing.md`

# Landing (Home) Page Specification

## 1. Maqsad

Mahsulotning asosiy kirish sahifasi. Foydalanuvchiga mahsulot haqida birinchi taassurot berish, asosiy afzalliklarni ko'rsatish va "Get Started" yoki "Watch Demo" orqali keyingi harakatga undash. Hech qanday autentifikatsiya talab qilinmaydi — to'liq statik sahifa.

---

## 2. Route

```
/          ← primary route
/home      ← alias (redirect to /)
```

---

## 3. Mockup reference

```
orcestor/examples/landing/landing-page-v1.jpg
```

> Mockupda quyidagilar ko'rsatilgan: Navbar yuqorida, Hero section markazda, Stats row, Features cards pastda.

---

## 4. Layout tuzilmasi

```
<RootLayout>
  └── <LandingLayout>
        ├── <Navbar />                  ← sticky top, z-50
        ├── <main>
        │     ├── <HeroSection />       ← full viewport height (min-h-screen)
        │     ├── <StatsRow />          ← 4-column grid
        │     └── <FeaturesSection />   ← 3-column cards grid
        └── <Footer />                  ← (minimal: links + copyright)
```

**Page wrapper:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

---

## 5. Komponentlar ro'yxati

### 5.1 `<Navbar />`

| Element              | Tavsif                                                       |
|----------------------|--------------------------------------------------------------|
| Logo                 | SVG yoki `<img>` — chapda, `/` ga link                       |
| Nav links            | Features `/features`, Pricing `/pricing`, About `/about`     |
| Login tugmasi        | Ghost/outline variant → `/sign-in`                           |
| Get Started tugmasi  | Primary (filled) variant → `/sign-in`                        |
| Sticky behavior      | `position: sticky; top: 0` + backdrop blur `backdrop-blur-md bg-white/80` |
| Mobile               | Hamburger menyu (responsive)                                 |

```tsx
// props type
interface NavbarProps {
  transparent?: boolean; // hero ustida shaffof holat
}
```

---

### 5.2 `<HeroSection />`

| Element      | Tavsif                                                           |
|--------------|------------------------------------------------------------------|
| Headline     | `"Streamline Your Workforce Management"` — H1, bold             |
| Subtitle     | `"All-in-one employee management platform for modern teams"` — muted text |
| CTA tugmalar | "Get Started" (primary) + "Watch Demo" (ghost/outline)          |
| Background   | Gradient: `from-indigo-50 via-white to-purple-50` yoki SVG pattern |
| Illustration | O'ng tomonda hero image/illustration (optional)                 |
| Layout       | 2-column grid (text chap, illustration o'ng) yoki centered single-column |

**CTA xatti-harakati:**

```
"Get Started"  → navigate('/sign-in')
"Watch Demo"   → openDemoModal()   // local useState bilan modal ochiladi
```

---

### 5.3 `<StatsRow />`

4 ta statistik karta, horizontal row:

| #  | Label              | Value        | Icon         |
|----|--------------------|--------------|--------------|
| 1  | Companies          | 50+          | `Building2`  |
| 2  | Employees Managed  | 10,000+      | `Users`      |
| 3  | Countries          | 12+          | `Globe`      |
| 4  | Uptime             | 99.9%        | `Activity`   |

```tsx
const STATS = [
  { label: 'Companies',          value: '50+',     icon: Building2 },
  { label: 'Employees Managed',  value: '10,000+', icon: Users     },
  { label: 'Countries',          value: '12+',     icon: Globe     },
  { label: 'Uptime',             value: '99.9%',   icon: Activity  },
];
```

Layout: `grid grid-cols-2 md:grid-cols-4 gap-6`

---

### 5.4 `<FeaturesSection />`

3 ta feature karta:

| #  | Title            | Description                                  | Icon           |
|----|------------------|----------------------------------------------|----------------|
| 1  | Smart Attendance | Automated time tracking with biometric support | `Clock`       |
| 2  | Leave Management | Streamlined leave requests and approvals      | `Calendar`     |
| 3  | Payroll Ready    | Integrated payroll with tax calculations      | `DollarSign`   |

Layout: `grid grid-cols-1 md:grid-cols-3 gap-8`

Section heading: `"Everything you need to manage your team"` (H2, centered)

---

### 5.5 `<DemoModal />`

| Element    | Tavsif                                          |
|------------|-------------------------------------------------|
| Trigger    | "Watch Demo" CTA tugmasi                        |
| Content    | `<iframe>` yoki placeholder video embed         |
| Close      | ESC tugmasi + overlay click + X button          |
| State      | `isDemoOpen: boolean` (local useState)          |
| Backdrop   | `bg-black/60 backdrop-blur-sm`                  |

```tsx
const [isDemoOpen, setIsDemoOpen] = useState(false);
```

---

## 6. Style (ranglar, tipografiya, spacing)

### Ranglar

```css
/* Primary brand */
--color-primary:       #6366f1;   /* indigo-500 */
--color-primary-dark:  #4f46e5;   /* indigo-600 */
--color-primary-light: #e0e7ff;   /* indigo-100 */

/* Neutral */
--color-text-primary:  #111827;   /* gray-900 */
--color-text-muted:    #6b7280;   /* gray-500 */
--color-bg:            #ffffff;
--color-bg-section:    #f9fafb;   /* gray-50 */

/* Accent */
--color-accent:        #8b5cf6;   /* violet-500 */
```

### Tipografiya

| Element      | Font              | Size        | Weight |
|--------------|-------------------|-------------|--------|
| H1 (Hero)    | Inter / system-ui | 4xl–6xl     | 700    |
| H2 (Section) | Inter / system-ui | 2xl–3xl     | 700    |
| Body         | Inter / system-ui | base (16px) | 400    |
| Subtitle     | Inter / system-ui | lg–xl       | 400    |
| Stats value  | Inter / system-ui | 3xl         | 700    |
| Stats label  | Inter / system-ui | sm          | 500    |

### Spacing

- Section padding: `py-24` (96px top/bottom)
- Card gap: `gap-6` to `gap-8`
- Container: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

### Shadows / Borders

- Card: `rounded-2xl shadow-md hover:shadow-xl transition-shadow`
- Navbar: `border-b border-gray-100` (scrolled holda)

---

## 7. States

| State           | Tavsif                                                          |
|-----------------|-----------------------------------------------------------------|
| Default         | To'liq statik render — loading yo'q                            |
| Loading         | Yo'q (statik sahifa, SSG/SSR ham bo'lishi mumkin)              |
| Error           | Yo'q (API chaqiruv yo'q)                                       |
| Modal open      | DemoModal ochiq — scroll lock `overflow-hidden` body-ga        |
| Mobile menu open| Hamburger menu toggled — nav links pastga tushadi              |

---

## 8. Animatsiyalar

### Hero Fade-in

```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-headline { animation: fadeInUp 0.6s ease forwards; }
.hero-subtitle { animation: fadeInUp 0.6s ease 0.15s forwards; opacity: 0; }
.hero-cta      { animation: fadeInUp 0.6s ease 0.3s  forwards; opacity: 0; }
```

**Framer Motion varianti:**

```tsx
<motion.h1
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6 }}
>
```

### Scroll Reveal (Features Section)

```tsx
<motion.div
  initial={{ opacity: 0, y: 32 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.2 }}
  transition={{ duration: 0.5, delay: index * 0.1 }}
>
```

### Stats Counter Animation

- Sahifa ko'rinishga kelganda raqamlar 0 dan target qiymatgacha animatsiya (optional)
- Library: `react-countup` yoki custom `useCountUp` hook

---

## 9. Responsive

| Breakpoint      | Xatti-harakat                                                    |
|-----------------|------------------------------------------------------------------|
| `xs` (<640px)   | Navbar hamburger menyu; Hero — single column; Stats 2×2 grid    |
| `sm` (640px+)   | Stats 2×2 → 4×1; Features 1-column                             |
| `md` (768px+)   | Features 3-column grid; Hero 2-column                           |
| `lg` (1024px+)  | Full desktop layout                                              |
| `xl` (1280px+)  | Max-width container clamps, centering                            |

**Mobile-specific:**

- Navbar: hamburger icon (Lucide `Menu`), click → fullscreen yoki dropdown overlay
- Hero CTA tugmalar: `flex-col w-full` → `flex-row` md da
- Feature cards: horizontal stack → vertical scroll

---

## 10. API endpointlar

```
Hech qanday API chaqiruv yo'q — sahifa to'liq statik.
```

---

## 11. Global state (Zustand)

```
Landing sahifasida global state ishlatilmaydi.
```

Local state:

```tsx
const [isDemoOpen, setIsDemoOpen]           = useState(false);
const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);
```

---

## 12. Muhim eslatmalar

1. **SEO:** `<title>`, `<meta description>`, Open Graph teglari o'rnatilsin (TanStack Head yoki `next/head`).
2. **Performance:** Hero image `loading="eager"`, qolgan rasmlar `loading="lazy"`.
3. **Accessibility:** CTA tugmalarda `aria-label`, modal-da focus trap, ESC-close.
4. **Route guard:** Bu sahifaga autentifikatsiya kerak emas — route guard qo'yilmasin.
5. **Demo Modal content:** Hozircha placeholder — keyinchalik `<iframe src="...">` bilan almashtiriladi.
6. **Navbar scroll behavior:** `scrollY > 10` bo'lganda `bg-white/80 backdrop-blur-md shadow-sm` klasslar qo'shilsin.
7. **CTA linking:** "Get Started" va "Login" har ikkisi `/sign-in`-ga link qilsin — dashboard redirect sign-in ichida hal qilinadi.


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/panel/dashboard.md`

# Dashboard Page Specification

## 1. Maqsad

Dashboard — xodim uchun asosiy kirish sahifasi. Bir qarashda bugungi holat, oylik davomat, ta'til balansi, maosh va oxirgi faoliyatni ko'rsatadi. Foydalanuvchi bu sahifadan Check In/Out qilishi, tezkor ma'lumot olishi va boshqa bo'limlarga o'tishi mumkin.

---

## 2. Route

```
/dashboard
```

Protected route. Autentifikatsiya talab qilinadi. Agar token yo'q yoki muddati tugagan bo'lsa → `/login` ga redirect.

---

## 3. Mockup Reference

```
orcestor/examples/panel/employee-panel-v1.jpg
```

---

## 4. Layout Tuzilmasi

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR (fixed left, 240px)                                │
├─────────────────────────────────────────────────────────────┤
│  TOPBAR (sticky, height: 64px)                              │
├─────────────────────────────────────────────────────────────┤
│  MAIN CONTENT (scroll)                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Welcome Banner + Check In/Out Button                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐               │
│  │ Stat 1 │ │ Stat 2 │ │ Stat 3 │ │ Stat 4 │               │
│  └────────┘ └────────┘ └────────┘ └────────┘               │
│  ┌──────────────────────┐  ┌─────────────────────────────┐  │
│  │  Attendance Calendar │  │  Recent Activity            │  │
│  └──────────────────────┘  └─────────────────────────────┘  │
│  ┌──────────────────────┐  ┌─────────────────────────────┐  │
│  │  My Leaves (mini)    │  │  Latest Payslip             │  │
│  └──────────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

- Sidebar: fixed, 240px
- Content area: `ml-[240px]` yoki sidebar state ga qarab
- Padding: `p-6` (24px)
- Grid system: Tailwind `grid grid-cols-4 gap-4` (stat kartalar uchun), `grid grid-cols-2 gap-6` (quyi bloklar)

---

## 5. Komponentlar Ro'yxati

### 5.1 Welcome Banner

```tsx
<WelcomeBanner
  name={user.firstName}
  date={today}          // "Saturday, August 23, 2026"
  checkInStatus={checkInStatus}   // 'not_started' | 'checked_in' | 'checked_out'
  onCheckIn={handleCheckIn}
  onCheckOut={handleCheckOut}
  isLoading={isCheckingIn}
/>
```

**Tarkib:**
- Katta sarlavha: `"Good morning, {firstName}! 👋"` (vaqtga qarab: Good morning/afternoon/evening)
- Kichik matn: bugungi sanani `EEEE, MMMM d, yyyy` formatida (`date-fns` bilan)
- O'ng tomonda: **Check In / Check Out** tugmasi

**Check In/Out tugma logikasi:**
```
if (todaySession === null || todaySession === undefined):
  → "Check In" (green button, icon: LogIn)
else if (todaySession.checkIn && !todaySession.checkOut):
  → "Check Out" (red/orange button, icon: LogOut)
else if (todaySession.checkIn && todaySession.checkOut):
  → Disabled button yoki "Completed" badge
```

**Check In API call:**
```ts
POST /api/v1/attendance/self/check-in
// body: FormData (notes, file optional)
// success → sessiyani refresh qil
```

**Check Out API call:**
```ts
POST /api/v1/attendance/self/check-out
// success → sessiyani refresh qil
```

---

### 5.2 Stat Cards (4 ta)

Har bir karta: `<StatCard />` komponenti

| # | Title | Value misoli | Icon | Color accent |
|---|-------|-------------|------|-------------|
| 1 | This Month Attendance | "18 / 22 days" | `CalendarCheck` | Blue |
| 2 | Late Arrivals | "3 times" | `Clock` | Orange |
| 3 | Leave Balance | "12 days" | `Umbrella` | Green |
| 4 | Net Salary | "$2,450.00" | `DollarSign` | Purple |

```tsx
<StatCard
  title="This Month Attendance"
  value="18 / 22"
  unit="days"
  icon={CalendarCheckIcon}
  accentColor="blue"
  loading={isLoading}
/>
```

---

### 5.3 Attendance Calendar

```tsx
<AttendanceCalendar
  month={currentMonth}   // { year: 2026, month: 8 }
  sessions={attendanceSessions}
  loading={isLoadingCalendar}
/>
```

**Color coding:**
```
present  → bg-green-100, border-green-400, dot: green
late     → bg-orange-100, border-orange-400, dot: orange
absent   → bg-red-100, border-red-400, dot: red
weekend  → bg-gray-50, text-gray-400
holiday  → bg-purple-50, text-purple-400
today    → ring-2 ring-blue-500
```

**Funksional:**
- Faqat joriy oy ko'rsatiladi (Dashboard uchun navigatsiya yo'q)
- Har bir kun ustiga hover → tooltip: "Check in: 09:05, Check out: 18:02, Worked: 8h 57m"
- Legend pastda: Present | Late | Absent | Weekend

---

### 5.4 Recent Activity List

```tsx
<RecentActivityList
  activities={recentSessions}  // ohirgi 5 ta session
  loading={isLoadingActivity}
/>
```

**Har bir item:**
```
[icon] [date]          [action]     [time]
       Aug 22, 2026    Checked In   09:05 AM
       Aug 22, 2026    Checked Out  18:02 PM
```

- Icon: `LogIn` (green) yoki `LogOut` (orange)
- Date: `MMM d, yyyy`
- Time: `hh:mm a`
- Max 5 ta yozuv
- "View all" link → `/attendance`

---

### 5.5 My Leaves Mini Table

```tsx
<MyLeavesTable
  leaves={recentLeaves}   // ohirgi 3 ta leave request
  loading={isLoadingLeaves}
/>
```

**Columns:** Type | From | To | Days | Status

**Status badge:**
```
Pending  → yellow badge
Approved → green badge
Rejected → red badge
```

- "View all" link → `/leaves`

---

### 5.6 Latest Payslip Breakdown

```tsx
<LatestPayslip
  payslip={latestPayroll}
  loading={isLoadingPayroll}
/>
```

**Tarkib:**
```
Month: August 2026
Status: [Paid badge]

Base Salary:        $3,000.00
+ Bonus:            $  200.00
- Penalty:          $   50.00
- Advance:          $  700.00
─────────────────────────────
Net Salary:         $2,450.00

Paid Date: Aug 15, 2026
[Download PDF] button
```

- Download PDF: hozircha placeholder yoki `window.print()` fallback
- "View all payslips" link → `/payslips`

---

## 6. Style (Ranglar, Tipografiya, Spacing)

### Ranglar (Tailwind)
```
Background (page):   bg-gray-50 yoki bg-slate-50
Card background:     bg-white
Card border:         border border-gray-200
Card shadow:         shadow-sm hover:shadow-md (transition)
Text primary:        text-gray-900
Text secondary:      text-gray-500
Text muted:          text-gray-400
Accent blue:         text-blue-600 / bg-blue-50
Accent green:        text-green-600 / bg-green-50
Accent orange:       text-orange-500 / bg-orange-50
Accent purple:       text-purple-600 / bg-purple-50
Button Check In:     bg-green-600 hover:bg-green-700 text-white
Button Check Out:    bg-red-600 hover:bg-red-700 text-white
```

### Tipografiya
```
Welcome heading:  text-2xl font-bold text-gray-900
Date subtitle:    text-sm text-gray-500
Card title:       text-sm font-medium text-gray-500 uppercase tracking-wide
Card value:       text-2xl font-bold text-gray-900
Section heading:  text-lg font-semibold text-gray-800
Table header:     text-xs font-semibold text-gray-500 uppercase
Table cell:       text-sm text-gray-700
```

### Spacing
```
Page padding:    p-6 (24px all sides)
Card padding:    p-5 yoki p-6
Card gap:        gap-4 (stat cards), gap-6 (sections)
Section margin:  mt-6
```

---

## 7. States

### 7.1 Loading State
- Har bir karta uchun alohida **skeleton** loader:
```tsx
<Skeleton className="h-4 w-24 mb-2" />
<Skeleton className="h-8 w-16" />
```
- Calendar loading: `grid` skeleton (42 ta kichik to'rtburchak)
- List loading: 5 ta row skeleton

### 7.2 Error State
```tsx
<ErrorAlert
  message="Ma'lumotlarni yuklashda xato yuz berdi"
  onRetry={refetch}
/>
```
- Har bir bo'lim mustaqil error/retry ko'rsatadi
- Global error → toast notification

### 7.3 Empty State
- Recent activity bo'sh: "Bugun hech qanday faoliyat yo'q" + ikon
- Leaves bo'sh: "Ta'til so'rovlari yo'q" + `/leaves` ga link
- Payslip yo'q: "Maosh ma'lumotlari mavjud emas"

### 7.4 Success State
- Check In muvaffaqiyatli: green toast "Siz muvaffaqiyatli Check In qildingiz!"
- Check Out muvaffaqiyatli: orange toast "Siz muvaffaqiyatli Check Out qildingiz!"

---

## 8. Animatsiyalar

```
Card hover:        transition-shadow duration-200 ease-in-out
Check In button:   scale-95 active:scale-100 transition-transform
Skeleton pulse:    animate-pulse (Tailwind built-in)
Page mount:        fade-in (opacity 0→1, 300ms) yoki Framer Motion
                   initial={{ opacity:0, y:10 }} animate={{ opacity:1, y:0 }}
Toast:             slide-in-right (shadcn/ui Sonner yoki React Hot Toast)
Calendar day hover: bg transition 150ms
```

---

## 9. Responsive

| Breakpoint | Layout |
|-----------|--------|
| `< 768px` (mobile) | Sidebar hidden/drawer. 1 column layout. Stat cards: 2x2 grid. Calendar full width. |
| `768px–1024px` (tablet) | Sidebar collapsed (icon only). Stat cards: 2x2. Bottom sections: stack vertically. |
| `>= 1024px` (desktop) | Full sidebar. Stat cards: 4 column. Bottom: 2 column grid. |

```tsx
// Stat cards
<div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

// Bottom sections
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
```

---

## 10. API Endpointlar

### 10.1 Auth / User Info
```
GET /api/v1/auth/me
Authorization: Bearer {token}

Response:
{
  id: string,
  firstName: string,
  lastName: string,
  email: string,
  role: string,
  employeeId: string,
  department: { id, name },
  position: { id, name }
}
```
Ref: `orcestor/project_docs/api/auth.md`

---

### 10.2 Attendance Sessions (Calendar + Recent Activity)
```
GET /api/v1/attendance/self/sessions
Authorization: Bearer {token}
Query params:
  dateFrom: "2026-08-01"
  dateTo:   "2026-08-31"
  page:     1
  limit:    100   (calendar uchun ko'p)

Response:
{
  data: [
    {
      id: string,
      date: "2026-08-22",
      checkIn: "2026-08-22T09:05:00",
      checkOut: "2026-08-22T18:02:00",
      workedMinutes: 537,
      status: "present" | "late" | "absent",
      notes: string | null
    }
  ],
  total: number,
  page: number,
  limit: number
}
```

**Today session (Check In/Out logika uchun):**
```ts
const todaySession = sessions.find(s => s.date === format(today, 'yyyy-MM-dd'))
```
Ref: `orcestor/project_docs/api/attendance.md`

---

### 10.3 Check In
```
POST /api/v1/attendance/self/check-in
Authorization: Bearer {token}
Content-Type: multipart/form-data

Body:
  notes: string (optional)
  file:  File   (optional, image/document)

Response 201:
{
  id: string,
  checkIn: "2026-08-23T09:05:00",
  status: "present" | "late"
}
```

### 10.4 Check Out
```
POST /api/v1/attendance/self/check-out
Authorization: Bearer {token}

Response 200:
{
  id: string,
  checkOut: "2026-08-23T18:02:00",
  workedMinutes: 537
}
```

---

### 10.5 Employee Leaves
```
GET /api/v1/employee-leaves
Authorization: Bearer {token}
Query params:
  limit: 3  (dashboard uchun faqat 3 ta)
  page:  1

Response:
{
  data: [
    {
      id: string,
      type: "annual" | "sick" | "unpaid",
      fromDate: "2026-08-10",
      toDate:   "2026-08-12",
      days:     3,
      status:   "pending" | "approved" | "rejected",
      reason:   string
    }
  ],
  total: number
}
```
Ref: `orcestor/project_docs/api/employee-leave.md`

---

### 10.6 Payrolls (Latest Payslip)
```
GET /api/v1/payrolls
Authorization: Bearer {token}
Query params:
  employeeId: "me"
  limit:      1
  sort:       "month:desc"

Response:
{
  data: [
    {
      id: string,
      month: "2026-08",
      baseSalary:  3000,
      bonus:        200,
      penalty:       50,
      advance:      700,
      netSalary:   2450,
      status:      "paid" | "pending",
      paidDate:    "2026-08-15" | null
    }
  ]
}
```
Ref: `orcestor/project_docs/api/payroll.md`

---

## 11. Global State (Zustand)

### `useAuthStore`
```ts
interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User) => void;
  logout: () => void;
}
// Dashboard da: user.firstName, user.lastName
```

### `useAttendanceStore`
```ts
interface AttendanceStore {
  sessions: AttendanceSession[];
  todaySession: AttendanceSession | null;
  isLoading: boolean;
  error: string | null;
  currentMonth: { year: number; month: number };
  fetchSessions: (dateFrom: string, dateTo: string) => Promise<void>;
  checkIn: (notes?: string, file?: File) => Promise<void>;
  checkOut: () => Promise<void>;
}
```

### `useLeaveStore`
```ts
interface LeaveStore {
  leaves: Leave[];
  totalLeaves: number;
  isLoading: boolean;
  fetchLeaves: (params?: LeaveParams) => Promise<void>;
}
```

### `usePayrollStore`
```ts
interface PayrollStore {
  payrolls: Payroll[];
  latestPayroll: Payroll | null;
  isLoading: boolean;
  fetchPayrolls: (params?: PayrollParams) => Promise<void>;
}
```

---

## 12. Muhim Eslatmalar

1. **Vaqtga qarab salomlashish:**
   ```ts
   const hour = new Date().getHours()
   const greeting =
     hour < 12 ? 'Good morning' :
     hour < 17 ? 'Good afternoon' : 'Good evening'
   ```

2. **Check In/Out tugma race condition:** Bir marta bosilganda `isSubmitting = true` qilib disable qil, response kelguncha qayta bosilmasligi uchun.

3. **Calendar va Recent Activity bir xil API:** `GET /api/v1/attendance/self/sessions` — oy boshidan oxirigacha, keyin frontend filter qiladi.

4. **Today session topish:**
   ```ts
   import { format, isToday, parseISO } from 'date-fns'
   const todaySession = sessions.find(s => isToday(parseISO(s.date)))
   ```

5. **Net Salary format:**
   ```ts
   new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
     .format(netSalary)
   ```

6. **Stat cards hisob-kitobi:**
   - `Present Days` = sessions filter `status === 'present' || status === 'late'`
   - `Late Arrivals` = sessions filter `status === 'late'`
   - `Leave Balance` = backend dan keladi (yoki `employee-leaves` aggregate)

7. **Error Boundary:** Har bir widget (calendar, payslip, leaves) alohida error boundary ichida bo'lsin, bitta xato butun dashboardni sindirmasin.

8. **Prefetching:** `useEffect` da parallel `Promise.all()` bilan barcha API larni bir vaqtda chaqir, ketma-ket emas:
   ```ts
   await Promise.all([
     fetchUser(),
     fetchSessions(dateFrom, dateTo),
     fetchLeaves({ limit: 3 }),
     fetchPayrolls({ limit: 1 })
   ])
   ```


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/project_docs/pages/landing/about.md`

# About Page Specification

## 1. Maqsad

Kompaniya haqida ishonch va shaffoflik yaratish sahifasi. Mijozlarga jamoani, missiyani va texnologik stack-ni ko'rsatish orqali ishonch uyg'otish. Stats, mission text, team cards va tech stack chips-dan iborat. To'liq statik sahifa.

---

## 2. Route

```
/about
```

---

## 3. Mockup reference

```
orcestor/examples/landing/about-page-v1.jpg
```

> Mockupda: Navbar, page hero, stats row, mission section, team cards grid, tech stack chips, Footer ko'rsatilgan.

---

## 4. Layout tuzilmasi

```
<RootLayout>
  └── <LandingLayout>
        ├── <Navbar />
        ├── <main>
        │     ├── <PageHero />          ← "About Us" heading + subtitle
        │     ├── <StatsRow />          ← 4 ta kompaniya statistikasi
        │     ├── <MissionSection />    ← Mission text + vision image
        │     ├── <TeamSection />       ← Team cards grid
        │     └── <TechStackSection />  ← Technology chips row
        └── <Footer />                  ← To'liq footer (links, social, copyright)
```

**Page wrapper:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

---

## 5. Komponentlar ro'yxati

### 5.1 `<PageHero />` (About variant)

| Element   | Mazmun                                                               |
|-----------|----------------------------------------------------------------------|
| Badge     | `"Our Story"` — pill/chip                                           |
| Heading   | `"Built for modern teams, by a team that cares"` — H1               |
| Subtitle  | `"We're on a mission to make HR management simple, transparent, and human."` |

---

### 5.2 `<StatsRow />` — Kompaniya statistikasi

4 ta stat karta, horizontal row:

| #  | Value     | Label           | Icon         |
|----|-----------|-----------------|--------------|
| 1  | 3+        | Years in market | `Calendar`   |
| 2  | 50+       | Companies served| `Building2`  |
| 3  | 10,000+   | Employees managed| `Users`     |
| 4  | 99.9%     | Uptime SLA      | `Activity`   |

```tsx
const ABOUT_STATS = [
  { value: '3+',      label: 'Years in market',     icon: Calendar  },
  { value: '50+',     label: 'Companies served',    icon: Building2 },
  { value: '10,000+', label: 'Employees managed',   icon: Users     },
  { value: '99.9%',   label: 'Uptime SLA',          icon: Activity  },
];
```

Layout: `grid grid-cols-2 md:grid-cols-4 gap-6`

---

### 5.3 `<MissionSection />`

**Layout:** 2-column grid (text chap, image/illustration o'ng), `md:grid-cols-2`

| Element        | Mazmun                                                             |
|----------------|--------------------------------------------------------------------|
| Section label  | `"Our Mission"` — small uppercase text, indigo                    |
| Heading        | `"Empowering teams through smart technology"` — H2               |
| Mission text   | Multi-paragraph company mission statement                         |
| Values list    | 3–4 ta core value (icon + text)                                   |
| Right side     | Abstract illustration yoki team/office photo                      |

**Mission text (static):**

```
We believe that managing people should never feel like managing paperwork.
Zdes was built to give HR teams and managers the tools they need to focus
on what matters most — their people.

From attendance tracking to payroll automation, every feature is designed
with simplicity and transparency in mind. We're a small but passionate team
committed to continuously improving how modern businesses manage their workforce.
```

**Core values:**

```tsx
const CORE_VALUES = [
  {
    icon: Heart,
    title: 'People First',
    description: 'Every decision starts with how it affects our users.',
  },
  {
    icon: Shield,
    title: 'Transparency',
    description: 'Open and honest in everything we do.',
  },
  {
    icon: Zap,
    title: 'Simplicity',
    description: 'Powerful tools that are easy to understand.',
  },
  {
    icon: RefreshCw,
    title: 'Continuous Improvement',
    description: 'Always learning, always getting better.',
  },
];
```

---

### 5.4 `<TeamSection />` — Jamoa kartalar

Section heading: `"Meet the team"` (H2, centered)
Subtitle: `"The passionate people behind Zdes"`

**Team members (static data):**

```tsx
const TEAM_MEMBERS = [
  {
    name:   'Fayzillo Nishonov',
    role:   'Founder & CEO',
    bio:    'Passionate about HR technology and building great products.',
    avatar: '/assets/team/fayzillo.jpg',  // placeholder bo'lsa initials fallback
    social: {
      linkedin: 'https://linkedin.com/in/fayzillo',
      github:   'https://github.com/fayzillo',
    },
  },
  {
    name:   'Team Member 2',
    role:   'CTO',
    bio:    'Full-stack engineer with 8+ years of experience.',
    avatar: '/assets/team/member2.jpg',
    social: { linkedin: '#', github: '#' },
  },
  {
    name:   'Team Member 3',
    role:   'Head of Design',
    bio:    'Crafting intuitive experiences for complex workflows.',
    avatar: '/assets/team/member3.jpg',
    social: { linkedin: '#', github: '#' },
  },
];
```

> **Eslatma:** Haqiqiy jamoa a'zolari ma'lumotlari to'ldirilgach almashtiriladi. Hozircha placeholder data.

**TeamCard tuzilmasi:**

```tsx
<div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100
                hover:shadow-md transition-shadow text-center">
  {/* Avatar */}
  <div className="mx-auto mb-4 h-20 w-20 rounded-full overflow-hidden bg-indigo-100">
    {avatar
      ? <img src={avatar} alt={name} className="h-full w-full object-cover" />
      : <span className="flex h-full w-full items-center justify-center
                         text-2xl font-bold text-indigo-600">
          {name.charAt(0)}
        </span>
    }
  </div>

  {/* Info */}
  <h3 className="font-semibold text-gray-900">{name}</h3>
  <p  className="text-sm text-indigo-600 mb-2">{role}</p>
  <p  className="text-sm text-gray-500 mb-4">{bio}</p>

  {/* Social links */}
  <div className="flex items-center justify-center gap-3">
    {social.linkedin && (
      <a href={social.linkedin} target="_blank" rel="noopener noreferrer"
         aria-label={`${name} LinkedIn`}>
        <Linkedin className="h-4 w-4 text-gray-400 hover:text-indigo-600 transition-colors" />
      </a>
    )}
    {social.github && (
      <a href={social.github} target="_blank" rel="noopener noreferrer"
         aria-label={`${name} GitHub`}>
        <Github className="h-4 w-4 text-gray-400 hover:text-gray-900 transition-colors" />
      </a>
    )}
  </div>
</div>
```

Layout: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8`

---

### 5.5 `<TechStackSection />`

Section heading: `"Built with modern technology"` (H2, centered)

**Tech stack items:**

```tsx
const TECH_STACK = [
  { name: 'NestJS',     color: 'red',    icon: '/icons/nestjs.svg'     },
  { name: 'PostgreSQL', color: 'blue',   icon: '/icons/postgres.svg'   },
  { name: 'Prisma',     color: 'indigo', icon: '/icons/prisma.svg'     },
  { name: 'Next.js',    color: 'gray',   icon: '/icons/nextjs.svg'     },
  { name: 'React',      color: 'cyan',   icon: '/icons/react.svg'      },
  { name: 'TypeScript', color: 'blue',   icon: '/icons/typescript.svg' },
  { name: 'Tailwind',   color: 'teal',   icon: '/icons/tailwind.svg'   },
  { name: 'Docker',     color: 'sky',    icon: '/icons/docker.svg'     },
];
```

**Chip tuzilmasi:**

```tsx
<div className="flex flex-wrap justify-center gap-3">
  {TECH_STACK.map(tech => (
    <div key={tech.name}
         className="flex items-center gap-2 rounded-full border border-gray-200
                    bg-white px-4 py-2 shadow-sm hover:shadow-md transition-shadow">
      <img src={tech.icon} alt={tech.name} className="h-5 w-5" />
      <span className="text-sm font-medium text-gray-700">{tech.name}</span>
    </div>
  ))}
</div>
```

---

### 5.6 `<Footer />` — To'liq Footer

**Footer tuzilmasi:**

```tsx
<footer className="bg-gray-900 text-gray-400">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">

      {/* Brand column */}
      <div className="col-span-1 md:col-span-2">
        <Logo className="mb-4" />
        <p className="text-sm leading-relaxed mb-6">
          All-in-one employee management platform for modern teams.
        </p>
        {/* Social links */}
        <div className="flex gap-4">
          <a href="#" aria-label="LinkedIn"><Linkedin className="h-5 w-5 hover:text-white transition-colors" /></a>
          <a href="#" aria-label="GitHub"><Github className="h-5 w-5 hover:text-white transition-colors" /></a>
          <a href="#" aria-label="Twitter/X"><Twitter className="h-5 w-5 hover:text-white transition-colors" /></a>
        </div>
      </div>

      {/* Product links */}
      <div>
        <h4 className="text-white font-semibold mb-4">Product</h4>
        <ul className="space-y-2 text-sm">
          <li><Link to="/features" className="hover:text-white transition-colors">Features</Link></li>
          <li><Link to="/pricing"  className="hover:text-white transition-colors">Pricing</Link></li>
          <li><a href="#changelog" className="hover:text-white transition-colors">Changelog</a></li>
        </ul>
      </div>

      {/* Company links */}
      <div>
        <h4 className="text-white font-semibold mb-4">Company</h4>
        <ul className="space-y-2 text-sm">
          <li><Link to="/about"   className="hover:text-white transition-colors">About</Link></li>
          <li><a href="#blog"     className="hover:text-white transition-colors">Blog</a></li>
          <li><a href="#careers"  className="hover:text-white transition-colors">Careers</a></li>
          <li><a href="#contact"  className="hover:text-white transition-colors">Contact</a></li>
        </ul>
      </div>

    </div>

    {/* Bottom bar */}
    <div className="mt-12 border-t border-gray-800 pt-8 flex flex-col sm:flex-row
                    justify-between items-center gap-4 text-sm">
      <p>© {new Date().getFullYear()} Zdes. All rights reserved.</p>
      <div className="flex gap-6">
        <a href="#privacy" className="hover:text-white transition-colors">Privacy Policy</a>
        <a href="#terms"   className="hover:text-white transition-colors">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>
```

---

## 6. Style (ranglar, tipografiya, spacing)

### Ranglar

```css
/* Page */
--bg-page:         #ffffff;
--bg-section-alt:  #f9fafb;   /* gray-50 — alternating sections */

/* Stats karta */
--stat-bg:   #f0f4ff;   /* indigo-50 */
--stat-icon: #6366f1;   /* indigo-500 */

/* Team card */
--team-card-bg:     #ffffff;
--team-card-border: #f3f4f6;   /* gray-100 */
--avatar-bg:        #e0e7ff;   /* indigo-100 */

/* Footer */
--footer-bg:   #111827;   /* gray-900 */
--footer-text: #9ca3af;   /* gray-400 */
```

### Tipografiya

| Element       | Size    | Weight | Color      |
|---------------|---------|--------|------------|
| H1 (Hero)     | 3xl–4xl | 700    | gray-900   |
| H2 (Section)  | 2xl–3xl | 700    | gray-900   |
| Stats value   | 3xl     | 700    | indigo-600 |
| Stats label   | sm      | 500    | gray-500   |
| Team name     | base    | 600    | gray-900   |
| Team role     | sm      | 500    | indigo-600 |
| Team bio      | sm      | 400    | gray-500   |
| Tech chip     | sm      | 500    | gray-700   |

### Spacing

- Section padding: `py-20` yoki `py-24`
- Team grid gap: `gap-8`
- Tech chips gap: `gap-3`
- Footer padding: `py-16`

---

## 7. States

| State   | Tavsif                                                         |
|---------|----------------------------------------------------------------|
| Default | Statik render — barcha content ko'rinadi                      |
| Hover   | Team card: `shadow-md`, social icon color o'zgaradi           |
|         | Tech chip: `shadow-md` transition                             |
|         | Footer links: `text-white` transition                         |
| Loading | Yo'q (statik sahifa)                                          |
| Error   | Yo'q (API yo'q)                                               |
| Avatar error | Fallback initials avatar ko'rsatiladi (image 404 bo'lsa)|

---

## 8. Animatsiyalar

### Stats counter (scroll reveal)

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.9 }}
  whileInView={{ opacity: 1, scale: 1 }}
  viewport={{ once: true }}
  transition={{ duration: 0.4, delay: index * 0.1 }}
>
```

### Mission section (slide in)

```tsx
// Chap tomondagi matn
<motion.div
  initial={{ opacity: 0, x: -40 }}
  whileInView={{ opacity: 1, x: 0 }}
  viewport={{ once: true, amount: 0.2 }}
  transition={{ duration: 0.6 }}
>

// O'ng tomondagi rasm
<motion.div
  initial={{ opacity: 0, x: 40 }}
  whileInView={{ opacity: 1, x: 0 }}
  viewport={{ once: true, amount: 0.2 }}
  transition={{ duration: 0.6, delay: 0.1 }}
>
```

### Team cards (stagger)

```tsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.5, delay: index * 0.1 }}
>
```

### Tech chips (fade in left-to-right)

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.8 }}
  whileInView={{ opacity: 1, scale: 1 }}
  viewport={{ once: true }}
  transition={{ duration: 0.3, delay: index * 0.05 }}
>
```

---

## 9. Responsive

| Breakpoint    | Layout                                              |
|---------------|-----------------------------------------------------|
| `xs` (<640px) | Stats 2×2 grid; Mission single column; Team 1 col  |
| `sm` (640px+) | Team 2 columns                                     |
| `md` (768px+) | Stats 4 col; Mission 2 col; Team 2-3 col           |
| `lg` (1024px+)| Team 3 columns; Full layout                        |

**Footer responsive:**
- Mobile: `flex-col` — branding, links vertikal
- Desktop: `md:grid-cols-4`

**Tech chips:** `flex-wrap` bilan har qanday ekranda moslashadi.

---

## 10. API endpointlar

```
Hech qanday API chaqiruv yo'q — sahifa to'liq statik.
Barcha ma'lumotlar (stats, team, tech stack) frontend konstantasida.
```

---

## 11. Global state (Zustand)

```
Bu sahifada global state ishlatilmaydi. Local state ham yo'q.
```

---

## 12. Muhim eslatmalar

1. **Team data:** Hozircha placeholder — haqiqiy jamoa a'zolari ma'lumotlari bildirilganda almashtiriladi.
2. **Avatar fallback:** `<img>` `onError` handlerida initials-based SVG fallback ko'rsating.
3. **Social links:** Footer va Team cards-dagi `href="#"` placeholder — haqiqiy linklar bilan almashtirilsin.
4. **Tech icons:** SVG iconlar `/public/icons/` papkasida saqlash, yoki `simple-icons` npm package ishlatish.
5. **Section background alternating:** Har ikkinchi section `bg-gray-50` bilan o'zgaruvchan background berish vizual ajratish uchun.
6. **Footer copyright year:** `new Date().getFullYear()` — har yil avtomatik yangilanadi.
7. **SEO:** `<title>About — Zdes</title>`, Organization schema markup (JSON-LD) qo'shing.
8. **Footer placement:** Footer faqat About sahifasida emas — `<LandingLayout>` ichida shared bo'lishi kerak.


## Manba: `zdes_archive_docs/raw_history/orcestor/analysis/T-005-datatable-api.md`

# DataTable API Tahlili (T-005)

## Taklif qilinayotgan API:
*   `@Input() columns: { key: string, label: string, sortable?: boolean }[]` - Ustunlar konfiguratsiyasi
*   `@Input() data: T[]` - Jadval ma'lumotlari (Generic T tipida)
*   `@Input() loading: boolean = false` - Yuklanish holati
*   `@Input() pageSize: number = 10` - Sahifa sig'imi
*   `@Input() emptyMessage: string = 'Ma\'lumot topilmadi'` - Bo'sh holat matni
*   `@Output() rowClick = new EventEmitter<T>()` - Qator bosilganda
*   `@Output() sortChange = new EventEmitter<{key: string, direction: 'asc' | 'desc'}>()` - Saralash o'zgarganda

## Moslashuvchanligi:
*   **Employees ro'yxati:** `columns` orqali rasmi, ismi, lavozimi kabi ustunlar beriladi. Harakatlar ustunini render qilish qiyinroq bo'lishi mumkin, shuning uchun odatda `ng-template` yoki `ContentChild` ishlatiladi, lekin ushbu oddiy versiyada `rowClick` orqali umumiy harakatni boshqarish mumkin.
*   **Attendance ro'yxati:** Sana filtrlari jadvaldan tashqarida bo'ladi va yangilangan `data` jadvalga uzatiladi. Jadval faqat taqdimot uchun xizmat qiladi. Client-side sort va pagination juda qo'l keladi.
