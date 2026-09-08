# 🐳 2. Rootless Docker Arxitekturasi (Container Sandbox)

## 📌 Muammoning Mohiyati
Klassik Docker arxitekturasida `docker` guruhi a'zosi bo'lgan foydalanuvchi aslida serverda `root` huquqiga tenglashib qoladi. Chunki:
- Docker daemoni tizimning `root` huquqida ishlaydi;
- Har qanday foydalanuvchi `docker run -v /:/host_root ...` buyrug'i orqali asosiy serverning butun fayllar tizimini o'zgartirishi mumkin;
- Boshqa dasturlarning ishlab turgan konteynerlarini ko'rish yoki to'xtatish xavfi mavjud edi.

---

## 🚀 Yechim: To'liq Rootless Docker

`fayzillo` foydalanuvchisi uchun **Rootless Docker** texnologiyasi muvaffaqiyatli joriy etildi.

### 🔍 Texnik Tekshiruv Natijasi:
```bash
$ docker info | grep -i "Security Options" -A 1
 Security Options:
  rootless
```

---

## 🛡️ Rootless Docker Xavfsizlik Tamoyillari

1. **User Namespace Izolyatsiyasi:**
   - Docker daemoni `systemd --user` sessiyasi doirasida ishlaydi.
   - Socket manzili: `unix:///run/user/1001/docker.sock`.
   - Foydalanuvchi tizimning `root` huquqiga ega bo'lmagan holda konteynerlarni to'liq boshqara oladi.

2. **Container Breakout Himoyasi:**
   - Konteyner ichida hatto `root` foydalanuvchisi (UID 0) ishlatilgan taqdirda ham, host operatsion tizimida u oddiy `fayzillo` (UID 1001) sifatida namoyon bo'ladi.
   - Shuning uchun konteynerdan chiqib ketish (breakout) orqali butun serverni egallash imkoniyati **0 ga teng**.

3. **Mavjud Tizim Konteynerlarining Ko'rinmasligi:**
   - Serverdagi boshqa tizim loyihalarining (masalan, `/opt/*` dagi) root konteynerlari `fayzillo` sessiyasiga ko'rinmaydi (`docker ps` faqat o'z konteynerlarini ko'rsatadi).
   - Bu boshqa loyihalarga tasodifan xalal berish xavfini to'liq bartaraf etadi.

4. **Portlarni Boshqarish Cheklovi:**
   - Rootless rejimida 1024 dan past bo'lgan portlarni (80, 443, 22) to'g'ridan-to'g'ri egallash cheklangan.
   - Bu bizning `15800 - 15900` oralig'idagi xavfsiz portlar qoidamiz bilan 100% uyg'undir.
