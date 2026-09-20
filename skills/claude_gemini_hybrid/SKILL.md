---
name: claude-gemini-hybrid
description: "Gibrid AI Dasturlash Tizimi: Claude'ni Bosh Arxitektor (Orchestrator), Gemini CLI (Antigravity)'ni esa Tezkor Ijrochi (Executer) sifatida birgalikda boshqarish skill to'plami."
---

# 🤖 Claude Orchestrator & Gemini Executer Hybrid Skill

Ushbu skill dasturlashda eng yuqori unumdorlikka erishish uchun ikki yetakchi AI modelining kuchli tomonlarini birlashtiradi:

1. **Claude (Sonnet / Opus) — The Orchestrator (Arxitektor & Strateg):**
   - Murakkab biznes-mantiq va arxitektura chizmalarini tuzadi.
   - Ko'rsatmalardan (Instructions) chetga chiqmaydi.
   - Katta vazifalarni aniq, kichik va mustaqil mini-topshiriqlarga (Atomic Tasks) bo'lib beradi.
   - Bajarilgan kod sifatini va edge-case'larni tekshiradi (Code Review).

2. **Gemini CLI / Antigravity — The Executer (Ijrochi & Kod Mashinasi):**
   - 1M+ kontekst oynasida to'liq loyiha fayllarini bir zumda o'qiydi.
   - Katta hajmdagi refaktoring, fayllar generatsiyasi va massiv o'zgarishlarni soniyalarda bajaradi.
   - Token limitlaridan xavotir olmasdan testlar va skriptlarni yurgizadi.

---

## 🔄 Gibrid Ishlash Sikli (Step-by-Step Workflow)

```
┌─────────────────────────────────────────────────────────────┐
│  1. CLAUDE ORCHESTRATOR                                     │
│  • Muammoni tahlil qiladi va arxitektura rejasini tuzadi    │
│  • Gemini uchun aniq `TASK_SPEC.md` tayyorlaydi             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  2. GEMINI EXECUTER (AGY CLI / ANTIGRAVITY)                 │
│  • `TASK_SPEC.md` ni o'qiydi                                │
│  • Fayllarni tahrirlaydi, kod yozadi, testlarni yurgizadi   │
│  • Natijalarni `EXECUTION_DIFF.md` ga yozadi                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  3. CLAUDE REVIEW & QA                                      │
│  • `EXECUTION_DIFF.md` ni o'qiydi                           │
│  • Xatolar yoki arxitektura buzilishlarini tekshiradi        │
│  • Keyingi bosqichga o'tadi yoki tuzatish beradi            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Qanday O'rnatish va Ishlatish?

1. Ushbu papkani loyihangizdagi `.gemini/skills/claude-gemini-hybrid/` yoki Claude Code maxsus papkasiga joylang.
2. Claude chatiga `templates/orchestrator_prompt.md` matnini Master Prompt sifatida bering.
3. Gemini CLI ga `templates/executer_prompt.md` matnini Ijrochi qoidasi sifatida bering.
