from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from minutes_app.ai_service import MODEL_NAME, generate_minutes
from minutes_app.document_export import export_docx, export_pdf
from minutes_app.file_readers import read_reference, read_transcript_text
from minutes_app.local_store import add_template, clear_draft, get_template, list_templates, load_draft, save_draft
from minutes_app.theme import theme_css

PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

st.set_page_config(page_title="Minutes Assistant", page_icon="📝", layout="wide")
st.markdown(theme_css(), unsafe_allow_html=True)


def _persist() -> None:
    save_draft({
        "transcript": st.session_state.get("transcript", ""),
        "speaker_notes": st.session_state.get("speaker_notes", ""),
        "format_prompt": st.session_state.get("format_prompt", ""),
        "selected_template_id": st.session_state.get("selected_template_id", ""),
        "minutes": st.session_state.get("minutes", ""),
        "unclear_attributions": st.session_state.get("unclear_attributions", []),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    })


def _save_uploaded_template() -> None:
    uploaded = st.session_state.get("template_upload")
    try:
        if not uploaded:
            raise ValueError("Choose a template file first.")
        text = read_reference(uploaded.name, uploaded.getvalue())
        entry = add_template(st.session_state.get("new_template_name", ""), Path(uploaded.name).suffix, uploaded.getvalue(), text)
        st.session_state.selected_template_id = entry["id"]
        st.session_state.template_message = f"Saved '{entry['name']}' for future meetings."
        _persist()
    except Exception as exc:
        st.session_state.template_message = f"Could not save template: {exc}"


def _clear_meeting() -> None:
    clear_draft()
    for key in ("transcript", "speaker_notes", "format_prompt", "minutes"):
        st.session_state[key] = ""
    st.session_state.unclear_attributions = []
    st.session_state.selected_template_id = ""
    st.session_state.upload_version = st.session_state.get("upload_version", 0) + 1
    st.session_state.clear_message = "Current meeting draft cleared. Saved templates remain."


def _cache_uploaded_transcript(widget_key: str) -> None:
    uploaded = st.session_state.get(widget_key)
    if uploaded is None:
        return
    try:
        st.session_state.transcript = read_transcript_text("", uploaded.name, uploaded.getvalue())
        _persist()
        st.session_state.upload_message = "Transcript loaded and auto-saved locally."
    except Exception as exc:
        st.session_state.upload_message = f"Could not load transcript: {exc}"


def _restore() -> None:
    if st.session_state.get("draft_loaded"):
        return
    saved = load_draft()
    for key in ("transcript", "speaker_notes", "format_prompt", "selected_template_id", "minutes", "unclear_attributions"):
        st.session_state.setdefault(key, saved.get(key, [] if key == "unclear_attributions" else ""))
    st.session_state.setdefault("upload_version", 0)
    st.session_state.draft_loaded = True


_restore()
st.markdown('<div class="hero"><h1>Meeting Minutes Assistant</h1><p>Turn an in-person meeting transcript into an editable draft, guided by your notes and preferred format.</p></div>', unsafe_allow_html=True)


