"""Streamlit entry point for the icon formatter."""

import streamlit as st

from src.st_pages.icon_formatter import render_icon_formatter
from src.st_pages.trim import render_trim


st.set_page_config(
    page_title="Icon Formatter",
    page_icon="🎨",
    layout="wide",
)

page = st.navigation(
    [
        st.Page(
            render_icon_formatter,
            title="Icon Formatter",
            default=True,
        ),
        st.Page(
            render_trim,
            title="Trim Icon",
            url_path="trim",
            visibility="hidden",
        ),
    ],
    position="hidden",
)
page.run()
