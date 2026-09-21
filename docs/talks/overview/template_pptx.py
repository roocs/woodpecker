"""Apply a private one-slide PPTX/POTX reference to the Quarto main talk.

Keep the reference's actual layout, master, theme and artwork in the output.
Template bytes are read at build time; none are stored in the source tree.
"""

import copy
import posixpath
import zipfile
from xml.etree import ElementTree as ET

from style_pptx import NS, REL, child, emu, order_children, place, tag, xml_bytes


def related(files, path, kind):
    relpath = posixpath.dirname(path) + "/_rels/" + posixpath.basename(path) + ".rels"
    relations = ET.fromstring(files[relpath])
    relation = next(r for r in relations if r.get("Type").endswith("/" + kind))
    return posixpath.normpath(posixpath.join(posixpath.dirname(path), relation.get("Target")))


def read_template(path):
    with zipfile.ZipFile(path) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    presentation = ET.fromstring(files["ppt/presentation.xml"])
    entries = presentation.findall("p:sldIdLst/p:sldId", NS)
    if len(entries) != 1:
        raise ValueError("Use a reference PPTX/POTX containing exactly one selected slide")
    slidepath = related(files, "ppt/presentation.xml", "slide")
    layoutpath = related(files, slidepath, "slideLayout")
    masterpath = related(files, layoutpath, "slideMaster")
    themepath = related(files, masterpath, "theme")
    slide, layout, master, theme = [
        ET.fromstring(files[p]) for p in (slidepath, layoutpath, masterpath, themepath)
    ]

    def placeholder(kind):
        for root in (layout, master):
            for shape in root.findall("p:cSld/p:spTree/p:sp", NS):
                ph = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
                if ph is not None and ph.get("type") == kind:
                    return shape
        raise ValueError(f"Template needs a {kind} placeholder")

    def color(node, fallback):
        if node is None:
            return fallback
        rgb = node.find("a:srgbClr", NS)
        if rgb is not None:
            return rgb.get("val")
        scheme = node.find("a:schemeClr", NS)
        if scheme is not None:
            value = scheme.get("val")
            value = {"tx1": "dk1", "bg1": "lt1"}.get(value, value)
            entry = theme.find(f"a:themeElements/a:clrScheme/a:{value}", NS)
            if entry is not None and len(entry):
                return entry[0].get("lastClr", entry[0].get("val", fallback))
        return fallback

    title, body = placeholder("title"), placeholder("body")
    title_style = title.find("p:txBody/a:lstStyle/a:lvl1pPr/a:defRPr", NS)
    body_style = body.find("p:txBody/a:lstStyle/a:lvl1pPr/a:defRPr", NS)
    background = next(
        (
            r.find("p:cSld/p:bg", NS)
            for r in (slide, layout, master)
            if r.find("p:cSld/p:bg", NS) is not None
        ),
        None,
    )
    bg = color(
        background.find("p:bgPr/a:solidFill", NS) if background is not None else None, "FFFFFF"
    )

    def font(style, kind):
        latin = style.find("a:latin", NS) if style is not None else None
        if latin is not None and not latin.get("typeface", "").startswith("+"):
            return latin.get("typeface")
        return theme.find(f"a:themeElements/a:fontScheme/a:{kind}Font/a:latin", NS).get("typeface")

    return (
        files,
        slidepath,
        {
            "background": bg,
            "foreground": color(
                body_style.find("a:solidFill", NS) if body_style is not None else None, "222222"
            ),
            "accent": color(
                title_style.find("a:solidFill", NS) if title_style is not None else None, "457B9D"
            ),
            "title_font": font(title_style, "major"),
            "body_font": font(body_style, "minor"),
            "size": presentation.find("p:sldSz", NS).attrib,
        },
    )


