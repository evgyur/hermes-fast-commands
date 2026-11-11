# Telegram scope and persistence notes

Use Telegram's documented [command scopes](https://core.telegram.org/bots/api#botcommandscope) and [command language handling](https://core.telegram.org/bots/api#getmycommands). Inspect only scopes relevant to the requested recipient and its inheritance chain. A narrow empty result is not the resolved effective menu.

Two separate writers can disagree:

- Telegram stores a list for a scope and optional language.
- Hermes may regenerate lists on startup, reconnect, configuration refresh or lazy chat registration.

Check the installed writer before selecting a persistent edit. A global/default change may be overwritten by gateway registration. An exact private-chat override may survive a writer that touches only broad scopes, but that must be verified for the installed release. Forum-specific writers may replace chat-scoped lists; do not apply a private-chat assumption to a forum.

For a configuration-owned menu, inspect the installed implementation of `platforms.telegram.extra.command_menu` before using it. Depending on release, priority changes ordering before truncation, not membership. Inspect whether quick-command aliases are actually included.

For an explicitly approved chat-only update, use an existing authorized credential mechanism, verify the bot with `getMe`, fetch the current exact list, write the proposed list with explicit scope/language, then compare exact readback. Also compare relevant broader scopes and language-specific variants against their pre-change values. Do not log token-bearing URLs or invent a credential-discovery recipe.

If persistence cannot be established without a gateway restart, report the limitation or use the existing authorized external lifecycle owner. Never restart merely to demonstrate that a menu update worked.
