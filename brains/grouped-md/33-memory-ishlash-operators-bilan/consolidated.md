# JavaScript Operatorlari va Xotira Boshqaruvi (JS Core Concepts)


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ovovo******utvata@gmail.com/javascript_operatorlari.md`

# JavaScript operatorlari

### 👤 Foydalanuvchi:

Salom Java scripda  operatorlar nomlanishi qisqa  o'zimni xatoliklarimni to'g'rillab olishim uchun aytib ber lopp shart emas 

### 🤖 ChatGPT:

Albatta. Qisqa ro'yxat:

- `=` — **Assignment** (qiymat berish)
- `+=`, `-=`, `*=`, `/=`, `%=` — **Assignment operators**
- `==` — **Loose equality**
- `===` — **Strict equality**
- `!=` — **Loose inequality**
- `!==` — **Strict inequality**
- `>` `<` `>=` `<=` — **Comparison operators**
- `+` `-` `*` `/` `%` `**` — **Arithmetic operators**
- `++` `--` — **Increment / Decrement**
- `&&` — **Logical AND**
- `||` — **Logical OR**
- `!` — **Logical NOT**
- `??` — **Nullish coalescing**
- `?.` — **Optional chaining**
- `?:` — **Ternary operator**
- `typeof` — **Type operator**
- `instanceof` — **Instance operator**
- `in` — **Property operator**
- `delete` — **Delete operator**
- `new` — **New operator**
- `void` — **Void operator**
- `,` — **Comma operator**
- `...` — **Spread / Rest operator**
- `await` — **Await operator**
- `yield` — **Yield operator** (generatorlarda)

Intervyu uchun eng ko'p so'raladiganlari:
`=`, `==`, `===`, `!=`, `!==`, `&&`, `||`, `!`, `??`, `?.`, `?:`, `typeof`, `instanceof`, `in`, `new`, `...`, `await`.

---

### 👤 Foydalanuvchi:

Guruhlari

### 🤖 ChatGPT:

Operatorlarni odatda quyidagi guruhlarga bo'lishadi:

1. **Arithmetic operators** (Arifmetik)
   - `+`, `-`, `*`, `/`, `%`, `**`, `++`, `--`

2. **Assignment operators** (Qiymat berish)
   - `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `&&=`, `||=`, `??=`

3. **Comparison operators** (Taqqoslash)
   - `==`, `===`, `!=`, `!==`, `>`, `<`, `>=`, `<=`

4. **Logical operators** (Mantiqiy)
   - `&&`, `||`, `!`, `??`

5. **Bitwise operators** (Bitli)
   - `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>`

6. **String operators**
   - `+`, `+=`

7. **Conditional (Ternary) operator**
   - `?:`

8. **Type operators**
   - `typeof`, `instanceof`

9. **Relational operators**
   - `in`

10. **Unary operators** (Bir operandli)
    - `+`, `-`, `!`, `~`, `typeof`, `delete`, `void`, `++`, `--`

11. **Special / Other operators**
    - `new`, `delete`, `await`, `yield`, `?.`, `...`, `,`

Intervyularda asosan dastlabki **5 ta guruh** (Arithmetic, Assignment, Comparison, Logical, Bitwise) va qo'shimcha ravishda **Ternary**, **Type (`typeof`, `instanceof`)**, **`in`**, **`new`**, **`?.`**, **`??`**, **`...`** ko'p uchraydi.

---

### 👤 Foydalanuvchi:

Asosiy mavzu if else gacha olib kelish 0 dan shunign uchun ifda ishlatilmaydigan murakkablar kerak emas

### 🤖 ChatGPT:

Agar maqsading **0 dan `if/else` gacha** o'rganish bo'lsa, operatorlarni shunday tartibda o'rgansang yetarli:

### 1. Arithmetic Operators (Arifmetik)
- `+`
- `-`
- `*`
- `/`
- `%`
- `**`

### 2. Assignment Operators (Qiymat berish)
- `=`
- `+=`
- `-=`
- `*=`
- `/=`
- `%=`

### 3. Increment / Decrement
- `++`
- `--`

### 4. Comparison Operators (Taqqoslash)
- `==`
- `===`
- `!=`
- `!==`
- `>`
- `<`
- `>=`
- `<=`

### 5. Logical Operators (Mantiqiy)
- `&&`
- `||`
- `!`

Shularni bilsang, `if`, `else if`, `else` mavzusiga bemalol o'tish mumkin.

Hozircha **kerak emas**:
- Bitwise (`&`, `|`, `^`, `<<`...)
- Ternary (`?:`)
- Nullish (`??`)
- Optional chaining (`?.`)
- `typeof`, `instanceof`, `in`
- `new`, `delete`, `void`
- Spread/Rest (`...`)
- `await`, `yield`

Bu operatorlar keyingi mavzularda o'rganiladi va `if/else`ni tushunish uchun shart emas.

---

### 👤 Foydalanuvchi:

If Else switch qanday operatorlar deyilardi

### 🤖 ChatGPT:

`if`, `else if`, `else` va `switch` **operator emas**.

Ular **Conditional Statements** (Shart operatorlari / Shartli boshqaruv konstruksiyalari) deb ataladi.

Qisqacha:

- `if` → **Conditional Statement**
- `else if` → **Conditional Statement**
- `else` → **Conditional Statement**
- `switch` → **Switch Statement** (ham shartli boshqaruv konstruksiyasi)

Demak, mavzular ketma-ketligi odatda shunday bo'ladi:

1. Variables
2. Data Types
3. Operators
4. **Conditional Statements** (`if`, `else if`, `else`, `switch`)
5. Loops (`for`, `while`, `do...while`)
6. Functions

Intervyuda "What are `if` and `switch`?" deb so'rashsa, **"They are conditional statements."** deb javob berish to'g'ri bo'ladi.

---

### 👤 Foydalanuvchi:

To

### 🤖 ChatGPT:

Ha, to'g'ri. Odatda 0 dan JavaScript quyidagicha ketadi:

