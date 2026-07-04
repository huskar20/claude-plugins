# Maintainers & governance

## Model

- **Owner:** the repo owner is the sole maintainer with merge rights to `main`.
- **All changes go through pull requests.** Direct pushes to `main` are blocked.
- **Every PR requires the owner's approval** (via CODEOWNERS) **and passing CI**
  (`scripts/validate.py`) before it can merge.

The [`.github/CODEOWNERS`](.github/CODEOWNERS) file assigns the owner as reviewer
on every path. Contributors fork, branch, and open PRs per
[CONTRIBUTING.md](CONTRIBUTING.md); the owner reviews and merges.

## One-time setup (do this right after pushing to GitHub)

### 1. CODEOWNERS — already set

[`.github/CODEOWNERS`](.github/CODEOWNERS) already routes every review to
`@huskar20`. If you ever transfer the repo, update that handle.

### 2. Protect the `main` branch

**GitHub web UI** (Settings → Branches → Add branch ruleset, or "Add rule" under
Branch protection rules), targeting `main`:

- ☑ Require a pull request before merging
  - ☑ Require approvals — set to **1**
  - ☑ Require review from Code Owners
  - ☑ Dismiss stale approvals when new commits are pushed
- ☑ Require status checks to pass before merging
  - add the **`validate`** check (the CI job)
- ☑ Block force pushes
- Leave **"Do not allow bypassing the above settings" unchecked** (see note below).

**Or via GitHub CLI** once authenticated:

```bash
gh api -X PUT repos/huskar20/claude-plugins/branches/main/protection \
  --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["validate"] },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false
}
JSON
```

## Note on approving your own changes

GitHub does not let you approve your **own** pull request. Because you are the only
reviewer, keep **admin bypass enabled** (`enforce_admins: false` above, and leave
"Do not allow bypassing" unchecked) so you can still merge your own PRs. The
protection then works exactly as intended:

- **Outside contributors** — cannot merge; their PR sits until *you* approve it.
- **You** — open a PR for your own changes (keeping history clean), and merge it
  yourself using your admin rights.

If you ever add a second trusted maintainer, you can flip on "include
administrators" for full four-eyes enforcement on everyone.
