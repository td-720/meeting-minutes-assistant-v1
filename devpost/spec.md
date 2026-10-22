---
doc: spec
status: approved
---

# Meeting Minutes Assistant — Technical Spec

## How This Works, In Plain Language

The app is a local browser page built with Python and Streamlit. Python runs on the secretary's computer, reads the meeting materials, and keeps the saved templates and current draft in a separate folder on that computer—not in the project or public repository.

When the secretary clicks **Generate**, the app makes one request to an online AI model with the transcript, speaker notes, and chosen template or structure. The model returns complete draft minutes following the requested sections, plus any unclear attributions. The secretary reviews and edits the result; the app saves the working draft locally and can create `.docx` and PDF downloads. The secretary remains responsible for checking the minutes before using them as official documentation.

- **Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`)** — a synthetic live request succeeded during the build. Use synthetic meeting materials only with Google's unpaid API tier because Google may use unpaid-tier data to improve products and may have human review. Model access, account quotas, and terms may change; check them before a later demo. Do not fabricate generation if access is blocked.

## The Core Journey Through the System

1. The secretary pastes transcript text or uploads a `.txt` file. The app also collects required notes listing key statements and who said each one. These may be provided in either order. PRD ref: `prd.md > Provide meeting materials`.
2. The secretary chooses a saved template from the local library, uploads a new `.docx` or text-readable `.pdf` template/previous-minutes reference, or enters the desired minutes structure in a prompt. PRD ref: `prd.md > Choose a minutes template`.
3. The app extracts readable text from the selected materials and assembles one request containing the transcript, notes, and reference structure. No model is called until the secretary clicks **Generate**. PRD ref: `prd.md > The Core Journey`.
4. The selected AI service returns minutes using the reference's headings and order. It must not invent a speaker attribution: unclear attributions are left blank and reported for the secretary to fill in. PRD ref: `prd.md > Generate, review, and export minutes`.
5. The app checks the response, displays it in a simple editable text area, and saves the active working copy on the computer. A proposed check for missing template headings is listed under **Decisions and Open Issues** for learner review. PRD ref: `prd.md > States and Boundaries`.
6. The secretary downloads the edited minutes as `.docx` or PDF. **Clear meeting** removes the current working copy; saved templates remain. PRD ref: `prd.md > Generate, review, and export minutes`.

## Stack

- **Python** — application language. The tested project environment uses Python 3.14.7. Dependencies are installed in `.venv/` and recorded in `requirements.txt`.
- **Streamlit** — local browser interface, file upload, text inputs, simple editor, and download controls. The learner chose this for a low-setup local app. Official documentation: `https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader`, `https://docs.streamlit.io/develop/api-reference/widgets/st.text_area`, `https://docs.streamlit.io/develop/api-reference/widgets/st.download_button`.
- **python-docx** — read `.docx` references and create basic `.docx` output with headings and paragraphs. It is not being used to clone every original page style. Official documentation: `https://python-docx.readthedocs.io/en/stable/`.
- **pypdf** — extract text from text-readable PDFs. It is not OCR; image-only scans are rejected with a clear message. PDF text extraction can be imperfect for tables and complicated page layouts, so the first version follows readable section structure rather than reproducing exact page appearance. Official documentation: `https://pypdf.readthedocs.io/en/stable/user/extract-text.html`.
- **ReportLab** — create PDF downloads from the same edited minutes content, using straightforward formatting. Official documentation: `https://docs.reportlab.com/reportlab/userguide/ch1_intro/`.
- **Google Gen AI Python SDK** — call the Gemini API once per Generate action, with `gemini-3.5-flash-lite`. Check the current SDK setup and Python version requirements before pinning. Official documentation: `https://ai.google.dev/gemini-api/docs/quickstart`.
- **Python standard library (`json`, `pathlib`)** — store the local template index and current draft; no database is needed for this single-user proof of concept.
- **Gemini API** — Google documents support for structured output with this model; use a structured response for minutes and unclear attributions. Official documentation: `https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite`, `https://ai.google.dev/gemini-api/docs/structured-output`.

## Where It Runs and How Someone Tries It

- Run locally on the learner's computer; no public app deployment, account system, or hosting plan.
- Start command: `python -m streamlit run app.py`. Streamlit prints the local browser address to open.
- Install dependencies in an isolated Python environment using `requirements.txt`; the listed versions were tested with Python 3.14.7.
- Live generation requires a Gemini API key configured locally; never put it in source control or share it in chat. A synthetic live request succeeded during the build. Use synthetic meeting materials only with the unpaid API tier. Do not fabricate minutes if the API call is unavailable.
- Submission still needs a short demo video and a public GitHub repository. The video should show a synthetic transcript, speaker notes, choosing a saved template, generating minutes in its section pattern, reviewing/editing, and downloading an output. Use clearly labeled synthetic meeting data, not confidential real records. The local app is sufficient to record; deployment is optional.