1. **Variables** (O'zgaruvchilar)
2. **Data Types** (Ma'lumot turlari)
3. **Operators** (Operatorlar)
4. **Conditional Statements** (Shartli konstruksiyalar)
   - `if`
   - `else if`
   - `else`
   - `switch`
5. **Loops** (Takrorlash konstruksiyalari)
   - `for`
   - `while`
   - `do...while`
6. **Functions** (Funksiyalar)

Shu ketma-ketlik `if` mavzusigacha o'qitish uchun ham, intervyu tayyorgarligi uchun ham juda qulay.

---

### 👤 Foydalanuvchi:

Condition operators degan atama bormi

### 🤖 ChatGPT:

Ha, lekin **`condition operators`** degan atama JavaScript'da standart termin emas.

To'g'ri atamalar:

- ✅ **Conditional statements** — `if`, `else`, `switch`
- ✅ **Comparison operators** — `>`, `<`, `===`, `!==`, ...
- ✅ **Logical operators** — `&&`, `||`, `!`

Ba'zan odamlar norasmiy ravishda "`condition operators`" deb aytishadi, chunki bu operatorlar shart yozishda ishlatiladi. Lekin texnik jihatdan bu noto'g'ri yoki kam ishlatiladigan atama.

Masalan:

```js
if (age >= 18 && isStudent) {
  // ...
}
```

Bu yerda:
- `if` — **Conditional statement**
- `>=` — **Comparison operator**
- `&&` — **Logical operator**

Shuning uchun dars yoki intervyuda **"Conditional statements"** va **"Comparison/Logical operators"** atamalarini ishlatish tavsiya etiladi.

---


## Manba: `zdes_archive_docs/raw_history/zdes_fix_orcestor/orcestor/memory/README.md`

# Memory Index\nHozircha memory yozuvi yo'q.


## Manba: `my_digital_brain/30_Resources/ai-chat-history/chatgpt/ovovo******utvata@gmail.com/stack_va_heap_farqi.md`

# Stack va Heap farqi

### 👤 Foydalanuvchi:

Javascriptda Stack vs HEAP  

### 🤖 ChatGPT:

Zo‘r savol Fayzillo 😎, keling buni oddiy qilib tushuntiraman:  

JavaScript’da **Stack** va **Heap** — bu xotira boshqaruvi uchun ishlatiladigan ikkita turli joy:  

---

## 🔹 Stack (to‘plam)
- **Primitive** (oddiy) qiymatlar shu yerda saqlanadi:  
  `Number`, `String`, `Boolean`, `Null`, `Undefined`, `Symbol`, `BigInt`.  
- **Stack** — juda tez ishlaydi 🚀. Chunki bu joyda qiymatlar **katta bo‘lmagan va qat’iy o‘lchamga ega**.  
- Stack **Last In, First Out (LIFO)** printsipida ishlaydi.  

Misol:  
```js
let x = 10;
let y = x;  
y = 20;

console.log(x); // 10
console.log(y); // 20
```
👉 `x` va `y` stack’da alohida saqlanadi. `y` o‘zgarganda `x`ga ta’sir qilmaydi.

---

## 🔹 Heap (uyum)
- **Objectlar** (`{}`, `[]`, `function`) shu yerda saqlanadi.  
- Heap — xotirada **dinamik** joy ajratadi. Chunki object yoki array qancha katta bo‘lishi oldindan noma’lum.  
- Bu joyda qiymatlar **reference (havola)** sifatida ishlatiladi.  

Misol:  
```js
let obj1 = { name: "Ali" };
let obj2 = obj1;

obj2.name = "Vali";

console.log(obj1.name); // "Vali"
console.log(obj2.name); // "Vali"
```
👉 `obj1` va `obj2` aslida **bitta joyni (Heapdagi objectni)** ko‘rsatadi. Shuning uchun bitta o‘zgarishi ikkinchisiga ham ta’sir qiladi.  

---

## 🧠 Yodda saqlash uchun qisqa
- **Stack** → oddiy, tez, value bo‘yicha saqlaydi.  
- **Heap** → murakkab, sekinroq, reference bo‘yicha saqlaydi.  

---

Xullas, `let a = 5` desang → stack.  
`let b = {num: 5}` desang → heap.  

---

❓Xohlaysanmi, men senga buni **xotirada diagramma** qilib chizib ko‘rsatib beray? Shu paytda `stack` va `heap` qanday ishlashini aniq ko‘rib tushunasan.

---

### 👤 Foydalanuvchi:

heap ramda saqlanadimi yoki diskda

### 🤖 ChatGPT:

Zo‘r joyiga tekkizding 👌  

👉 **Heap ham, Stack ham — RAM (tezkor xotira)** ichida joylashadi.  
Disk (HDD/SSD) bu yerda umuman ishlatilmaydi.  

---

🔹 **Stack** → RAM’ning bir qismi, unda primitiv qiymatlar va chaqirilayotgan funksiya ma’lumotlari saqlanadi.  
🔹 **Heap** → RAM’ning boshqa qismi, unda objectlar, arraylar va funksiyalar kabi murakkab ma’lumotlar joylashadi.  

📌 **Disk** faqat:  
- dastur RAM’ga yuklanayotganda,  
- yoki sen o‘zing ma’lumotni localStorage, file system yoki database’ga yozsang ishlatiladi.  

---

Demak qisqa qilib:  
- **Heap** → RAM’da (dinamik xotira).  
- **Stack** → RAM’da (tezkor, tartibli xotira).  
- **Disk** → umuman boshqa narsa (saqlash qurilmasi).  

---

Xohlaysanmi, men senga **Stack vs Heap RAM bo‘linishi** bo‘yicha chizilgan diagramma qilib beray? Shunda aniq ko‘rasan ular qanday joylashganini.

---

### 👤 Foydalanuvchi:

stringda ham dinamik bo'ladiyu

### 🤖 ChatGPT:

Ha, to‘g‘ri gap qilding 😁 — string aslida **dinamik uzunlikka ega** bo‘ladi.  
JavaScript’da bu biroz nozik joy:  

---

### 🔹 Nega string baribir **stack**da?
- JavaScript’da stringlar **primitive type** hisoblanadi.  
- Primitivlar (`number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`, `string`) **stack’da saqlanadi**.  
- Lekin string **o‘zgarmas** (`immutable`) bo‘lgani uchun, u “dinamik” ko‘rinsa ham aslida boshqa usulda boshqariladi.

---

### 🔹 Aslida qanday ishlaydi?
- Sen `let s = "hello"` desang, `s` o‘zgaruvchisi **stack’da reference (ko‘rsatkich)** sifatida turadi.  
- O‘sha reference esa RAM’dagi **string pool (heap ichidagi maxsus joy)**ga ko‘rsatadi.  
- Har safar sen stringni o‘zgartirsang (`s = s + " world"`), JavaScript eski stringni o‘zgartirmaydi, balki **yangi string** yaratadi va `s` endi unga ko‘rsatadi.  

---

### 🔹 Misol
```js
let a = "salom";
let b = a;

b = b + " dunyo";

console.log(a); // "salom"
console.log(b); // "salom dunyo"
```

👉 `a` va `b` stack’da alohida saqlanadi, lekin ikkalasi ham dastlab bitta `"salom"` stringiga reference qilib turgan.  
`b` ga qo‘shimcha qo‘shganingda, `"salom dunyo"` degan **yangi string heap’da yaratiladi**.  

---

### 🧠 Xulosa
- **String** → primitive → stack’da turadi (reference sifatida).  
- Ammo haqiqiy matn (harflar) → heap’dagi **string pool**da saqlanadi.  
- Shuning uchun string **dinamik bo‘lishi mumkin**, lekin **immutability** (o‘zgarmaslik) tamoyili saqlanib qoladi.  

---

❓Endi savol: xohlaysanmi men senga **stack + heap + string pool**ni diagramma qilib chizib tushuntirib beray? Shunda butun mexanizm ko‘zingda jonlanadi.

---

### 👤 Foydalanuvchi:

xotiradan joy ajaratishi qanday bo'ladi

### 🤖 ChatGPT:

Ooo, sen endi **chuqurroq memory management** mavzusiga kirib ketyapsan 🔥. Bu juda zo‘r, chunki ko‘pchilik “stack-heap” deyishga o‘rganib qolgan, lekin *qanday qilib xotiradan joy ajratilishi*ni bilmaydi.  

Keling, bosqichma-bosqich ko‘rib chiqamiz:  

---

## 🔹 1. Stack’da joy ajratish
- Stack RAM ichida **kontinual (ketma-ket)** joyda ishlaydi.  
- Yangi funksiya chaqirilganda unga **stack frame** ochiladi: unda lokal o‘zgaruvchilar, argumentlar, qaytish manzili saqlanadi.  
- Joy ajratish oddiygina **pointerni siljitish** orqali bo‘ladi (shuning uchun juda tez 🚀).  

👉 Misol:
```js
function foo() {
  let a = 10; // stack’da joy ajratildi
  let b = 20; // yana joy qo‘shildi
  return a + b;
}
foo();
```
Bu yerda `a` va `b` stack frame ichida joylashadi. Funksiya tugagach, stack pointer orqaga qaytadi va joy “bo‘shagan” hisoblanadi.  

---

## 🔹 2. Heap’da joy ajratish
- Heap RAM ichida joylashgan, lekin tartibsiz ishlaydi.  
- Ob’ekt yoki massiv yaratganda **memory manager** (ya’ni JS engine ichidagi allocator) bo‘sh joy qidiradi va undan foydalanadi.  
- Bu jarayon stack’dagidek oddiy emas, chunki joy topishi kerak, kerak bo‘lsa fragmentatsiya bilan shug‘ullanadi.  
- Heap’dagi xotira **avtomatik bo‘shatilmaydi**, balki **Garbage Collector (GC)** kelib, ishlatilmayotgan reference’larni yo‘qotadi.  

👉 Misol:
```js
let obj = { name: "Ali" }; // heap’dan joy ajratiladi
```
`obj`ning reference’i stack’da, lekin `{name: "Ali"}`ning o‘zi heap’da turadi.  

---

## 🔹 3. Garbage Collector
- JS’da **manual free()** yo‘q (C/C++ dagidek emas).  
- Chrome/V8 kabi engine’lar **Mark-and-Sweep GC** ishlatadi:  
  1. **Reachable objects** (hali foydalanilayotganlari) belgilanadi.  
  2. Qolgan “yetib bo‘lmaydigan” objectlar o‘chiriladi.  
  3. Joy bo‘shatiladi va keyin yana ishlatiladi.  

👉 Demak, sen `obj = null` qilsang, GC keyinchalik uni “yetib bo‘lmaydi” deb belgilaydi va RAM’dan chiqarib tashlaydi.  

---

## 🔹 Diagramma (oddiy ko‘rinish)

```
RAM:
 ┌───────────────┐
 │    Stack       │  -> primitive values, references
 │  [a=10]        │
 │  [b=20]        │
 │  [obj -> #123] │
 └───────────────┘
 
 ┌───────────────┐
 │    Heap        │  -> objects, arrays, functions
 │ #123 {name:"Ali"} │
 │ #124 [1,2,3]      │
 └───────────────┘
```

---

## 🧠 Qisqa Xulosa
- **Stack** → joy ajratish = pointerni siljitish (tez).  
- **Heap** → joy ajratish = bo‘sh joy qidirish + GC boshqaruvi (sekinroq).  
- **Garbage Collector** → keraksiz ma’lumotlarni tozalab, RAMni “yuvib” turadi.  

---

❓Endi savol: xohlaysanmi, men senga **Garbage Collector qanday ishlashini animatsiya-style diagramma** qilib chizib beray? Shunda qanday qilib eski objectlar o‘chirilishini jonli ko‘rgan bo‘larding.

---

### 👤 Foydalanuvchi:

stringga  ramdan foydalaninsh massiv qoidasi ishlaydimi yani agar string ma'lumot turgan joyda yangi qiymat qo'shish uchin xotira katakchalari yetmasa butunlay stringni boshqa joyga ko'chirililadimi

### 🤖 ChatGPT:

Ooo, endi sen “low-level string memory management” darajasiga kirib ketyapsan 😎. Juda to‘g‘ri savol berding: **string RAM’da massiv kabi saqlanadimi?** va **agar joy yetmasa nima bo‘ladi?**  

Keling, toza qilib ajratib beraman:  

---

## 🔹 1. String = massivga o‘xshaydi, lekin...
- Ha, string **RAM ichida ketma-ket katakchalarda (array kabi)** saqlanadi.  
- Har bir belgiga **UTF-16 code unit** joylashadi (JavaScript string’lari UTF-16’da saqlanadi).  
- Masalan, `"Ali"` → `[65][108][105]` tarzda RAM’da ketma-ket joylashadi.  

---

## 🔹 2. String **immutable**
- JavaScript’da string **o‘zgarmas** (immutable).  
- Demak, sen `"Ali"` stringiga `" Vali"` qo‘shmoqchi bo‘lsang → u asl stringni kengaytirmaydi.  
- Balki, **yangi RAM joy ajratiladi** va eski stringdan belgilar ko‘chirilib, yangi belgilar qo‘shiladi.  

👉 Bu sen aytgandek, massiv qoidasi ishlamaydi. C/C++ dagi `char[]` massivida joy yetmasa realloc yoki qo‘shni katakchalar ishlatiladi. Lekin JS string’da **har safar yangi string** yaratib yuboriladi.  

---

## 🔹 3. Joy yetmasa nima bo‘ladi?
- Agar `"Ali"` saqlanayotgan joyning yonida bo‘sh katakchalar bo‘lmasa, **yangi joy heap’da ajratiladi**.  
- Eski string (“Ali”) o‘z holicha turaveradi.  
- Yangi string (“Ali Vali”) butunlay boshqa joyda yaratiladi.  
- Stack’dagi reference endi yangi joyni ko‘rsatadi, eski string esa **garbage collector** tomonidan keyinchalik o‘chiriladi (agar boshqa reference bo‘lmasa).  

---

## 🔹 4. Diagramma

```
Heap:
 [#101] "Ali"   ----┐
                     │
Stack:               │
 [s -> #101] --------┘

s = s + " Vali";

Heap:
 [#101] "Ali"
 [#102] "Ali Vali"   ----┐
                         │
Stack:                   │
 [s -> #102] ------------┘
```

👉 Ko‘ryapsanmi, string joyini kengaytirib qo‘yilmaydi, **butunlay yangi string** boshqa joyda paydo bo‘ladi.  

---

## 🧠 Xulosa
- Ha, string RAM’da massiv kabi saqlanadi (UTF-16 code units).  
- Ammo JS string **immutable** → joy yetmasa, yangisi boshqa joyda yaratiladi.  
- Eski string GC kelguncha turaveradi.  

---

❓Xohlaysanmi men senga **C/C++ string (mutable)** bilan **JS string (immutable)** RAM’da qanday farq qilishini yonma-yon diagramma qilib ko‘rsatib beray? Shunda “nima uchun JS stringni qo‘shish sekinroq” ekanini ham ko‘rasan.

---

### 👤 Foydalanuvchi:

HEAP da Linkid LIst qoidasi ishlaydimi yani POINTR kabi

### 🤖 ChatGPT:

O‘sha joyini juda to‘g‘ri ushlading, Fayzillo 👌. Endi bu narsani yaxshilab ochib beraman:  

---

## 🔹 Heap’da “Linked List” qoidasi ishlaydimi?
- **Heapning o‘zi** → oddiygina katta bo‘sh RAM hududi. Unda qanday qilib ma’lumot saqlanishi – bu **data structure** (ma’lumot tuzilmasi)ga bog‘liq.  
- Ya’ni, **JavaScript objectlari, arraylari, functionlari** — hammasi **Heap’da joylashadi**, lekin ular qanday joylashishini **JS engine (V8, SpiderMonkey, Chakra...)** hal qiladi.  

👉 **Linked List** qoidasi Heap’da avtomatik ishlamaydi, lekin:  
- **Heapdagi objectlar** o‘zaro **reference (pointer)** orqali bog‘lanishi mumkin.  
- Bu reference — **Linked List pointeri**ga juda o‘xshaydi.  

---

## 🔹 Misol: Linked List JS’da
JavaScript pointer’ni bevosita ko‘rsatmaydi, lekin **object reference** aslida RAM pointeridir.  

```js
let node1 = { value: 10, next: null };
let node2 = { value: 20, next: null };
node1.next = node2;

console.log(node1); 
// { value: 10, next: { value: 20, next: null } }
```

🔍 Bu yerda:
- `node1` stack’da → Heap’dagi `{ value:10, next:null }`ga ko‘rsatadi.  
- `node2` ham stack’da → Heap’dagi boshqa objectga ko‘rsatadi.  
- `node1.next = node2` qilganingda → `node1` objecti ichida `node2`ning Heap’dagi addressiga reference saqlanadi.  

👉 Bu xuddi **Linked List pointer mantig‘i**.  

---

## 🔹 Aslida “pointer” nima bo‘ladi JS’da?
- C/C++ dagidek aniq **RAM manzilini** ko‘rsata olmaysan.  
- JS’da **reference** bor — bu aslida pointerning abstraktsiyasi.  
- Heap ichida obyektlar xotirada tarqoq joylashadi, lekin ular bir-birini “ko‘rsatib” bog‘lanishi mumkin → bu Linked List, Tree, Graph tuzish imkonini beradi.  

---

## 🔹 Diagramma (misol)
```js
let node1 = { val: 10, next: null };
let node2 = { val: 20, next: null };
node1.next = node2;
```

Heap:
```
[#101] { val: 10, next: #102 } --->  [#102] { val: 20, next: null }
```

Stack:
```
[node1 -> #101]
[node2 -> #102]
```

👉 Ko‘ryapsanmi, bu mutlaqo **pointer-style bog‘lanish**.  

---

## 🧠 Xulosa
- **Heapning o‘zi** Linked List qilmaydi, u faqat bo‘sh joy.  
- **Object reference** esa pointer vazifasini bajaradi.  
- Shuning uchun, JS’da Linked List, Tree, Graph tuzsa bo‘ladi → ular Heap’da pointer (reference) orqali bog‘lanadi.  

---

❓Xohlaysanmi men senga **Heap ichida Linked List qanday ko‘rinishini** bosqichma-bosqich diagramma qilib beray, masalan `1 -> 2 -> 3` list yaratib? Shunda RAM ichida qanday bog‘lanishini vizual ko‘rib olasan.

---


## Manba: `misc/sfmt.pdf`

SIMD-oriented Fast Mersenne Twister: a
128-bit Pseudorandom Number Generator ?
Mutsuo Saito1 and Makoto Matsumoto2
1 Dept. of Math. Hiroshima University saito@math.sci.hiroshima-u.ac.jp
2 Dept. of Math. Hiroshima University m-mat@math.sci.hiroshima-u.ac.jp
Summary. Mersenne Twister (MT) is a widely-used fast pseudorandom number
generator (PRNG) with a long period of 219937 −1, designed 10 years ago based
on 32-bit operations. In this decade, CPUs for personal computers have acquired
newfeatures,suchasSingleInstructionMultipleData(SIMD)operations(i.e.,128-
bit operations) and multi-stage pipelines. Here we propose a 128-bit based PRNG,
named SIMD-oriented Fast Mersenne Twister (SFMT), which is analogous to MT
but making full use of these features. Its recursion fits pipeline processing better
than MT, and it is roughly twice as fast as optimised MT using SIMD operations.
Moreover, the dimension of equidistribution of SFMT is better than MT.
We also introduce a block-generation function, which fills an array of 32-bit
integers in one call. It speeds up the generation by a factor of two. A speed com-
parison with other modern generators, such as multiplicative recursive generators,
shows an advantage of SFMT. The implemented C-codes are downloadable from
http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/index.html.
1 Introduction
Recently, the scale of simulations is getting larger, and faster pseudorandom
number generators (PRNGs) are required. The power of CPUs for usual per-
sonal computers are now sufficiently strong for such purposes, and the ne-
cessity of efficient PRNGs for CPUs on PCs is increasing. One such gener-
ator is Mersenne Twister (MT) [11], which is based on a linear recursion
modulo 2 over 32-bit words. An implementation MT19937 has the period of
219937 −1. MT was designed 10 years ago, and the architectures of CPUs,
such as Pentium and PowerPC, have changed. They have Single Instruction
Multiple Data (SIMD) operations, which may be regarded as operations on
128-bit registers. Also, they have more registers and automatic parallelisms
by multi-stage pipelining. These are not reflected in the design of MT.
? This study is partially supported by JSPS/MEXT Grant-in-Aid for Scientific
ResearchNo.18654021,No.16204002,andJSPSCore-to-CoreProgramNo.18005.
2 Mutsuo Saito and Makoto Matsumoto
In this article, we propose an MT-like pseudorandom number generator
that makes full use of these new features: SFMT, a SIMD-oriented Fast
Mersenne Twister. We implemented an SFMT with the period a multiple
of 219937−1, named SFMT19937, which has a better equidistribution prop-
erty than MT. SFMT is much faster than MT, even without using SIMD
instructions.
There is an argument that the CPU time consumed for function calls
to PRNG routines occupies a large part of the random number generation.
This is not always the case: one can avoid the function calls by (1) inline-
expansion and/or (2) generation of pseudorandom numbers in an array in
one call. Actually some demanding users re-coded MT to avoid the function
call; see the homepage of [11]. In this article, we introduce a block-generation
scheme which is much faster than using function calls.
2 SIMD-oriented Fast Mersenne Twister
We propose a SIMD-oriented Fast Mersenne Twister (SFMT) pseudorandom
number generator. It is a Linear Feedbacked Shift Register (LFSR) generator
based on a recursion over F128. We identify the set of bits {0,1} with the two
2
element field F . This means that every arithmetic operation is done modulo
2
2. A w-bit integer is identified with a horizontal vector in Fw, and + denotes
2
the sum as vectors (i.e., bit-wise exor), not as integers. We consider three
cases: w is 32, 64 or 128.
2.1 LFSR generators
A LFSR method is to generate a sequence x ,x ,x ,... of elements Fw by a
0 1 2 2
recursion
x :=g(x ,x ,...,x ), (1)
i+N i i+1 i+N−1
where x ∈ Fw and g : (Fw)N → Fw is an F -linear function (i.e., the multi-
i 2 2 2 2
plication of a (wN ×w)-matrix from the right to a wN-dimensional vector)
and use it as a pseudorandom w-bit integer sequence. In the implementation,
thisrecursioniscomputedbyusinganarrayW[0..N-1]ofN integersofw-bit
size, by the simultaneous substitutions
W[0]←W[1], W[1]←W[2], ...,W[N−2]←W[N−1], W[N−1]←g(W[0],...,W[N−1]).
The first N −1 substitutions shift the content of the array, hence the name
of LFSR. Note that in the implementation we may use an indexing technique
to avoid computing these substitutions, see [5, P.28 Algorithm A]. The array
W[0..N-1] is called the state array. Before starting the generation, we need
to set some values to the state array, which is called the initialization.
Mersenne Twister (MT) [11] is an example with
SIMD-oriented Fast Mersenne Twister 3
g(w ,...,w )=(w |w )A+w ,
0 N−1 0 1 M
where (w |w ) denotes the concatenation of the 32−r most significant bits
0 1
(MSBs) of w and the r least significant bits (LSBs) of w , A is a (32×32)-
0 1
matrixforwhichthemultiplicationwAiscomputablebyafewbit-operations,
and M is an integer (1 < M < N). Its period is 232N−r −1, chosen to be a
Mersenneprime.Toobtainabetterequidistributionproperty,MTtransforms
the sequence by a suitably chosen (32×32) matrix T, namely, MT outputs
x T,x T,x T,... (called tempering).
0 1 2
2.2 New features of modern CPUs for personal computers
ModernCPUsforpersonalcomputers(e.g.PentiumandPowerPC)havenew
features such as (1) fast integer multiplication instructions (2) fast floating
point operations (3) SIMD operations (4) multi-stage pipelining. These were
not common to standard PC CPUs, when MT was designed.
AnadvantageofF -lineargeneratorsoverintegermultiplicationgenerators
2
(suchasLinearCongruentialGenerators[5]orMultipleRecursiveGenerators
[6]) was high-speed generation by avoiding multiplications. This advantage is
now smaller, since 32-bit integer multiplication is now quite fast.
Among the new features, (3) and (4) fit F -linear generators. Our idea
2
is simple: to design a 128-bit integer PRNG, considering the benefit of such
parallelism in the recursion.
2.3 The recursion of SFMT
We choose g in the recursion (1) as
g(w ,...,w )=w A+w B+w C+w D, (2)
0 N−1 0 M N−2 N−1
where w ,w ,... are w(= 128)-bit integers (= horizontal vectors in F128),
0 M 2
andA,B,C,Daresparse128×128matricesoverF forwhichwA,wB,wC,wD
2
can be computed by a few SIMD bit-operations. The choice of the suffixes
N −1, N −2 is for speed: in the implementation of g, W[0] and W[M] are
read from the array W, while the copies of W[N-2] and W[N-1] are kept in two
128-bit registers in the CPU, say r1 and r2. Concretely speaking, we assign
r2←r1andr1←“the result of (2)”ateverygeneration,thenr2(r1)keeps
a copy of W[N-2] (W[N-1], respectively). The merit of doing this is to use the
pipelineeffectively.TofetchW[0]andW[M]frommemorytakessometime.In
the meantime, the CPU can compute w C and w D, because copies of
N−2 N−1
w and w are kept in the registers. This selection was made through
N−2 N−1
experiments on the speed of generation.
By trial and error, we searched for a set of parameters of SFMT, with
the period being a multiple of 219937 −1 and having good equidistribution
properties. The degree of recursion N is d19937/128e = 156, and the linear
transformations A,B,C,D are as follows.
4 Mutsuo Saito and Makoto Matsumoto
128
• wA:=(w<<8)+w.
This notation means that w is regarded as a single 128-bit integer, and
wA is the result of the left-shift of w by 8 bits. There is such a SIMD
operation in both Pentium SSE2 and PowerPC AltiVec SIMD instruction
sets (SSE2 permits only a multiple of 8 as the amount of shifting). Note
that the notation + means the exclusive-or in this article.
32
• wB :=(w>>11)&(BFFFFFF6 BFFAFFFF DDFECB7F DFFFFFEF).
This notation means that w is considered to be a quadruple of 32-bit
integers, and each 32-bit integer is shifted to the right by 11 bits, (thus
the eleven most significant bits are filled with 0s, for each 32-bit integer).
The C-like notation & means the bitwise AND with a constant 128-bit
integer, denoted in the hexadecimal form.
Inthesearch,thisconstantisgeneratedasfollows.Eachbitinthe128-bit
integerisindependentlyrandomlychosen,withtheprobabilitytochoose1
being7/8.Thisisbecauseweprefertohavemore1’sforadenserfeedback.
128
• wC :=(w>>8).
This is the right shift of an 128-bit integer by 8 bits, similar to the first.
32
• wD :=(w<<18).
Similartothesecond,w iscutintofourpiecesof32-bitintegers,andeach
of these is shifted by 18 bits to the left.
All these instructions are available in both Intel Pentium’s SSE2 and Pow-
erPC’s AltiVec SIMD instruction sets. Figure 1 shows a concrete description
of SFMT19937 generator with period a multiple of 219937−1.
128 bit
W0
1
<
2
<
88
AND
0xBFFFFFF6
W122 3 > 2 >11 0xBFFAFFFF +
0xDDFECB7F
0xDFFFFFEF
1 > 2 > 8 8
W154
W155 3 < 2 <18
Fig. 1. A circuit-like description of SFMT19937.
2.4 Endianness
Let x[0..3] be an array of 32-bit integers of size four. There are two natural
ways to convert the array to a 128-bit integer. One is to concatenate in the
SIMD-oriented Fast Mersenne Twister 5
orderofx[3]x[2]x[1]x[0],fromMSBstoLSBs,whichiscalledthelittle-endian
system, adopted in Pentium. The converse is the big-endian system adopted
in PowerPC, see [18].
The descriptions in this article is based on the former. To assure the
portability for both endian systems, we implemented two codes: one is for
little-endiansystem(SSE2ofPentium)andtheotherisforbig-endiansystem
(AltiVec of PowerPC), to assure the exactly same outputs as 32-bit integer
generators.Inthelattercode,therecursion(2)isconsideredasarecursionon
quadruplesof32-bitintegers,ratherthan128-bitintegers,sothatthecontent
ofthestatearraycoincidesbothforlittleandbigendiansystems,asanarray
of 32-bit integers (not as 128-bit integers). Thus, shift-operations on 128-bit
integersinthelittle-endiansystemisdifferentfromthatinthebig-endiansys-
tem. PowerPC supports arbitrary permutations of 16 blocks of 8-bit integers
in a 128-bit register, which can emulate the shift in (2).
2.5 Block-generation
Intheblock-generationscheme,theuserofthePRNGspecifiesanarrayofw-
bitintegersofthelengthL,wherew =32,64or128andLisspecifiedbythe
user. In the case of SFMT19937, wL should be a multiple of 128 and no less
than N ×128, since the array needs to accommodate the state space (note
that N = 156). By calling the block generation function with the pointer
to this array, w, and L, the routine fills up the array with pseudorandom
integers, as follows. SFMT19937 keeps the state space S in an internal array
of 128-bit integers of length 156. We concatenate this state array with the
user-specifiedarray,usingtheindexingtechnique.Then,theroutinegenerates
128-bit integers in the user-specified array by recursion (2), as described in
Figure 2, until it fills up the array. The last 156 128-bit integers are copied
back to the internal array of SFMT19937. This makes the generation much
faster than sequential generation (i.e., one generation per one call) as shown
in Table 1.
3 How to select the recursion and parameters.
Wewroteacodetocomputetheperiodandthedimensionsofequidistribution
(DE, see §3.2). Then, we searched for a recursion with good DE admitting a
fast implementation.
3.1 Computation of the Period
An LFSR that obeys the recursion (1) may be considered as an automaton,
with the state space S = (Fw)N and the state transition function f : S → S
2
given by (w ,...,w ) 7→ (w ,...,w ,g(w ,...,w )). As a w-bit
0 N−1 1 N−1 0 N−1
integer generator, the output function is o:S →Fw, (w ,...,w )7→w .
2 0 N−1 0
6 Mutsuo Saito and Makoto Matsumoto
128 bit
g
internal
156
array
user-
L specified
array
g
156 copied
back to
internal
array
Fig. 2. Block-generation scheme
Let χ be the characteristic polynomial of f : S → S. If χ is primitive,
f f
then the period of the state transition takes the maximal value 2dim(S)−1 [5,
§3.2.2]. However, to check the primitivity, we need the integer factorization
of this number, which is often hard for dim(S) = nw > 10000. On the other
hand, the primarity test is much easier than the factorization, so many huge
primes of the form 2p−1 have been found. Such a prime is called a Mersenne
prime, and p is called the Mersenne exponent, which itself is a prime.
MTandWELL[15]discardr specificbitsfromthearrayS,sothatnw−r
is a Mersenne exponent. Then, the primitivity of χ is easily checked by the
f
algorithm in [5, §3.2.2], avoiding the integer factorization.
SFMT adopted another method to avoid the integer factorization, the re-
ducible transition method (RTM), which uses a reducible characteristic poly-
nomial with a large primitive factor. This idea appeared in [4] [1][2], and
applications in the present context are discussed in detail in another article
[16], therefore we only briefly recall it.
Let p be the Mersenne exponent, and N := dp/we. Then, we randomly
chooseparametersfortherecursionofLFSR(1).ByapplyingtheBerlekamp-
MasseyAlgorithmtotheoutputsequence,weobtainχ (t).(Notethatadirect
f
computation of det(tI−f) is time-consuming because dim(S)=19968.)
By using a sieve, we remove all factors of small degree from χ , until we
f
know that it has no irreducible factor of degree p, or that it has a (possibly
reducible) factor of degree p. In the latter case, the factor is passed to the
primitivity test described in [5, §3.2.2].
Suppose that we found a recursion with an irreducible factor of desired
degree p in χ (t). Then, we have a factorization
f
SIMD-oriented Fast Mersenne Twister 7
χ =φ φ ,
f p r
where φ is a primitive polynomial of degree p and φ is a polynomial of
p r
degree r = wN −p. These are coprime, since we assume p > r. Let Ker(g)
denote the kernel of a linear transformation g. By putting V := Ker(φ (f))
p p
and V :=Ker(φ (f)), we have a decomposition into f-invariant subspaces
r r
S =V ⊕V (dimV =p, dimV =r).
p r p r
Note that the characteristic polynomial of the restriction f of f to V is
p p
φ (t), and that of the restriction f to V is φ (t). For any state s ∈ S, we
p r r r
denote s = s +s for the corresponding decomposition with s ∈ V and
p r p p
s ∈ V . Then, the k-th state fk(s) is equal to fk(s )+fk(s ). This implies
r r p p r r
that the automaton is equivalent to the sum of two automata f : V → V
p p p
and f : V → V . To combine two linear automata by sum is well-studied
r r r
as combined Tausworthe generators or combined LFSRs, see [3] [7] [8]. Their
purpose is to obtain a good PRNG from several simple generators, which is
different from ours.
The period length of the state transition is the least common multiple of
that started from s and that started from s . Hence, if s 6= 0, then the
p r p
period is a nonzero multiple of 2p−1. We checked the following.
Proposition 1.The period of SFMT19937 as a 128-bit integer generator is
a nonzero multiple of 219937 −1, if the 32 MSBs of w are set to the value
0
6d736d6d in hexadecimal form.
This value of w assures that s 6=0, see [16] for a way to find such a value.
0 p
Remark 1.The number of non-zero terms in χ (t) is an index measuring the
f
amount of bit-mixing. In the case of SFMT19937, the number of nonzero
terms is 6711, which is much larger than 135 of MT, but smaller than 8585
of WELL19937c [15].
3.2 Computation of the dimension of equidistribution
We briefly recall the definition of dimension of equidistribution (cf. [3][7]).
Definition 1. A periodic sequence with period P
χ:=x ,x ,...,x ,x =x ,...
0 1 P−1 P 0
of v-bit integers is said to be k-dimensionally equidistributed if any kv-bit
pattern occurs equally often as a k-tuple
(x ,x ,...,x )
i i+1 i+k−1
for a period i = 0,...,P − 1. We allow an exception for the all-zero pat-
tern, which may occur once less often. (This last loosening of the condition
is technically necessary, because the zero state does not occur in an F -linear
2
generator). The largest value of such k is called the dimension of equidistri-
bution (DE).
8 Mutsuo Saito and Makoto Matsumoto
We want to generalize this definition slightly. We define the k-window set
of the periodic sequence χ as
W (χ):={(x ,x ,...,x )|i=0,1,...,P −1},
k i i+1 i+k−1
which is considered as a multi-set, namely, the multiplicity of each element is
considered.
Forapositiveintegermandamulti-setT,letusdenotebym·T themulti-
set where the multiplicity of each element in T is multiplied by m. Then, the
above definition of equidistribution is equivalent to
W (χ)=(m·Fvk)\{0},
k 2
wheremisthemultiplicityoftheoccurrences,andtheoperator\meansthat
the multiplicity of 0 is subtracted by one.
Definition 2. In the above setting, if there exist a positive integer m and a
multi-subset D ⊂(m·Fvk) such that
2
W (χ)=(m·Fvk)\D,
k 2
we say that χ is k-dimensionally equidistributed with defect ratio #(D)/#(m·
Fvk), where the cardinality is counted with multiplicity.
2
Thus, in Definition 1, the defect ratio up to 1/(P +1) is allowed to claim the
dimension of equidistribution. If P =219937−1, then 1/(P +1)=2−19937. In
the following, the dimension of equidistribution allows the defect ratio up to
2−19937.
For a w-bit integer sequence, its dimension of equidistribution at v-bit ac-
curacyk(v)isdefinedastheDEofthev-bitsequence,obtainedbyextracting
the v MSBs from each of the w-bit integers. If the defect ratio is 1/(P +1),
then there is an upper bound
k(v)≤blog (P +1)/vc.
2
Thegapbetweentherealizedk(v)andtheupperboundiscalledthedimension
defect at v of the sequence, and denoted by
d(v):=blog (P +1)/vc−k(v).
2
The summation of all the dimension defects at 1≤v ≤32 is called the total
dimension defect, denoted by ∆.
There is a difficulty in computing k(v) when a 128-bit integer generator
is used as a 32-bit (or 64-bit) integer generator. SFMT generates a sequence
x ,x ,x ,...of128-bitintegers.Then,theyareconvertedtoasequenceof32-
0 1 2
bit integers x [0],x [1],x [2],x [3],x [0],x [1],..., where x[0] is the 32 LSBs
0 0 0 0 1 1
of x, x[1] is the 33rd–64th bits, x[2] is the 65rd–96th bits, and x[3] is the 32
MSBs.
SIMD-oriented Fast Mersenne Twister 9
Then,weneedtomodifythemodelautomatonasfollows.Thestatespace
is S0 :=S×{0,1,2,3}, the state transition function f0 :S0 →S0 is
(cid:189)
(s,i+1)( if i<3),
f0(s,i):=
(f(s),0) ( if i=3)
and the output function is
o0 :S0 →F32, ((w ,...,w ),i)7→w [i].
2 0 N−1 0
We fix 1 ≤ v ≤ w, and let o (s,i) be the k-tuple of the v MSBs of the
k
consecutive k-outputs from the state (s,i).
Proposition 2.Assume that f is bijective. Let k0 = k0(v) denote the maxi-
mum k such that
o (−,i):V →Fkv, s7→o (s,i) (3)
k p 2 k
are surjective for all i = 0,1,2,3. Take an initial state s satisfying s 6= 0.
p
Then,the32-bitoutputsequenceisatleastk0(v)-dimensionallyequidistributed
with v-bit accuracy with defect ratio 2−p.
Moreover, if 4 < k0(v)+1, then for any initial state with s = s 6= 0
p
(hence s = 0), the dimension of equidistribution with defect ratio 2−p is
r
exactly k0(v).
Proof. Take s ∈ S with s 6= 0. Then, the orbit of s by f has the form of
p
(V −{0})×U ⊂V ×V , since p>r and 2p−1 is a prime. The surjectivity
p p r
of the linear mapping o (−,i) implies that the image of
k0
o (−,i):V ×U →Fkv
k0 p 2
is m·Fkv as a multi-set for some m. The defect comes from 0 ∈ V , whose
2 p
ratio in V is 2−p. Then the first statement follows, since W (χ) is the union
p k0
of the images o (−,i)((V −{0})×U) for i=0,1,2,3.
k0 p
Forthelatterhalf,wedefineL asthemultisetoftheimageofo (−,i):
i k0+1
V →
F(k0+1)v.
Because of s = 0, we have U = {0}, and the union of
p 2 r
(L − {0}) (i = 0,1,2,3) as a multi-set is W (χ). If the sequence is
i k0+1
(k0+1)-dimensionally equidistributed, then the multiplicity of each element
in W (χ) is at most 2p×4/2(k0+1)v.
k0+1
On the other hand, the multiplicity of an element in L is equal to the
i
cardinality of the kernel of o (−,i). Let d be its dimension. Then by
k0+1 i
the dimension theorem, we have d ≥ p−(k0 +1)v, and the equality holds
i
if and only if o (−,i) is surjective. Thus, if there is a nonzero element
k0+1
x ∈ ∩3 L , then its multiplicity in W (χ) is no less than 4×2p−(k0+1)v,
i=0 i k0+1
and since one of o (−,i) is not surjective by the definition of k0, its multi-
k0+1
plicity actually exceeds 4×2p−(k0+1)v, which implies that the sequence is not
(k0+1)-dimensionally equidistributed, and the proposition follows. Since the
codimension of L is at most v, that of ∩3 L is at most 4v. The assumed
i i=0 i
inequality on k0 implies the existence of nonzero element in the intersection.
10 Mutsuo Saito and Makoto Matsumoto
Thedimensionofequidistributionk(v)dependsonthechoiceoftheinitial
state s. The above proposition implies that k0(v) coincides with k(v) for the
worst choice of s under the condition s 6= 0. Thus, we adopt the following
p
definition (analogously to t in [7]).
l
Definition 3. Let k be the maximum such that (3) is satisfied. We call this
the dimension of equidistribution of v-bit accuracy, and denote it simply by
k(v). We have an upper bound k(v)≤bp/vc.
We define the dimension defect at v by
(cid:88)w
d(v):=bp/vc−k(v) and ∆:= d(v).
v=1
We may compute k(v) by standard linear algebra. We used a more efficient
algorithm based on a weighted norm, generalizing [3]. This will be written
somewhere else, because of lack of space.
4 Comparison of speed
We compared two algorithms: MT19937 and SFMT19937, with implementa-
tions using and without using SIMD instructions.
We measured the speeds for four different CPUs: Pentium M 1.4GHz,
Pentium IV 3GHz, AMD Athlon 64 3800+, and PowerPC G4 1.33GHz. In
returningtherandomvalues,weusedtwodifferentmethods.Oneissequential
generation,whereone32-bitrandomintegerisreturnedforonecall.Theother
is block generation, where an array of random integers is generated for one
call (cf. [5]). For detail, see §2.5 below.
We measured the consumed CPU time in second, for 108 generations of
32-bit integers. More precisely, in case of the block generation, we generate
105 of 32-bit random integers by one call, and this is iterated for 103 times.
Forsequentialgeneration,thesame108 32-bitintegersaregenerated,oneper
call.Weusedtheinlinedeclarationinlinetoavoidthefunctioncall,andun-
signed 32-bit, 64-bit integer types uint32 t, uint64 t defined in INTERNA-
TIONAL STANDARD ISO/IEC 9899 : 1999(E) Programming Language-C,
Second Edition (which we shall refer to as C99 in the rest of this article). Im-
plementations without SIMD are written in C99, whereas those with SIMD
use some standard SIMD extension of C99 supported by the compilers icl
(Intel C compiler) and gcc.
Table 1 summarises the speed comparisons. The first four lines list the
CPU time (in seconds) needed to generate 108 32-bit integers, for a Pentium-
M CPU with the Intel C/C++ compiler. The first line lists the seconds for
the block-generation scheme. The second line shows the ratio of CPU time to
that of SFMT(SIMD). Thus, SFMT coded in SIMD is 2.10 times faster than
MTcodedinSIMD,and3.77timesfasterthanMTwithoutSIMD.Thethird
SIMD-oriented Fast Mersenne Twister 11
line lists the seconds for the sequential generation scheme. The fourth line
lists the ratio, with the basis taken at SFMT(SIMD) block-generation (not
sequential). Thus, the block-generation of SFMT(SIMD) is 2.00 times faster
than the sequential-generation of SFMT(SIMD).
Roughly speaking, in the block generation, SFMT(SIMD) is twice as fast
as MT(SIMD), and four times faster than MT without using SIMD. Even in
the sequential generation case, SFMT(SIMD) is still considerably faster than
MT(SIMD).
CPU/compiler return MT MT(SIMD)SFMTSFMT(SIMD)
Pentium-M block 1.122 0.627 0.689 0.298
1.4GHz (ratio) 3.77 2.10 2.31 1.00
Intel C/C++ seq 1.511 1.221 1.017 0.597
ver. 9.0 (ratio) 5.07 4.10 3.41 2.00
Pentium IV block 0.633 0.391 0.412 0.217
3GHz (ratio) 2.92 1.80 1.90 1.00
Intel C/C++ seq 1.014 0.757 0.736 0.412
ver. 9.0 (ratio) 4.67 3.49 3.39 1.90
Athlon 64 3800+ block 0.686 0.376 0.318 0.156
2.4GHz (ratio) 4.40 2.41 2.04 1.00
gcc seq 0.756 0.607 0.552 0.428
ver. 4.0.2 (ratio) 4.85 3.89 3.54 2.74
PowerPC G4 block 1.089 0.490 0.914 0.235
1.33GHz (ratio) 4.63 2.09 3.89 1.00
gcc seq 1.794 1.358 1.645 0.701
ver. 4.0.0 (ratio) 7.63 5.78 7.00 2.98
Table1.TheCPUtime(sec.)for108generationsof32-bitintegers,forfourdifferent
CPUs and two different return-value methods. The ratio to the SFMT coded in
SIMD is listed, too.
CPU return mrg rand48 rand random256g2 well xor3
Pentium M block 3.277 1.417 0.453 0.230 1.9700.296
seq 3.255 1.417 0.527 0.610 2.2661.018
Pentium IV block 2.295 1.285 0.416 0.121 0.9190.328
seq 2.395 1.304 0.413 0.392 1.0330.702
Athlon block 1.781 0.770 0.249 0.208 0.7530.294
seq 1.798 0.591 0.250 0.277 0.8740.496
PowerPC block 2.558 1.141 0.411 0.653 1.7920.618
seq 2.508 1.132 0.378 1.072 1.7621.153
Table 2. The CPU time (sec.) for 108 generations of 32-bit integers, by six other
PRNGs.
12 Mutsuo Saito and Makoto Matsumoto
Table 2 lists the CPU time for generating 108 32-bit integers, for four
PRNGs from the GNU Scientific Library and two recent generators. They
are re-coded with inline specification. Generators examined were: a multi-
ple recursive generator mrg [6], linear congruential generators rand48 and
rand, a lagged fibonacci generator random256g2, a WELL generator well
(WELL19937c in [15]), and a XORSHIFT generator xor3 [14] [10]. The ta-
ble shows that SFMT(SIMD) is faster than these PRNGs, except for the
outdated linear congruential generator rand, the lagged-fibonacci generator
random256g2 (which is known to have poor randomness, cf. [13]), and xor3
with a Pentium-M.
5 Dimension of equidistribution
Table 3 lists the dimension defects d(v) of SFMT19937 (as a 32-bit integer
generator) and of MT19937, for v =1,2,...,32. SFMT has smaller values of
the defect d(v) at 26 values of v. The converse holds for 6 values of v, but the
difference is small. The total dimension defect ∆ of SFMT19937 as a 32-bit
integer generator is 4188, which is smaller than the total dimension defect
6750 of MT19937.
v MTSFMT v MTSFMT v MTSFMT v MTSFMT
d(1) 0 0 d(9) 346 1 d(17) 549 543 d(25) 174 173
d(2) 0 *2 d(10) 124 0 d(18) 484 478 d(26) 143 142
d(3) 405 1 d(11) 564 0 d(19) 426 425 d(27) 115 114
d(4) 0 *2 d(12) 415 117 d(20) 373 372 d(28) 89 88
d(5) 249 2 d(13) 287 285 d(21) 326 325 d(29) 64 63
d(6) 207 0 d(14) 178 176 d(22) 283 282 d(30) 41 40
d(7) 355 1 d(15) 83 *85 d(23) 243 242 d(31) 20 19
d(8) 0 *1 d(16) 0 *2 d(24) 207 206 d(32) 0 *1
Table 3. Dimension defects d(v) of MT19937 and SFMT19937 as a 32-bit integer
generator. The mark * means that MT has a smaller defect than SFMT at that
accuracy.
We also computed the dimension defects of SFMT19937 as a 64-bit (128-
bit) integer generator, and the total dimension defect ∆ is 14089 (28676,
respectively). In some applications, the distribution of LSBs is important. To
check them, we inverted the order of the bits (i.e. the i-th bit is exchanged
with the (w−i)-th bit) in each integer, and computed the total dimension
defect. It is 10328 (21337, 34577, respectively) as a 32-bit (64-bit, 128-bit,
respectively) integer generator. Throughout the experiments, d0(v) is very
small for v ≤10. We consider that these values are satisfactorily small, since
theyarecomparablewithMTforwhichnostatisticaldeviationrelatedtothe
dimension defect has been reported, as far as we know.
SIMD-oriented Fast Mersenne Twister 13
6 Recovery from 0-excess states
For an LFSR with a sparse feedback function g, we observe the following
phenomenon: if the bits in the state space contain too many 0’s and few 1’s
(called a 0-excess state), then this tendency continues for many steps, since
only a small part is changed in the state array at one step, and the change is
not well-reflected to the next setp because of the sparseness.
We measure the recovery time from 0-excess states, by the method intro-
duced in [15], as follows.
1. Choose an initial state with only one bit being 1.
2. Generate k pseudorandom numbers, and discard them.
3. Compute the ratio of 1’s among the next 32000 bits of outputs (i.e., in
the next 1000 pseudorandom 32-bit integers).
4. Let γ be the average of the ratio over all such initial states.
k
We draw graphs of these ratio γ (1≤k ≤20000) in Figure 3 for the follow-
k
ing generators: (1) WELL19937c, (2) PMT19937 [16], (3) SFMT19937, and
(4) MT19937. Because of its dense feedback, WELL19937c shows the fastest
0.5
WELLc
PMT
SFMT
0.4 MT
0.3
0.2
0.1
0
0 5000 10000 15000 20000
Fig. 3. γ (k = 0,...,20000): Starting from extreme 0-excess states, discard the
k
firstk outputsandthenmeasuretheratioγ of1’sinthenext1000outputs.Inthe
k
orderoftherecoveryspeed:(1)WELL19937c,(2)PMT19937,(3)SFMT19937,and
(3) MT19937.
recovery among the compared generators. SFMT is better than MT, since its
recursion refers to two most recently computed words (W[N-1] and W[N-2])
that acquire new 1s, while MT refers only to the words generated long before
(W[M] and W[0]). PMT19937 shows faster recovery than SFMT19937, since
PMT19937hastwofeedbackloops.Thespeedofrecoveryfrom0-excessstates
is a trade-off with the speed of generation. Such 0-excess states will not hap-
pen practically, since the probability that 19937 random bits have less than
14 Mutsuo Saito and Makoto Matsumoto
19937×0.4 of 1’s is about 5.7×10−177. The only plausible case would be
that a poor initialization scheme gives a 0-excess initial state (or gives two
initial states whose Hamming distance is too small). In a typical simulation,
the number of initializations is far smaller than the number of generations,
therefore we may spend more CPU time in the initialization than the genera-
tion. Under the assumption that a good initialization scheme is provided, the
slower recovery of SFMT compared to WELL would perhaps not be a great
issue.
7 Concluding remarks
WeproposedtheSFMTpseudorandomnumbergenerator,whichisaveryfast
generator with satisfactorily high-dimensional equidistribution property.
It is difficult to measure the generation speed of a PRNG in a fair way,
since it depends heavily on the circumstances. The WELL [15] generators
have the best possible dimensions of equidistribution (i.e. ∆=0) for various
periods (21024−1 to 219937−1). If we use the function call to the PRNG for
each generation, then a large part of the CPU time is consumed for handling
the function call, and in the experiments in [15] or [14], WELL is not much
slower than MT. On the other hand, if we avoid the function call, WELL is
slower than MT for some CPUs, as seen in Table 1.
Since∆=0,WELLhasabetterqualitythanMTorSFMTinatheoretical
sense.However,onemayarguewhetherthisdifferenceisobservableornot.In
the case of an F -linear generator, the dimension of equidistribution k(v) of
2
v-bit accuracy means that there is no constant linear relation among the kv
bits, but there exists a linear relation among the (k+1)v bits, where kv bits
((k+1)v bits) are taken from all the consecutive k integers (k+1 integers,
respectively) by extracting the v MSBs from each. However, the existence of
a linear relation does not necessarily mean the existence of some observable
bias.Accordingto[12],itrequires1028 samplestodetectanF -linearrelation
2
with 15 (or more) terms among 521 bits, by weight distribution test. If the
number of bits is increased, the necessary sample size is increased rapidly.
Thus, it seems that k(v) of SFMT19937 is sufficiently large, far beyond the
level of the observable bias. On the other hand, the speed of the generator
is observable. Thus, SFMT focuses more on the speed, for applications that
require fast generations. (Note: the referee pointed out that statistical tests
based on the rank of F -matrix is sensitive to the linear relations [9], so the
2
above observation is not necessarily true.)
There is a trade-off between the speed and portability. We prepared (1)
a standard C code of SFMT, which uses functions specified in C99 only, (2)
an optimized C code for Intel Pentium SSE2, and (3) an optimized C code
for PowerPC AltiVec. The optimized codes require the icl (Intel C Compiler)
or gcc compiler with suitable options. We had put and will keep the newest
version of the codes in the homepage [17].
SIMD-oriented Fast Mersenne Twister 15
References
1. R.P. Brent and P. Zimmermann. Random number generators with period di-
visible by a Mersenne prime. In Computational Science and its Applications -
ICCSA 2003, volume 2667, pages 1–10, 2003.
2. R.P. Brent and P.Zimmermann. Algorithms for finding almost irreducible and
almost primitive trinomials. Fields Inst. Commun., 41:91–102, 2004.
3. R. Couture, P. L’Ecuyer, and S. Tezuka. On the distribution of k-dimensional
vectors for simple and combined Tausworthe sequences. Math. Comp.,
60(202):749–761, 1993.
4. M.Fushimi. Randomnumbergenerationwiththerecursionx =x ⊕x .
t t−3p t−3q
Journal of Computational and Applied Mathematics, 31:105–118, 1990.
5. D. E. Knuth. The Art of Computer Programming. Vol.2. Seminumerical Algo-
rithms. Addison-Wesley, Reading, Mass., 3rd edition, 1997.
6. P. L’Ecuyer. A search for good multiple recursive random number genarators.
ACM Transactions on Modeling and Computer Simulation, 3(2):87–98, April
1993.
7. P.L’Ecuyer.Maximallyequidistributedcombinedtausworthegenerators. Math.
Comp., 65(213):203–213, 1996.
8. P. L’Ecuyer. Tables of maximally equidistributed combined lfsr generators.
Math. Comp., 68(225):261–269, 1999.
9. P.L’EcuyerandR.Simard.TestU01:AClibraryforempiricaltestingofrandom
number generators. ACM Transactions on Mathematical Software, 2006. to
appear.
10. G. Marsaglia. Xorshift RNGs. Journal of Statistical Software, 8(14):1–6, 2003.
11. M. Matsumoto and T. Nishimura. Mersenne twister: A 623-dimensionally
equidistributeduniformpseudorandomnumbergenerator.ACMTrans.onMod-
eling and Computer Simulation, 8(1):3–30, January 1998. http://www.math.
sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html.
12. M. Matsumoto and T. Nishimura. A nonempirical test on the weight of pseu-
dorandomnumbergenerators. InMonteCarloandQuasi-MonteCarlomethods
2000, pages 381–395. Springer-Verlag, 2002.
13. M.MatsumotoandT.Nishimura.Sum-discrepancytestonpseudorandomnum-
ber generators. Mathematics and Computers in Simulation, 62(3-6):431–442,
2003.
14. F.PannetonandP.L’Ecuyer.OntheXorshiftrandomnumbergenerators.ACM
Transactions on Modeling and Computer Simulation, 15(4):346–361, 2005.
15. F.Panneton,P.L’Ecuyer,andM.Matsumoto. Improvedlong-periodgenerators
based on linear reccurences modulo 2. ACM Transactions on Mathematical
Software, 32(1):1–16, 2006.
16. M. Saito, H. Haramoto, F. Panneton, T. Nishimura, and M. Matsumoto. Pul-
monary LFSR: pseudorandom number generators with multiple feedbacks and
reducible transitions. 2006. submitted.
17. M. Saito and M. Matsumoto. SFMT Homepage. http://www.math.sci.
hiroshima-u.ac.jp/~m-mat/MT/SFMT/index.html.
18. EndiannessfromWikipedia,thefreeencyclopedia. http://en.wikipedia.org/
wiki/Endianness.


## Manba: `my_digital_brain/30_Resources/scripting_tools/scripting/README.md`

# scripting_learinig

# Reja

- varieblelar bilan ishlash
- qiymatlar bilan ishlash