templates = list_templates()
template_names = {item["id"]: item["name"] for item in templates}
template_ids = [item["id"] for item in templates]
if st.session_state.get("selected_template_id") not in template_ids:
    st.session_state.selected_template_id = ""

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("1 · Meeting materials")
    pasted = st.text_area("Paste meeting transcript", key="transcript", height=180, placeholder="Paste a synthetic in-person meeting transcript here…", on_change=_persist)
    transcript_upload_key = f"transcript_upload_{st.session_state.upload_version}"
    transcript_file = st.file_uploader("Or upload transcript (.txt, max 2 MB)", type=["txt"], key=transcript_upload_key, max_upload_size=2, on_change=_cache_uploaded_transcript, args=(transcript_upload_key,))
    if st.session_state.get("upload_message"):
        st.info(st.session_state.pop("upload_message"))
    notes = st.text_area("Secretary's speaker notes (required)", key="speaker_notes", height=130, placeholder="Example: Amina chaired the meeting. David reported on the budget…", on_change=_persist)

    st.subheader("2 · Choose the minutes format")
    options = [""] + template_ids
    selected = st.selectbox("Saved template", options, format_func=lambda item: "Choose a saved template…" if not item else template_names.get(item, "Saved template"), key="selected_template_id", on_change=_persist)
    format_prompt = st.text_area("Or describe the structure", key="format_prompt", height=100, placeholder="Example: 1.0 Opening  2.0 Matters arising  3.0 AOB", on_change=_persist)
    new_template_file = st.file_uploader("Add and save a reusable template/reference (.docx, .pdf, or .txt; max 8 MB)", type=["docx", "pdf", "txt"], key="template_upload", max_upload_size=8)
    if new_template_file:
        default_name = Path(new_template_file.name).stem
        template_name = st.text_input("Name this template", value=default_name, key="new_template_name")
        st.button("Save template to library", on_click=_save_uploaded_template)
        if st.session_state.get("template_message"):
            st.info(st.session_state.pop("template_message"))

with right:
    st.subheader("3 · Generate and review")
    if st.button("Generate draft minutes", type="primary", use_container_width=True):
        try:
            transcript = read_transcript_text(pasted, transcript_file.name if transcript_file else None, transcript_file.getvalue() if transcript_file else None)
            if not transcript:
                raise ValueError("Add a transcript by pasting text or uploading a .txt file.")
            if not notes.strip():
                raise ValueError("Speaker notes are required. Add key statements and who said them.")
            reference_text = ""
            if selected:
                template = get_template(selected)
                if not template:
                    raise ValueError("That saved template could not be found. Choose or upload another one.")
                reference_text = template.get("text", "")
            elif format_prompt.strip():
                reference_text = format_prompt.strip()
            else:
                raise ValueError("Choose a saved template or describe the desired minutes structure.")
            with st.spinner("Preparing your draft from the provided materials…"):
                result = generate_minutes(transcript, notes, reference_text)
            st.session_state.minutes = result["minutes_text"]
            st.session_state.unclear_attributions = result["unclear_attributions"]
            save_draft({"transcript": transcript, "speaker_notes": notes, "format_prompt": reference_text, "selected_template_id": selected or "", "minutes": st.session_state.minutes, "unclear_attributions": st.session_state.unclear_attributions, "saved_at": datetime.now(timezone.utc).isoformat()})
            st.success("Draft generated. Review and edit it before using it as official minutes.")
        except Exception as exc:
            st.error(f"Could not generate minutes: {exc}")
            _persist()

    minutes = st.text_area("Editable draft minutes", key="minutes", height=370, placeholder="Generated minutes will appear here. You can edit the text before downloading.", on_change=_persist)
    if st.session_state.get("unclear_attributions"):
        st.warning("Please clarify these speaker attributions before finalizing:")
        for item in st.session_state.unclear_attributions:
            st.write(f"- {item}")
    if minutes.strip():
        docx_data = export_docx(minutes)
        pdf_data = export_pdf(minutes)
        download_left, download_right = st.columns(2)
        with download_left:
            st.download_button("Download DOCX", docx_data, file_name="meeting-minutes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with download_right:
            st.download_button("Download PDF", pdf_data, file_name="meeting-minutes.pdf", mime="application/pdf", use_container_width=True)

st.divider()
st.button("Clear current meeting draft", type="secondary", on_click=_clear_meeting)
if st.session_state.get("clear_message"):
    st.success(st.session_state.pop("clear_message"))
st.markdown(
    f'''<footer class="app-footer">
    <p><strong>Privacy:</strong> Generate sends the transcript, notes, and format reference to Google Gemini. Google may use unpaid-tier content to improve products and have it reviewed by people. Use synthetic data only—not real or confidential meeting records.</p>
    <p>Model: {MODEL_NAME} · Drafts and templates are stored locally outside this project.</p>
    </footer>''',
    unsafe_allow_html=True,
)
