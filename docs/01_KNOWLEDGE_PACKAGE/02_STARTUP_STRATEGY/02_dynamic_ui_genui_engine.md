# ⚡ Dynamic UI (GenUI) & Client-Side Engine
**Idea Reference:** Parking Lot #16 & #17
**Author:** Fayzillo Ummatov

## 1. The Core Problem
In standard agency/SaaS workflows, frontend creation is the biggest bottleneck. Designing, coding, and binding state across 20+ screens takes 2-3 weeks per project.

## 2. The GenUI Solution
1. **Declarative Component Schema**:
   - The LLM emits a high-level JSON UI tree with standard design tokens and Tailwind utility mappings.
2. **Instant WebAssembly / React Runtime**:
   - Renders interactive forms, tables, metric cards, and charts in real-time without full rebuild cycles.
3. **Zero-Latency State Synchronization**:
   - React Query + WebSockets keep the dynamic UI instantly synced with NestJS backend state.
4. **Telegram Mini App (TMA) Optimization**:
   - Mobile-first card layouts (strictly adhering to mobile viewport rules with no overflowing tables).
