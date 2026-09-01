"""Color mappings for the solid and dominant variants."""

from __future__ import annotations

from PIL import Image

from src.config.icon import GRAY, TRANSPARENT, WHITE
from src.formatter.palette import flattened_data


def map_variant(
    standard: Image.Image,
    theme: tuple[int, int, int],
    variant_type: str,
) -> Image.Image:
    """Map an exact three-color standard icon to a two-color variant."""
    if variant_type == "solid":
        mapping = {theme: theme, WHITE: theme, GRAY: WHITE}
    elif variant_type == "dominant":
        mapping = {theme: theme, WHITE: WHITE, GRAY: theme}
    else:
        raise ValueError(f"Unknown variant type: {variant_type}")

    source_pixels = list(flattened_data(standard.convert("RGBA")))
    replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    for pixel in set(source_pixels):
        red, green, blue, alpha = pixel
        if alpha == 0:
            replacements[pixel] = TRANSPARENT
            continue
        source_rgb = (red, green, blue)
        if source_rgb not in mapping:
            raise ValueError(f"Unexpected standard-icon color: {source_rgb}")
        replacements[pixel] = (*mapping[source_rgb], alpha)

    result = Image.new("RGBA", standard.size)
    result.putdata([replacements[pixel] for pixel in source_pixels])
    return result
