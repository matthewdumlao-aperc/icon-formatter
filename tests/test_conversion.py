import unittest

from PIL import Image

from src.config.icon import BLACK, TRANSPARENT, WHITE
from src.formatter import convert_to_black


class ConvertToBlackTests(unittest.TestCase):
    def test_maps_gray_and_black_to_black_and_light_pixels_to_white(self):
        source = Image.new("RGB", (3, 1))
        source.putdata([(128, 128, 128), BLACK, (240, 240, 240)])

        converted = convert_to_black(source)

        self.assertEqual(converted.mode, "RGBA")
        self.assertEqual(
            [converted.getpixel((x, 0)) for x in range(3)],
            [(*BLACK, 255), (*BLACK, 255), (*WHITE, 255)],
        )

    def test_can_make_the_light_class_transparent(self):
        source = Image.new("RGB", (2, 1))
        source.putdata([(128, 128, 128), WHITE])

        converted = convert_to_black(source, transparent_background=True)

        self.assertEqual(converted.getpixel((0, 0)), (*BLACK, 255))
        self.assertEqual(converted.getpixel((1, 0)), TRANSPARENT)

    def test_treats_source_transparency_as_background(self):
        source = Image.new("RGBA", (2, 1), TRANSPARENT)
        source.putpixel((0, 0), (*BLACK, 255))

        opaque = convert_to_black(source)
        transparent = convert_to_black(source, transparent_background=True)

        self.assertEqual(opaque.getpixel((1, 0)), (*WHITE, 255))
        self.assertEqual(transparent.getpixel((1, 0)), TRANSPARENT)

    def test_rejects_threshold_outside_byte_range(self):
        source = Image.new("RGB", (1, 1), BLACK)

        for threshold in (-1, 256):
            with self.subTest(threshold=threshold), self.assertRaisesRegex(
                ValueError, "between 0 and 255"
            ):
                convert_to_black(source, threshold=threshold)


if __name__ == "__main__":
    unittest.main()
