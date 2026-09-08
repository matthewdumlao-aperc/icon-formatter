import unittest

from PIL import Image

from src.config.icon import BLACK, TRANSPARENT, WHITE
from src.formatter import trim_image
from src.formatter.palette import flattened_data


class TrimImageTests(unittest.TestCase):
    def test_crops_near_white_margins_to_content(self):
        source = Image.new("RGB", (10, 8), (247, 250, 245))
        for y in range(2, 6):
            for x in range(3, 8):
                source.putpixel((x, y), BLACK)

        trimmed = trim_image(source)

        self.assertEqual(trimmed.mode, "RGBA")
        self.assertEqual(trimmed.size, (5, 4))
        self.assertEqual(set(flattened_data(trimmed)), {(*BLACK, 255)})

    def test_crops_transparency_and_preserves_pixels_inside_bounds(self):
        source = Image.new("RGBA", (7, 6), TRANSPARENT)
        source.putpixel((2, 1), (20, 40, 60, 128))
        source.putpixel((5, 4), (*BLACK, 255))

        trimmed = trim_image(source)

        self.assertEqual(trimmed.size, (4, 4))
        self.assertEqual(trimmed.getpixel((0, 0)), (20, 40, 60, 128))
        self.assertEqual(trimmed.getpixel((3, 3)), (*BLACK, 255))
        self.assertEqual(trimmed.getpixel((1, 1)), TRANSPARENT)

    def test_ignores_opaque_white_pixels_when_finding_transparent_bounds(self):
        source = Image.new("RGBA", (8, 8), TRANSPARENT)
        source.putpixel((1, 1), (*WHITE, 255))
        source.putpixel((4, 3), (*BLACK, 255))

        trimmed = trim_image(source)

        self.assertEqual(trimmed.size, (1, 1))
        self.assertEqual(trimmed.getpixel((0, 0)), (*BLACK, 255))

    def test_rejects_images_without_visible_non_white_content(self):
        for source in (
            Image.new("RGB", (4, 4), WHITE),
            Image.new("RGBA", (4, 4), TRANSPARENT),
        ):
            with self.subTest(mode=source.mode), self.assertRaisesRegex(
                ValueError, "no non-white artwork"
            ):
                trim_image(source)


if __name__ == "__main__":
    unittest.main()
