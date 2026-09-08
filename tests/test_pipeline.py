import unittest

from PIL import Image

from src.config.icon import (
    DEFAULT_ARTWORK_SIZE,
    DEFAULT_PADDING,
    BLACK,
    TRANSPARENT,
    WHITE,
)
from src.formatter import format_icon
from src.formatter.palette import flattened_data


class FormatterPipelineTests(unittest.TestCase):
    def test_builds_four_default_size_palette_safe_variants(self):
        source = Image.new("RGB", (200, 100), WHITE)
        for y in range(20, 80):
            for x in range(40, 160):
                source.putpixel((x, y), BLACK)

        theme = (0, 112, 192)
        icons = format_icon(source, theme)

        output_size = DEFAULT_ARTWORK_SIZE + (2 * DEFAULT_PADDING)
        for image in icons.variants().values():
            self.assertEqual(image.size, (output_size, output_size))
            self.assertEqual(image.mode, "RGBA")
        for image in (icons.standard, icons.solid, icons.dominant):
            self.assertEqual(image.getpixel((0, 0)), TRANSPARENT)
        self.assertEqual(
            icons.dominant_no_circle.getpixel((0, 0)), (*WHITE, 255)
        )

        standard_colors = {
            pixel[:3]
            for pixel in flattened_data(icons.standard)
            if pixel[3] != 0
        }
        solid_colors = {
            pixel[:3]
            for pixel in flattened_data(icons.solid)
            if pixel[3] != 0
        }
        dominant_colors = {
            pixel[:3]
            for pixel in flattened_data(icons.dominant)
            if pixel[3] != 0
        }
        self.assertLessEqual(standard_colors, {theme, WHITE, BLACK})
        self.assertLessEqual(solid_colors, {theme, WHITE})
        self.assertLessEqual(dominant_colors, {theme, WHITE})

    def test_circle_free_background_can_be_transparent(self):
        source = Image.new("RGB", (10, 10), BLACK)

        icons = format_icon(
            source,
            (0, 112, 192),
            transparent_background=True,
        )

        self.assertEqual(icons.dominant_no_circle.getpixel((0, 0)), TRANSPARENT)

    def test_variant_center_pixel_mappings(self):
        source = Image.new("RGB", (10, 10), BLACK)
        theme = (10, 80, 160)
        icons = format_icon(source, theme)

        output_size = DEFAULT_ARTWORK_SIZE + (2 * DEFAULT_PADDING)
        center = (output_size // 2, output_size // 2)
        self.assertEqual(icons.standard.getpixel(center)[:3], BLACK)
        self.assertEqual(icons.solid.getpixel(center)[:3], WHITE)
        self.assertEqual(icons.dominant.getpixel(center)[:3], theme)

    def test_black_theme_remains_distinct_from_black_artwork(self):
        source = Image.new("RGB", (10, 10), BLACK)

        icons = format_icon(source, BLACK)

        output_size = DEFAULT_ARTWORK_SIZE + (2 * DEFAULT_PADDING)
        center = (output_size // 2, output_size // 2)
        self.assertEqual(icons.standard.getpixel(center)[:3], BLACK)
        self.assertEqual(icons.solid.getpixel(center)[:3], WHITE)
        self.assertEqual(icons.solid.getpixel((output_size // 2, 10))[:3], BLACK)
        self.assertEqual(icons.dominant.getpixel(center)[:3], BLACK)

    def test_solid_white_artwork_has_no_inner_circle_seam(self):
        source = Image.new("RGB", (10, 10), WHITE)
        theme = (0, 112, 192)

        solid = format_icon(source, theme).solid
        visible_colors = {
            pixel[:3] for pixel in flattened_data(solid) if pixel[3] != 0
        }

        self.assertEqual(visible_colors, {theme})

    def test_custom_artwork_and_padding_set_output_size(self):
        source = Image.new("RGB", (10, 10), BLACK)

        icons = format_icon(
            source,
            (0, 112, 192),
            artwork_size=600,
            padding=75,
            theme_ring_width=40,
            white_ring_width=25,
        )

        for image in icons.variants().values():
            self.assertEqual(image.size, (750, 750))

    def test_padding_may_be_smaller_than_combined_ring_widths(self):
        source = Image.new("RGB", (10, 10), BLACK)

        icons = format_icon(
            source,
            (0, 112, 192),
            artwork_size=400,
            padding=10,
            theme_ring_width=30,
            white_ring_width=20,
        )

        self.assertEqual(icons.standard.size, (420, 420))

    def test_rejects_rings_that_consume_the_entire_circle(self):
        source = Image.new("RGB", (10, 10), BLACK)

        with self.assertRaisesRegex(ValueError, "leave no room"):
            format_icon(
                source,
                (0, 112, 192),
                artwork_size=100,
                padding=0,
                theme_ring_width=30,
                white_ring_width=20,
            )


if __name__ == "__main__":
    unittest.main()
