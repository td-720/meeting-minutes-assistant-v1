from minutes_app.theme import HARBOR_LIGHT, contrast_ratio, theme_css


def test_harbor_light_text_pairs_meet_wcag_aa():
    palette = HARBOR_LIGHT
    pairs = [
        (palette["text"], palette["background"]),
        (palette["text"], palette["surface"]),
        (palette["muted"], palette["background"]),
        (palette["muted"], palette["surface"]),
        (palette["on_primary"], palette["primary"]),
        (palette["on_primary"], palette["primary_hover"]),
        (palette["link"], palette["surface"]),
        (palette["warning_text"], palette["warning_background"]),
    ]
    assert all(contrast_ratio(foreground, background) >= 4.5 for foreground, background in pairs)


def test_harbor_light_controls_have_visible_borders():
    palette = HARBOR_LIGHT
    assert contrast_ratio(palette["border"], palette["background"]) >= 3.0
    assert contrast_ratio(palette["border"], palette["surface"]) >= 3.0


def test_harbor_light_css_applies_palette_to_ui_controls():
    css = theme_css()
    for token in HARBOR_LIGHT.values():
        assert token in css
    assert "textarea" in css
    assert "stFileUploaderDropzone" in css
    assert '[data-testid="stTextAreaRootElement"]' in css
    assert '[data-testid="stSelectbox"] [role="combobox"]' in css
    assert '[data-testid="stBaseButton-primary"] *' in css
    assert "linear-gradient" not in css
