"""Stage Quarto inputs and publish self-contained decks; never edit the inputs."""

import argparse
import shutil
from html.parser import HTMLParser
from pathlib import Path

TALKS = Path(__file__).resolve().parent
BUILD = TALKS.parent / "_build/talks"


class DeckAssets(HTMLParser):
    """Reject missing companion assets in the self-contained publication format."""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        resources = [attrs.get("src"), attrs.get("poster")]
        if tag == "link" and attrs.get("rel") == "stylesheet":
            resources.append(attrs.get("href"))
        for resource in filter(None, resources):
            if not resource.startswith("data:"):
                raise ValueError(f"Deck asset is not embedded: {resource}")


def verify(sources):
    site = TALKS.parents[1] / "site/talks"
    landing = (site / "index.html").read_text(encoding="utf-8")
    expected = {site / "index.html"}
    for source in sources:
        name = source.parent.name
        html = site / name / "index.html"
        pdf = site / name / "slides.pdf"
        DeckAssets().feed(html.read_text(encoding="utf-8"))
        if not pdf.read_bytes().startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {pdf}")
        for filename in ("index.html", "slides.pdf"):
            if not any(
                f'href="{url}"' in landing
                for url in (f"{name}/{filename}", f"{name}/" if filename == "index.html" else "")
            ):
                raise ValueError(f"Missing Talks page link: {name}/{filename}")
        expected.update((html, pdf))
        print(f"Verified site/talks/{name}/: embedded HTML assets, PDF and landing links")
    actual = {path for path in site.rglob("*") if path.is_file()}
    if actual != expected:
        raise ValueError(f"Unexpected or missing published talk files: {actual ^ expected}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "publish", "clean", "verify"])
    args = parser.parse_args()
    sources = sorted(TALKS.glob("*/slides.qmd"))
    if not sources:
        raise SystemExit("No talk sources found")
    if args.action in {"prepare", "clean"}:
        shutil.rmtree(BUILD, ignore_errors=True)
        for source in sources:
            for name in ("index.html", "slides.pdf"):
                (source.parent / name).unlink(missing_ok=True)
    if args.action == "prepare":
        shutil.copytree(TALKS / "shared", BUILD / "shared")
        for source in sources:
            shutil.copytree(
                source.parent,
                BUILD / source.parent.name,
                ignore=shutil.ignore_patterns(
                    "__pycache__",
                    "*.html",
                    "*.pdf",
                    "*.pptx",
                    "*.revealjs.md",
                    "*_files",
                    ".quarto",
                    "_freeze",
                ),
            )
    elif args.action == "publish":
        for source in sources:
            for name in ("index.html", "slides.pdf"):
                shutil.copy2(BUILD / source.parent.name / name, source.parent / name)
    elif args.action == "verify":
        verify(sources)


if __name__ == "__main__":
    main()
