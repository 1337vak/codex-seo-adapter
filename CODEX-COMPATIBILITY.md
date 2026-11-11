# Codex compatibility contract

Use the installed plugin root when resolving `skills/`, `scripts/`, `schema/`,
`data/`, and role-reference paths. Before shell commands, set `PLUGIN_ROOT` to
the absolute installed directory containing `.codex-plugin/plugin.json`.
`PLUGIN_ROOT` in prose is a path to resolve, not automatic shell interpolation.

Invoke the hub with `$codex-seo:seo` and the requested command, or invoke the
specific skill such as `$codex-seo:seo-schema`. Source slash-command examples
refer to these workflows; they are not registered Codex slash commands.

Read specialist briefs under `skills/seo/references/roles/` only as needed.
Delegate through the native subagent capability when available and within its
actual concurrency limit; otherwise perform those specialist checks directly.
Claude model choices, turn budgets, tool names, and allowlists do not create
Codex permissions or independently installed agents. Preserve domain checks,
observed evidence, limitations, and meaningful user authorization.

Run `scripts/claude-seo doctor --json` before dependency-dependent helpers. The
launcher keeps its upstream name and `CLAUDE_SEO_*` application settings for
compatibility, while runtime state is stored in Codex's plugin data directory.
Run its `setup` command only for an explicitly requested runtime setup or repair.
It uses an isolated environment; browser installation and API authentication
remain separate prerequisites. Never invent API results or treat configured
credentials as evidence of a successful call.

The schema hook adapts Codex Write/Edit and apply_patch events to the unchanged
upstream JSON-LD validator. It checks surviving edited files and provides
diagnostics; a post-edit hook cannot undo a write. Codex requires review and
trust of the exact installed hook before it executes. Public-directory packages
must omit hooks and document the resulting manual validation step.

Optional MCP tools must already be connected and authorized in Codex. Do not run
upstream Claude extension installers or edit Claude settings. DataForSEO cost
guards, audit-target authorization, SSRF protection, untrusted page-content
handling, and source-evidence requirements remain applicable. Additional
extensions beyond the two bundled skill mirrors require a separate adaptation.

SEO references are pinned historical guidance. Verify time-sensitive search
policies, service features, prices, and current recommendations against primary
sources before presenting them as current facts.
