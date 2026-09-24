# Run directly with make -C docs/talks, or through the root Makefile.
TALKS_DIR := $(CURDIR)
BUILD := $(abspath _build)
TALKS := $(patsubst %/slides.qmd,%,$(wildcard */slides.qmd))
DECKTAPE ?= decktape
DECKTAPE_FLAGS ?=

.DEFAULT_GOAL := help
.PHONY: help slides slides-html slides-pdf publish slides-clean install install-pdf

help:
	@echo "Woodpecker talk targets:"
	@echo "  help          Show this target overview (default)"
	@echo "  slides-html   Render all talks as standalone Reveal.js HTML"
	@echo "  slides-pdf    Render HTML, then export PDFs with DeckTape"
	@echo "  slides        Build both HTML and PDF"
	@echo "  publish       Build and stage HTML/PDF for MkDocs (no deployment)"
	@echo "  slides-clean  Remove generated talk outputs and staging files"
	@echo "  install       Install Quarto and Node in the active woodpecker Conda environment"
	@echo "  install-pdf   Install HTML tools plus DeckTape and its browser"
	@echo "Run 'make docs' from the repository root to build the complete site."

slides-html:
	python build.py prepare
	@set -e; for talk in $(TALKS); do \
		(cd "$(BUILD)/$$talk" && sh "$(TALKS_DIR)/quarto.sh" render slides.qmd --to revealjs --output index.html); \
	done

slides-pdf: slides-html
	@set -e; for talk in $(TALKS); do \
		$(DECKTAPE) reveal --size 1600x900 --load-pause 2000 --pause 1000 $(DECKTAPE_FLAGS) "$(BUILD)/$$talk/index.html" "$(BUILD)/$$talk/slides.pdf"; \
	done

slides: slides-pdf

publish: slides
	python build.py publish

slides-clean:
	python build.py clean

install:
	@test "$$CONDA_DEFAULT_ENV" = woodpecker && test -n "$$CONDA_PREFIX" || { echo "Activate the woodpecker Conda environment first." >&2; exit 1; }
	conda env update --name woodpecker --file environment.yml
	sh quarto.sh --version

install-pdf: install
	npm install --global --prefix "$$CONDA_PREFIX" decktape@3.16.1
