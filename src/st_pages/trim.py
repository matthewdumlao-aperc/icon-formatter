"""A directly addressable page for trimming icon artwork."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import UnidentifiedImageError

from src.formatter import trim_image
from src.st_utils.downloads import png_bytes
from src.st_utils.layout import apply_page_layout
from src.st_utils.uploads import open_image_upload


RESULT_KEY = "trimmed_icon_result"


def render_trim() -> None:
    apply_page_layout()
    st.title("Trim Icon")
    st.write(
        "Upload an icon to crop away its exterior white and transparent space."
    )

    with st.form("trim_icon_controls"):
        upload_column, *_ = st.columns(6)
        with upload_column:
            uploaded = st.file_uploader(
                "Icon artwork",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=False,
                help="PNG, JPG, and JPEG images are supported.",
            )

        trim_clicked = st.form_submit_button(
            "Trim icon",
            type="primary",
            width="stretch",
        )

    if trim_clicked:
        st.session_state.pop(RESULT_KEY, None)
        if uploaded is None:
            st.error("Upload a PNG, JPG, or JPEG image before trimming.")
        else:
            try:
                source = open_image_upload(uploaded.getvalue())
                with st.spinner("Trimming icon…"):
                    trimmed = trim_image(source)
                    encoded = png_bytes(trimmed)
            except (OSError, UnidentifiedImageError, ValueError) as error:
                st.error(f"Could not trim this image: {error}")
            else:
                st.session_state[RESULT_KEY] = {
                    "image": trimmed,
                    "encoded": encoded,
                    "original_name": Path(uploaded.name).stem or "icon",
                    "original_size": source.size,
                }

    result = st.session_state.get(RESULT_KEY)
    if result is None:
        st.caption("Choose an image, then trim it to its visible content.")
        return

    _, output_column, _ = st.columns([1, 0.5, 1], gap="large")
    with output_column:
        st.image(result["image"], width=250)
        st.download_button(
            "Download",
            data=result["encoded"],
            file_name=f"{result['original_name']}-trimmed.png",
            mime="image/png",
            key="download-trimmed",
            on_click="ignore",
            width="stretch",
        )

    original_width, original_height = result["original_size"]
    trimmed_width, trimmed_height = result["image"].size
    st.caption(
        f"Original: {original_width} × {original_height} px · "
        f"Trimmed: {trimmed_width} × {trimmed_height} px · RGBA PNG"
    )
