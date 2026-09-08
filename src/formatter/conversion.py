"""Threshold-based conversion of two-color artwork to black and white."""

from PIL import Image

from src.config.icon import BLACK, DEFAULT_FOREGROUND_THRESHOLD
from src.formatter.palette import normalize_uploaded_artwork
from src.formatter.variants import map_uncircled_dominant, reveal_black_artwork


def convert_to_black(
    image: Image.Image,
    *,
    transparent_background: bool = False,
    threshold: int = DEFAULT_FOREGROUND_THRESHOLD,
) -> Image.Image:
    """Map darker pixels to black and lighter pixels to white or transparency."""
    normalized, _ = normalize_uploaded_artwork(
        image,
        foreground_threshold=threshold,
    )
    if transparent_background:
        return map_uncircled_dominant(
            normalized,
            BLACK,
            transparent_background=True,
        )
    return reveal_black_artwork(normalized)
