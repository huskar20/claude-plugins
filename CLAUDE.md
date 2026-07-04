# CLAUDE.md — rules for authoring plugins in this marketplace

This file governs every plugin in this repository. It is loaded automatically when
developing here with Claude. Human contributors: read it too — CI enforces the
structural parts, and reviewers enforce the rest.

## What this repo is

A **plugin marketplace**: a Git repo whose `.claude-plugin/marketplace.json` lists
plugins that users install into Claude. Each plugin lives in its own directory
under `plugins/`. Adding a plugin means adding its directory **and** registering it
in `marketplace.json`.

## Golden rules

1. **One plugin, one directory** under `plugins/<plugin-name>/`. `<plugin-name>`
   is kebab-case (lowercase letters, numbers, hyphens) and must match the `name`
   in that plugin's `plugin.json` and its entry in `marketplace.json`. Names must
   **not contain "claude" or "anthropic"** — Claude Code rejects them as
   impersonating an official marketplace. (The GitHub repo name may contain
   "claude"; only the `name` fields inside the manifests are checked.)
2. **Never commit personal data or secrets.** No real names (beyond an author
   attribution the author consents to), emails, phone numbers, API keys, tokens,
   spreadsheet/document IDs, file paths outside the repo, or customer data. A
   plugin's *users* generate their own data locally at runtime — it must never
   land in this repo. CI scans for common leak patterns; do not defeat it.
3. **Validate before every PR:** `python3 scripts/validate.py` must pass. If you
   have the Claude CLI, also run `claude plugin validate plugins/<name>/.claude-plugin/plugin.json`.
4. **Bump versions on every change.** Update the plugin's `plugin.json` `version`
   (semver) AND the matching `version` in `marketplace.json`. New plugins start at
   `0.1.0`.

## Required plugin structure

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED manifest
├── skills/                  # skills as SKILL.md files (preferred component)
│   └── <skill-name>/
│       ├── SKILL.md
│       └── references/      # optional supporting detail
├── agents/                  # optional: subagent .md files
├── .mcp.json                # optional: MCP server definitions
└── README.md                # REQUIRED: what it does, requirements, install
```

Only create directories the plugin actually uses. Kebab-case every directory and
file name.

### plugin.json

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "One clear sentence about what it does.",
  "author": { "name": "Your Name" },
  "keywords": ["…"]
}
```

`name` (kebab-case) and `version` (semver) are the load-bearing fields.

### marketplace.json entry

Add an object to the `plugins` array:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Same one-liner as plugin.json.",
  "version": "0.1.0",
  "author": { "name": "Your Name" },
  "category": "productivity",
  "keywords": ["…"]
}
```

`source` is the relative path to the plugin directory. Keep `version` in sync with
the plugin's own manifest.

## Writing skills

- **Progressive disclosure.** Keep `SKILL.md` lean (aim under ~3,000 words); push
  detailed procedures, schemas, and examples into `references/` files the skill
  points to. Load reference files only when needed.
- **Frontmatter `description` is a trigger, not a summary.** Write it in the third
  person and pack in the concrete phrases a user would say ("use when the user says
  '…'"). This is how the skill gets discovered.
- **Skill bodies are instructions for Claude, not docs for the user.** Write
  imperative, verb-first directives ("Read the config", not "You should read the
  config").
- **Portability.** For paths inside a plugin, reference `${CLAUDE_PLUGIN_ROOT}` in
  hooks and MCP configs — never hardcode absolute paths. Between skills in the same
  plugin, use relative paths (`../other-skill/…`).

## Safety rules for automation plugins

Plugins that act on the user's behalf (fill forms, send messages, edit shared
docs, spend money) must follow these — the `career-hunter` plugin is the reference
implementation:

- **Answer only from declared sources.** Never invent, round up, or embellish
  facts about the user. If an answer isn't in the user's profile/config, skip and
  flag it — don't guess.
- **Ask before irreversible or outward-facing actions** unless the user has
  durably authorized them in that plugin's setup (submitting, sending, publishing,
  paying, deleting, changing sharing/permissions).
- **Never handle credentials in plaintext.** No typing/storing passwords; no
  entering SSNs, DOB, or government IDs; never solve captchas.
- **Use environment variables for any secret** an MCP server needs; document them
  in the plugin README.
- Make the risky default the safe one (e.g. offer "review before submit"), and let
  the user opt into more automation explicitly.

## Reviewer checklist (also the PR template)

- [ ] Directory is `plugins/<kebab-name>/` and matches `plugin.json` `name`
- [ ] Registered in `marketplace.json` with matching `name`/`version`/`source`
- [ ] `python3 scripts/validate.py` passes
- [ ] Version bumped (plugin.json + marketplace.json) if anything changed
- [ ] Plugin has its own `README.md` (purpose, requirements, install)
- [ ] No personal data, secrets, tokens, IDs, or machine-specific paths
- [ ] Skills use frontmatter with trigger-phrase descriptions; heavy detail in `references/`
- [ ] Automation plugins follow the safety rules above
