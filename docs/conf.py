# -*- coding: utf-8 -*-
import sphinx_rtd_theme
import os
import sys

docs_root = os.path.dirname(__file__)
lib_root = os.path.dirname(docs_root)
sys.path.insert(1, lib_root)
import construct_launcher

project = construct_launcher.__title__
copyright = '2018, ' + construct_launcher.__author__
author = construct_launcher.__author__
version = construct_launcher.__version__
release = construct_launcher.__version__
language = None

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

templates_path = ['templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}
htmlhelp_basename = project + 'doc'
intersphinx_mapping = {'https://docs.python.org/': None}