## Look and Feel

Use the learner-selected Harbor Light theme: pale blue background (`#F3F8FB`), white surfaces, navy text (`#16324F`), slate secondary text (`#4B6275`), and ocean-blue primary buttons (`#075985`). Contrast checks live in `tests/test_theme.py`. Keep the input flow readable and uncluttered. The edit area and exports use clear section headings, order, and numbering from the chosen reference where extractable. Use straightforward fonts and spacing; exact replication of page layout and complex tables is outside this proof of concept. Source: `prd.md > Look and Feel`.

## Components

### Local Streamlit Interface

Collect transcript text or `.txt` upload, required speaker/key-statement notes, and either a saved template choice, a new reference upload, or a written structure prompt. Inputs can be entered in either order. Show validation for missing required items. Display generated minutes in a simple text editor, show unresolved speaker attributions, and provide `.docx`/PDF downloads and **Clear meeting**. Implements `prd.md > Provide meeting materials`, `prd.md > Generate, review, and export minutes`, and `prd.md > States and Boundaries`.

### Reference and Transcript Reader

- Read pasted transcript text or decode uploaded `.txt` as text.
- Read `.docx` paragraph/heading text with `python-docx`.
- Read text from `.pdf` pages with `pypdf`; if extraction yields no usable text, show an unreadable/scanned-PDF message. No OCR or image-to-text conversion.
- Extract the visible heading/section sequence where practical and provide the reference text/structure to the AI request. Complicated tables and exact visual layout are not guaranteed. Implements `prd.md > Provide meeting materials`.

### Local Template and Draft Store

