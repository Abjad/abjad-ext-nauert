import os
import sys

import nauert

sys.path.insert(0, os.path.abspath("../../source"))

autodoc_member_order = "groupwise"

copyright = "2016-2025, Joséphine Wolf Oberholtzer & Tsz Kiu Pang"

extensions = [
    "abjad.ext.sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"

# html_favicon = "_static/favicon.ico"
# html_logo = "_static/abjad-logo.png"
# html_show_copyright = False
# html_show_sourcelink = False
# html_show_sphinx = False
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "canonical_url": "https://abjad.github.io/nauert",
    # most important setting:
    # navigation_depth=1 makes sidebar completely flat;
    # leave flat navigation in place forever:
    "navigation_depth": 1,
    "sticky_navigation": False,
    "style_external_links": True,
    "style_nav_header_background": "#ffeedd",
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("http://www.sphinx-doc.org/en/master/", None),
}

project = "nauert"
pygments_style = "sphinx"

release = nauert.__version__

smartquotes = True

templates_path = ["_templates"]
todo_include_todos = True

uqbar_api_title = "Nauert API"
uqbar_api_source_paths = ["nauert"]
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]

uqbar_book_console_setup = [
    "import abjad",
    "import nauert",
    "from fractions import Fraction",
]
uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True

version = nauert.__version__
