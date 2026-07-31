"""Sphinx configuration for hwid.

See https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

from datetime import datetime, timezone

# -- Project information -----------------------------------------------------
project = "hwid"
author = "Hasan Sezer Taşan"
copyright = f"{datetime.now(tz=timezone.utc):%Y}, Hasan Sezer Taşan"  # noqa: A001

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",  # emits .nojekyll so GitHub Pages serves _static/
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx_paramlinks",
    "auto_pytabs.sphinx_ext",
    "myst_parser",
]

# Both reStructuredText and (via MyST) Markdown source files are supported.
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# autosectionlabel can emit duplicate-label warnings across documents; the
# document prefix keeps them unique, so no blanket suppression is needed.
autosectionlabel_prefix_document = True

# -- Autodoc / Napoleon ------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"
autoclass_content = "both"
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- auto-pytabs -------------------------------------------------------------
# Keep the version tabs in sync with this project's supported Python range
# (requires-python >= 3.10, classifiers/CI up to 3.14). auto-pytabs otherwise
# defaults to (3, 7), which would mislabel the rendered examples.
auto_pytabs_min_version = (3, 10)
auto_pytabs_max_version = (3, 14)

# -- Intersphinx -------------------------------------------------------------
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


# -- HTML output (Shibuya theme) ---------------------------------------------
# https://shibuya.lepture.com/
html_theme = "shibuya"
html_title = "hwid"
html_theme_options = {
    "accent_color": "amber",
    "github_url": "https://github.com/hasansezertasan/hwid",
}
