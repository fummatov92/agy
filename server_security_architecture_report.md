# 🛡️ VPS Server Xavfsizlik Arxitekturasi va Himoya Choralari | Mas'ul Agent ID: `a8b64ff4-d90b-4ac1-9c7c-129824ce21b6`

Ushbu hujjat **Fayzillo Ummatov**ning shaxsiy Contabo VPS serverida (`fayzillo@<HOST_NAME>`, IP: `<SERVER_IP>`) joriy etilgan umumiy axborot xavfsizligi, tarmoq izolyatsiyasi, kesh va ma'lumotlar bazasi himoyasi, shuningdek sun'iy intellekt (AGY Core Engine) faoliyati uchun o'rnatilgan cheklovlar haqidagi to'liq tahliliy hisobotdir. Hujjat Claude yoki boshqa audit tizimlarida mustaqil xavfsizlik tahlilini (Security Audit) o'tkazish uchun maxsus tayyorlandi.

---

## 📌 1. Boshqaruv Muhiti va Server Izolyatsiyasi (Blast Radius Reduction)

Serverda mavjud tizim xizmatlari va parallel production loyihalariga zarracha xavf tug'dirmaslik uchun AI agenti va yangi loyihalar uchun qat'iy chegaralar belgilangan:

1. **Izolyatsiyalangan Ishchi Hudud:**
   * AI agenti va yangi ishlab chiqiladigan barcha dasturlar FAQAT `/home/fayzillo/Desktop/` katalogi doirasida ish olib boradi.
   * Tizimning ildiz kataloglariga (`/`, `/root/`, `/etc/`, `/srv/`, `/var/`) va `.ssh` konfiguratsiyalariga to'g'ridan-to'g'ri teginish qat'iyan taqiqlangan.
2. **Hamkasb va Parallel Loyihalar Daxlsizligi:**
   * `/opt/mahala`, `/opt/online-magazin` va boshqa ishlab turgan tizim papkalari AI ta'sir doirasidan butunlay ajratilgan.
   * Ular alohida tizim foydalanuvchilari va mustaqil konteyner tarmoqlarida ishlaydi.
3. **Foydalanuvchi Ruxsatlari (Least Privilege Principle):**
   * Jarayonlar cheklangan huquqlarga ega `fayzillo` foydalanuvchisi nomidan bajariladi.
   * Rootless Docker muhiti orqali konteynerlarning host tizimiga bevosita chiqib ketish (container breakout) xavfi minimallashtirilgan.

---

## 🌐 2. Tarmoq va Portlar Xavfsizligi (Port Isolation & Zero-Conflict Policy)

Serverdagi portlar to'qnashuvini oldini olish va ochiq portlar orqali tashqi hujumlarga yo'l qo'ymaslik uchun maxsus port siyosati joriy qilingan:

1. **Ajratilgan Portlar Diapazoni (15800 – 15900):**
   * Serverdagi standart va muhim portlar band: `4000` (Mahala API), `8090` (Sifat/Online-magazin API), `5432/5433` (PostgreSQL), `6379` (Redis).
   * Yangi loyihalar va xizmatlar FAQAT **15800 dan 15900 gacha** bo'lgan portlar oralig'ida ochiladi (masalan: `15810` - ZDES backend, `15820` - ZDES frontend, `15976/15977` - Sessiya Connector).
2. **Lokal Tarmoq Cheklovi (Loopback Binding):**
   * Yangi ichki konteynerlar va Nginx portlari to'g'ridan-to'g'ri `0.0.0.0` ga emas, balki faqat lokal `127.0.0.1` (localhost) ga ulanadi (`127.0.0.1:15810:80`).
   * Bu tashqi internet foydalanuvchilarining to'g'ridan-to'g'ri ichki portlarga kirishini bloklaydi.
3. **Yagona Kirish Darvozasi — Caddy Reverse Proxy & Avto-SSL:**
   * Serverga barcha tashqi HTTP/HTTPS trafigi faqat markaziy **Caddy** web-serveri orqali kiradi.
   * Barcha domenlar (`*.safira.uz`, `*.duckdns.org`) uchun Let's Encrypt / ZeroSSL orqali TLS 1.3 shifrlangan SSL sertifikatlari avtomatik boshqariladi.
   * Caddy konfiguratsiyasi har bir yangilanish oldidan `caddy validate` orqali sintaktik tekshiriladi va uzilishsiz (`reload`) qo'llaniladi.

---

## 🗄️ 3. Ma'lumotlar Bazasi va Kesh Tizimi Xavfsizligi

Loyihalararo ma'lumotlar chalkashib ketishi (Cross-project data contamination) va server diski to'lib qolishining oldi olingan:

1. **Tashqi Bulut Baza (Neon Cloud PostgreSQL):**
   * Yangi loyihalar (masalan, ZDES) uchun lokal server diski va RAM-ini tejash maqsadida Neon Cloud PostgreSQL dan foydalaniladi.
   * Baza trafigi SSL orqali shifrlangan va PgBouncer connection pooling (`connection_limit=5`) orqali ulanishlar soni me'yorda saqlanadi.
