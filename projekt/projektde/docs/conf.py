"""Sphinx configuration for the Ultrasonic distance instrument project."""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "Ultrasonic distance instrument"
author = "Marcel Hrbáček, Matěj Dostál, Matouš Dorazil"
copyright = "2026, " + author
release = "0.1"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

# MicroPython-only modules do not exist on a PC; mock them for autodoc.
autodoc_mock_imports = ["machine", "framebuf", "micropython"]
autodoc_member_order = "bysource"

language = "cs"
exclude_patterns = ["_build"]
html_theme = "alabaster"
