"""Render repository Markdown as a readable PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


SOURCE_FILES = (
    Path("README.md"),
    Path("methodology/fear-greed-formula.md"),
    Path("methodology/normalization.md"),
    Path("methodology/weighting.md"),
    Path("guides/setup.md"),
    Path("guides/data-pipeline.md"),
    Path("guides/usage.md"),
    Path("architecture/overview.md"),
    Path("architecture/data-flow.md"),
)


def _group(value: str, start: int) -> tuple[str, int] | None:
    """Read one brace-delimited LaTex group, including nested braces."""
    if start >= len(value) or value[start] != "{":
        return None
    depth, index = 1, start + 1
    while index < len(value) and depth:
        depth += (value[index] == "{") - (value[index] == "}")
        index += 1
    return (value[start + 1 : index - 1], index) if depth == 0 else None


def _fractions(value: str) -> str:
    """Change LaTex fractions to plain notation without losing nested terms."""
    parts: list[str] = []
    index = 0
    while index < len(value):
        marker = value.find(r"\frac", index)
        if marker < 0:
            parts.append(value[index:])
            break
        parts.append(value[index:marker])
        numerator = _group(value, marker + len(r"\frac"))
        denominator = _group(value, numerator[1]) if numerator else None
        if not numerator or not denominator:
            parts.append(r"\frac")
            index = marker + len(r"\frac")
            continue
        parts.append(f"({numerator[0]}) / ({denominator[0]})")
        index = denominator[1]
    return "".join(parts)


def math_text(value: str) -> str:
    """Convert the small LaTex subset used in this repository to plain text."""
    value = _fractions(value.strip())
    value = re.sub(r"\\(?:begin|end)\{(?:aligned|array)\}", "", value)
    value = value.replace("\\\\", "\n").replace("&", "")
    for old, new in {
        r"\times": " x ", r"\Rightarrow": " -> ", r"\left": "",
        r"\right": "", r"\qquad": "   ", r"\quad": "   ",
        r"\operatorname": "", r"\mathbf": "", r"\text": "",
        r"\le": " <= ", r"\ge": " >= ", "{,}": ",",
    }.items():
        value = value.replace(old, new)
    value = re.sub(r"\\([A-Za-z]+)", r"\1", value)
    return re.sub(r"[ \t]+", " ", value.replace("{", "").replace("}", "")).strip()


def inline(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = html.escape(value, quote=False)
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(r"\$([^$]+)\$", lambda item: math_text(item.group(1)), value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    return re.sub(r"(?<!\*)\*([^*]+)\*", r"<i>\1</i>", value)


def page_number(canvas: object, document: object) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 1.05 * cm, f"IndieKator - halaman {document.page}")
    canvas.restoreState()


def story(markdown: str) -> list[object]:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=25, spaceAfter=14))
    styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, spaceBefore=11, spaceAfter=6))
    styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, spaceAfter=7))
    styles.add(ParagraphStyle("Cell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11))
    styles.add(ParagraphStyle("HeaderCell", parent=styles["Cell"], fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle("Quote", parent=styles["Body"], fontName="Helvetica-Oblique", leftIndent=12, borderColor=colors.HexColor("#94A3B8"), borderWidth=1, borderPadding=6, spaceAfter=8))
    styles.add(ParagraphStyle("Formula", parent=styles["Code"], fontName="Courier", fontSize=8.5, leading=12, backColor=colors.HexColor("#F1F5F9"), borderColor=colors.HexColor("#CBD5E1"), borderWidth=.5, borderPadding=7, spaceBefore=4, spaceAfter=9))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=8.5, leading=11, backColor=colors.HexColor("#F8FAFC"), borderColor=colors.HexColor("#CBD5E1"), borderWidth=.5, borderPadding=7, spaceBefore=4, spaceAfter=9))

    result: list[object] = []
    lines, index = markdown.splitlines(), 0
    while index < len(lines):
        current = lines[index].strip()
        if not current:
            index += 1
        elif current.startswith("```"):
            index, code = index + 1, []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            result.append(Paragraph(html.escape("\n".join(code)).replace("\n", "<br/>"), styles["CodeBlock"]))
            index += 1
        elif current == "$$":
            index, formula = index + 1, []
            while index < len(lines) and lines[index].strip() != "$$":
                formula.append(lines[index])
                index += 1
            result.append(Paragraph(html.escape(math_text("\n".join(formula))).replace("\n", "<br/>"), styles["Formula"]))
            index += 1
        elif current.startswith("# "):
            result.append(Paragraph(inline(current[2:]), styles["DocTitle"])); index += 1
        elif current.startswith("## "):
            result.append(Paragraph(inline(current[3:]), styles["H1"])); index += 1
        elif current.startswith("### "):
            result.append(Paragraph(inline(current[4:]), styles["H2"])); index += 1
        elif current.startswith("> "):
            quote = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote.append(lines[index].strip()[2:]); index += 1
            result.append(Paragraph(inline(" ".join(quote)), styles["Quote"]))
        elif re.match(r"[-*] ", current):
            items = []
            while index < len(lines) and re.match(r"[-*] ", lines[index].strip()):
                items.append(ListItem(Paragraph(inline(lines[index].strip()[2:]), styles["Body"])))
                index += 1
            result.extend([ListFlowable(items, bulletType="bullet", leftIndent=16), Spacer(1, 5)])
        elif current.startswith("|"):
            table = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                row = lines[index].strip().strip("|").split("|")
                if not all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in row):
                    style = styles["HeaderCell"] if not table else styles["Cell"]
                    table.append([Paragraph(inline(cell.strip()), style) for cell in row])
                index += 1
            width = (A4[0] - 3.6 * cm) / len(table[0])
            rendered = Table(table, colWidths=[width] * len(table[0]), repeatRows=1, hAlign="LEFT")
            rendered.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#CBD5E1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            result.extend([rendered, Spacer(1, 7)])
        else:
            paragraph = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not candidate or candidate == "$$" or candidate.startswith(("#", "> ", "|")):
                    break
                paragraph.append(candidate); index += 1
            result.append(Paragraph(inline(" ".join(paragraph)), styles["Body"]))
    return result


def handbook_story() -> list[object]:
    """Load every published document in the handbook's canonical order."""
    result: list[object] = []
    for source in SOURCE_FILES:
        if not source.is_file():
            raise FileNotFoundError(f"handbook source file not found: {source}")
        result.extend(story(source.read_text(encoding="utf-8")))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("output/pdf/indiekator-docs.pdf"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(args.output), pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.7 * cm, bottomMargin=1.7 * cm, title="IndieKator Documentation", author="IndieKator")
    document.build(handbook_story(), onFirstPage=page_number, onLaterPages=page_number)
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
