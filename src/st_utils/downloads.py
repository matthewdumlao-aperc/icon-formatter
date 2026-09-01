"""In-memory image downloads for Streamlit."""

from io import BytesIO

from PIL import Image


def png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()
