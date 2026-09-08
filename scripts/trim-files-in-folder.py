"""Trim every untrimmed file in one folder to its visible content."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.formatter import trim_image
from src.st_utils.downloads import png_bytes


TRIMMED_SUFFIX = "-trimmed"
SUPPORTED_SUFFIXES = frozenset({".png", ".jpg", ".jpeg"})


def is_trimmed(path: Path) -> bool:
    """Return whether a filename already uses the formatter's trimmed suffix."""
    return path.stem.casefold().endswith(TRIMMED_SUFFIX)


def trim_files_in_folder(folder: Path) -> tuple[int, int]:
    """Trim immediate files in a folder and return processed and failed counts."""
    processed = 0
    failed = 0

    for source_path in sorted(folder.glob("*")):
        if (
            not source_path.is_file()
            or source_path.suffix.casefold() not in SUPPORTED_SUFFIXES
            or is_trimmed(source_path)
        ):
            continue

        output_path = source_path.with_name(
            f"{source_path.stem}{TRIMMED_SUFFIX}.png"
        )
        try:
            with Image.open(source_path) as source:
                source.load()
                trimmed = trim_image(source)
            output_path.write_bytes(png_bytes(trimmed))
        except (OSError, UnidentifiedImageError, ValueError) as error:
            failed += 1
            print(f"Could not trim {source_path.name}: {error}", file=sys.stderr)
        else:
            processed += 1
            print(f"Trimmed {source_path.name} -> {output_path.name}")

    return processed, failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Trim exterior white or transparent space from every untrimmed "
            "file in a folder."
        )
    )
    parser.add_argument("folder", help="Folder containing files to trim.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = Path(args.folder)

    if not folder.is_dir():
        print(f"Folder does not exist or is not a directory: {folder}", file=sys.stderr)
        return 2

    processed, failed = trim_files_in_folder(folder)
    print(f"Finished: {processed} trimmed, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
