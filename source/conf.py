# -- N.E.K.O Plugin SDK Documentation - Sphinx Configuration --

import os
import sys

# Add project root to sys.path so autodoc can find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# -- Project information ---------------------------------------------------
project = "N.E.K.O Plugin SDK"
copyright = "2024-2026, N.E.K.O Team"
author = "N.E.K.O Team"
release = "0.1.0"

# -- General configuration -------------------------------------------------
extensions = [
    # Core Sphinx
    "sphinx.ext.autodoc",
    # "sphinx.ext.autosummary",  # disabled: hand-written reference .rst files
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",

    # Markdown support (write docs in .md instead of .rst)
    "myst_parser",

    # UI enhancements
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",

    # Pydantic model documentation
    "sphinxcontrib.autodoc_pydantic",
]

# MyST-Parser settings (Markdown support)
myst_enable_extensions = [
    "colon_fence",        # ::: directives
    "deflist",            # Definition lists
    "fieldlist",          # Field lists
    "tasklist",           # - [x] checkboxes
    "substitution",       # {{variable}} substitution
    "attrs_inline",       # {.class} inline attributes
    "attrs_block",        # Block attributes
]
myst_heading_anchors = 3

# Source file suffixes (support both .md and .rst)
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb" if False else "myst",  # Use myst for .md files
}

# The master doc
master_doc = "index"

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Language
language = "zh_CN"

# -- autodoc configuration -------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": False,
    "exclude-members": "__init__, __repr__, __str__, __hash__, __eq__",
    "show-inheritance": True,
    "inherited-members": False,
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_class_signature = "separated"
autodoc_docstring_signature = True
autodoc_mock_imports = [
    "zmq",
    "ormsgpack",
    "msgpack",
    "aiohttp",
    "fastapi",
    "uvicorn",
    # "pydantic",  # removed: real import needed for autodoc-pydantic
    "sqlalchemy",
    "tomli",
    "tomllib",
    "loguru",
]

# autosummary (disabled — we use hand-written .rst)
# autosummary_generate = True

# Napoleon settings (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = {}

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# -- Options for HTML output -----------------------------------------------
html_theme = "furo"
html_title = "N.E.K.O Plugin SDK"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#6C5CE7",
        "color-brand-content": "#6C5CE7",
        "color-api-background": "#F8F7FF",
        "color-api-background-hover": "#EDEAFF",
        "color-highlight-on-target": "#F0EDFF",
        "color-admonition-title--note": "#6C5CE7",
        "color-admonition-title-background--note": "#F0EDFF",
    },
    "dark_css_variables": {
        "color-brand-primary": "#A29BFE",
        "color-brand-content": "#A29BFE",
        "color-api-background": "#1E1B2E",
        "color-api-background-hover": "#2D2B45",
        "color-highlight-on-target": "#2D2B45",
        "color-admonition-title--note": "#A29BFE",
        "color-admonition-title-background--note": "#1E1B2E",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view"],
    "footer_icons": [
        {
            "name": "N.E.K.O",
            "url": "#",
            "html": '<span>Built with Sphinx &amp; Furo</span>',
            "class": "",
        },
    ],
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]

# -- Suppress warnings --------------------------------------------------------
suppress_warnings = [
    "ref.python",       # ambiguous cross-references (PluginContextProtocol etc.)
]

import logging

class _DuplicateFilter(logging.Filter):
    """Filter out 'duplicate object description' and docutils inline markup warnings."""
    _SUPPRESSED = (
        "duplicate object description",
        "重复的对象描述",
        "Inline literal start-string",
        "Inline interpreted text",
        "Inline strong start-string",
        "Inline emphasis start-string",
        "Definition list ends without",
        "Block quote ends without",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not any(s in msg for s in self._SUPPRESSED)

def setup(app):
    for name in ("sphinx.domains.python", "docutils"):
        lg = logging.getLogger(name)
        lg.addFilter(_DuplicateFilter())
    # Also attach to root sphinx logger for docutils warnings
    logging.getLogger("sphinx").addFilter(_DuplicateFilter())

# -- autodoc-pydantic configuration ----------------------------------------
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_model_show_validator_members = True
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_settings_show_json = False

# -- todo extension ---------------------------------------------------------
todo_include_todos = True
