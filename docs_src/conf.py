# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path --
# Specify the path where `__init__.py` is located.

import os
import sys

sys.path.insert(0, os.path.abspath("../src/amedas"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "amedas - Raspberry Pi"
copyright = "2024, tomosatoP"
author = "tomosatoP"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    # "sphinx.ext.napoleon",
]

add_module_names = False

# -- autodoc : configration --
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autoclass_content = "both"
autodoc_member_order = "bysource"
# autodoc_typehints = "description"
autodoc_default_options = {
    "private-members": False,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
