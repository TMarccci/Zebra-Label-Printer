from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import markdown as md
import requests

from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

try:
    # Optional legacy engine (kept for compatibility).
    from xhtml2pdf import pisa  # type: ignore

    _HAS_XHTML2PDF = True
except Exception:
    pisa = None
    _HAS_XHTML2PDF = False


def _windows_fonts_dir() -> Path | None:
    windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot")
    if not windir:
        return None
    fonts = Path(windir) / "Fonts"
    return fonts if fonts.exists() else None


@dataclass(frozen=True)
class FontSpec:
    family: str
    regular: Path
    bold: Path | None = None
    italic: Path | None = None
    bold_italic: Path | None = None


def _pick_windows_unicode_font() -> FontSpec | None:
    """Pick a Windows TTF font likely to include HU/CZ accented glyphs."""
    fonts_dir = _windows_fonts_dir()
    if not fonts_dir:
        return None

    candidates = [
        FontSpec("AppFont", fonts_dir / "segoeui.ttf", fonts_dir / "segoeuib.ttf", fonts_dir / "segoeuii.ttf", fonts_dir / "segoeuiz.ttf"),
        FontSpec("AppFont", fonts_dir / "arial.ttf", fonts_dir / "arialbd.ttf", fonts_dir / "ariali.ttf", fonts_dir / "arialbi.ttf"),
        # Arial Unicode MS is rare but excellent if present.
        FontSpec("AppFont", fonts_dir / "arialuni.ttf"),
        FontSpec("AppFont", fonts_dir / "calibri.ttf", fonts_dir / "calibrib.ttf", fonts_dir / "calibrii.ttf", fonts_dir / "calibriz.ttf"),
    ]

    for spec in candidates:
        if spec.regular.exists():
            return spec

    return None


def _register_reportlab_family(spec: FontSpec) -> tuple[str, str, str, str]:
        """Register fonts for ReportLab and return (normal, bold, italic, bold_italic) font names."""

        family = spec.family
        normal = family
        bold = f"{family}-Bold"
        italic = f"{family}-Italic"
        bold_italic = f"{family}-BoldItalic"

        pdfmetrics.registerFont(TTFont(normal, str(spec.regular)))
        if spec.bold and spec.bold.exists():
                pdfmetrics.registerFont(TTFont(bold, str(spec.bold)))
        else:
                bold = normal
        if spec.italic and spec.italic.exists():
                pdfmetrics.registerFont(TTFont(italic, str(spec.italic)))
        else:
                italic = normal
        if spec.bold_italic and spec.bold_italic.exists():
                pdfmetrics.registerFont(TTFont(bold_italic, str(spec.bold_italic)))
        else:
                bold_italic = bold if bold != normal else italic

        pdfmetrics.registerFontFamily(family, normal=normal, bold=bold, italic=italic, boldItalic=bold_italic)
        return normal, bold, italic, bold_italic


def ensure_reportlab_unicode_font() -> tuple[str, str, str, str]:
        """Ensure ReportLab uses a font with HU/CZ accented glyphs."""

        spec = _pick_windows_unicode_font()
        if spec:
                return _register_reportlab_family(spec)
        return ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique")


def _link_callback(uri: str, rel: str, base_dir: Path) -> str:
    # Allow remote images/links.
    lowered = uri.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        return uri

    # If it's already an absolute Windows path (C:\... or C:/...) or UNC path, return it.
    if len(uri) >= 3 and uri[1] == ":" and (uri[2] == "\\" or uri[2] == "/"):
        return uri
    if uri.startswith("\\\\"):
        return uri

    # Handle file:// URIs.
    if lowered.startswith("file:///"):
        uri = uri[8:]
    elif lowered.startswith("file://"):
        uri = uri[7:]

    p = Path(uri)
    if not p.is_absolute():
        p = (base_dir / p).resolve()

    return str(p)


_RE_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_RE_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_HTML_IMG = re.compile(r"<\s*img\b[^>]*?\bsrc\s*=\s*['\"]([^'\"]+)['\"][^>]*?>", re.IGNORECASE)
_RE_HTML_TAG = re.compile(r"<[^>]+>")
_RE_HTML_IMG_WIDTH = re.compile(r"<\s*img\b[^>]*?\bwidth\s*=\s*['\"]?([^'\"\s>]+)", re.IGNORECASE)
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_INLINE_CODE = re.compile(r"`([^`]+)`")
_RE_IMAGE_PLACEHOLDER = re.compile(r"\bImage(?:\[(?P<width>\d+(?:\.\d+)?)\])?:\s*(?P<src>\S+)")
_RE_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)


