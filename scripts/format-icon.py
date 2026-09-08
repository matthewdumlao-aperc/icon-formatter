"""Generate app icon variants and a trimmed derivative from one local image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.formatter import format_icon, trim_image
from src.formatter.palette import format_hex, parse_theme_hex
from src.st_utils.downloads import png_bytes
from src.st_utils.uploads import open_image_upload


def format_icon_file(
    icon_path: Path,
    theme_value: str,
    *,
    transparent_background: bool = True,
) -> list[Path]:
    """Render all variants beside one source file and return their paths."""
    theme = parse_theme_hex(theme_value)
    source = open_image_upload(icon_path.read_bytes())
    icon_set = format_icon(
        source,
        theme,
        transparent_background=transparent_background,
    )
    theme_hex = format_hex(theme)[1:]

    output_paths: list[Path] = []
    for variant_name, image in icon_set.variants().items():
        output_path = icon_path.with_name(
            f"{icon_path.stem}-{variant_name}-{theme_hex}.png"
        )
        output_path.write_bytes(png_bytes(image))
        output_paths.append(output_path)

    trimmed_variant = trim_image(icon_set.dominant_no_circle)
    trimmed_path = icon_path.with_name(
        f"{icon_path.stem}-dominant-no-circle-trimmed-{theme_hex}.png"
    )
    trimmed_path.write_bytes(png_bytes(trimmed_variant))
    output_paths.append(trimmed_path)

    return output_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate all four app variants and a trimmed circle-free "
            "dominant variant for one icon."
        )
    )
    parser.add_argument("icon", help="Path to a PNG, JPG, or JPEG icon.")
    parser.add_argument(
        "color",
        help="Six-digit theme hex with or without #, such as 9C5E31.",
    )
    parser.add_argument(
        "--not-transparent",
        action="store_true",
        help=(
            "Keep the circle-free dominant background white instead of "
            "making it transparent."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    icon_path = Path(args.icon)

    if not icon_path.is_file():
        print(f"Icon does not exist or is not a file: {icon_path}", file=sys.stderr)
        return 2

    try:
        output_paths = format_icon_file(
            icon_path,
            args.color,
            transparent_background=not args.not_transparent,
        )
    except (OSError, UnidentifiedImageError, ValueError) as error:
        print(f"Could not format {icon_path.name}: {error}", file=sys.stderr)
        return 1

    for output_path in output_paths:
        print(f"Created {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
