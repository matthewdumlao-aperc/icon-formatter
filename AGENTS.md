# Working agreement

## Project purpose

This repository contains a Streamlit app that converts uploaded two-color icon
artwork into the APERC standard, solid, dominant, and circle-free dominant icon
variants.

## Source layout

- Keep the Streamlit entry point in `app.py`.
- Keep image-processing code independent of Streamlit in `src/formatter/`.
- Keep application constants in `src/config/`.
- Keep page rendering in `src/st_pages/`.
- Keep Streamlit-specific helpers in `src/st_utils/`.
- Keep tests in `tests/`, following the source layout.
- Do not add `__pycache__` directories; they are generated and ignored.

## Image invariants

- Accept PNG, JPG, and JPEG uploads.
- Treat transparent pixels as white without cropping exterior margins.
- Classify uploaded artwork as exactly white and `#000000` by nearest-color
  mapping. Use `#808080` only as an internal marker while building variants so
  black remains available as a theme color.
- Take the theme color from user-supplied hex input; never infer it from pixels.
- Preserve the artwork aspect ratio.
- Produce square RGBA PNG outputs sized as artwork plus twice the padding.
- Default to 900 px artwork, 50 px padding per side, a 30 px theme ring, and a
  20 px white ring.
- Keep artwork size, padding, theme-ring width, and white-ring width
  independently configurable.
- Do not process uploads until the user explicitly selects the render button.
- Show the standard, solid, dominant, and circle-free dominant outputs together
  after rendering.

## Interface invariants

- Keep the desktop application container fixed at 1380 px.
- Accept only one uploaded file and preserve its remove control after selection.
- Keep the upload, theme, and four geometry inputs in six equal columns.
- Center all four outputs side by side at a 250 px preview width.
- Keep processing metadata below the output row.
- Keep visible variant names out of the interface; distinguish downloaded files
  through their filename suffixes.

## Development

- Use `/home/dev/Desktop/venv-streamlit/bin/python` for local commands.
- Declare deployment dependencies in `requirements.txt`.
- Run tests with:
  `/home/dev/Desktop/venv-streamlit/bin/python -m unittest discover -s tests -v`
- Keep files with LF line endings. `.gitattributes` enforces this across Windows
  and Linux checkouts.
