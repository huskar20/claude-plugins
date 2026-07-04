# Career Hunter

End-to-end job-search automation for Claude. Interview once, then let Claude
hunt matching roles, submit applications in your name, and keep a Google Sheets
tracker in sync with your Gmail — for any role type (data engineer, security
engineer, PM, designer…), tuned to your titles, salary floor, location, and
work-authorization answers.

## What's inside

| Skill | Invoke with | What it does |
|---|---|---|
| **setup** | "set up career hunter" | Guided interview → generates your personal `career-profile.md`, creates the Google Sheets tracker from scratch, configures caps/schedule/notifications, and asks the key safety question: fully-automatic submission, or review-each-application-before-submit. |
| **apply** | "run the job hunt" | Searches LinkedIn Jobs, Indeed, and Greenhouse/Lever/Ashby boards for roles matching your profile, scores them, fills and submits applications (honoring your submission mode), logs every one to the tracker, and reports a summary. |
| **sync** | "sync my job search" | Scans Gmail since the last sync for confirmations, rejections, interview invites, and engaged recruiter threads; appends/updates tracker rows; creates a calendar event for each confirmed interview; and pushes a notification when an interview lands. |

## Requirements

- **Claude desktop app** with the **Claude-in-Chrome extension** connected
  (all form-filling and sheet edits happen in your own Chrome, with your own
  logged-in sessions).
- **Gmail**, **Google Drive**, and **Google Calendar** connectors enabled.
- A resume PDF.

> Installing the plugin only adds the skills — it can't turn connectors on for
> you. The first time you run **"set up career hunter,"** setup checks that
> Gmail, Drive, and Calendar are connected and tells you exactly what's missing
> before continuing.

## Quick start

1. Install the plugin (see the marketplace README for terminal vs. desktop steps),
   then **restart Claude Code / reload the desktop app** so the skills register.
2. Open or create a folder to use as your job-search workspace and say
   **"set up career hunter"** — always run setup **first**; the other skills depend
   on the profile and config it creates and will redirect you here if they're missing.
3. Answer the interview (role, titles, salary, location, work auth, EEO defaults,
   submission mode). Setup creates:
   - `career-profile.md` — your answers; edit it by hand any time
   - `career-hunter-state/` — config and run state
   - a `Job_Search_Tracker` Google Sheet with **Applications, Interview Notes,
     Contacts, and Dashboard** tabs
4. Say **"run the job hunt"** to apply, **"sync my job search"** to reconcile
   Gmail with the tracker — or let setup schedule both.

## Safety model

- Every form answer comes from `career-profile.md` or your resume — nothing is
  ever invented. Unanswerable questions mean the application is skipped and
  flagged, never guessed.
- SSN/DOB/government IDs are never entered. Assessments and video interviews
  are never started. Captchas are never solved. Passwords are never typed —
  only "Continue with Google" SSO, and only if you allowed it in setup.
- "Review before submit" mode keeps a human click on every submission.
- Applications are sent in your name: even in fully-automatic mode, you own the
  results. Check the tracker and summaries regularly.
