# BRIEFING — 2026-09-06T22:30:00+05:00

## Mission
Investigate Telegram bot architecture, Telegraf regex collisions, channel/group permissions verification, and error containment in `/home/fayzillo/Desktop/Loyihalar/bot_post_using`.

## 🔒 My Identity
- Archetype: explorer
- Roles: Telegram Bot Architecture & Edge Cases Investigator
- Working directory: /home/fayzillo/Downloads/brains/.agents/explorer_2
- Original parent: 3ab1345d-8ae4-484d-ad0f-f9e0cd64e5e0
- Milestone: Investigation of Telegraf bot architecture, regex collisions, and permissions

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Write only inside /home/fayzillo/Downloads/brains/.agents/explorer_2
- Default Language: Uzbek
- Follow verification and evidence chain standards

## Current Parent
- Conversation ID: 3ab1345d-8ae4-484d-ad0f-f9e0cd64e5e0
- Updated: 2026-09-06T22:30:00+05:00

## Investigation State
- **Explored paths**:
  - `src/main.ts`, `src/app.module.ts`, `src/core/core.module.ts`
  - `src/core/bot_connector.service.ts`, `src/core/state.service.ts`, `src/core/message_queue.service.ts`
  - `src/global/user_filter/user_filter.guard.ts`, `src/global/errorhandler/all-exceptions.filter.ts`
  - `src/modules/admin/admin.update.ts`, `src/modules/admin/admin.service.ts`
  - `src/modules/channels/channels.service.ts`, `src/modules/groups/groups.service.ts`, `src/modules/posts/posts.service.ts`
  - `src/common/utils/_cb_functions/index.ts`, `src/common/utils/_message_generator/index.ts`
  - `history/task_001_...` through `history/task_021_...`, git history & commits
- **Key findings**:
  - Telegraf regex collision root cause: unanchored RegExp triggers matching compound/substring callbacks; resolved by adding `^` start anchors to all 11 action triggers and using non-capturing optional groups `/^back_to_posts(?::(.+))?/` for backward-compatible parametric navigation.
  - Channel vs Group permission matrix: distinct `getChatMember` checks (`can_post_messages` for channels, `status !== 'kicked'/'left'` and `can_send_messages !== false` for groups).
  - Exception containment during broadcast: individual try/catch blocks prevent 403 Forbidden on one chat from halting delivery to others; logging per-target failures in PostgreSQL and MongoDB.
  - 3-tier resilient state machine (Memory + Redis + MongoDB) avoiding Telegraf session data loss and handling BigInt serialization.
  - Defense against unauthorized bot addition via `@On('my_chat_member')` with immediate `leaveChat`.
- **Unexplored areas**: None within the assigned Explorer 2 scope.

## Key Decisions Made
- Fully documented all observations, logic chains, caveats, conclusions, and verification methods in `handoff.md`.
- Successfully verified project TypeScript compilation with `npm run build`.

## Artifact Index
- /home/fayzillo/Downloads/brains/.agents/explorer_2/DISPATCH.md — Task instructions from orchestrator
- /home/fayzillo/Downloads/brains/.agents/explorer_2/handoff.md — Complete 5-component technical handoff report
- /home/fayzillo/Downloads/brains/.agents/explorer_2/progress.md — Execution progress and timestamp heartbeat
