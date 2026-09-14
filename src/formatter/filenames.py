"""Filename construction for formatted icon outputs."""


def formatted_icon_filename(
    basename: str,
    variant: str,
    theme_hex: str,
) -> str:
    """Return a parseable PNG filename for one formatted icon variant."""
    normalized_basename = basename.replace("_", "-") or "icon"
    return f"{normalized_basename}_{variant}_{theme_hex}.png"
