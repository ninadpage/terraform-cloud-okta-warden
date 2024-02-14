"""Sphinx configuration."""
project = "Terraform Cloud Okta Warden"
author = "Ninad Page"
copyright = "2024, Ninad Page"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
