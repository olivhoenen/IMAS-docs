"""Helpers for the Sphinx configuration (kept in a module so Sphinx can pickle them)."""


def jupyter_style_slug(title: str) -> str:
    """Anchor like Jupyter/Colab ("Install the package" -> "Install-the-package"), so that
    links between the tutorial notebooks work both in Colab and on this site."""
    return "-".join(title.split())
