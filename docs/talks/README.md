# Woodpecker overview presentation

Edit **`overview-slides.md` at the repository root**. It is the canonical content
source; do not edit the generated Quarto file. The build preserves the text and
slide order, converts Mermaid fences into Quarto cells, adds Reveal.js metadata
and diagram layout classes, and substitutes a local copy of the same bird photo.

## Dependencies

Python 3.10+, Quarto 1.6–1.x (including its Pandoc, Deno and Sass tools), Node.js
22, and a Chromium browser are required. PDF export uses DeckTape 3.16.1. No TeX
installation is needed. To add tools to the existing Woodpecker Conda environment:

```sh
conda activate woodpecker
make -C docs/talks install-pdf
```

`install` adds Quarto and Node from `environment.yml`; `install-pdf` also installs
DeckTape and its Puppeteer browser with npm. Installation requires network access.
An existing environment containing these tools (including Rook's environment)
can also build the deck without installing anything in Woodpecker.

`quarto.sh` supplies Conda's split Quarto tool paths and reuses DeckTape's installed
headless Chrome. You can set `QUARTO_CHROMIUM` to another installed Chromium
executable. HTML-only users still need a browser for Mermaid SVG prerendering;
installing the PDF tools supplies it. Builds do not install packages or browsers.
Headless Chrome needs permission to open a local debugging port.

## Build (work in progress)

Presentation tooling is kept in this subdirectory while it is being developed.
With the tools' environment active, run:

```sh
cd docs/talks
make slides-html   # standalone Reveal.js HTML
make slides-pdf    # rebuild HTML, then export PDF with DeckTape
make slides        # both formats
make slides-clean  # delete only docs/_build/talks/overview/
```

From the repository root, use `make -C docs/talks slides` (or another target above).
The root Makefile does not expose slide targets. Generated `slides.qmd`,
`slides.revealjs.md`, `slides.html`, `slides.pdf`, and Quarto support files stay in
`docs/_build/talks/overview/`, already ignored by `.gitignore`. Open `slides.html`
directly in a browser; its scripts, styles, diagrams, and photo are embedded.
The source hyperlinks remain links to external sites.

## Rendering and styling

Adapted from Rook's `docs/talks/milano-2026/`: the white background, blue headings,
Arial typography, Mermaid configuration, `quarto.sh`, and `svg.lua` pipeline.
Quarto prerenders diagrams with `htmlLabels: false`; the Lua filter rejects
`foreignObject`, restores case-sensitive SVG attributes, and embeds each SVG as a
base64 image. Native SVG text stays isolated from Reveal/PDF CSS. `keep-md` is
required because the filter reads Quarto's intermediate SVG output.

`overview/theme.scss` controls layout without changing slide content. Tall diagrams
use a separate column, horizontal diagrams have a height limit, and the naming
slide places the photo and credit beside the text. The original photograph and
its license are documented in `overview/assets/README.md`.

After content changes, inspect all HTML slides and DeckTape PDF pages, especially
the photo/table slide, tall diagrams, long identifiers, and dense bullet lists.
Check clipping, diagram labels, image loading, and unintended line breaks.
