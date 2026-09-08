import unittest

from PIL import Image

from src.config.icon import BLACK, INTERNAL_ARTWORK_COLOR, WHITE
from src.formatter.palette import (
    flattened_data,
    normalize_uploaded_artwork,
    parse_theme_hex,
)


class ThemeColorTests(unittest.TestCase):
    def test_parses_hash_and_plain_hex(self):
        self.assertEqual(parse_theme_hex("#1a2B3c"), (26, 43, 60))
        self.assertEqual(parse_theme_hex("1A2B3C"), (26, 43, 60))
        self.assertEqual(parse_theme_hex("#000000"), BLACK)

    def test_rejects_invalid_and_palette_colors(self):
        for value in ("#123", "blue", "#FFFFFF", "808080"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_theme_hex(value)


class PaletteNormalizationTests(unittest.TestCase):
    def test_preserves_canvas_fills_transparency_and_snaps_colors(self):
        image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
        image.putpixel((1, 1), (250, 250, 250, 255))
        image.putpixel((2, 1), (128, 128, 128, 255))
        image.putpixel((1, 2), (0, 0, 0, 0))
        image.putpixel((2, 2), (200, 200, 200, 128))

        normalized, report = normalize_uploaded_artwork(image)

        self.assertEqual(normalized.size, (4, 4))
        self.assertEqual(
            normalized.getpixel((2, 1)), (*INTERNAL_ARTWORK_COLOR, 255)
        )
        self.assertGreater(report.corrected_pixel_count, 0)
        self.assertGreater(report.transparent_pixel_count, 0)
        visible = {pixel[:3] for pixel in flattened_data(normalized)}
        self.assertLessEqual(visible, {WHITE, INTERNAL_ARTWORK_COLOR})


if __name__ == "__main__":
    unittest.main()
