---
doc: prd
status: approved
---

# Meeting Minutes Assistant — Product Requirements

A tool for company and organization secretaries to turn in-person meeting transcripts into editable minutes guided by speaker notes and a chosen reference format. Working title; the learner has not selected a final name. Source: `scope.md > Who It's For`, `scope.md > The Unique Kernel`.

## The Core Journey

1. The secretary opens the tool and provides a transcript file and their notes identifying key statements and who said each one. Both are required, and they can be provided in either order. Source: `scope.md > The Core Loop`.
2. The secretary chooses a saved template from a simple template library, uploads a new template to keep for later meetings, or enters the desired minutes structure in a prompt (for example, numbered sections such as an introduction and AOB). A saved template can be selected again in a few clicks. The chosen template or written structure guides the output so it follows the intended pattern rather than inventing a noticeably different format. Source: `scope.md > The Unique Kernel`, `scope.md > The Core Loop`.
3. The secretary asks the assistant to generate minutes. The minutes follow the provided guidance and use the transcript together with the secretary's speaker notes.
4. If a speaker attribution is unclear, the assistant leaves that attribution blank and alerts the secretary to provide the missing information instead of guessing.
5. The secretary reviews and edits the minutes, then downloads them as `.docx` or PDF for presentation at a later meeting or for documentation. Source: `scope.md > What "Working" Looks Like`, `scope.md > The POC Boundary`.
6. The app automatically saves the current meeting's work on the same computer. If the app is closed, the secretary can reopen and restore the draft; a **Clear meeting** action deletes that working copy.

## Screens and Layout

The visual proof of concept needs an input surface for the transcript upload, required speaker/key-statement notes, and formatting guidance. The secretary may provide the transcript and notes in any order, then choose a saved template, upload a new one, or enter a structure in a prompt. The template library should make saved structures easy to select without requiring elaborate management features. It also needs a generated-minutes view where the secretary can review and edit the result and download it in either supported output format. The exact arrangement and number of screens have not been established; do not add unrelated screens.

## Look and Feel

A calm, professional interface using ocean blue to help build trust. No exact shade, typography, or visual references have been selected. Source: learner's PRD interview answer.

## Features and Behavior

### Provide meeting materials

- The secretary uploads the in-person meeting transcript.
- The transcript may be pasted as text or uploaded as a `.txt` file. A template or previous-minutes reference may be uploaded as `.docx` or a text-readable `.pdf`; scanned image-only PDFs are not supported in the first version because OCR is out of scope.
- The secretary provides notes containing key statements and who said each one; this is compulsory because the transcript may not identify speakers.
- The transcript and notes can be supplied in either order.
- The secretary chooses a previously saved template, uploads a new template to retain for later meetings, or enters the desired structure in a prompt. A previous set of minutes may serve as a formatting reference.
- A template describes the desired structure of the final minutes (for example, numbered sections such as introduction and AOB); it should guide the output rather than lead to a noticeably different format.

### Choose a minutes template

- Keep uploaded templates available for later meetings in a simple library.
- Let the secretary select the template needed for a meeting in a few clicks.
- Keep the library focused on saving and selecting templates; advanced template-management capabilities are outside this proof of concept.

### Generate, review, and export minutes

- The assistant creates complete minutes using the transcript, notes, and provided formatting guidance.
- The secretary can edit the generated minutes in a simple text editor for the text and section headings.
- Downloaded `.docx` and PDF files use straightforward formatting; the proof of concept does not reproduce every visual detail of the uploaded reference.
- Automatically save the current meeting's transcript, notes, generated minutes, and edits on the same computer, so the secretary can restore work after closing the app.
- Provide a **Clear meeting** action that deletes the current working copy; this is not a multi-meeting history or archive.

## States and Boundaries

- **Required input missing** — generation requires both a transcript and speaker/key-statement notes. The interface should make clear which required input is missing.
- **Unsupported or unreadable file** — explain which file could not be read and preserve the current meeting draft; image-only scanned PDFs are unsupported.
- **No saved template yet** — the secretary can upload a template or enter the desired minutes structure in a prompt instead.
- **Speaker attribution unclear** — leave the attribution blank and notify the secretary to supply the missing information; do not guess.
- **App closed during a meeting** — restore the locally auto-saved working copy when the secretary reopens the app; the secretary can clear it when done.
- **Normal completion** — show the generated minutes for review and editing, with `.docx` and PDF download options.

## Product Decisions

- Transcript and speaker/key-statement notes are both compulsory; the secretary may provide them in any order.
- Formatting guidance can be given in a prompt or through an uploaded template/previous minutes reference.
- Uploaded templates remain available in a simple library for later meetings; the secretary can select the needed template in a few clicks.
- The current meeting's working copy is auto-saved on the same computer and can be restored after closing the app; the secretary can delete it with **Clear meeting**. This does not create a meeting archive.
- When no template is selected, the secretary can describe the desired final-minutes structure in a prompt.
- The reference is used to preserve formatting patterns, not to produce a noticeably different format.
- Unclear speaker attribution must be left blank and flagged for the secretary, not invented.
- Generated minutes must be editable and downloadable as `.docx` and PDF.
- The interface should feel calm and professional, with ocean blue used to build trust.

## What We're Building

A focused proof of concept for in-person meeting minutes: upload a transcript, provide required speaker/key-statement notes, choose a saved template from a simple library or provide the desired structure in a prompt, generate editable minutes that follow that guidance, flag unclear speaker attribution rather than guessing, download the result as `.docx` or PDF, and auto-save/restore the current meeting locally until cleared.

## Deferred From the POC

- Virtual-meeting capture and integrations — explicitly outside the idea's in-person meeting focus. Source: `scope.md > Explicitly Cut`.
- A complete platform beyond the focused transcript-to-minutes proof of concept. Source: `scope.md > The POC Boundary`.

## Possible Later Enhancements

A broader product may add capabilities beyond this proof of concept; specific later features have not been chosen.

## Non-Goals

- Capturing or processing virtual meetings — the project is for physical, in-person meetings. Source: `scope.md > Explicitly Cut`.
- Automatically guessing who spoke when the secretary's notes do not make attribution clear.
- Building a complete meeting-management platform; the goal is to demonstrate the minutes-generation workflow. Source: `scope.md > The POC Boundary`.

## Open Questions

- **Can be resolved in `4-spec`:** What upload-size limits should the proof of concept use? Set them after choosing the AI service and checking its current limits.
