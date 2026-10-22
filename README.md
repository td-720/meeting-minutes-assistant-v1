# Local Meeting Minutes Assistant

A local proof of concept for turning synthetic in-person meeting transcripts and secretary speaker notes into editable minutes guided by a saved template or a written structure.

## Run it

1. Install Python 3.14 (or a compatible Python version).
2. From the project folder, create and activate a virtual environment:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Generation uses Google's `gemini-3.5-flash-lite` model; Google currently lists standard text input/output as free tier. Free access and request limits can depend on your account/region and may change. Copy `.env.example` to `.env`; replace its placeholder with your API key from Google AI Studio. Never share the key in chat or commit `.env`.
4. Start the app:

   ```sh
   python -m streamlit run app.py
   ```

5. Open the local address Streamlit prints, add synthetic transcript text and speaker notes, choose or add a template (or write a structure), then click **Generate draft minutes**.

## Privacy for the demo

Use invented names, organizations, and meeting events only. The free/unpaid Gemini API tier may use submitted content to improve Google products and may involve human review. Generation sends the transcript, notes, and selected format reference to Google. Local autosave is stored under `~/.meeting-minutes-assistant/`, outside this repository. Never use confidential real meeting material with the unpaid tier.

## Supported files

- Transcript: pasted text or `.txt` up to 2 MB.
- Template/reference: `.docx`, text-readable `.pdf`, or `.txt` up to 8 MB.
- Exports: `.docx` and PDF.
- Scanned/image-only PDFs and OCR are not supported.

## Tests

```sh
.venv/bin/python -m pytest -q
```

The test suite covers file extraction, local save/restore, clear-draft behavior, and document exports. Live generation requires a valid API key and is intentionally tested manually with synthetic data.
