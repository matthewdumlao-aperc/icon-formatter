"""Shared Streamlit page layout."""

import streamlit as st


def apply_page_layout() -> None:
    """Apply the fixed desktop layout shared by the app pages."""
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
