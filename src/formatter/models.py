"""Data returned by the icon-formatting pipeline."""

from dataclasses import dataclass

from PIL import Image


@dataclass(frozen=True)
class PaletteReport:
    """Summary of changes made while normalizing an uploaded image."""

    source_color_count: int
    corrected_pixel_count: int
    transparent_pixel_count: int
    cropped_transparent_margin: bool


@dataclass(frozen=True)
class IconSet:
    """The normalized upload and its four generated variants."""

    normalized_artwork: Image.Image
    standard: Image.Image
    solid: Image.Image
    dominant: Image.Image
    dominant_no_circle: Image.Image
    palette_report: PaletteReport

    def variants(self) -> dict[str, Image.Image]:
        return {
            "standard": self.standard,
            "solid": self.solid,
            "dominant": self.dominant,
            "dominant-no-circle": self.dominant_no_circle,
        }
