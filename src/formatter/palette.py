"""Theme parsing and two-color artwork normalization."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable

from PIL import Image

from src.config.icon import GRAY, TRANSPARENT, WHITE
from src.formatter.models import PaletteReport


HEX_COLOR = re.compile(r"^#?([0-9a-fA-F]{6})$")


def flattened_data(image: Image.Image) -> Iterable[tuple[int, int, int, int]]:
    """Return a flat RGBA pixel iterator across supported Pillow versions."""
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()


def parse_theme_hex(value: str) -> tuple[int, int, int]:
    """Parse a six-digit theme hex string and reject palette collisions."""
    match = HEX_COLOR.fullmatch(value.strip())
    if match is None:
        raise ValueError("Enter a six-digit hex color such as #0070C0.")

    digits = match.group(1)
    theme = tuple(int(digits[index : index + 2], 16) for index in (0, 2, 4))
    if theme in {WHITE, GRAY}:
        raise ValueError("The theme color must differ from white and #808080.")
    return theme


def format_hex(color: tuple[int, int, int]) -> str:
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"


def color_distance_squared(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
) -> int:
    return sum((left - right) ** 2 for left, right in zip(first, second))


def nearest_color(
    color: tuple[int, int, int],
    palette: tuple[tuple[int, int, int], ...],
) -> tuple[int, int, int]:
    return min(palette, key=lambda candidate: color_distance_squared(color, candidate))


def _flatten_against_white(pixel: tuple[int, int, int, int]) -> tuple[int, int, int]:
    red, green, blue, alpha = pixel
    if alpha == 255:
        return red, green, blue
    if alpha == 0:
        return WHITE
    return tuple(
        round((channel * alpha + 255 * (255 - alpha)) / 255)
        for channel in (red, green, blue)
    )


def normalize_uploaded_artwork(
    image: Image.Image,
) -> tuple[Image.Image, PaletteReport]:
    """Crop transparent margins, fill alpha with white, and enforce two colors."""
    rgba = image.convert("RGBA")
    alpha_bounds = rgba.getchannel("A").getbbox()
    if alpha_bounds is None:
        raise ValueError("The uploaded image is fully transparent.")

    full_bounds = (0, 0, rgba.width, rgba.height)
    cropped_margin = alpha_bounds != full_bounds
    if cropped_margin:
        rgba = rgba.crop(alpha_bounds)

    source_pixels = list(flattened_data(rgba))
    unique_pixels = Counter(source_pixels)
    replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    source_colors: set[tuple[int, int, int]] = set()
    corrected_pixels = 0
    transparent_pixels = 0

    for pixel, count in unique_pixels.items():
        flattened = _flatten_against_white(pixel)
        source_colors.add(flattened)
        replacement_rgb = nearest_color(flattened, (WHITE, GRAY))
        replacements[pixel] = (*replacement_rgb, 255)

        if pixel[3] < 255:
            transparent_pixels += count
        if flattened != replacement_rgb:
            corrected_pixels += count

    normalized = Image.new("RGBA", rgba.size)
    normalized.putdata([replacements[pixel] for pixel in source_pixels])
    report = PaletteReport(
        source_color_count=len(source_colors),
        corrected_pixel_count=corrected_pixels,
        transparent_pixel_count=transparent_pixels,
        cropped_transparent_margin=cropped_margin,
    )
    return normalized, report


def snap_rgb_to_palette(
    image: Image.Image,
    palette: tuple[tuple[int, int, int], ...],
) -> Image.Image:
    """Remove RGB colors introduced by resizing while preserving edge alpha."""
    rgba = image.convert("RGBA")
    source_pixels = list(flattened_data(rgba))
    unique_pixels = set(source_pixels)
    replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}

    for pixel in unique_pixels:
        red, green, blue, alpha = pixel
        if alpha == 0:
            replacements[pixel] = TRANSPARENT
        else:
            replacement_rgb = nearest_color((red, green, blue), palette)
            replacements[pixel] = (*replacement_rgb, alpha)

    snapped = Image.new("RGBA", rgba.size)
    snapped.putdata([replacements[pixel] for pixel in source_pixels])
    return snapped
