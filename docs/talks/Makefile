# Run directly with make -C docs/talks, or through the root Makefile.
TALKS_DIR := $(CURDIR)
BUILD := $(abspath ../_build/talks)
TALKS := $(patsubst %/slides.qmd,%,$(wildcard */slides.qmd))
DECKTAPE ?= decktape
DECKTAPE_FLAGS ?=

.DEFAULT_GOAL := slides
.PHONY: slides slides-html slides-pdf publish slides-clean install install-pdf

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