2. **Kesh Izolyatsiyasi (Namespace Prefixes):**
   * Kesh uchun Upstash Cloud Redis (yoki lokal Redis) ishlatiladi.
   * Kesh kalitlari loyihalar bo'yicha qat'iy prefikslangan:
     - Mahala: ichki cache service fallback.
     - Telegram botlar: `bull:*`, `session:*`.
     - ZDES: `cache:<resource>:*`.
   * Ushbu ajratish orqali bitta loyiha boshqa loyihaning kesh ma'lumotlarini o'chirib yuborishi yoki buzishi mutlaqo imkonsiz.
3. **Statik Fayllar (Uploads) Himoyasi:**
   * Yuklanayotgan fayllar Docker konteynerining o'zida qolib ketmaydi (konteyner hajmi shishib ketmaydi).
   * Hostdagi alohida izolyatsiya qilingan jildga (`/home/fayzillo/Desktop/temp/uploadss-zdes`) ulanib, Nginx orqali faqat o'qish huquqi (`:ro`) bilan statik tarqatiladi.

---

## 🤖 4. AI Engine va Avtonom Agent Xavfsizlik Qoidalari (AGY Guardrails)

Serverda JarvisOS AI Core Engine (Antigravity CLI) avtonom ishlaganda inson nazorati va xavfsizligini ta'minlovchi filtrlar:

1. **Xato Tuzatish Protokoli (Diagnostic First):**
   * Tizimda xato chiqqanida AI darhol fayllarni o'zgartirmaydi.
   * Avval muammoning sababi, ta'sir doirasi va taklif etilayotgan yechim foydalanuvchiga matn shaklida tushuntiriladi. Faqat foydalanuvchi "tuzat" deb tasdiqlagach amaliy o'zgartirish kiritiladi.
2. **Tushunishni Tasdiqlash va Fakt-Cheking:**
   * Ish boshlashdan oldin AI vazifani qanday tushunganini qisqa bayon qiladi.
   * Yangi topshiriqda eski sessiya xulosalariga ko'r-ko'rona ishonmasdan, jonli server holatini (portlar, git, docker, loglar) qayta tekshiradi (Fresh State Fact-Checking).
3. **Zero Secret Leak (Maxfiylik Majburiyati):**
   * Hisobotlar, GitHub repolari va ommaviy matnlarda serverning real IP-manzillari, ma'lumotlar bazasi parollari, API kalitlar yoki tokenlar chiqib ketmasligi uchun majburiy maskalash qo'llaniladi (`<SERVER_IP>`, `[REDACTED_CREDENTIALS]`, `<DB_ENDPOINT>`).
4. **Sirlarni va Kontekstni Maqsadli Tozalash (Targeted On-Demand Sanitization):**
   * AI xotirasi yoki chat loglaridagi maxfiy kalitlarni tozalash (Secret Sanitization) HECH QACHON avtomatik yoki barcha sessiyalarni birdaniga tozalash shaklida bajarilmaydi.
   * Bu amaliyot FAQAT foydalanuvchining aniq buyrug'i bilan va FAQAT foydalanuvchi ko'rsatgan bitta `Session ID` doirasidagina maqsadli amalga oshiriladi.

---

## 🪵 5. Monitoring, Logger va Alert Tizimi

1. **Izolyatsiyalangan Nginx Loglari:**
   * Barcha so'rovlar alohida log fayllariga yo'naltirilgan (`/home/fayzillo/Desktop/logs/zdes/backend/` va `frontend/`).
   * `access.log` — barcha keluvchi so'rovlar monitoringi.
   * `error.log` — Nginx va upstream xatolarini zudlik bilan qayd etish.
2. **PM2 Process Manager:**
   * Botlar va backend servislar (`sessiya-bot`, `sessiya-backend`, `telegram-userbot`) PM2 ostida klaster/fork rejimida ishlaydi, xatolik yuz berganda avtomatik qayta tiklanadi.
3. **Telegram Live Dispatch Protocol:**
   * Uzoq vaqt oladigan operatsiyalarda (build, test, git sync) Telegram xabari real-vaqt rejimida (`update_live_msg.js`) bosqichma-bosqich yangilanib, jarayonning to'xtab qolmaganligi haqida adminni xabardor qilib turadi.

---

## 🎯 6. Xulosa va Claude Analizi Uchun Tavsiyalar

Ushbu xavfsizlik modeli **"Defense-in-Depth" (Ko'p bosqichli chuqur mudofaa)** tamoyiliga asoslangan bo'lib:
- Tashqi qatlamda: Caddy SSL + domenlar filtratsiyasi.
- O'rta qatlamda: Loopback portlar + izolyatsiyalangan Nginx reverse proxy.
- Ichki qatlamda: Rootless Docker konteynerlari + ajratilgan bulut bazalar.
- Boshqaruv qatlamida: Qat'iy qoidalar bilan cheklangan AI agenti (Least Privilege AI Engine).

*Hisobot tuzuvchi: AGY Core AI Engine (Agent ID: `a8b64ff4-d90b-4ac1-9c7c-129824ce21b6`)*
