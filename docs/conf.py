"""Sphinx configuration for the Ultrasonic distance instrument project."""
import os
import sys

# the source code is in the src/ folder at the top level of the repository
sys.path.insert(0, os.path.abspath("../src"))

project = "Ultrasonic distance instrument"
author = "Marcel Hrbacek, Matej Dostal, Matous Dorazil"
copyright = "2026, " + author
release = "0.2"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

# MicroPython-only modules do not exist on a PC; mock them for autodoc.
autodoc_mock_imports = ["machine", "micropython"]

# MicroPython adds sleep_us / sleep_ms to the time module; CPython does not
# have them, so add dummy versions to allow importing the drivers on a PC.
import time  # noqa: E402

for _name in ("sleep_us", "sleep_ms"):
    if not hasattr(time, _name):
        setattr(time, _name, lambda *_args: None)
autodoc_member_order = "bysource"

language = "en"
exclude_patterns = ["_build"]
html_theme = "alabaster"
