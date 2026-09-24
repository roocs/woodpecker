.PHONY: help install install-uv install-plugins install-plugins-uv dev dev-uv format lint lint-fix check test docs docs-check-browser docs-serve talks talks-html talks-pdf talks-clean docs-clean list-fixes

CHECK_PATH ?= .
PYTHON ?= $(shell python -c 'import sys; print(sys.executable)')
PLUGIN_PATHS := plugins/woodpecker-atlas-plugin \
	plugins/woodpecker-cmip6-plugin \
	plugins/woodpecker-cmip6-decadal-plugin \
	plugins/woodpecker-cmip7-plugin \
	plugins/woodpecker-xmip-plugin
PLUGIN_INSTALL_ARGS := $(foreach p,$(PLUGIN_PATHS),-e $(p))

help:
	@echo "Common targets (run after conda env is activated):"
	@echo "  make install    - install package in editable mode"
	@echo "  make install-uv - install package in editable mode via uv"
	@echo "  make install-plugins    - install woodpecker then local plugin packages"
	@echo "  make install-plugins-uv - install woodpecker then local plugin packages via uv"
	@echo "  make dev        - install package + extras + plugins (recommended)"
	@echo "  make dev-uv     - dev install via uv (same as make dev)"
	@echo "  make format     - run Ruff formatter"
	@echo "  make lint       - run Ruff lint checks"
	@echo "  make lint-fix   - auto-fix Ruff lint issues"
	@echo "  make check      - run fix checks (default path: .)"
	@echo "  make test       - run pytest test suite"
	@echo "  make docs       - build complete site, including HTML/PDF talks"
	@echo "  make docs-check-browser - check the built site in Chromium"
	@echo "  make docs-serve - build and serve the complete site at localhost:8000"
	@echo "  make talks      - render all talks to HTML and PDF"
	@echo "  make talks-html / talks-pdf - render slide formats"
	@echo "  make docs-clean - remove generated site and talk outputs"
	@echo "  make list-fixes - show registered fixes"

install:
	pip install -e .

install-uv:
	uv pip install --python "$(PYTHON)" -e .

install-plugins: install
	pip install $(PLUGIN_INSTALL_ARGS)

install-plugins-uv: install-uv
	uv pip install --python "$(PYTHON)" $(PLUGIN_INSTALL_ARGS)

dev:
	pip install -e ".[docs,dev,full]"
	pip install $(PLUGIN_INSTALL_ARGS)

dev-uv:
	uv pip install --python "$(PYTHON)" -e ".[docs,dev,full]"
	uv pip install --python "$(PYTHON)" $(PLUGIN_INSTALL_ARGS)

format:
	ruff format .

lint:
	ruff check .

lint-fix:
	ruff check . --fix

check:
	woodpecker check $(CHECK_PATH)

test:
	pytest -v

talks-html:
	$(MAKE) -C talks slides-html

talks-pdf:
	$(MAKE) -C talks slides-pdf

talks:
	$(MAKE) -C talks slides

talks-clean:
	$(MAKE) -C talks slides-clean

docs-clean: talks-clean
	python -c 'import shutil; shutil.rmtree("site", ignore_errors=True); shutil.rmtree(".cache/mkdocs-jupyter", ignore_errors=True)'

docs: talks
	python scripts/generate_fix_catalog.py
	python scripts/generate_recipe_catalog.py
	python scripts/generate_fix_webpage.py
	NO_MKDOCS_2_WARNING=1 mkdocs build --strict
	python talks/build.py publish
	python talks/build.py verify

docs-check-browser:
	node scripts/check_docs_browser.cjs

docs-serve: docs
	python -m http.server 8000 --bind 127.0.0.1 --directory site

list-fixes:
	woodpecker list-fixes
