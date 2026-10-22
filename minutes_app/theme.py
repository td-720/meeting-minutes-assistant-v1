from __future__ import annotations

from string import Template

HARBOR_LIGHT = {
    "background": "#F3F8FB",
    "surface": "#FFFFFF",
    "text": "#16324F",
    "muted": "#4B6275",
    "border": "#708899",
    "primary": "#075985",
    "primary_hover": "#064A6F",
    "on_primary": "#FFFFFF",
    "link": "#075985",
    "warning_background": "#FFF4CC",
    "warning_text": "#5C3B00",
}


def _linear_channel(channel: int) -> float:
    value = channel / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(color: str) -> float:
    value = color.lstrip("#")
    if len(value) != 6:
        raise ValueError("Color must be a six-digit hex value.")
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return 0.2126 * _linear_channel(red) + 0.7152 * _linear_channel(green) + 0.0722 * _linear_channel(blue)


def contrast_ratio(foreground: str, background: str) -> float:
    first, second = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (first + 0.05) / (second + 0.05)


def theme_css() -> str:
    stylesheet = Template("""
<style>
:root {
  color-scheme: light;
  --app-background: $background;
  --app-surface: $surface;
  --app-text: $text;
  --app-muted: $muted;
  --app-border: $border;
  --app-primary: $primary;
  --app-primary-hover: $primary_hover;
  --app-primary-text: $on_primary;
  --app-link: $link;
  --app-warning-background: $warning_background;
  --app-warning-text: $warning_text;
}
.stApp, [data-testid="stAppViewContainer"] {
  background: var(--app-background) !important;
  color: var(--app-text) !important;
}
[data-testid="stHeader"] { background: var(--app-background) !important; }
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li, h1, h2, h3, h4, h5, h6,
label, legend, [data-testid="stWidgetLabel"] p {
  color: var(--app-text) !important;
}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p,
small, .stFileUploader small, [data-testid="stFileUploaderDropzoneInstructions"] {
  color: var(--app-muted) !important;
}
a, a:visited { color: var(--app-link) !important; }
.hero {
  padding: 1.3rem 1.5rem;
  border-radius: 12px;
  color: var(--app-primary-text) !important;
  background: var(--app-primary);
  margin-bottom: 1rem;
}
.hero h1, .hero p { color: var(--app-primary-text) !important; }
.hero p { margin-bottom: .1rem; }
.privacy {
  padding: .8rem 1rem;
  background: var(--app-warning-background);
  color: var(--app-warning-text) !important;
  border: 1px solid var(--app-border);
  border-radius: 8px;
}
.privacy strong, .privacy p { color: var(--app-warning-text) !important; }
.app-footer {
  margin-top: 1rem;
  padding: .65rem 0 1.1rem;
  border-top: 1px solid var(--app-border);
  color: var(--app-muted) !important;
  font-size: .75rem;
  line-height: 1.45;
}
.app-footer p { color: var(--app-muted) !important; margin: .25rem 0; }
.app-footer strong { color: var(--app-text) !important; }
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
  color: var(--app-text) !important;
  background: var(--app-surface) !important;
  border-color: var(--app-border) !important;
}
[data-testid="stTextAreaRootElement"] {
  background: var(--app-surface) !important;
  border: 1px solid var(--app-border) !important;
}
[data-testid="stTextAreaRootElement"] textarea {
  background: transparent !important;
  color: var(--app-text) !important;
}
[data-testid="stSelectbox"] [role="combobox"] {
  background: var(--app-surface) !important;
  color: var(--app-text) !important;
  border-color: var(--app-border) !important;
}
textarea::placeholder, input::placeholder { color: var(--app-muted) !important; opacity: 1 !important; }
[data-testid="stFileUploaderDropzone"] {
  background: var(--app-surface) !important;
  border: 1px solid var(--app-border) !important;
}
[data-testid="stFileUploaderDropzone"] button {
  color: var(--app-primary) !important;
  border-color: var(--app-primary) !important;
}
[data-testid="stBaseButton-primary"], .stButton > button[kind="primary"] {
  color: var(--app-primary-text) !important;
  background: var(--app-primary) !important;
  border: 2px solid var(--app-primary) !important;
}
[data-testid="stBaseButton-primary"] * { color: var(--app-primary-text) !important; }
[data-testid="stBaseButton-primary"]:hover, .stButton > button[kind="primary"]:hover {
  background: var(--app-primary-hover) !important;
  border-color: var(--app-primary-hover) !important;
}
[data-testid="stBaseButton-secondary"], .stButton > button[kind="secondary"],
.stDownloadButton > button {
  color: var(--app-text) !important;
  background: var(--app-surface) !important;
  border: 1px solid var(--app-border) !important;
}
button:focus-visible, textarea:focus-visible, input:focus-visible,
[role="combobox"]:focus-visible {
  outline: 3px solid var(--app-primary) !important;
  outline-offset: 2px !important;
}
[data-testid="stAlert"] { border: 1px solid var(--app-border) !important; }
[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p { color: var(--app-text) !important; }
hr { border-color: var(--app-border) !important; }
</style>
""")
    return stylesheet.substitute(HARBOR_LIGHT)
