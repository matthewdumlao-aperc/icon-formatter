"""End-to-end public icon-formatting operation."""

from PIL import Image

from src.config.icon import (
    DEFAULT_ARTWORK_SIZE,
    DEFAULT_PADDING,
    DEFAULT_THEME_RING_WIDTH,
    DEFAULT_WHITE_RING_WIDTH,
)
from src.formatter.geometry import build_standard_icon, build_uncircled_artwork
from src.formatter.models import IconSet
from src.formatter.palette import normalize_uploaded_artwork
from src.formatter.variants import map_uncircled_dominant, map_variant


def format_icon(
    image: Image.Image,
    theme: tuple[int, int, int],
    artwork_size: int = DEFAULT_ARTWORK_SIZE,
    padding: int = DEFAULT_PADDING,
    theme_ring_width: int = DEFAULT_THEME_RING_WIDTH,
    white_ring_width: int = DEFAULT_WHITE_RING_WIDTH,
) -> IconSet:
    """Normalize one upload and return all four configured icon variants."""
    if artwork_size <= 0:
        raise ValueError("Artwork size must be greater than zero.")
    if padding < 0:
        raise ValueError("Padding cannot be negative.")
    if theme_ring_width <= 0:
        raise ValueError("Theme ring width must be greater than zero.")
    if white_ring_width < 0:
        raise ValueError("White ring width cannot be negative.")

    canvas_size = artwork_size + (2 * padding)
    if theme_ring_width + white_ring_width >= canvas_size / 2:
        raise ValueError("The ring widths leave no room for the artwork.")

    normalized, report = normalize_uploaded_artwork(image)
    standard = build_standard_icon(
        normalized,
        theme,
        artwork_size,
        padding,
        theme_ring_width,
        white_ring_width,
    )
    uncircled_artwork = build_uncircled_artwork(normalized, artwork_size, padding)
    return IconSet(
        normalized_artwork=normalized,
        standard=standard,
        solid=map_variant(standard, theme, "solid"),
        dominant=map_variant(standard, theme, "dominant"),
        dominant_no_circle=map_uncircled_dominant(uncircled_artwork, theme),
        palette_report=report,
    )
