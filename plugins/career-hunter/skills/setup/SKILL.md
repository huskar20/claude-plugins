---
name: setup
description: One-time Career Hunter onboarding — interview the user about their target role, salary, location, work authorization, and preferences; generate their personal career-profile.md; create the Google Sheets job tracker from scratch; and configure automation options. Use when the user says "set up career hunter", "set up my job search", "onboard me", "create my job tracker", or invokes the plugin for the first time (the apply and sync skills also redirect here when no profile exists).
---

# Career Hunter — Setup

Onboard a new user end to end: interview → profile file → tracker spreadsheet →
automation config. Everything the `apply` and `sync` skills need is produced here.
Re-running setup is safe: offer to update the existing profile instead of starting over.

## Outputs (all in the user's working folder)

| File | Purpose |
|---|---|
| `career-profile.md` | Canonical answers for every application form. The user edits it by hand afterward; other skills re-read it every run. |
| `career-hunter-state/config.json` | Spreadsheet ID, resume path, submission mode, caps, schedule, notification prefs. |
| `career-hunter-state/seen_jobs.json` | Created empty; the apply skill's dedupe memory. |
| `career-hunter-state/last_run.json` | Created empty; the sync skill's watermark. |

## Step 1 — Check prerequisites

Verify each connector is actually present (list the available tools / connectors,
don't assume), and tell the user plainly what is missing rather than failing
later. A plugin cannot gate its own installation on connectors — this check is
the real gate, so do it thoroughly and stop if a required piece is absent.

1. **Gmail connector** — needed by sync (and apply, for email verification codes).
2. **Google Drive connector** — **creates** the tracker spreadsheet file
   (`create_file`) and **reads** it for dedupe in apply/sync.
3. **Google Calendar connector** — needed so sync can create an event when it
   detects a confirmed interview. If it's missing, say so; the user can still
   proceed (sync will fall back to notification-only) but flag it as a TODO.
4. **Claude-in-Chrome extension, connected** — `list_connected_browsers`;
   **populates** the new tracker's tab structure/dropdowns/formulas and **writes**
   application rows, and fills application forms. All in the user's own Chrome
   session. (The Drive MCP makes the file; there is no Sheets-cell MCP, so the
   in-sheet structure is built in Chrome.)
5. **Resume file** — ask the user to place their resume PDF in the working folder
   (or a subfolder) and confirm its path. Record it in config. If they don't have
   it ready, continue setup and leave a TODO in the summary.

If any required connector (Gmail, Drive, Calendar) is not connected, tell the user
exactly which one and how to enable it in their Claude app's connector settings
before the dependent skill will work.

## Step 2 — The interview

Use AskUserQuestion throughout, a few related questions per call, in this order.
Everything here maps to a section of `references/profile-template.md` — read that
template first so answers land in the right places. Never invent an answer the
user didn't give; leave the field marked `TODO (ask owner)` instead.

1. **Identity & contact** — full legal name, email, phone, city/state/zip,
   LinkedIn URL, GitHub/portfolio URL (optional).
2. **Target role** — free-text: what role are they hunting (e.g. "data engineer",
   "senior security engineer", "product manager")? Then confirm:
   - a list of 4–8 acceptable job titles (draft it for them from the role — e.g.
     data engineer → Data Engineer, Senior Data Engineer, Analytics Engineer,
     Data Platform Engineer — and let them edit),
   - level (junior / mid / senior / staff / lead) and whether management roles are acceptable,
   - 5–10 key skills/keywords from their background for search queries and form
     keyword fields (ask them to list their real stack — do not guess).
3. **Location** — fully remote only? Or also onsite/hybrid within a metro area
   (which one, what radius)? Willing to relocate?
4. **Compensation** — target base, target total comp, and the **auto-skip floor**
   (posted max below which the apply skill never applies). Explain the floor's job.
5. **Work authorization** — authorized to work in-country? Need sponsorship now or
   in future? Citizen? Active security clearance? These are answered verbatim on
   forms and also drive hard skips (e.g. skip roles requiring citizenship or a
   clearance the user lacks).
6. **Availability** — earliest start, notice period, travel tolerance.
7. **Logins** — does the user sign in to LinkedIn/Indeed/ATS sites with
   **Google SSO**, and may the apply skill use "Continue with Google" when a login
   wall appears? (Passwords are never typed or stored regardless.)
8. **Voluntary EEO defaults** (explain these are optional self-identification
   questions on US applications; recording defaults avoids stopping mid-form) —
   gender, Hispanic/Latino, race/ethnicity, disability status, protected-veteran
   status, "how did you hear about us" convention.
9. **Submission mode** — the most important safety question:
   - **Fully automatic**: the apply skill submits applications without per-form
     confirmation (still bounded by every guardrail).
   - **Review before submit**: the apply skill fills everything, then stops and
     asks the user to review and click Submit themselves.
   Record the choice in config as `submission_mode: "auto" | "review"`.
10. **Caps & cadence** — daily application cap (default 10), per-company cap
    (default 2 per rolling 7 days), which days of the week apply runs are allowed.
11. **Notifications & calendar** — (a) push notification when an interview invite
    is detected? (default yes); (b) may sync auto-create a Google Calendar event
    on the user's own calendar for each confirmed interview? (default yes; record
    as `create_calendar_events`). Note it only creates events for interviews the
    user has confirmed, on their own calendar, with no external invitees.

