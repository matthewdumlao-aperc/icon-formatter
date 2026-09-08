"""Image-upload helpers shared by Streamlit pages."""

from io import BytesIO

from PIL import Image

from src.config.icon import ACCEPTED_IMAGE_FORMATS


def open_image_upload(data: bytes) -> Image.Image:
    """Decode one supported upload and detach it from the byte stream."""
    with Image.open(BytesIO(data)) as opened:
        if opened.format not in ACCEPTED_IMAGE_FORMATS:
            raise ValueError("Upload a PNG, JPG, or JPEG image.")
        opened.load()
        return opened.copy()
