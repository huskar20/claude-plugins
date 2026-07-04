# Tracker spreadsheet schema (Applications tab)

Row layout: **row 1 = title banner** (merged or plain, cosmetic), **row 2 = header
row**, **data starts at row 3**. Entry number N lives on sheet row N+2.

**The owner may edit this schema by hand later** (insert columns, add statuses).
The apply and sync skills must therefore **re-read the header row (row 2) at the
start of every run and map fields by NAME**, never by fixed column letters. The
table below is the layout as created by setup; treat it as a hint, not gospel.

| Col | Field | Notes / conventions |
|-----|-------|---------------------|
| A | # | sequential entry number |
| B | Company | |
| C | Interview Date | e.g. `6/24/2026 10:30` |
| D | Role | use `TBD` if unknown |
| E | Location | |
| F | Mode | dropdown: Hybrid / Remote / Onsite |
| G | Source | e.g. `Direct`, `LinkedIn`, `Indeed`, `LinkedIn (Recruiter)` |
| H | JD Link | canonical posting URL, tracking params stripped |
| I | Comp Range (JD) | as posted, e.g. `$180K-$225K base`; `Not listed` if absent |
| J | My Target TC ($K) | number from the profile, e.g. `350` |
| K | Applied Date | format like `Jun 17, 2026` |
| L | Last Activity | format like `Jun 17, 2026` |
| M | Stage | dropdown: `Applied` / `HR Call` / `HM Call` / `Technical Screen` / `Final Round` / `Offer` / `Hired` / `Closed` |
| N | Status | dropdown: `Applied` / `Active` / `Rejected` / `Offer` / `Completed` / `Withdrawn` / `Interview Scheduling` / `Recruiter Outreach` |
| O | Contact | recruiter/contact name |
| P | Contact Info | email or `LinkedIn InMail` |
| Q | Additional | free slot (resume version, portal links) |
| R | Next Step | |
| S | Next Step Date | |
| T | Notes | short, factual; include the email date |

## Conventions the skills rely on

- **Stage for a fresh application is `Applied`** (not "Application").
- **Status `Active`** = live interview process. **Status `Applied`** = submitted,
  no response yet. `Recruiter Outreach` = engaged recruiter conversation with no
  formal application yet.
- A value typed into a dropdown cell that isn't in the list commits with a soft
  red validation flag — acceptable, don't fight it.
- Rejections: set Stage `Closed`, Status `Rejected`, update Last Activity, append
  a dated note. Never delete rows.
- The Notes column is scannable history: append with ` | ` separators, keep each
  entry short and dated.

## Dropdowns (data validation)

Three columns on the Applications tab are dropdowns (Data → Data validation,
criteria = **Dropdown**). Apply each to the whole data range of its column
(e.g. `F3:F1000`, `M3:M1000`, `N3:N1000` — the reference sheet has them split
into smaller ranges only because the owner extended them over time; one range
per column is cleaner). A value typed that isn't in the list still commits, with
a soft red flag — that's expected (e.g. `Recruiter Outreach` in Status).

| Column | Field | Options | Chip color |
|---|---|---|---|
| F | Mode | Remote, Hybrid, Onsite | none (default gray) |
| M | Stage | Applied, HR Call, HM Call, Technical Screen, Final Round, Offer, Hired, Closed | none (default gray) |
| N | Status | Active, Rejected, Offer, Completed, Withdrawn, Interview Scheduling, Applied | **colored — see below** |

**Status chip colors** (set per option in the dropdown editor — this is what
paints the Status cells; it is NOT conditional formatting):

| Option | Color |
|---|---|
| Active | green |
| Interview Scheduling | green |
| Rejected | dark red |
| Withdrawn | dark maroon |
| Offer | purple |
| Completed | dark gray |
| Applied | light gray (default) |

(`Recruiter Outreach` is used off-list and shows with the soft red flag.)

## Colors & formatting (manual cell fills — no conditional formatting)

All coloring below is plain cell fill / text formatting, applied once at setup.
Exact hex isn't critical; match the semantic color.

