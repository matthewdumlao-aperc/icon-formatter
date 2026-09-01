"""The icon formatter Streamlit page."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

from src.config.icon import (
    ACCEPTED_IMAGE_FORMATS,
    DEFAULT_ARTWORK_SIZE,
    DEFAULT_PADDING,
    DEFAULT_THEME_RING_WIDTH,
    DEFAULT_WHITE_RING_WIDTH,
)
from src.formatter import format_icon
from src.formatter.models import PaletteReport
from src.formatter.palette import format_hex, parse_theme_hex
from src.st_utils.downloads import png_bytes


RESULT_KEY = "rendered_icon_result"
PROMPT_TEMPLATE = (
    "Let's make an icon for: \n\n"
    "Specifications: Create the icon artwork at 900 × 900 px using only "
    "#FFFFFF and #000000. Do not add an outer circle. Keep the design bold, "
    "centered, and recognizable when reduced to 450 × 450 px."
)


def _open_upload(data: bytes) -> Image.Image:
    with Image.open(BytesIO(data)) as opened:
        if opened.format not in ACCEPTED_IMAGE_FORMATS:
            raise ValueError("Upload a PNG, JPG, or JPEG image.")
        opened.load()
        return opened.copy()


def _show_palette_report(report: PaletteReport) -> None:
    details = [f"Detected {report.source_color_count:,} source RGB color(s)."]
    if report.corrected_pixel_count:
        details.append(
            f"Mapped {report.corrected_pixel_count:,} pixel(s) to black or white."
        )
    else:
        details.append("The visible artwork already used the standard palette.")
    if report.transparent_pixel_count:
        details.append(
            f"Filled {report.transparent_pixel_count:,} transparent or "
            "partially transparent pixel(s) with white."
        )
    st.markdown(
        f'<div class="palette-report">{" ".join(details)}</div>',
        unsafe_allow_html=True,
    )


def _show_prompt_guide() -> None:
    st.divider()
    st.markdown("#### Icon prompt guide")
    st.caption("Fill in the icon details after the colon, then copy the prompt:")
    st.code(PROMPT_TEMPLATE, language=None, wrap_lines=True)


def render_icon_formatter() -> None:
    st.html(
        """
        <style>
        div[data-testid="stMainBlockContainer"] {
            box-sizing: border-box;
            width: 1380px;
            min-width: 1380px;
            max-width: 1380px;
            margin-inline: auto;
            padding-top: 2rem;
        }
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
            margin-inline: auto;
        }
        div[data-testid="stImage"] img {
            display: block;
            margin-inline: auto;
        }
        div[data-testid="stColumn"]
        div[data-testid="stElementContainer"]:has(div[data-testid="stImage"]) {
            width: fit-content !important;
            margin-inline: auto !important;
        }
        section[data-testid="stFileUploaderDropzone"]
        > div:has([data-testid="stFileUploaderDropzoneInstructions"]) {
            display: none;
        }
        section[data-testid="stFileUploaderDropzone"] {
            min-height: 0;
            padding: 0;
            border: 0;
            background: transparent;
        }
        div[data-testid="stFileUploader"]:has(
            div[data-testid="stFileUploaderFile"]
        ) section[data-testid="stFileUploaderDropzone"] button {
            display: none;
        }
        .palette-report {
            background: #f5f5f5;
            border: 1px solid #e6e6e6;
            border-radius: 0.5rem;
            color: #666666;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0 1rem;
        }
        </style>
        """
    )
    st.title("Icon Formatter")
    st.write(
        "Upload white and #000000 artwork, then provide the theme color for "
        "the generated icon set."
    )

    with st.form("icon_formatter_controls"):
        (
            upload_column,
            theme_column,
            size_column,
            padding_column,
            theme_ring_column,
            white_ring_column,
        ) = st.columns(6)
        with upload_column:
            uploaded = st.file_uploader(
                "Icon artwork",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=False,
                help=(
                    "PNG transparency is filled with white. "
                    "JPG and JPEG are also supported."
                ),
            )
        with theme_column:
            theme_value = st.text_input(
                "Theme color",
                value="#000000",
                max_chars=7,
                help="Enter a six-digit RGB hex color. Black is supported.",
            )

        with size_column:
            artwork_size = st.number_input(
                "Artwork size (px)",
                min_value=100,
                max_value=1600,
                value=DEFAULT_ARTWORK_SIZE,
                step=10,
                help="The square area used to fit and center the uploaded artwork.",
            )
        with padding_column:
            padding = st.number_input(
                "Padding per side (px)",
                min_value=0,
                max_value=200,
                value=DEFAULT_PADDING,
                step=5,
                help="Output size equals artwork size plus padding on both sides.",
            )

        with theme_ring_column:
            theme_ring_width = st.number_input(
                "Theme ring width (px)",
                min_value=1,
                max_value=200,
                value=DEFAULT_THEME_RING_WIDTH,
                step=1,
            )
        with white_ring_column:
            white_ring_width = st.number_input(
                "White ring width (px)",
                min_value=0,
                max_value=200,
                value=DEFAULT_WHITE_RING_WIDTH,
                step=1,
                help="Larger values clip the artwork farther inside the theme ring.",
            )

        render_clicked = st.form_submit_button(
            "Render icons",
            type="primary",
            width="stretch",
        )

    if render_clicked:
        st.session_state.pop(RESULT_KEY, None)
        if uploaded is None:
            st.error("Upload a PNG, JPG, or JPEG image before rendering.")
        else:
            try:
                theme = parse_theme_hex(theme_value)
                source = _open_upload(uploaded.getvalue())
                with st.spinner("Rendering all four variants…"):
                    icon_set = format_icon(
                        source,
                        theme,
                        artwork_size=int(artwork_size),
                        padding=int(padding),
                        theme_ring_width=int(theme_ring_width),
                        white_ring_width=int(white_ring_width),
                    )
                    encoded_variants = {
                        name: png_bytes(image)
                        for name, image in icon_set.variants().items()
                    }
            except (OSError, UnidentifiedImageError, ValueError) as error:
                st.error(f"Could not format this image: {error}")
            else:
                st.session_state[RESULT_KEY] = {
                    "icon_set": icon_set,
                    "encoded_variants": encoded_variants,
                    "original_name": Path(uploaded.name).stem or "icon",
                    "theme": theme,
                    "artwork_size": int(artwork_size),
                    "padding": int(padding),
                    "theme_ring_width": int(theme_ring_width),
                    "white_ring_width": int(white_ring_width),
                }

    result = st.session_state.get(RESULT_KEY)
    if result is None:
        st.caption("Choose the settings, then render all four icon variants.")
        _show_prompt_guide()
        return

    icon_set = result["icon_set"]
    output_size = result["artwork_size"] + (2 * result["padding"])
    columns = st.columns(4, gap="large")
    theme_hex = format_hex(result["theme"])[1:]
    for column, (name, image) in zip(columns, icon_set.variants().items()):
        with column:
            st.image(image, width=250)
            st.download_button(
                "Download",
                data=result["encoded_variants"][name],
                file_name=f"{result['original_name']}-{name}-{theme_hex}.png",
                mime="image/png",
                key=f"download-{name}",
                on_click="ignore",
                width="stretch",
            )

    _show_palette_report(icon_set.palette_report)
    st.caption(
        f"Theme: {format_hex(result['theme'])} · "
        f"Output: {output_size} × {output_size} PNG · "
        f"Artwork: {result['artwork_size']}px · "
        f"Padding: {result['padding']}px per side · "
        f"Rings: {result['theme_ring_width']}px theme + "
        f"{result['white_ring_width']}px white"
    )

    _show_prompt_guide()