def _escape_para(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _escape_attr(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;")
        .replace("'", "&#39;")
    )


def _render_bold(text: str) -> str:
    """Render **bold** in plain text into ReportLab markup, escaping the rest."""

    out: list[str] = []
    last = 0
    for m in _RE_BOLD.finditer(text):
        out.append(_escape_para(text[last:m.start()]))
        out.append(f"<b>{_escape_para(m.group(1))}</b>")
        last = m.end()
    out.append(_escape_para(text[last:]))
    return "".join(out)


def _normalize_url_display(url: str) -> str:
    # Drop trailing punctuation that commonly follows links in prose.
    return url.rstrip(").,;:!?")


def _render_text_with_links(text: str) -> str:
    """Render markdown links and raw URLs into clickable anchors."""

    def render_plain_with_urls(s: str) -> str:
        out: list[str] = []
        last = 0
        for m in _RE_URL.finditer(s):
            out.append(_render_bold(s[last:m.start()]))
            raw_url = m.group(0)
            url = _normalize_url_display(raw_url)
            href = _escape_attr(url)
            label = _escape_para(url)
            out.append(f"<a href='{href}' color='blue'>{label}</a>")
            last = m.end()
        out.append(_render_bold(s[last:]))
        return "".join(out)

    out2: list[str] = []
    last2 = 0
    for m in _RE_MD_LINK.finditer(text):
        out2.append(render_plain_with_urls(text[last2:m.start()]))
        label_raw = m.group(1)
        url_raw = m.group(2).strip()
        url = _normalize_url_display(url_raw)
        out2.append(
            f"<a href='{_escape_attr(url)}' color='blue'>{_render_bold(label_raw)}</a>"
        )
        last2 = m.end()
    out2.append(render_plain_with_urls(text[last2:]))
    return "".join(out2)


def _inline_markup(text: str) -> str:
    """Convert a small subset of Markdown inline formatting to ReportLab Paragraph markup."""

    # Keep inline code segments literal (no links/bold inside).
    parts = text.split("`")
    rendered: list[str] = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            rendered.append(f"<font face='Courier'>{_escape_para(part)}</font>")
        else:
            rendered.append(_render_text_with_links(part))
    return "".join(rendered)


def _parse_img_tag(line: str) -> tuple[str, float | None] | None:
    """Return (src, width_px) if line contains an <img> tag."""

    m = _RE_HTML_IMG.search(line)
    if not m:
        return None
    src = m.group(1).strip()

    width_px: float | None = None
    mw = _RE_HTML_IMG_WIDTH.search(line)
    if mw:
        raw = mw.group(1).strip().rstrip("px")
        try:
            width_px = float(raw)
        except Exception:
            width_px = None

    return src, width_px


def _parse_image_placeholder(text: str) -> tuple[str, float | None] | None:
    m = _RE_IMAGE_PLACEHOLDER.search(text)
    if not m:
        return None
    src = m.group("src").strip()
    width_px: float | None = None
    if m.group("width"):
        try:
            width_px = float(m.group("width"))
        except Exception:
            width_px = None
    return src, width_px


def _is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"}
    except Exception:
        return False


def _download_to_cache(url: str) -> Path:
    cache_dir = Path(tempfile.gettempdir()) / "zlp_md_to_pdf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    parsed = urlparse(url)
    name = Path(parsed.path).name or "image"
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    target = cache_dir / safe

    if target.exists() and target.stat().st_size > 0:
        return target

    r = requests.get(url, timeout=20)
    r.raise_for_status()
    target.write_bytes(r.content)
    return target


def _resolve_image_src(src: str, base_dir: Path) -> Path | None:
    if _is_http_url(src):
        try:
            return _download_to_cache(src)
        except Exception:
            return None

    # file path
    p = Path(src)
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    return p if p.exists() else None


def _fit_image(img: RLImage, max_width_pt: float, max_height_pt: float) -> RLImage:
    """Scale image down (never up) to fit within max box."""

    try:
        w = float(img.imageWidth)
        h = float(img.imageHeight)
    except Exception:
        return img

    if w <= 0 or h <= 0:
        return img

    scale = min(max_width_pt / w, max_height_pt / h, 1.0)
    img.drawWidth = w * scale
    img.drawHeight = h * scale
    return img


def _sanitize_inline_html(text: str) -> str:
    """Remove/neutralize embedded HTML so ReportLab Paragraph can parse safely.

    - Converts <img ... src="..."> to a short 'Image: <url>' placeholder.
    - Strips remaining HTML tags.
    """

    # Replace <img ...> with its src (keep information without rendering images).
    def repl_img(m: re.Match[str]) -> str:
        src = m.group(1).strip()
        width_px: float | None = None
        mw = _RE_HTML_IMG_WIDTH.search(m.group(0))
        if mw:
            raw = mw.group(1).strip().rstrip("px")
            try:
                width_px = float(raw)
            except Exception:
                width_px = None
        if width_px:
            return f"Image[{width_px:g}]: {src}"
        return f"Image: {src}"

    text = _RE_HTML_IMG.sub(repl_img, text)
    # Strip any other tags (e.g. <br>, <b>, etc.).
    text = _RE_HTML_TAG.sub("", text)
    return text.strip()


def _md_to_reportlab_blocks(md_text: str) -> list[tuple[str, object]]:
    """Very small Markdown block parser suited for the tutorial files."""

    blocks: list[tuple[str, object]] = []
    lines = md_text.replace("\r\n", "\n").split("\n")
    i = 0
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph(buf: list[str]) -> None:
        if not buf:
            return
        text = " ".join([x.strip() for x in buf]).strip()
        if text:
            blocks.append(("p", text))
        buf.clear()

    paragraph: list[str] = []
    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                flush_paragraph(paragraph)
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_paragraph(paragraph)
            level = len(m.group(1))
            blocks.append((f"h{level}", m.group(2).strip()))
            i += 1
            continue

        # Horizontal rule
        if line.strip() in {"---", "***", "___"}:
            flush_paragraph(paragraph)
            blocks.append(("hr", ""))
            i += 1
            continue

        # Tables (simple pipe tables)
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?\s*-+", lines[i + 1]):
            flush_paragraph(paragraph)
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip() != "":
                table_lines.append(lines[i])
                i += 1
            blocks.append(("table", table_lines))
            continue

        # Lists
        if re.match(r"^\s*[-*]\s+", line):
            flush_paragraph(paragraph)
            items: list[str] = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            blocks.append(("ul", items))
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            flush_paragraph(paragraph)
            items2: list[str] = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items2.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            blocks.append(("ol", items2))
            continue

        # Blank line ends paragraph
        if line.strip() == "":
            flush_paragraph(paragraph)
            i += 1
            continue

        # Standalone <img ...> line becomes an image block.
        img = _parse_img_tag(line)
        if img and line.strip().lower().startswith("<img"):
            flush_paragraph(paragraph)
            blocks.append(("img", img))
            i += 1
            continue

        # Replace Markdown images with a short placeholder (we don't know placement inline).
        replaced = _RE_MD_IMAGE.sub(lambda m2: f"Image: {m2.group(2)}", line)
        paragraph.append(_sanitize_inline_html(replaced))
        i += 1

    flush_paragraph(paragraph)
    if in_code and code_lines:
        blocks.append(("code", "\n".join(code_lines)))
    return blocks


def _pipe_table_to_matrix(table_lines: list[str]) -> list[list[str]]:
    def split_row(row: str) -> list[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [_sanitize_inline_html(c.strip()) for c in row.split("|")]

    rows = [split_row(r) for r in table_lines if r.strip()]
    # Drop the separator row (dashes)
    if len(rows) >= 2:
        rows.pop(1)
    return rows


def _build_reportlab_story(md_text: str, base_dir: Path) -> list[object]:
    normal, bold, italic, bold_italic = ensure_reportlab_unicode_font()
    base = getSampleStyleSheet()

    body = ParagraphStyle(
        name="Body",
        parent=base["Normal"],
        fontName=normal,
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
    )
    body_bold = ParagraphStyle(name="BodyBold", parent=body, fontName=bold)
    code_style = ParagraphStyle(name="Code", parent=body, fontName="Courier", fontSize=9, leading=11)

    heading_styles: dict[str, ParagraphStyle] = {
        "h1": ParagraphStyle(name="H1", parent=body_bold, fontSize=18, leading=22, spaceBefore=8, spaceAfter=6),
        "h2": ParagraphStyle(name="H2", parent=body_bold, fontSize=14, leading=18, spaceBefore=8, spaceAfter=6),
        "h3": ParagraphStyle(name="H3", parent=body_bold, fontSize=12, leading=16, spaceBefore=8, spaceAfter=4),
        "h4": ParagraphStyle(name="H4", parent=body_bold, fontSize=11, leading=14, spaceBefore=6, spaceAfter=3),
        "h5": ParagraphStyle(name="H5", parent=body_bold, fontSize=11, leading=14, spaceBefore=6, spaceAfter=3),
        "h6": ParagraphStyle(name="H6", parent=body_bold, fontSize=11, leading=14, spaceBefore=6, spaceAfter=3),
    }

    story: list[object] = []

    # Printable area (A4 minus margins) for automatic image scaling.
    page_w, page_h = pagesizes.A4
    max_img_w = page_w - (14 * mm) - (14 * mm)
    max_img_h = page_h - (16 * mm) - (16 * mm)

    for kind, payload in _md_to_reportlab_blocks(md_text):
        if kind in heading_styles:
            story.append(Paragraph(_inline_markup(str(payload)), heading_styles[kind]))
            continue
        if kind == "p":
            story.append(Paragraph(_inline_markup(str(payload)), body))
            story.append(Spacer(1, 4))
            continue
        if kind == "code":
            pre = Preformatted(str(payload), code_style)
            box = Table([[pre]])
            box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            story.append(box)
            story.append(Spacer(1, 8))
            continue
        if kind == "hr":
            story.append(Spacer(1, 6))
            rule = Table([[""]], colWidths=[170 * mm])
            rule.setStyle(
                TableStyle(
                    [
                        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ]
                )
            )
            story.append(rule)
            story.append(Spacer(1, 6))
            continue
        if kind in {"ul", "ol"}:
            items = payload  # type: ignore[assignment]
            for idx, item in enumerate(items, start=1):
                prefix = "• " if kind == "ul" else f"{idx}. "
                story.append(Paragraph(_inline_markup(prefix + str(item)), body))
            story.append(Spacer(1, 6))
            continue
        if kind == "img":
            src, width_px = payload  # type: ignore[misc]
            local = _resolve_image_src(str(src), base_dir)
            if local is None:
                story.append(Paragraph(_inline_markup(f"Image: {src}"), body))
                story.append(Spacer(1, 6))
                continue

            img_flow = RLImage(str(local))
            # If width is provided, scale to that width in points.
            if width_px:
                target_w = float(width_px) * 0.75  # px->pt approx at 96dpi
                if img_flow.imageWidth:
                    scale = target_w / float(img_flow.imageWidth)
                    img_flow.drawWidth = target_w
                    img_flow.drawHeight = float(img_flow.imageHeight) * scale
            # Always cap to printable area.
            img_flow = _fit_image(img_flow, max_width_pt=max_img_w, max_height_pt=max_img_h)
            story.append(img_flow)
            story.append(Spacer(1, 8))
            continue
        if kind == "table":
            matrix_raw = _pipe_table_to_matrix(payload)  # type: ignore[arg-type]

            if not matrix_raw:
                continue

            ncols = max(len(r) for r in matrix_raw)
            if ncols <= 0:
                continue

            # Set explicit column widths so content (especially images) fits inside the table.
            if ncols == 2:
                col_widths = [max_img_w * 0.28, max_img_w * 0.72]
            else:
                col_widths = [max_img_w / ncols] * ncols

            # Convert any <img> placeholders inside cells into images.
            matrix: list[list[object]] = []
            for row in matrix_raw:
                out_row: list[object] = []
                # Pad short rows (some markdown tables can be ragged)
                if len(row) < ncols:
                    row = row + [""] * (ncols - len(row))

                for col_idx, cell in enumerate(row):
                    img = _parse_img_tag(cell) or _parse_image_placeholder(cell)
                    if img:
                        src, width_px = img
                        local = _resolve_image_src(str(src), base_dir)
                        if local:
                            img_flow = RLImage(str(local))
                            if width_px:
                                target_w = float(width_px) * 0.75
                                if img_flow.imageWidth:
                                    scale = target_w / float(img_flow.imageWidth)
                                    img_flow.drawWidth = target_w
                                    img_flow.drawHeight = float(img_flow.imageHeight) * scale
                            # Fit to column width (minus padding) and also cap to page height.
                            cell_max_w = max(col_widths[col_idx] - 12, 50)
                            cell_max_h = max_img_h * 0.75
                            img_flow = _fit_image(img_flow, max_width_pt=cell_max_w, max_height_pt=cell_max_h)
                            out_row.append(img_flow)
                            continue
                    out_row.append(Paragraph(_inline_markup(str(cell)), body))
                matrix.append(out_row)
            if matrix:
                tbl = Table(matrix, hAlign="LEFT", colWidths=col_widths, repeatRows=1)
                tbl.setStyle(
                    TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, 0), bold),
                            ("FONTSIZE", (0, 0), (-1, -1), 9),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ]
                    )
                )
                story.append(tbl)
                story.append(Spacer(1, 8))
            continue

    return story


