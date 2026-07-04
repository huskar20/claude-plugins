# Claude Plugins

A community marketplace of [Claude](https://claude.com) plugins — skills, agents,
and automations you can install into Claude Code or the Claude desktop app.

## Installing

Career Hunter installs like any Claude plugin. There are two environments:

### Claude Code (terminal)

Run these in an **interactive** `claude` session — the `/plugin` commands aren't
available in non-interactive or embedded runs:

```
/plugin marketplace add huskar20/huskar20-plugins
/plugin install career-hunter
```

Then **restart Claude Code** (start a fresh session) so the plugin's skills
register. Update later with `/plugin marketplace update huskar20-plugins`.

### Claude desktop app

Add the marketplace and install `career-hunter` from the app's **plugin /
marketplace settings**, pointing it at the `huskar20/huskar20-plugins` repo. If
your desktop version accepts the `/plugin` slash commands in chat, the two commands
above work there too. After installing, **reload the app** so the skills load.
(The exact menu location varies by app version.)

### First thing after installing (both environments)

Open or create a folder to use as your job-search workspace, then say:

> **set up career hunter**

This one-time onboarding interviews you and builds your profile + tracker. **Run it
before** "run the job hunt" or "sync my job search" — those skills depend on the
profile and config it creates, and will send you back to setup if they're missing.

## Available plugins

| Plugin | What it does | Version |
|---|---|---|
| **career-hunter** | End-to-end job-search automation: guided onboarding builds your profile + a Google Sheets tracker, then auto-apply and Gmail-sync skills hunt roles, submit applications, keep the tracker current, and add confirmed interviews to your calendar. | 0.2.0 |

Each plugin has its own README under [`plugins/`](./plugins/) with full details
and requirements.

## Contributing

New plugins and improvements are welcome. Two documents govern the process:

- **[CLAUDE.md](./CLAUDE.md)** — the rules every plugin in this marketplace must
  follow (structure, writing style, safety, versioning). Read it before building.
  If you develop with Claude, it will load these rules automatically.
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** — the practical workflow: fork, branch,
  validate, open a PR.

A GitHub Action validates every pull request against the structural rules, so
check locally first:

```
python3 scripts/validate.py
```

All changes land through pull requests reviewed and approved by the repo owner —
direct pushes to `main` are blocked. See [MAINTAINERS.md](./MAINTAINERS.md) for
the governance model.

## Repository layout

```
huskar20-plugins/
├── .claude-plugin/
│   └── marketplace.json      # the marketplace manifest (lists every plugin)
├── plugins/
│   └── <plugin-name>/        # one directory per plugin
│       ├── .claude-plugin/plugin.json
│       ├── skills/…
│       └── README.md
├── scripts/validate.py       # portable structural validator (used by CI)
├── CLAUDE.md                 # rules for plugin authors
├── CONTRIBUTING.md           # contribution workflow
└── LICENSE                   # MIT
```

## License

[MIT](./LICENSE). Plugins in this marketplace are free to use and adapt. Each
plugin generates and stores its users' personal data locally on their own
machine — nothing personal is committed to this repository.
