"""Convert two-color images in a folder to black foreground artwork."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.formatter import convert_to_black
from src.st_utils.downloads import png_bytes


OUTPUT_SUFFIX = "-black"
SUPPORTED_SUFFIXES = frozenset({".png", ".jpg", ".jpeg"})


def is_converted(path: Path) -> bool:
    """Return whether a filename already uses this script's output suffix."""
    return path.stem.casefold().endswith(OUTPUT_SUFFIX)


def convert_files_in_folder(
    folder: Path,
    *,
    transparent_background: bool = False,
) -> tuple[int, int]:
    """Convert immediate image files and return processed and failed counts."""
    processed = 0
    failed = 0

    for source_path in sorted(folder.glob("*")):
        if (
            not source_path.is_file()
            or source_path.suffix.casefold() not in SUPPORTED_SUFFIXES
            or is_converted(source_path)
        ):
            continue

        output_path = source_path.with_name(
            f"{source_path.stem}{OUTPUT_SUFFIX}.png"
        )
        try:
            with Image.open(source_path) as source:
                source.load()
                converted = convert_to_black(
                    source,
                    transparent_background=transparent_background,
                )
            output_path.write_bytes(png_bytes(converted))
        except (OSError, UnidentifiedImageError, ValueError) as error:
            failed += 1
            print(f"Could not convert {source_path.name}: {error}", file=sys.stderr)
        else:
            processed += 1
            print(f"Converted {source_path.name} -> {output_path.name}")

    return processed, failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert darker areas to black and lighter areas to white for "
            "every two-color image in a folder."
        )
    )
    parser.add_argument("folder", help="Folder containing PNG or JPG files.")
    parser.add_argument(
        "--transparent",
        action="store_true",
        help="Convert the light/background color to transparency instead of white.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = Path(args.folder)

    if not folder.is_dir():
        print(f"Folder does not exist or is not a directory: {folder}", file=sys.stderr)
        return 2

    processed, failed = convert_files_in_folder(
        folder,
        transparent_background=args.transparent,
    )
    print(f"Finished: {processed} converted, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