def apply_template(source, template):
    files, seed_path, profile = read_template(template)
    if (int(profile["size"]["cx"]), int(profile["size"]["cy"])) != (12192000, 6858000):
        raise ValueError("The overview template must use a 13⅓ × 7½ inch widescreen canvas")
    seed = ET.fromstring(files[seed_path])
    seed_relpath = (
        posixpath.dirname(seed_path) + "/_rels/" + posixpath.basename(seed_path) + ".rels"
    )
    seed_rels = ET.fromstring(files[seed_relpath])
    presentation = ET.fromstring(files["ppt/presentation.xml"])
    relations = ET.fromstring(files["ppt/_rels/presentation.xml.rels"])
    for relation in list(relations):
        if relation.get("Type").endswith("/slide"):
            relations.remove(relation)
    slide_list = presentation.find("p:sldIdLst", NS)
    slide_list.clear()
    types = ET.fromstring(files["[Content_Types].xml"])
    type_ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    for entry in list(types):
        if entry.get("PartName", "").startswith("/ppt/slides/"):
            types.remove(entry)
        if entry.get("PartName") == "/ppt/presentation.xml":
            entry.set(
                "ContentType",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
            )
    # Keep the reference's package intact, replacing its single slide in place.
    src_pres = ET.fromstring(source["ppt/presentation.xml"])
    src_rels = {r.get("Id"): r for r in ET.fromstring(source["ppt/_rels/presentation.xml.rels"])}
    for number, entry in enumerate(src_pres.findall("p:sldIdLst/p:sldId", NS), 1):
        path = posixpath.normpath("ppt/" + src_rels[entry.get(tag("r:id"))].get("Target"))
        source_slide = ET.fromstring(source[path])
        slide = copy.deepcopy(seed)
        tree = slide.find("p:cSld/p:spTree", NS)
        # Preserve artwork and footer fields; replace only title/body placeholders.
        for shape in list(tree)[2:]:
            ph = shape.find(".//p:ph", NS)
            if ph is not None and ph.get("type") in {"title", "ctrTitle", "body", "subTitle"}:
                tree.remove(shape)
            elif ph is not None and ph.get("type") == "sldNum":
                for value in shape.findall(".//a:t", NS):
                    value.text = str(number)
        rels = ET.Element(f"{{{REL}}}Relationships")
        for relation in seed_rels:
            if not relation.get("Type").endswith("/notesSlide"):
                rels.append(copy.deepcopy(relation))
        mapping = {}
        relpath = posixpath.dirname(path) + "/_rels/" + posixpath.basename(path) + ".rels"
        for relation in ET.fromstring(source[relpath]):
            if relation.get("Type").endswith(("/slideLayout", "/notesSlide")):
                continue
            imported = copy.deepcopy(relation)
            new_id = f"woodpeckerRel{len(rels) + 1}"
            mapping[relation.get("Id")] = new_id
            imported.set("Id", new_id)
            if imported.get("TargetMode") != "External":
                old_path = posixpath.normpath(
                    posixpath.join(posixpath.dirname(path), imported.get("Target"))
                )
                if not old_path.startswith("ppt/media/"):
                    raise ValueError(f"Unsupported content relationship: {old_path}")
                new_path = "ppt/media/woodpecker-" + posixpath.basename(old_path)
                files[new_path] = source[old_path]
                imported.set("Target", "../media/" + posixpath.basename(new_path))
            rels.append(imported)
        first_shape_id = 1 + max(int(n.get("id")) for n in tree.findall(".//p:cNvPr", NS))
        for index, original in enumerate(list(source_slide.find("p:cSld/p:spTree", NS))[2:]):
            shape = copy.deepcopy(original)
            for element in shape.iter():
                for key, value in list(element.attrib.items()):
                    if key.startswith("{" + NS["r"] + "}"):
                        element.set(key, mapping[value])
            shape.find(".//p:cNvPr", NS).set("id", str(first_shape_id + index))
            restyle(shape, profile, title=index == 0)
            tree.append(shape)
        enlarge_visuals(tree, number, profile)
        outpath = f"ppt/slides/slide{number}.xml"
        files[outpath] = xml_bytes(slide)
        files[f"ppt/slides/_rels/slide{number}.xml.rels"] = xml_bytes(rels)
        rid = f"woodpeckerSlide{number}"
        ET.SubElement(
            relations,
            f"{{{REL}}}Relationship",
            Id=rid,
            Type=NS["r"] + "/slide",
            Target=f"slides/slide{number}.xml",
        )
        ET.SubElement(slide_list, tag("p:sldId"), {"id": str(255 + number), tag("r:id"): rid})
        ET.SubElement(
            types,
            f"{{{type_ns}}}Override",
            PartName="/" + outpath,
            ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
        )
    extensions = {e.get("Extension") for e in types}
    for extension, mime in (("png", "image/png"), ("jpg", "image/jpeg")):
        if extension not in extensions:
            ET.SubElement(types, f"{{{type_ns}}}Default", Extension=extension, ContentType=mime)
    files["ppt/presentation.xml"] = xml_bytes(presentation)
    files["ppt/_rels/presentation.xml.rels"] = xml_bytes(relations)
    files["[Content_Types].xml"] = xml_bytes(types)
    # Underlines identify links; use the reference's foreground for readable contrast.
    for path in list(files):
        if path.startswith("ppt/theme/") and path.endswith(".xml"):
            theme = ET.fromstring(files[path])
            for kind in ("hlink", "folHlink"):
                color = theme.find(f"a:themeElements/a:clrScheme/a:{kind}", NS)
                if color is not None:
                    color[:] = [ET.Element(tag("a:srgbClr"), val=profile["foreground"])]
            files[path] = xml_bytes(theme)
    return files