Use a per-user application data directory outside the source project, such as `~/.meeting-minutes-assistant/` (resolved from the user's home directory). Keep:

- `templates/` — uploaded template/previous-minutes source files that the secretary chose to retain.
- `templates.json` — small index of template IDs, display names, file types, and local file paths.
- `current_draft.json` — one active meeting's transcript text, notes, selected template ID or structure prompt, generated minutes, edited minutes, and last-save time.

Save the active draft after input changes and generated/edit updates. On app start, restore it if present. **Clear meeting** deletes only `current_draft.json`; it does not delete the template library. Do not store runtime meeting data inside the repository. Streamlit's session state is for an open session, so it is not the durable store for restoring work after the app is closed. Official documentation: `https://docs.streamlit.io/develop/concepts/architecture/session-state`.

### One-Step AI Generator

Use one function, conceptually `generate_minutes(transcript_text, speaker_notes, reference_text_or_prompt)`, called only when the secretary selects **Generate**. It calls Google's Gemini API with model ID `gemini-3.5-flash-lite`, and requests a structured response containing complete minutes plus a list of attributions that need clarification. Do not add autonomous planning, tools, background jobs, or multi-agent loops. Keep `GEMINI_API_KEY` outside source control in a local environment setting; never put keys in the repository or conversation.

Add a visible notice that generation sends meeting materials to Google. Use synthetic meeting materials only for unpaid-tier tests: Google states that unpaid-tier prompts and responses may be used to improve its products and may be reviewed by people. Do not describe the app as suitable for confidential records under this arrangement.

The provider and intended test model are selected. Verify the current model availability, free-tier limits, response schema behavior, and SDK setup with a synthetic meeting sample during the build. Implements `prd.md > The Core Journey` and `prd.md > Generate, review, and export minutes`.

### Document Exporter

Convert the edited sectioned text into a simple `.docx` using `python-docx` and a PDF using ReportLab. Both downloads must contain the secretary's latest edits and preserve the selected headings/order/numbering as supported. Do not overwrite uploaded reference files. Implements `prd.md > Generate, review, and export minutes`.

## Data Model

- **Template entry:** unique local ID, display name, original extension (`.docx`, text-readable `.pdf`, or `.txt`), and stored source-file path. Template source files remain available between meetings.
- **Current meeting draft:** transcript text, required speaker/key-statement notes, selected template ID or structure prompt, generated minutes text, edited minutes text, and save timestamp. There is only one resumable meeting draft; this is not a history/archive.
- **Data flow:** transcript and notes enter the local app; template/reference text is read locally; the current draft is saved locally. On Generate, the transcript, notes, and chosen reference text are sent over the internet to Google's Gemini API. The returned minutes are saved locally, displayed for editing, and rendered into the two download formats. Clearing the meeting removes the local draft but not templates.

## File Structure

```text
meeting-minutes-assistant/
├── app.py                         # Streamlit entry point and page flow
├── minutes_app/
│   ├── ai_service.py               # Single-call Gemini API adapter
│   ├── document_export.py          # DOCX and PDF output
│   ├── file_readers.py             # TXT, DOCX, and text-based PDF extraction
│   ├── local_store.py              # Template library and current-draft save/restore
│   └── theme.py                    # Harbor Light palette and contrast styling
├── tests/
│   ├── test_core.py
│   └── test_theme.py
├── requirements.txt                # Tested, pinned Python dependencies
├── README.md                       # Setup, local run, and demo instructions
├── .gitignore                      # Secrets and generated local artifacts
└── devpost/                        # Curriculum skills and approved planning documents
```

Runtime templates and meeting drafts live outside this tree under the local application data directory.

## External Services and Dependencies

- **Google Gemini API — model `gemini-3.5-flash-lite`:** one request per Generate action. Send extracted transcript text, speaker notes, and either reference text or the user's structure prompt; request structured output containing `minutes_text` and `unclear_attributions`. Authenticate with `GEMINI_API_KEY` from a local environment setting. Keep the key in the local Python process, not in browser code. Model and structured-output references: `https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite`, `https://ai.google.dev/gemini-api/docs/structured-output`.
- **Free-tier caution:** This plan targets Google's unpaid Gemini API tier for a synthetic-data proof of concept. Google documents that unpaid-tier usage may use submitted content to improve its products and may involve human review; therefore use synthetic demo materials only. Limits, regional access, model availability, and terms can change. Check them in Google's official docs before implementation and demonstrate a working synthetic sample. Sources: `https://ai.google.dev/gemini-api/terms`, `https://ai.google.dev/gemini-api/docs/rate-limits`.
- **Streamlit, `python-docx`, `pypdf`, and ReportLab:** install locally from their documented Python packages. Pin versions only after confirming compatibility with the installed Python interpreter and testing exports/reading.
- No hosted app, remote database, cloud file storage, user account service, or payment service.

## Important Failure Modes

- **Missing or unreadable input** → explain which required item is missing or which file could not be read, and preserve the saved draft. No OCR fallback.
- **AI provider unavailable, key absent, or request rejected** → show a clear error, keep the transcript/notes/template/draft intact, and do not produce simulated minutes.
- **Unclear speaker or missing template section** → leave the attribution blank and flag it; if the proposed heading check is approved, identify any absent template sections for secretary review. Never silently invent speakers or claim the template was followed if a section is missing.

## What Was Simplified and Why

- **Local single-user app** instead of hosted multi-user service — matches local-only hosting and avoids accounts, deployment, and synchronization.
- **One active draft plus saved local templates** instead of a meeting archive — supports resume after closing while limiting stored meeting history.
- **One AI request per Generate action** instead of an autonomous multi-step agent — directly proves transcript-to-minutes generation with less complexity.
- **Text-readable PDF extraction, no OCR** — keeps the file path small; scanned-image PDFs receive a clear unsupported-file message.
- **Simple text editor and basic document styling** instead of a full Word-like editor or exact reference-document cloning — keeps focus on matching section structure and producing editable minutes.

## Decisions and Open Issues

### Agreed decisions

- The learner chose Python + Streamlit and a locally running browser app.
- The app may send meeting materials to a hosted AI model; Google Gemini is selected for API integration.
- Use `gemini-3.5-flash-lite` on the free API tier for synthetic-data proof-of-concept testing, after checking current availability and quota. Do not use confidential real meeting data with the unpaid tier.
- One AI request per Generate action; no autonomous multi-step behavior.
- Transcript is pasted text or `.txt`; template/previous-minutes reference is `.docx` or text-readable `.pdf`; output is `.docx` and PDF.
- OCR is excluded.
- Templates and one auto-saved current meeting draft stay on the same computer, outside the project/repository. The current draft can be cleared; templates remain.
- The generated result uses a simple editable text area and basic export styling; section structure and order matter more than exact page appearance.
- Ocean-blue, calm, professional visual direction.
- The learner's app-versus-agent uncertainty was clarified: the app is the secretary's workspace, while the AI handles one bounded generation task in one request.

### Verified during the build

- A synthetic live request succeeded with `gemini-3.5-flash-lite`; future access and account quota must still be checked before demos.
- Local API-key configuration is implemented without placing the key in source control.
- Upload limits are set to 2 MB for transcript TXT and 8 MB for template/reference files.
- Python 3.14.7 with the versions in `requirements.txt` passed the test suite.

### Deferred from this proof of concept

- Deterministically compare every generated heading with the selected template and flag omitted sections. The secretary reviews the generated structure manually; no second AI request or heading-diff feature is implemented.
