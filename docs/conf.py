"""Sphinx configuration for the IMAS documentation hub."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "IMAS documentation hub"
author = "ITER Organization and IMAS contributors"
copyright = "ITER Organization"

extensions = [
    "myst_nb",  # Markdown (MyST) pages and Jupyter notebooks
    "sphinx.ext.intersphinx",  # checked links into the docs of each IMAS component
    "sphinx_design",  # cards, grids and tabs
    "sphinx_copybutton",
    "sphinx.ext.githubpages",  # adds .nojekyll so GitHub Pages serves _static/
    "sphinx_immaterial",  # the theme must also be an extension, to merge its default options
]

# -- Markdown ----------------------------------------------------------------
myst_enable_extensions = ["colon_fence", "deflist", "substitution", "attrs_inline"]
myst_heading_anchors = 3

# Jupyter-style anchors, so links between tutorial notebooks work in Colab and here.
myst_heading_slug_func = "hub_slugs.jupyter_style_slug"

# Rich/ANSI-coloured outputs (IMAS logs, IDStools tables) can't be syntax-highlighted,
# but they are still rendered: don't let that fail the build.
suppress_warnings = ["misc.highlighting_failure"]

exclude_patterns = [
    "_build",
    "_templates",
    "_ext",
    "**/.ipynb_checkpoints",
]

# -- Notebook and code-cell execution ----------------------------------------
# Notebooks and {code-cell} blocks run at build time so examples never go stale.
nb_execution_mode = "cache"
nb_execution_timeout = 600
nb_execution_raise_on_error = True
nb_execution_in_temp = True  # downloaded data and written data entries stay out of the source tree
nb_execution_show_tb = True
nb_execution_excludepatterns = [
    "tutorials/notebooks/05_SimDB.ipynb",  # needs ITER authentication
]
nb_merge_streams = True

# -- Links to the documentation of IMAS components ----------------------------
# Use them as {external+imas-python:doc}`intro` or {external+imas-python:py:class}`imas.DBEntry`.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "imas-python": ("https://imas-python.readthedocs.io/en/stable", None),
    "imas-core": ("https://imas-core.readthedocs.io/en/latest", None),
    "imas-dd": ("https://imas-data-dictionary.readthedocs.io/en/latest", None),
    "imas-cpp": ("https://imas-cpp.readthedocs.io/en/stable", None),
    "imas-fortran": ("https://imas-fortran.readthedocs.io/en/latest", None),
    "imas-matlab": ("https://imas-matlab.readthedocs.io/en/latest", None),
    "imas-java": ("https://imas-java.readthedocs.io/en/latest", None),
    "idstools": ("https://imas-idstools.readthedocs.io/en/latest", None),
    "imas-validator": ("https://imas-validator.readthedocs.io/en/stable", None),
    "simdb": ("https://simdb.readthedocs.io/en/latest", None),
    "iwrap": ("https://iwrap.readthedocs.io/en/stable", None),
    "imas-muscle3": ("https://imas-muscle3.readthedocs.io/en/latest", None),
    "imas-paraview": ("https://imas-paraview.readthedocs.io/en/stable", None),
}
# Only explicit {external+name:...} roles resolve externally, to avoid surprises.
intersphinx_disabled_reftypes = ["*"]

# -- HTML output --------------------------------------------------------------
html_theme = "sphinx_immaterial"
html_title = "IMAS documentation hub"
html_theme_options = {
    "repo_url": "https://github.com/olivhoenen/IMAS-docs",
    "repo_name": "IMAS-docs",
    "edit_uri": "blob/main/docs",
    "features": [
        "navigation.tabs",
        "navigation.sections",
        "navigation.top",
        "search.highlight",
        "content.code.copy",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "toggle": {"icon": "material/weather-night", "name": "Switch to dark mode"},
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "indigo",
            "toggle": {"icon": "material/weather-sunny", "name": "Switch to light mode"},
        },
    ],
}

linkcheck_ignore = [r"https://zenodo\.org/.*"]  # rate-limited, checked by the build itself
