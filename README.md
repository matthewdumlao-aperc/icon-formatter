# Icon Formatter

A Streamlit app for turning white artwork with black or gray foreground into four
PNG icon variants using a user-provided theme color and geometry.

## Inputs

- One PNG, JPG, or JPEG icon at a time
- Artwork containing white with black or gray foreground; pixels below the
  default luminance threshold of 192 are mapped to foreground
- A theme color supplied as a six-digit hex value
- Artwork size, padding, theme-ring width, and white-ring width in pixels

Transparent pixels are treated as white without cropping the uploaded canvas.
PNG, JPG, and JPEG images all retain their original exterior margins.

Black artwork is temporarily represented by an internal `#808080` marker while
variants are built, allowing `#000000` to remain available as a theme color.
Public outputs use black and white as specified.

## Outputs

- **Standard:** configurable theme and white rings around the normalized
  white/black artwork
- **Solid:** white is mapped to the theme color and black is mapped to white
- **Dominant:** white remains white and black is mapped to the theme color
- **Dominant without circle:** black is mapped to the theme color; white remains
  white by default and can optionally become transparent; no rings or circular
  clipping are applied

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
- Allow the circle-free dominant background to be white or transparent,
  defaulting to white.
- Provide a reusable specification line for prompting an LLM to create suitable
  source artwork.
- Name downloads as `{name}-{type}-{six-digit-theme-hex}.png`.

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