def restyle(shape, profile, *, title):
    """Fit the reviewed layout inside the reference's title/body/footer margins."""
    transform = shape.find("p:spPr/a:xfrm", NS)
    if transform is None:
        transform = shape.find("p:xfrm", NS)
    offset, extent = transform.find("a:off", NS), transform.find("a:ext", NS)
    if title:
        offset.attrib.update(x="618435", y="518575")
        extent.attrib.update(cx="10735500", cy="916500")
    else:
        # Reserve the template's footer and start below its title placeholder.
        scale = 0.83
        offset.set("y", emu(1.8 + (int(offset.get("y")) / 914400 - 1.4) * scale))
        extent.set("cy", str(round(int(extent.get("cy")) * scale)))
        if shape.tag == tag("p:pic"):
            width = int(extent.get("cx"))
            offset.set("x", str(round(int(offset.get("x")) + width * (1 - scale) / 2)))
            extent.set("cx", str(round(width * scale)))
    for props in (
        shape.findall(".//a:rPr", NS)
        + shape.findall(".//a:defRPr", NS)
        + shape.findall(".//a:endParaRPr", NS)
    ):
        if not title and props.get("sz"):
            props.set("sz", str(round(int(props.get("sz")) * 0.9)))
        font = props.find("a:latin", NS)
        mono = font is not None and font.get("typeface") == "Consolas"
        if font is not None and font.get("typeface") != "Consolas":
            font.set("typeface", profile["title_font"] if title else profile["body_font"])
        fill = child(props, "a:solidFill")
        old_color = fill.find("a:srgbClr", NS)
        old_color = old_color.get("val") if old_color is not None else None
        fill[:] = [
            ET.Element(tag("a:srgbClr"), val=profile["accent"] if title else profile["foreground"])
        ]
        if props.find("a:hlinkClick", NS) is not None:
            fill[0].set("val", profile["accent"])
        elif mono and old_color in CODE_COLORS:
            fill[0].set("val", CODE_COLORS[old_color])
    for spacing in shape.findall(".//a:spcPts", NS):
        spacing.set("val", str(round(int(spacing.get("val")) * 0.7)))
    for row in shape.findall(".//a:tr", NS):
        row.set("h", str(round(int(row.get("h")) * 0.83)))
    for fill in shape.findall(".//a:tcPr/a:solidFill", NS):
        fill[:] = [ET.Element(tag("a:srgbClr"), val=profile["background"])]


# High-contrast equivalents of Pandoc's light-background syntax colors.
CODE_COLORS = {
    "007020": "C792EA",  # keywords
    "008000": "82AAFF",  # functions
    "19177C": "FFCB6B",  # constants and self
    "666666": "89DDFF",  # operators
    "4070A0": "C3E88D",  # strings
    "40A070": "F78C6C",  # numbers
    "902000": "FFCB6B",  # shell escapes
    "06287E": "C3E88D",  # shell options
}


