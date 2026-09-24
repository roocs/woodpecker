# Woodpecker talks

Edit each talk's `slides.qmd` directly: it is the sole editable slide source.

- `overview/slides.qmd` is the evolving project overview.
- `milano-2026/slides.qmd` preserves the version prepared for Milano 2026,
  including its appendix. Keep event content identifiable rather than replacing
  it with the next talk.
- `shared/` holds the existing Reveal.js theme, SVG filter and attributed photo.

The original root Markdown and generated Quarto deck were compared during the
migration: all text and slide order were preserved. The short Quarto copy only
had private PPTX styling differences. The Markdown converter and PPTX adapters
have been removed. **PPTX is not generated.**

## Toolchain

Use Python with the repository's docs dependencies and local plugins (`make dev`),
Quarto **1.9.38**, Node.js **22**, and DeckTape **3.16.1**. DeckTape's npm install
also installs Puppeteer's Chromium browser. PDF export prints the Reveal.js deck;
no TeX or private template is needed. Install tools once with network access:

```sh
conda activate woodpecker
make -C docs/talks install-all
```

`install` installs only the basics for HTML slides (Quarto and Node).
`install-pdf` adds PDF support (DeckTape and its browser), including the basics.
`install-all` installs the basics and every extension; currently PDF is the only
extension, so it runs `install-pdf`.

Alternatively install Quarto 1.9.38 and Node 22 separately, then run
`npm install --global decktape@3.16.1`. On Linux the browser also needs its usual
system libraries. The existing docs workflow uses Ubuntu, the official Quarto
setup action, Node 22 and this same npm command before running `make docs`.
`quarto.sh` supports Conda's split tool packages and reuses DeckTape's installed
browser for Mermaid rendering. Builds do not install tools or download browsers.

## Local build (repository root)

```sh
make talks-html   # all standalone Reveal.js decks
make talks-pdf    # HTML first, then PDF using DeckTape
make talks        # both formats
make docs         # talks + generated references + strict MkDocs build in site/
make docs-serve   # build talks, then serve with MkDocs; rerun after QMD edits
make docs-clean   # remove generated site, staged decks and temporary talk builds and notebook cache
```

The slide targets are also available as `make -C docs/talks slides-html`,
`slides-pdf`, `slides`, and `slides-clean`. `DECKTAPE` and `DECKTAPE_FLAGS` can
be overridden for an existing local installation.

Rendering runs on copies under ignored `docs/talks/_build/`. `make docs` stages
only `index.html` and `slides.pdf` into each source directory before MkDocs
builds. HTML embeds the photo, SVG diagrams, CSS and JavaScript, so the
decks work under the GitHub Pages `/woodpecker/` prefix without companion files.
Sources and build tools are excluded from MkDocs. `make docs` also checks the
final talk links, PDF headers, embedded HTML assets and published file list. Generated output is ignored
by Git; never commit HTML, PDFs or Quarto intermediates.

## Published paths and future talks

The normal [Talks page](index.md) links to:

- `https://roocs.github.io/woodpecker/talks/overview/` (`index.html`, `slides.pdf`)
- `https://roocs.github.io/woodpecker/talks/milano-2026/` (`index.html`, `slides.pdf`)

For another event, add `<event-name>/slides.qmd` with the same relative shared
asset paths and self-contained Reveal.js configuration, then add its links to
`index.md`. The Makefile discovers `*/slides.qmd` automatically. Keep directory
names stable once published. Changes under `docs/` trigger the single docs
workflow, which uploads the complete `site/` and deploys it from `main`.

The presentation design is adapted from Rook's Milano deck: white background,
blue headings, Arial typography, and static Mermaid SVGs. Review dense appendix
slides after content changes. Changes to shared styling affect every deck;
copy styling into an event directory if it later needs to remain frozen.
