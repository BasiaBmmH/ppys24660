import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # zakłada, że kod jest poziom wyżej niż docs/
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'WisielecGame'
copyright = '2025, s24660 BarbaraMichalik (BasiaBmmH on github)'
author = 's24660 BarbaraMichalik (BasiaBmmH on github)'
release = '0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Obsługa Google/NumPy-style docstrings
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