def set_font_size(shape, points):
    for name in ("a:rPr", "a:defRPr", "a:endParaRPr"):
        for props in shape.findall(".//" + name, NS):
            props.set("sz", str(round(points * 100)))


def code_panel(shape, box, points, profile):
    """Style an editable code text box with padding and a contrasting background."""
    place(shape, box)
    set_font_size(shape, points)
    props = child(shape, "p:spPr")
    child(child(props, "a:prstGeom"), "a:avLst")
    props.find("a:prstGeom", NS).set("prst", "rect")
    # A darker shade of the reference background, independent of its exact palette.
    background = profile["background"]
    darker = "".join(f"{round(int(background[i : i + 2], 16) * 0.55):02X}" for i in (0, 2, 4))
    no_fill = props.find("a:noFill", NS)
    if no_fill is not None:
        props.remove(no_fill)
    child(props, "a:solidFill")[:] = [ET.Element(tag("a:srgbClr"), val=darker)]
    order_children(
        props,
        "a:xfrm a:custGeom a:prstGeom a:noFill a:solidFill a:gradFill "
        "a:blipFill a:pattFill a:grpFill a:ln a:effectLst a:effectDag a:scene3d a:sp3d a:extLst",
    )
    body = shape.find("p:txBody", NS)
    child(body, "a:bodyPr").attrib.update(
        lIns=emu(0.18), rIns=emu(0.18), tIns=emu(0.1), bIns=emu(0.1)
    )
    for spacing in body.findall(".//a:spcPts", NS):
        spacing.set("val", "0")
    for spacing in body.findall(".//a:lnSpc/a:spcPct", NS):
        spacing.set("val", "100000")


def split_body(shape):
    """Separate a caption from code without rewriting its text or links."""
    paragraphs = shape.findall("p:txBody/a:p", NS)
    if len(paragraphs) != 2:
        raise ValueError("The core example requires one code block and one explanatory paragraph")
    extra = copy.deepcopy(shape)
    extra.find("p:txBody", NS).remove(extra.findall("p:txBody/a:p", NS)[0])
    shape.find("p:txBody", NS).remove(paragraphs[1])
    return extra


def enlarge_visuals(tree, slide_number, profile):
    # Imported content follows the template's group properties and footer shapes.
    pictures = [s for s in tree if s.tag == tag("p:pic")]
    # The selected reference stores its logo in the layout, outside this tree.
    if len(pictures) != 1:
        raise ValueError("Expected one content image on each overview slide")
    picture = pictures[0]
    texts = [s for s in tree if s.tag == tag("p:sp") and s.find(".//p:ph", NS) is None]
    _title, first, second = texts
    if slide_number == 1:
        place(picture, (8.6, 1.8, 4.0, 4.4), picture=True)
        place(second, (8.55, 6.35, 4.1, 0.55))
    elif slide_number == 3:
        place(first, (0.65, 1.85, 6.5, 2.55))
        place(picture, (7.45, 1.8, 5.3, 2.6), picture=True)
        place(second, (0.65, 4.65, 12.05, 2.1))
    elif slide_number == 5:
        place(picture, (1.25, 1.45, 10.8, 0.95), picture=True)
        code = split_body(first)
        explanation = split_body(second)
        place(first, (0.65, 2.52, 12.05, 0.3))
        code_panel(code, (0.65, 2.9, 12.05, 2.2), 17.5, profile)
        code_panel(second, (0.65, 6.05, 12.05, 0.62), 15, profile)
        place(explanation, (0.65, 6.7, 12.05, 0.3))
        table = next(s for s in tree if s.tag == tag("p:graphicFrame"))
        place(table, (0.65, 5.3, 12.05, 0.65))
        for cell in table.findall(".//a:tc", NS):
            child(cell, "a:tcPr").attrib.update(marT=emu(0.02), marB=emu(0.02))
        for extra in (code, explanation):
            next_id = 1 + max(int(n.get("id")) for n in tree.findall(".//p:cNvPr", NS))
            extra.find(".//p:cNvPr", NS).set("id", str(next_id))
            tree.append(extra)
    else:
        place(picture, (0.75, 2.2, 11.85, 2.3), picture=True)
        place(second, (0.65, 4.75, 12.05, 2.0))
