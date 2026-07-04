# Claude Plugins

A community marketplace of [Claude](https://claude.com) plugins — skills, agents,
and automations you can install into Claude Code or the Claude desktop app.

## Install the marketplace

```
/plugin marketplace add huskar20/claude-plugins
```

Then browse and install:

```
/plugin install career-hunter
```

Update later with `/plugin marketplace update huskar20-plugins`.

## Available plugins

| Plugin | What it does | Version |
|---|---|---|
| **career-hunter** | End-to-end job-search automation: guided onboarding builds your profile + a Google Sheets tracker, then auto-apply and Gmail-sync skills hunt roles, submit applications, keep the tracker current, and add confirmed interviews to your calendar. | 0.1.0 |

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
claude-plugins/
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
