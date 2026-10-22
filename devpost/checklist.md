---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. Generate and edit minutes from a synthetic meeting**
  Becomes usable: A running local app where a synthetic transcript, secretary notes, and a simple structure prompt produce editable draft minutes through one Gemini API request.
  Why now: This proves the project's unique core—minutes generation—early, while revealing whether the free model and structured response are usable before investing in file handling or exports.
  PRD ref: `prd.md > The Core Journey`, `prd.md > Provide meeting materials`, `prd.md > Generate, review, and export minutes`
  Spec ref: `spec.md > One-Step AI Generator`, `spec.md > Local Streamlit Interface`, `spec.md > Look and Feel`
  Build: Scaffold the project per the spec's file structure, install dependencies, add the guided transcript and notes fields, a structure prompt and template input, a clear free-tier data warning, Gemini credential handling, one-call generation, attribution clarification notices, and editable minutes. Use synthetic content only. If the proposed model cannot be used at no cost for this account, stop live-generation work and show the blocker before switching provider/model.
  Verify (mechanical): Run focused tests for input validation and Gemini response parsing; start Streamlit; with a configured Gemini key, generate from synthetic data and confirm draft minutes and attribution warnings display. If free-tier access is unavailable, report the blocker and do not fake a successful API result.
  Learner check: Open the local app, generate minutes from the synthetic example, and tell me if the result follows the sample structure and what you'd change.
  Commit: `Build synthetic meeting minutes generation`

- [x] **2. Save work locally and reuse a template**
  Becomes usable: The app restores the current meeting after restart and allows a saved template to be selected for another synthetic meeting.
  Why now: Once generation works, persistence and template reuse complete the central repeatable workflow without risking real meeting data.
  PRD ref: `prd.md > Choose a minutes template`, `prd.md > Generate, review, and export minutes`, `prd.md > States and Boundaries`
  Spec ref: `spec.md > Local Template and Draft Store`, `spec.md > Data Model`, `spec.md > Reference and Transcript Reader`
  Build: Add TXT transcript and DOCX/text-PDF template reading; local template library and autosaved draft outside the repository; restore/clear behavior. Keep file validation and safe storage paths.
  Verify (mechanical): Run reader and store tests; save a draft and template, restart the app, and verify restoration and template selection; verify clear removes the draft but retains templates.
  Learner check: Save a synthetic meeting and a template, restart the app, and confirm both the draft and template are available. Passed: learner confirmed the previous draft restored and the sample template remained available after refresh.
  Commit: `Persist drafts and reusable templates`

- [x] **3. Export edited minutes and prepare the demo**
  Becomes usable: The secretary can download the edited minutes as DOCX and PDF, and the full synthetic-data journey is documented for a demo.
  Why now: Exports complete the PRD's output behavior after the generated/editable content and saved workflow have been proven.
  PRD ref: `prd.md > Generate, review, and export minutes`, `prd.md > The Core Journey`
  Spec ref: `spec.md > Document Exporter`, `spec.md > Where It Runs and How Someone Tries It`, `spec.md > File Structure`
  Build: Implement DOCX/PDF export from the latest edited minutes, add README setup/run/demo guidance, finish checks, and ensure secrets and runtime meeting data are excluded from Git.
  Verify (mechanical): Run the full test suite; create both exports from edited synthetic minutes and verify they are readable and contain the latest text; inspect staged diff for secrets/private material; start the app using README instructions.
  Learner check: Edit the synthetic draft, download both formats, and confirm the changes appear in each file. Passed: learner confirmed both DOCX and PDF contained the latest edit.
  Commit: `Export and document meeting minutes demo`

## Hands-on Checkpoints

- [x] Early usable behavior explored — after slice 1; learner tries generation and gives feedback. The learner confirmed the generated headings were in the requested order; the running app also showed the unclear-speaker warning.
- [x] Final kick-the-tires exploration and feedback completed. The learner tried generation, draft/template restore, and both exports, then reported the app was okay.

## Final Review

- [x] Final review complete — the learner said the app was okay and asked to ship; no further fixes were requested.

## Code Tour and App Map

- [x] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [x] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [x] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: Brief evidence-based recap connected user-observed behavior to verification: synthetic generation preserved heading order, the template and draft persisted after refresh, and edits appeared in both exports. Full suite: 13 passed; app health: ok.
Route and stops: Reference-only route in `app-map.html`: `app.py` (`_restore()`, Generate button) → `minutes_app/ai_service.py` (`generate_minutes()`) → `minutes_app/document_export.py` (`export_docx()`, `export_pdf()`). No interactive editor tour was performed.
Edit outcome: No optional code edit requested; no code changed during wrap-up.
Reflection: Optional transfer question offered: what would you do differently next time you start with an agent?
Activity mode: Brief evidence-based recap using the learner's completed live-app checks; `app-map.html` provides a reference route.

## Revisions

- Updated the initial Gemini 3.1 preview choice after checking Google's release notes: that preview was shut down, and Google recommends Gemini 3.5 Flash-Lite for new projects. The app and spec now use `gemini-3.5-flash-lite`, which supports structured output and is listed with a free API tier.
- Following learner feedback, moved the AI data-use disclosure from the prominent form area to a 12px, high-contrast footer while retaining the synthetic-data warning and model/local-storage details.
- Aligned the technical spec with the built app (Gemini 3.5 Flash-Lite, tested Python/dependencies, Harbor Light, and actual file structure); documented the automated heading-comparison idea as deferred rather than implemented.
