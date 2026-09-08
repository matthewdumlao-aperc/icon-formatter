"""Color mappings for the solid and dominant variants."""

from __future__ import annotations

from PIL import Image

from src.config.icon import BLACK, INTERNAL_ARTWORK_COLOR, TRANSPARENT, WHITE
from src.formatter.palette import flattened_data


def map_variant(
    standard: Image.Image,
    theme: tuple[int, int, int],
    variant_type: str,
) -> Image.Image:
    """Map an exact three-color standard icon to a two-color variant."""
    if variant_type == "solid":
        mapping = {theme: theme, WHITE: theme, INTERNAL_ARTWORK_COLOR: WHITE}
    elif variant_type == "dominant":
        mapping = {theme: theme, WHITE: WHITE, INTERNAL_ARTWORK_COLOR: theme}
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


def reveal_black_artwork(image: Image.Image) -> Image.Image:
    """Convert the internal artwork marker to black for public output."""
    source_pixels = list(flattened_data(image.convert("RGBA")))
    replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    for pixel in set(source_pixels):
        red, green, blue, alpha = pixel
        if alpha != 0 and (red, green, blue) == INTERNAL_ARTWORK_COLOR:
            replacements[pixel] = (*BLACK, alpha)
        else:
            replacements[pixel] = pixel

    result = Image.new("RGBA", image.size)
    result.putdata([replacements[pixel] for pixel in source_pixels])
    return result


def map_uncircled_dominant(
    artwork: Image.Image,
    theme: tuple[int, int, int],
    *,
    transparent_background: bool = True,
) -> Image.Image:
    """Map marked artwork to the theme and choose its background treatment."""
    source_pixels = list(flattened_data(artwork.convert("RGBA")))
    replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    background = TRANSPARENT if transparent_background else (*WHITE, 255)
    for pixel in set(source_pixels):
        red, green, blue, alpha = pixel
        if alpha == 0 or (red, green, blue) == WHITE:
            replacements[pixel] = background
        elif (red, green, blue) == INTERNAL_ARTWORK_COLOR:
            replacements[pixel] = (*theme, alpha)
        else:
            raise ValueError(
                f"Unexpected normalized-artwork color: {(red, green, blue)}"
            )

    result = Image.new("RGBA", artwork.size)
    result.putdata([replacements[pixel] for pixel in source_pixels])
    return result