def convert_markdown_file_to_pdf_reportlab(input_md: Path, output_pdf: Path) -> None:
    md_text = input_md.read_text(encoding="utf-8")
    story = _build_reportlab_story(md_text, base_dir=input_md.parent)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=pagesizes.A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=input_md.stem,
    )
    doc.build(story)


def convert_markdown_file_to_pdf_xhtml2pdf(input_md: Path, output_pdf: Path, css_text: str | None) -> None:
    if not _HAS_XHTML2PDF:
        raise RuntimeError("xhtml2pdf is not installed; use --engine reportlab")

    base_dir = input_md.parent
    md_text = input_md.read_text(encoding="utf-8")
    html_body = md.markdown(md_text, extensions=["extra", "tables", "toc", "sane_lists"], output_format="html5")

    css = css_text or ""
    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{css}</style>"
        "</head><body>"
        f"{html_body}"
        "</body></html>"
    )

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as f:
        result = pisa.CreatePDF(
            src=html,
            dest=f,
            encoding="utf-8",
            link_callback=lambda uri, rel: _link_callback(uri, rel, base_dir),
        )
    if result.err:
        raise RuntimeError(f"PDF generation failed for {input_md.name}")


def convert_markdown_file_to_pdf(input_md: Path, output_pdf: Path, css_text: str | None, engine: str) -> None:
    if not input_md.exists() or not input_md.is_file():
        raise FileNotFoundError(str(input_md))

    engine = engine.lower().strip()
    if engine == "reportlab":
        return convert_markdown_file_to_pdf_reportlab(input_md=input_md, output_pdf=output_pdf)
    if engine == "xhtml2pdf":
        return convert_markdown_file_to_pdf_xhtml2pdf(input_md=input_md, output_pdf=output_pdf, css_text=css_text)
    raise ValueError(f"Unknown engine: {engine}")


