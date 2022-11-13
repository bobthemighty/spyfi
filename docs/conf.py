"""Sphinx configuration."""
project = "Spyfi"
author = "Bob Gregory"
copyright = "2022, Bob Gregory"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
