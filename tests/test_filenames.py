"""Tests for formatted icon output filenames."""

import unittest

from src.formatter.filenames import formatted_icon_filename


class FormattedIconFilenameTests(unittest.TestCase):
    def test_uses_underscores_only_as_suffix_separators(self) -> None:
        filename = formatted_icon_filename(
            "my_energy_icon",
            "dominant-no-circle",
            "0072CE",
        )

        self.assertEqual(
            filename,
            "my-energy-icon_dominant-no-circle_0072CE.png",
        )

    def test_uses_icon_when_basename_is_empty(self) -> None:
        filename = formatted_icon_filename("", "standard", "0072CE")

        self.assertEqual(filename, "icon_standard_0072CE.png")


if __name__ == "__main__":
    unittest.main()