- **Row 1 title banner (every tab):** dark navy fill, **white bold centered** title
  (the tab's name, e.g. `JOB SEARCH DASHBOARD`, `RECRUITER & CONTACT DIRECTORY`).
- **Row 2 header row (all data tabs):** dark navy fill, white bold text.
- **Applications — column C (Interview Date):** light green fill on the header and
  its cells, so interview rows stand out at a glance.
- **Status column (N):** colored via the dropdown chips above — no separate rule.

### Dashboard tab formatting

- **Row 1 banner:** dark navy, white bold `JOB SEARCH DASHBOARD`.
- **Summary cards — row 3 header cells, each a distinct fill:** Total Applied =
  navy, Active = green, Rejected = red, Offers = amber/gold, In Final Round =
  blue, Stalled = orange. Row 4 (the formula values) sits on light gray with large
  bold numbers.
- **Row 6 banner:** dark navy, white bold `PIPELINE FUNNEL`.
- **Funnel rows 7–13:** bold stage labels in column B on light gray, counts in
  column C.

## Creating the sheet

The full create-then-populate procedure is in this skill's `SKILL.md` (**Step 4**):
the Google Drive MCP `create_file` makes the spreadsheet, then Chrome populates the
tabs, the dropdowns + Status chip colors above, the fills above, the supporting-tab
layouts below, and the Dashboard formulas below. The apply/sync skills only ever
write to `Applications`; the three supporting tabs are for the user's manual use.

## Supporting tabs (exact layout, mirrored from the reference tracker)

Each has a **row 1 title banner** and a **row 2 header row** (data from row 3),
same pattern as Applications.

### Interview Notes

- Row 1 banner: `INTERVIEW NOTES`
- Row 2 headers (A–G): **Company · Date · Round · Interviewers · Questions Asked ·
  My Answers / Notes · Outcome / Follow-up**

### Contacts

- Row 1 banner: `RECRUITER & CONTACT DIRECTORY`
- Row 2 headers (A–G): **Name · Company · Title · Email · LinkedIn · Relationship ·
  Notes**

### Dashboard

Live summary driven by `COUNTA`/`COUNTIF` over the Applications tab. Recreate it
with the same formulas so it auto-updates as applications are logged. Layout:

- Row 1 banner: `JOB SEARCH DASHBOARD`
- **Summary cards** — headers in row 3, formula values in row 4:

  | Cell | Header (row 3) | Formula (row 4) |
  |---|---|---|
  | B | Total Applied | `=COUNTA(Applications!B3:B180)` |
  | C | Active | `=COUNTIF(Applications!N3:N180,"Active")` |
  | D | Rejected | `=COUNTIF(Applications!N3:N180,"Rejected")` |
  | E | Offers | `=COUNTIF(Applications!N3:N180,"Offer")` |
  | F | In Final Round | `=COUNTIF(Applications!M3:M180,"Final Round")` |
  | G | Stalled | `=COUNTIF(Applications!N3:N180,"Stalled")` |

- Row 6 banner: `PIPELINE FUNNEL`
- **Funnel** — label in column B, count in column C (rows 7–13), each count
  `=COUNTIF(Applications!M3:M180,"<label>")` (column M = Stage):

  | Row | B (label) | C (formula) |
  |---|---|---|
  | 7 | Applied | `=COUNTIF(Applications!M3:M180,"Applied")` |
  | 8 | HR Call | `=COUNTIF(Applications!M3:M180,"HR Call")` |
  | 9 | HM Call | `=COUNTIF(Applications!M3:M180,"HM Call")` |
  | 10 | Technical Screen | `=COUNTIF(Applications!M3:M180,"Technical Screen")` |
  | 11 | Final Round | `=COUNTIF(Applications!M3:M180,"Final Round")` |
  | 12 | Offer | `=COUNTIF(Applications!M3:M180,"Offer")` |
  | 13 | Hired | `=COUNTIF(Applications!M3:M180,"Hired")` |

The `…3:180` ranges intentionally extend far past current data so new rows are
counted automatically without touching the Dashboard. The summary "Active/
Rejected/Offer/Stalled" cards read the **Status** column (N); "In Final Round"
and the whole funnel read the **Stage** column (M). If you rearranged the
Applications columns, point these at the correct letters.
