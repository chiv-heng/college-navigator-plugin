#!/usr/bin/env python3
"""
Generate a formatted PDF from a markdown college counselor report.

Usage:
    python generate-pdf-report.py input.md [output.pdf]

If output path is not specified, generates {input_stem}.pdf

Requirements (one of):
    pip install markdown weasyprint   # Best quality — requires brew install pango
    pip install markdown reportlab    # Good quality — no system deps
"""

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# WeasyPrint renderer (best quality, requires system libs)
# ---------------------------------------------------------------------------

def generate_with_weasyprint(md_content: str, output_path: str, title: str) -> None:
    """Generate PDF using markdown + weasyprint."""
    import markdown
    from weasyprint import HTML

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"],
    )

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
    @page {{
        size: letter;
        margin: 1in;
        @bottom-center {{
            content: counter(page) " of " counter(pages);
            font-size: 9pt;
            color: #666;
        }}
    }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #1a1a1a;
    }}
    h1 {{
        font-size: 20pt;
        border-bottom: 2px solid #2c5282;
        padding-bottom: 8px;
        color: #2c5282;
    }}
    h2 {{
        font-size: 15pt;
        color: #2c5282;
        margin-top: 24px;
        border-bottom: 1px solid #cbd5e0;
        padding-bottom: 4px;
        break-after: avoid;
    }}
    h3 {{
        font-size: 12pt;
        color: #4a5568;
        margin-top: 16px;
        break-after: avoid;
    }}
    h4 {{
        break-after: avoid;
    }}
    h2 + *, h3 + *, h4 + * {{
        break-before: avoid;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 12px 0;
        font-size: 10pt;
        break-inside: avoid;
    }}
    tr {{
        break-inside: avoid;
    }}
    th, td {{
        border: 1px solid #cbd5e0;
        padding: 6px 10px;
        text-align: left;
    }}
    th {{
        background-color: #edf2f7;
        font-weight: 600;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 20px 0;
        break-after: avoid;
    }}
    ul {{
        padding-left: 20px;
    }}
    li {{
        margin-bottom: 4px;
        break-inside: avoid;
    }}
    em {{
        color: #718096;
    }}
    strong {{
        color: #2d3748;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=html_doc).write_pdf(output_path)


# ---------------------------------------------------------------------------
# ReportLab renderer (good quality, no system deps)
# ---------------------------------------------------------------------------

def generate_with_reportlab(md_content: str, output_path: str) -> None:
    """Generate a styled PDF using markdown (for HTML conversion) + reportlab."""
    import markdown as md_lib
    from xml.etree import ElementTree as ET

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        KeepTogether, HRFlowable, PageBreak,
    )

    # -- Colors ---------------------------------------------------------------
    BLUE = HexColor("#2c5282")
    DARK = HexColor("#1a1a1a")
    GRAY = HexColor("#4a5568")
    LIGHT_GRAY = HexColor("#cbd5e0")
    TABLE_HEADER_BG = HexColor("#edf2f7")

    # -- Styles ---------------------------------------------------------------
    base = getSampleStyleSheet()

    styles = {
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"],
            fontSize=11, leading=16, textColor=DARK,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"],
            fontSize=20, leading=24, textColor=BLUE,
            spaceAfter=10, spaceBefore=0,
            borderWidth=0,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"],
            fontSize=15, leading=19, textColor=BLUE,
            spaceBefore=18, spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"],
            fontSize=12, leading=15, textColor=GRAY,
            spaceBefore=12, spaceAfter=4,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4", parent=base["Heading4"],
            fontSize=11, leading=14, textColor=GRAY,
            spaceBefore=8, spaceAfter=3,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"],
            fontSize=11, leading=16, textColor=DARK,
            leftIndent=20, bulletIndent=8,
            spaceAfter=3,
        ),
        "checkbox": ParagraphStyle(
            "Checkbox", parent=base["BodyText"],
            fontSize=11, leading=16, textColor=DARK,
            leftIndent=20, bulletIndent=8,
            spaceAfter=3,
        ),
        "table_header": ParagraphStyle(
            "TH", parent=base["BodyText"],
            fontSize=10, leading=13, textColor=DARK,
            fontName="Helvetica-Bold",
        ),
        "table_cell": ParagraphStyle(
            "TD", parent=base["BodyText"],
            fontSize=10, leading=13, textColor=DARK,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=base["BodyText"],
            fontSize=10, leading=14, textColor=GRAY,
            spaceAfter=2,
        ),
        "footer": ParagraphStyle(
            "Footer", parent=base["BodyText"],
            fontSize=9, leading=12, textColor=HexColor("#a0aec0"),
            spaceBefore=20,
        ),
    }

    # -- Markdown → HTML → flowables -----------------------------------------

    html = md_lib.markdown(md_content, extensions=["tables", "fenced_code"])
    # Wrap in a root element for valid XML parsing
    html = f"<root>{html}</root>"
    # Clean up common markdown artifacts that break XML parsing
    html = html.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
    # Fix bare < and > inside text (not tags) — crude but effective
    # Also handle unclosed <br> tags
    html = re.sub(r"<br\s*/?>", "<br/>", html)

    try:
        root = ET.fromstring(html)
    except ET.ParseError:
        # If HTML is too messy for XML parsing, fall back to line-by-line
        _generate_line_by_line(md_content, output_path, styles)
        return

    story = []

    def inline_markup(el):
        """Convert an element's text + children to reportlab-compatible XML.

        Handles nested structures like <li><p><strong>text</strong> more</p></li>
        by recursing into block-level children (p, div, span) transparently.
        """
        parts = []
        if el.text:
            parts.append(_escape(el.text))
        for child in el:
            tag = child.tag.lower()
            if tag == "strong" or tag == "b":
                parts.append(f"<b>{inline_markup(child)}</b>")
            elif tag == "em" or tag == "i":
                parts.append(f"<i>{inline_markup(child)}</i>")
            elif tag == "code":
                parts.append(f"<font face='Courier'>{_escape(child.text or '')}</font>")
            elif tag == "a":
                link_text = child.text or child.get("href", "")
                parts.append(f"<u><font color='#2c5282'>{_escape(link_text)}</font></u>")
            elif tag == "br":
                parts.append("<br/>")
            elif tag in ("p", "div", "span"):
                # Recurse into block-level wrappers (e.g., <li><p>...</p></li>)
                parts.append(inline_markup(child))
            else:
                # Unknown tag — extract text content recursively
                parts.append(inline_markup(child))
            if child.tail:
                parts.append(_escape(child.tail))
        return "".join(parts)

    def _escape(text):
        """Escape text for reportlab XML paragraphs."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

    def process_element(el):
        tag = el.tag.lower()

        if tag in ("h1", "h2", "h3", "h4"):
            text = inline_markup(el)
            story.append(Paragraph(text, styles[tag]))

        elif tag == "p":
            text = inline_markup(el)
            if not text.strip():
                return
            # Detect metadata lines like **Date:** ...
            if text.startswith("<b>") and ":" in text[:60]:
                story.append(Paragraph(text, styles["meta"]))
            else:
                story.append(Paragraph(text, styles["body"]))

        elif tag == "hr":
            story.append(HRFlowable(
                width="100%", thickness=1, color=LIGHT_GRAY,
                spaceBefore=10, spaceAfter=10,
            ))

        elif tag in ("ul", "ol"):
            items = []
            for i, li in enumerate(el.findall("li")):
                text = inline_markup(li)
                # Detect checkbox items: - [ ] or - [x]
                if text.startswith("[ ] ") or text.startswith("[x] "):
                    check = "\u2610 " if text.startswith("[ ]") else "\u2611 "
                    items.append(Paragraph(
                        f"{check}{text[4:]}", styles["checkbox"]
                    ))
                elif tag == "ol":
                    items.append(Paragraph(
                        f"{i + 1}. {text}", styles["bullet"]
                    ))
                else:
                    items.append(Paragraph(
                        f"\u2022 {text}", styles["bullet"]
                    ))
            # Keep short lists together
            if len(items) <= 6:
                story.append(KeepTogether(items))
            else:
                story.extend(items)

        elif tag == "table":
            _add_table(el, story, styles)

        elif tag == "blockquote":
            for child in el:
                text = inline_markup(child)
                bq_style = ParagraphStyle(
                    "BQ", parent=styles["body"],
                    leftIndent=20, textColor=GRAY,
                    borderPadding=(0, 0, 0, 8),
                )
                story.append(Paragraph(text, bq_style))

        elif tag == "pre":
            code = el.find("code")
            text = _escape(code.text if code is not None and code.text else (el.text or ""))
            code_style = ParagraphStyle(
                "Code", parent=styles["body"],
                fontName="Courier", fontSize=9, leading=12,
                leftIndent=12, backColor=HexColor("#f7fafc"),
                borderPadding=6, spaceAfter=8,
            )
            story.append(Paragraph(text.replace("\n", "<br/>"), code_style))

        # Recurse into divs or other containers
        elif tag in ("div", "section", "root"):
            for child in el:
                process_element(child)

    def _add_table(table_el, story, styles):
        """Convert an HTML table element to a reportlab Table."""
        data = []
        header_rows = 0

        thead = table_el.find("thead")
        tbody = table_el.find("tbody")

        if thead is not None:
            for tr in thead.findall("tr"):
                row = []
                for th in tr:
                    row.append(Paragraph(inline_markup(th), styles["table_header"]))
                data.append(row)
                header_rows += 1

        body = tbody if tbody is not None else table_el
        for tr in body.findall("tr"):
            row = []
            is_header_row = all(td.tag == "th" for td in tr)
            for td in tr:
                cell_style = styles["table_header"] if td.tag == "th" else styles["table_cell"]
                row.append(Paragraph(inline_markup(td), cell_style))
            if is_header_row and not thead and len(data) == header_rows:
                header_rows += 1
            data.append(row)

        if not data:
            return

        # Ensure all rows have same column count
        max_cols = max(len(r) for r in data)
        for row in data:
            while len(row) < max_cols:
                row.append(Paragraph("", styles["table_cell"]))

        col_width = (letter[0] - 2 * inch) / max_cols
        # repeatRows causes header row(s) to repeat on each page
        t = Table(data, colWidths=[col_width] * max_cols,
                  repeatRows=header_rows if header_rows > 0 else 0)

        style_cmds = [
            ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
        if header_rows > 0:
            style_cmds.append(
                ("BACKGROUND", (0, 0), (-1, header_rows - 1), TABLE_HEADER_BG)
            )

        t.setStyle(TableStyle(style_cmds))
        # Small tables: keep together. Large tables: let them split with repeated headers.
        if len(data) <= 8:
            story.append(KeepTogether([t]))
        else:
            story.append(t)
        story.append(Spacer(1, 6))

    # Process all top-level elements
    for child in root:
        process_element(child)

    # -- Build PDF ------------------------------------------------------------
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
    )

    # Add page numbers
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(HexColor("#999999"))
        canvas.drawCentredString(
            letter[0] / 2, 0.5 * inch,
            f"{doc.page}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def _generate_line_by_line(md_content, output_path, styles):
    """Ultra-simple fallback if HTML parsing fails."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=inch, bottomMargin=inch)
    story = []

    for line in md_content.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 8))
        elif stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], styles["h1"]))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], styles["h2"]))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], styles["h3"]))
        elif stripped.startswith("---"):
            story.append(Spacer(1, 6))
        elif stripped.startswith("- "):
            text = stripped[2:]
            story.append(Paragraph(f"\u2022 {text}", styles["bullet"]))
        else:
            # Basic bold/italic conversion
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", stripped)
            text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
            story.append(Paragraph(text, styles["body"]))

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(HexColor("#999999"))
        from reportlab.lib.pagesizes import letter as lt
        canvas.drawCentredString(lt[0] / 2, 0.5 * inch, f"{doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate-pdf-report.py input.md [output.pdf]")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = str(input_path.with_suffix(".pdf"))

    md_content = input_path.read_text(encoding="utf-8")

    # Extract title from first heading
    title = "Student Profile Report"
    for line in md_content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Try weasyprint first, then reportlab
    try:
        generate_with_weasyprint(md_content, output_path, title)
        print(f"PDF generated (weasyprint): {output_path}")
    except (ImportError, OSError):
        try:
            print("weasyprint not available, using reportlab...")
            generate_with_reportlab(md_content, output_path)
            print(f"PDF generated (reportlab): {output_path}")
        except ImportError:
            print("ERROR: No PDF library available.")
            print("Install one of:")
            print("  pip install markdown reportlab          # Recommended")
            print("  pip install markdown weasyprint          # Requires: brew install pango")
            sys.exit(1)


if __name__ == "__main__":
    main()
