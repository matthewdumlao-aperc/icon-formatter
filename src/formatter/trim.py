"""Crop exterior white and transparent space from uploaded artwork."""

from PIL import Image, ImageChops

from src.config.icon import WHITE


WHITE_TOLERANCE = 15


def trim_image(image: Image.Image) -> Image.Image:
    """Return a tight RGBA crop around pixels that are not transparent or white."""
    if image.width <= 0 or image.height <= 0:
        raise ValueError("The uploaded image has invalid dimensions.")

    rgba = image.convert("RGBA")
    flattened = Image.new("RGBA", rgba.size, (*WHITE, 255))
    flattened.alpha_composite(rgba)

    white_background = Image.new("RGB", rgba.size, WHITE)
    difference = ImageChops.difference(flattened.convert("RGB"), white_background)
    content_mask = difference.point(
        lambda value: 255 if value > WHITE_TOLERANCE else 0
    )
    bounds = content_mask.getbbox()
    if bounds is None:
        raise ValueError("The uploaded image contains no non-white artwork.")

    return rgba.crop(bounds)
