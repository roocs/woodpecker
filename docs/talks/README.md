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
use a separate column, horizontal diagrams have a height limit, and the title
slide places the photo and attribution beside the presenter and contributor credits. The original photograph and
its license are documented in `overview/assets/README.md`.

After content changes, inspect all HTML slides and DeckTape PDF pages, especially
the title slide, tall diagrams, long identifiers, and dense bullet lists.
Check clipping, diagram labels, image loading, and unintended line breaks.

## Milano delivery (5–10 minutes)

The main talk is the title page plus five content slides. Stop at **Summary and
next step**; the appendix is for questions and follow-up, not the timed talk.
The reviewed title page is retained. Each of the five main content slides uses
a diagram and a small amount of text. Detailed material is numbered A1–A16 after an appendix divider.

| Slide | 5-minute delivery | Extended delivery |
| --- | --- | --- |
| Title | 20 seconds | 30 seconds |
| 1. What is Woodpecker? | 40 seconds | 90 seconds |
| 2. Why a common interface? | 50 seconds | 90 seconds |
| 3. Independent plugins, shared access | 70 seconds | 120 seconds |
| 4. A concrete use case: Rook | 60 seconds | 120 seconds |
| 5. Summary and next step | 60 seconds | 90 seconds |
| Total | 5 minutes | 9 minutes |

For the short version, explain the plugin idea and Rook example without opening
code or discussing identifier syntax. For the extended version, use the extra
time to explain ownership, recipe reuse, and the proposed joint plugin fix;
leave roughly a minute for a question. Detailed API examples, the plugin list,
and the proposed ESGF Errata connection remain available in the appendix.
