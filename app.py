"""Streamlit entry point for the icon formatter."""

import streamlit as st

from src.st_pages.icon_formatter import render_icon_formatter


st.set_page_config(
    page_title="Icon Formatter",
    page_icon="🎨",
    layout="wide",
)

render_icon_formatter()
