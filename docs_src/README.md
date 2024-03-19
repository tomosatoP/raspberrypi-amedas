# Create API documentation using docstring & Sphinx.

Target libraries:
- src/amedas/libs

## Install Sphinx packages
~~~sh
# Install group docs ["sphinx", "sphinx-rtd-theme"]
docker compose run --entrypoint "poetry update --lock --with docs" amedas
docker compose run --entrypoint "poetry install --with docs" amedas
~~~

## Make directries and configuration files.

~~~sh
docker compose run --entrypoint "poetry run sphinx-quickstart docs_src" amedas
# Selected root path: docs
# > Separate source and build directories (y/n) [n]: n
# > Project name: Amedas - Raspberry Pi
# > Author name(s): tomosatoP
# > Project release []: 0.1.0
# > Project language [en]: en
~~~

## Modify the configuration files.

docs_src/Makefile

~~~diff
@@ -6,7 +6,7 @@
 SPHINXOPTS    ?=
 SPHINXBUILD   ?= sphinx-build
 SOURCEDIR     = .
-BUILDDIR      = _build
+BUILDDIR      = ../docs
 
 # Put it first so that "make" without argument is like "make help".
 help:
~~~

docs_src/conf.py

~~~diff
@@ -3,6 +3,14 @@
 # For the full list of built-in configuration values, see the documentation:
 # https://www.sphinx-doc.org/en/master/usage/configuration.html
 
+# -- Path --
+# Specify the path where `__init__.py` is located.
+
+import os
+import sys
+
+sys.path.insert(0, os.path.abspath("../src/amedas"))
+
 # -- Project information -----------------------------------------------------
 # https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
 
@@ -14,7 +22,25 @@
 # -- General configuration ---------------------------------------------------
 # https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
 
-extensions = []
+extensions = [
+    "sphinx.ext.autodoc",
+    "sphinx.ext.viewcode",
+    "sphinx.ext.todo",
+    "sphinx.ext.githubpages",
+    # "sphinx.ext.napoleon",
+]
+
+add_module_names = False
+
+# -- autodoc : configration --
+# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
+autoclass_content = "both"
+autodoc_member_order = "bysource"
+# autodoc_typehints = "description"
+autodoc_default_options = {
+    "private-members": False,
+    "show-inheritance": True,
+}
 
 templates_path = ["_templates"]
 exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
@@ -22,5 +48,5 @@
 # -- Options for HTML output -------------------------------------------------
 # https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
 
-html_theme = "arabaster"
+html_theme = "sphinx_rtd_theme"
 html_static_path = ["_static"]
~~~


### Add docstring of modules `src/amedas/libs/` to the documents source.

~~~sh
docker compose run --entrypoint "poetry run sphinx-apidoc -f -o docs_src src/amedas/libs" amedas
# These files are created: modules.rst, libs.rst
~~~

docs_src/index.rsx

~~~diff
@@ -10,7 +10,7 @@
    :maxdepth: 2
    :caption: Contents:
 
-
+   modules
 
 Indices and tables
 ==================
~~~


## Create documents under the folder `docs`.

~~~sh
docker compose run --entrypoint "poetry run sphinx-build -b html docs_src docs" amedas
~~~

---

If you want to remove the contents of `docs`:

~~~sh
docker compose run --entrypoint "poetry run make -C docs_src clean" amedas
~~~
