---
name: hermes-test-commands
description: Use when personalizing a Hermes Telegram command menu.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [hermes, telegram, commands, personalization]
---

# Hermes Test Commands

Make the Telegram `/` menu reflect commands the user actually sends, rather than a generic feature list. This is a small procedural skill, not a plugin or an automatic history collector.

## When to use

Use for inspecting, ranking or replacing a Hermes bot's slash-command suggestions. Do not use for changing command handlers, migrating profiles or enabling automatic monitoring.

## Required workflow

### 1. Inspect first

For questions about the current menu, inspect before suggesting possibilities or asking permission to look. Bind the actual bot identity, owning profile, running source and requested chat. Use the installed runtime and current official [Hermes documentation](https://hermes-agent.nousresearch.com/docs/), not an assumed checkout.

Read Telegram `getMyCommands` for the exact chat, its private/group scope and the default scope, checking the relevant language and empty-language fallback. Empty narrow scopes inherit broader menus; they do not imply an empty visible menu. Inspect the installed menu builder and registration writer: newer releases may locate the adapter inside a platform plugin.

### 2. Count real usage

Read only the authorized user's history, from all profiles only when requested. Inspect the current schema; do not assume a fixed database layout. Include real-user ingress records when direct handlers bypass conversational history. Verify sender identity per message where available; a session creator is not necessarily every message's author.

Count an actual leading slash invocation, not a mention in prose. Strip only verified transport headers and the complete quoted-reply envelope. Exclude assistant/tool output, generated summaries, scheduled prompts, agent messages and commands inside quotations or attachments. Deduplicate copied/branched/replayed inputs by stable platform, chat and message identity. Missing identities reduce confidence; disclose coverage instead of inventing exact all-time totals.

Keep raw history local. Retain only command names, aggregate counts and the minimum local evidence needed for verification. Do not publish a user's command inventory or usage profile.

### 3. Rank and reconcile

Sort by descending frequency; use most recent invocation to break ties and name as a final deterministic tie-breaker. Apply explicit user exclusions after ranking. Add optional utility commands only when approved; append them unless another order is requested. Omitted commands remain executable.

Check every proposed entry against the current handlers, skills and quick aliases. Menu discovery may omit a working quick alias; absence from the generated menu is not proof that its handler is missing. Conversely, adding a name to Telegram does not create a handler. Report unsupported historical names rather than silently repairing or renaming them.

### 4. Choose the narrowest persistent writer

For supported global cap/priority changes, use the installed configuration contract. Priority is not necessarily an exact-only allowlist, and quick aliases may not participate in the builder. Confirm behavior before editing. See [scope and persistence notes](references/telegram-scopes.md).

For one private chat, an explicitly scoped Telegram `BotCommandScopeChat` menu can be appropriate, but only after verifying that startup/reconnect and lazy writers will not overwrite it. Do not assume a private-chat recipe also works for forums. Preserve unrelated chats, languages, bots and profile configuration. Translate menu descriptions independently of the global interface language when requested.

### 5. Apply only the authorized change

Inspection and ranking are read-only. A menu replacement requires explicit approval for that bot and scope. Before writing, verify `getMe`, inspect the latest menu again, and preserve its prior command-list metadata locally for recovery. Never export tokens, copy credentials between users, weaken a destination guard or restart a gateway from its own turn. Use existing authorized credential and lifecycle mechanisms. Do not execute a command merely to test its menu entry.

### 6. Readback is mandatory

After `setMyCommands`, call `getMyCommands` for the exact scope/language and compare the entire ordered list and descriptions. Verify affected inheritance and that unrelated scopes remain unchanged. A successful API write is not completion. If the result is ambiguous, read back before retrying; never blindly resend.

## Output contract

Report history coverage, counting/deduplication rules, ranked entries, exclusions and approved additions, exact scope, observed readback, persistence behavior and remaining uncertainty. Distinguish a menu update from installing a skill, changing a handler or executing any command. Do not claim a restart test that was not performed.

## Quick Test Checklist

- Positive: inspect a user's current menu without changing it.
- Positive: rank authorized history, exclude quoted commands and repeated message identities, then apply a user-approved chat-only list.
- Positive: remove two requested entries while preserving the relative order of all others.
- Negative: a successful write without exact readback must not be reported as done; a request to inspect must not mutate the menu.

## Done criteria

The approved ordered list is read back from the exact target; unrelated scope/language state is preserved; source history and credentials remain private. If a required writer, identity or authorization check is unavailable, name that precise blocker rather than modifying a broader scope.