def _iter_inputs(paths: list[Path], recursive: bool) -> list[Path]:
    inputs: list[Path] = []
    for p in paths:
        if p.is_dir():
            iterator = p.rglob("*.md") if recursive else p.glob("*.md")
            inputs.extend([x for x in iterator if x.is_file()])
        else:
            inputs.append(p)
    # De-dupe, keep stable order.
    seen: set[str] = set()
    unique: list[Path] = []
    for p in inputs:
        key = str(p.resolve()).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return unique


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF.")
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more .md files or directories containing .md files.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="",
        help="Output directory for generated PDFs. Defaults next to each input file.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="When a directory is provided, search for .md files recursively.",
    )
    parser.add_argument(
        "--engine",
        choices=["reportlab", "xhtml2pdf"],
        default="reportlab",
        help="PDF engine to use. 'reportlab' embeds Windows fonts and renders HU/CZ accents reliably.",
    )
    parser.add_argument(
        "--css",
        type=str,
        default="",
        help="Optional path to a CSS file (only used with --engine xhtml2pdf).",
    )

    args = parser.parse_args(argv)

    input_paths = [Path(p) for p in args.paths]
    md_files = _iter_inputs(input_paths, recursive=args.recursive)
    if not md_files:
        print("No markdown files found.", file=sys.stderr)
        return 2

    css_text: str | None = None
    if args.css:
        css_path = Path(args.css)
        if not css_path.exists() or not css_path.is_file():
            print(f"CSS file not found: {css_path}", file=sys.stderr)
            return 2
        css_text = css_path.read_text(encoding="utf-8")

    outdir = Path(args.outdir) if args.outdir else None

    failures = 0
    for input_md in md_files:
        try:
            if outdir is None:
                output_pdf = input_md.with_suffix(".pdf")
            else:
                output_pdf = (outdir / input_md.with_suffix(".pdf").name)

            convert_markdown_file_to_pdf(input_md=input_md, output_pdf=output_pdf, css_text=css_text, engine=args.engine)
            print(f"OK: {input_md} -> {output_pdf}")
        except Exception as e:
            failures += 1
            print(f"FAIL: {input_md}: {e}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
