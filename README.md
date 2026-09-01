# Icon Formatter

A Streamlit app for turning white and `#808080` artwork into four consistent
PNG icon variants using a user-provided theme color and geometry.

## Inputs

- One PNG, JPG, or JPEG icon at a time
- Artwork containing white and `#808080`; off-palette pixels are mapped to the
  nearest of those two colors
- A theme color supplied as a six-digit hex value
- Artwork size, padding, theme-ring width, and white-ring width in pixels

Transparent exterior margins are cropped from PNG uploads. Any remaining
transparent pixels are treated as white. JPG images use their full canvas.

## Outputs

- **Standard:** configurable theme and white rings around the normalized
  white/gray artwork
- **Solid:** white is mapped to the theme color and gray is mapped to white
- **Dominant:** white remains white and gray is mapped to the theme color
- **Dominant without circle:** gray is mapped to the theme color while white
  becomes transparent; no rings or circular clipping are applied

The artwork is centered without changing its aspect ratio. Output width and
height equal the artwork size plus twice the per-side padding. Defaults are a
900 px artwork area, 50 px padding, 30 px theme ring, and 20 px white ring.

Rendering only starts when **Render icons** is selected. All four generated
variants are then shown together with individual download buttons.

## Interface

- Accept one uploaded file and retain its remove control after selection.
- Present the upload, theme, and four geometry settings in six equal columns.
- Use a fixed 1380 px application container for the desktop layout.
- Show all four generated variants side by side as centered 250 px previews.
- Place palette-correction and render-setting details below the previews.
- Provide a reusable specification line for prompting an LLM to create suitable
  source artwork.

## Local development

Install the dependencies from `requirements.txt`, then run:

```bash
/home/dev/Desktop/venv-streamlit/bin/python -m streamlit run app.py
```

Run the tests with:

```bash
/home/dev/Desktop/venv-streamlit/bin/python -m unittest discover -s tests -v
```

## Project layout

```text
app.py                  Streamlit entry point
src/config/             Application and image-formatting constants
src/formatter/          Streamlit-independent image processing
src/sample/             Reference input artwork
src/st_pages/           Streamlit page renderers
src/st_utils/           Streamlit-specific helpers
tests/                  Automated tests
```