## Step 3 — Write the profile

Fill `references/profile-template.md` with the interview answers and write it to
`career-profile.md` in the working folder. Keep the template's section structure
and its "Never answer / always skip-and-flag" list intact (add any user additions).
Tell the user this file is theirs to edit by hand any time.

## Step 4 — Create the tracker

Ask: create a new Google Sheets tracker, or connect an existing one (paste URL/ID)?

**Creating new:** the Google Drive MCP creates the spreadsheet **file**; Chrome
then populates its structure. (There is no Sheets-cell MCP, so the multi-tab
layout, dropdowns, and Dashboard formulas are filled in via Chrome — but the file
itself is made by the MCP, which is reliable and doesn't depend on the browser.)
Full per-tab headers and the Dashboard formulas are in `references/tracker-schema.md`.

1. **Create the file — Google Drive MCP `create_file`:** `title:
   "Job_Search_Tracker_<year>"`, `contentMimeType:
   application/vnd.google-apps.spreadsheet` (no content needed — returns a new blank
   spreadsheet). Capture the returned file **id**, build the edit URL
   `https://docs.google.com/spreadsheets/d/<id>/edit`, and store both in
   `config.json` **now**, before populating — so a later failure still leaves a
   usable, recorded sheet.
2. **Populate the structure — Chrome:** open the edit URL and, per the schema,
   rename the default tab to `Applications` (row-1 banner, row-2 headers via the
   Name Box method in `../sync/references/sheet-writing.md`), add the Stage/Status
   dropdowns, then add the **Interview Notes**, **Contacts**, and **Dashboard**
   tabs — entering the Dashboard's `COUNTA`/`COUNTIF` formulas exactly as listed so
   it stays live. The apply/sync skills only ever write to `Applications`.
3. **If Chrome isn't connected:** the spreadsheet still exists (the MCP made it),
   just empty — record it and flag in the summary that its tabs/headers/Dashboard
   need populating in Chrome before apply/sync can use it. (Optional shortcut to at
   least seed the `Applications` header row without Chrome: create the file via
   `create_file` with the 20 column headers as `textContent` CSV and
   `contentMimeType: text/csv`, which converts into a single populated sheet.)

**Connecting existing:** read the sheet via the Drive connector, read its header
row, and record the ID. If its columns differ from the schema, record the actual
header mapping in config — the other skills map by column NAME at runtime anyway.

## Step 5 — Optional scheduling

If the user's Claude app supports scheduled tasks, offer to create:
- an **apply run** on the days chosen in the interview (e.g. Tue/Wed/Thu mornings), and
- a **daily sync** run.
If scheduling isn't available, tell them the manual invocations: "run the job hunt"
(apply) and "sync my job search" (sync).

## Step 6 — Write config and finish

Write `career-hunter-state/config.json`:

```json
{
  "spreadsheet_id": "...",
  "spreadsheet_url": "...",
  "resume_path": "...",
  "submission_mode": "auto | review",
  "daily_cap": 10,
  "per_company_cap_7d": 2,
  "apply_days": ["Tue", "Wed", "Thu"],
  "push_on_interview": true,
  "create_calendar_events": true,
  "google_sso_allowed": true,
  "created_utc": "<ISO-8601>"
}
```

Create `career-hunter-state/seen_jobs.json` as `{"last_run_utc": null, "jobs": {}}`
and `career-hunter-state/last_run.json` as `{}`.

Close with a short summary: what was created, where the profile lives, how to edit
it, the two invocation phrases, and any TODOs (missing resume, unanswered fields).
