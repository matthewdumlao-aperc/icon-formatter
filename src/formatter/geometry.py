"""Canvas and artwork geometry for 1000 px icon output."""

from __future__ import annotations

from PIL import Image, ImageChops, ImageDraw

from src.config.icon import (
    ANTIALIAS_SCALE,
    INTERNAL_ARTWORK_COLOR,
    TRANSPARENT,
    WHITE,
)
from src.formatter.palette import snap_rgb_to_palette


def resize_rgba(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize RGBA pixels in premultiplied form to avoid transparent fringes."""
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def fit_artwork(image: Image.Image, artwork_size: int) -> Image.Image:
    """Fit artwork inside a centered square without distortion."""
    if image.width <= 0 or image.height <= 0:
        raise ValueError("The uploaded image has invalid dimensions.")

    scale = min(artwork_size / image.width, artwork_size / image.height)
    fitted_size = (
        max(1, round(image.width * scale)),
        max(1, round(image.height * scale)),
    )
    fitted = resize_rgba(image, fitted_size)
    fitted = snap_rgb_to_palette(fitted, (WHITE, INTERNAL_ARTWORK_COLOR))

    content = Image.new("RGBA", (artwork_size, artwork_size), (*WHITE, 255))
    offset = (
        (artwork_size - fitted.width) // 2,
        (artwork_size - fitted.height) // 2,
    )
    content.alpha_composite(fitted, offset)
    return content


def _circle_layer(
    theme: tuple[int, int, int],
    canvas_size: int,
    theme_ring_width: int,
) -> Image.Image:
    """Draw the outer circle at high resolution, then antialias it."""
    large_size = canvas_size * ANTIALIAS_SCALE
    ring = theme_ring_width * ANTIALIAS_SCALE
    large = Image.new("RGBA", (large_size, large_size), TRANSPARENT)
    draw = ImageDraw.Draw(large)
    draw.ellipse((0, 0, large_size - 1, large_size - 1), fill=(*theme, 255))
    draw.ellipse(
        (ring, ring, large_size - ring - 1, large_size - ring - 1),
        fill=(*WHITE, 255),
    )
    resized = resize_rgba(large, (canvas_size, canvas_size))
    # The circle does not contain the internal artwork marker. Snapping its
    # antialiased inner edge against all three standard colors can create a
    # marker seam that later becomes white in the solid variant.
    return snap_rgb_to_palette(resized, (theme, WHITE))


def _artwork_mask(
    canvas_size: int,
    artwork_size: int,
    padding: int,
    theme_ring_width: int,
    white_ring_width: int,
) -> Image.Image:
    """Intersect the artwork circle with the user-selected white clearance."""
    artwork_circle = Image.new("L", (artwork_size, artwork_size), 0)
    ImageDraw.Draw(artwork_circle).ellipse(
        (0, 0, artwork_size - 1, artwork_size - 1),
        fill=255,
    )

    clearance = theme_ring_width + white_ring_width
    safe_circle = Image.new("L", (canvas_size, canvas_size), 0)
    ImageDraw.Draw(safe_circle).ellipse(
        (
            clearance,
            clearance,
            canvas_size - clearance - 1,
            canvas_size - clearance - 1,
        ),
        fill=255,
    )
    safe_crop = safe_circle.crop(
        (padding, padding, padding + artwork_size, padding + artwork_size)
    )
    return ImageChops.multiply(artwork_circle, safe_crop)


def build_standard_icon(
    artwork: Image.Image,
    theme: tuple[int, int, int],
    artwork_size: int,
    padding: int,
    theme_ring_width: int,
    white_ring_width: int,
) -> Image.Image:
    """Add the theme ring and white gap to normalized two-color artwork."""
    canvas_size = artwork_size + (2 * padding)
    standard = _circle_layer(theme, canvas_size, theme_ring_width)
    content = fit_artwork(artwork, artwork_size)
    mask = _artwork_mask(
        canvas_size,
        artwork_size,
        padding,
        theme_ring_width,
        white_ring_width,
    )
    standard.paste(content, (padding, padding), mask)
    return snap_rgb_to_palette(standard, (theme, WHITE, INTERNAL_ARTWORK_COLOR))


def build_uncircled_artwork(
    artwork: Image.Image,
    artwork_size: int,
    padding: int,
) -> Image.Image:
    """Fit normalized artwork on a transparent canvas without circular clipping."""
    canvas_size = artwork_size + (2 * padding)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), TRANSPARENT)
    canvas.alpha_composite(fit_artwork(artwork, artwork_size), (padding, padding))
    return canvas
