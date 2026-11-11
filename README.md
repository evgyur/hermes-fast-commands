# Hermes Test Commands

A small, public Hermes skill for personalizing Telegram slash-command menus from actual usage.

The method is simple:

**Inspect → count real invocations → deduplicate → rank → apply user preferences → update the narrowest persistent scope → read back.**

It requires inspection before advice, separates visible suggestions from executable handlers, and never treats a successful API write as proof that the intended menu was installed.

## What it covers

- Current bot identity and Telegram scope/language inheritance.
- Authorized cross-profile history, including commands handled before an agent turn.
- Quoted replies, generated messages and replayed-history exclusions.
- Frequency ordering, explicit exclusions and approved utility additions.
- Configuration-owned menus versus chat-specific Telegram menus.
- Exact-target verification without unnecessary gateway restarts.

## Install

Clone into the active profile's skill directory; for the default profile:

```sh
git clone https://github.com/evgyur/hermes-test-commands.git "$HOME/.hermes/skills/hermes-test-commands"
```

For another profile, use that profile's actual skill root. Do not overwrite an existing installation. Use Hermes's supported skill refresh/discovery mechanism if needed; a gateway restart is not inherently required.

Example requests:

- “Inspect my current Telegram command menu. Do not change it.”
- “Rank commands I actually sent across my authorized profiles, show the proposed order, then wait for approval.”
- “Apply the approved menu only to this private chat. Preserve other scopes and verify the result.”

## Boundaries

This is guidance, not an executable plugin, database scanner, security control or background job. It contains no personal history, private command list, credentials, deployment paths or account identifiers. Loading it does not authorize reading other users' history or modifying a bot.

Implementation details must be reconciled against the installed Hermes release and [official documentation](https://hermes-agent.nousresearch.com/docs/). User-specific rankings and verification receipts belong outside a public repository.

## Validation

```sh
python3 -m unittest discover -s tests -v
```

The tests validate the document's structure, size and essential procedural contracts, including negative checks. They do not simulate Telegram or prove live API behavior. No CI workflow is bundled.

MIT licensed. This is an independent community skill, not an official Hermes integration.
