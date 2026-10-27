#!/usr/bin/env python3
"""Render a client one-pager as a single A4 PDF.

    python one_pager.py content.json out.pdf

content.json holds the words; this script holds the layout. It uses the
standard Helvetica faces, which PDF readers carry themselves, so nothing is
embedded and the file stays a few KB: small enough to attach anywhere.
Exits non-zero if the content doesn't fit on one page, because a one-pager
that spills onto a second page is the thing it exists not to be.

The page is a header (title, subtitle, byline, lead) followed by `blocks`,
drawn top to bottom. Block types:

  table     heading, columns[], rows[][]       first column set in bold
  columns   left{}, right{}                    each: heading + bullets[] | steps[[name, text]] | text, optional note
  callout   heading, items[], note             tinted panel, numbered items
  timeline  heading, phases[[when, name, [lines]]], highlight (index)
  needs     label, text                        ruled line above

See one_pager.example.json for a full page.
"""
import json
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, KeepInFrame, Paragraph, Spacer, Table, TableStyle

INK = colors.HexColor("#16181d")
QUIET = colors.HexColor("#5b616e")
RULE = colors.HexColor("#dfe2e8")
ACCENT = colors.HexColor("#1f6feb")
TINT = colors.HexColor("#eef4ff")

W, H = A4
M = 15 * mm
CW = W - 2 * M  # content width
GAP = 4.2 * mm  # between blocks


def style(name, size, lead=None, font="Helvetica", color=INK, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=lead or size * 1.38, textColor=color, **kw)


S = {
    "title": style("title", 22, 24, "Helvetica-Bold"),
    "subtitle": style("subtitle", 11, 14, color=QUIET),
    "by": style("by", 8.2, 11, color=QUIET, alignment=TA_RIGHT),
    "lead": style("lead", 10, 14),
    "h2": style("h2", 7.8, 10, "Helvetica-Bold", ACCENT),
    "th": style("th", 7.6, 10, "Helvetica-Bold", QUIET),
    "cell": style("cell", 8.4, 11.2),
    "cellb": style("cellb", 8.4, 11.2, "Helvetica-Bold"),
    "body": style("body", 8.6, 11.8),
    "note": style("note", 7.8, 10.4, color=QUIET),
    "small": style("small", 7.8, 10.2, color=QUIET),
    "phw": style("phw", 9.6, 12, "Helvetica-Bold"),
}

FLAT = [("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP")]


def p(text, s="body"):
    return Paragraph(text, S[s])


def h2(text):
    return [p(text.upper(), "h2"), Spacer(0, 1.6 * mm)]


def marked(rows, mark_width):
    t = Table(rows, colWidths=[mark_width, None])
    t.setStyle(TableStyle(FLAT + [("TOPPADDING", (0, 0), (-1, -1), 0.7), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.7)]))
    return t


def bullets(items):
    return marked([[p('<font color="#1f6feb">•</font>'), p(t)] for t in items], 3.4 * mm)


def steps(items):
    return marked([[p(f'<font color="#1f6feb"><b>{i}</b></font>'), p(f"<b>{name}</b> {text}")]
                   for i, (name, text) in enumerate(items, 1)], 4.6 * mm)


def panel(flowables, width, bg=None, border=RULE, line=0.6, pad=2.6 * mm):
    t = Table([[flowables]], colWidths=[width])
    cmds = [("BOX", (0, 0), (-1, -1), line, border), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
            ("TOPPADDING", (0, 0), (-1, -1), pad * 0.85), ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if bg:
        cmds.append(("BACKGROUND", (0, 0), (-1, -1), bg))
    t.setStyle(TableStyle(cmds))
    return t


def column(spec):
    out = h2(spec["heading"]) if spec.get("heading") else []
    if "bullets" in spec:
        out.append(bullets(spec["bullets"]))
    if "steps" in spec:
        out.append(steps(spec["steps"]))
    if "text" in spec:
        out.append(p(spec["text"]))
    if spec.get("note"):
        out += [Spacer(0, 1.4 * mm), p(spec["note"], "note")]
    return out


def block_table(b):
    first = b.get("first_width", 30) * mm
    rest = CW - first
    split = b.get("split", 0.55)
    rows = [[p(x, "th") for x in b["columns"]]]
    rows += [[p(r[0], "cellb")] + [p(x, "cell") for x in r[1:]] for r in b["rows"]]
    t = Table(rows, colWidths=[first, rest * split, rest * (1 - split)])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
        ("TOPPADDING", (0, 1), (-1, -1), 1.4 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
    ]))
    return h2(b["heading"]) + [t]


def block_columns(b):
    gutter = 7 * mm
    col = (CW - gutter) / 2
    t = Table([[column(b["left"]), column(b["right"])]], colWidths=[col + gutter, col])
    t.setStyle(TableStyle(FLAT + [("RIGHTPADDING", (0, 0), (0, 0), gutter)]))
    return [t]


def block_callout(b):
    inner = h2(b["heading"])
    if b.get("intro"):
        inner += [p(b["intro"]), Spacer(0, 1.6 * mm)]
    inner.append(steps(b["items"]))
    if b.get("note"):
        inner += [Spacer(0, 1.6 * mm), p(b["note"], "note")]
    return [panel(inner, CW, bg=TINT, border=TINT, pad=3.4 * mm)]


def block_timeline(b):
    phases = b["phases"]
    n, gap = len(phases), 2.2 * mm
    pw = (CW - gap * (n - 1)) / n
    hl = b.get("highlight")
    cells, widths = [], []
    for i, (when, name, lines) in enumerate(phases):
        on = i == hl
        cells.append(panel([p(when, "phw"), p(name, "small"), Spacer(0, 1.6 * mm), p("<br/>".join(lines))],
                           pw, bg=TINT if on else None, border=ACCENT if on else RULE, line=1.2 if on else 0.6))
        widths.append(pw)
        if i < n - 1:
            cells.append("")
            widths.append(gap)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle(FLAT))
    return h2(b["heading"]) + [t]


def block_needs(b):
    t = Table([[p(f"<b>{b.get('label', 'What we need from you')}:</b> {b['text']}")]], colWidths=[CW])
    t.setStyle(TableStyle(FLAT + [("LINEABOVE", (0, 0), (-1, 0), 0.8, INK), ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm)]))
    return [t]


BLOCKS = {"table": block_table, "columns": block_columns, "callout": block_callout,
          "timeline": block_timeline, "needs": block_needs}


def build(c):
    left = [p(c["title"], "title")]
    if c.get("subtitle"):
        left += [Spacer(0, 1 * mm), p(c["subtitle"], "subtitle")]
    head = Table([[left, p("<br/>".join(c.get("byline", [])), "by")]], colWidths=[CW * 0.62, CW * 0.38])
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LINEBELOW", (0, 0), (-1, 0), 1.4, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    story = [head, Spacer(0, 3.5 * mm), p(c["lead"], "lead")]
    for b in c["blocks"]:
        story.append(Spacer(0, GAP))
        story += BLOCKS[b["type"]](b)
    return story


def footer(canvas, c):
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(M, 13 * mm, W - M, 13 * mm)
    canvas.setFont("Helvetica", 7.4)
    canvas.setFillColor(QUIET)
    canvas.drawString(M, 9 * mm, c.get("footer_left", ""))
    canvas.drawRightString(W - M, 9 * mm, c.get("footer_right", ""))


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    content = json.load(open(sys.argv[1], encoding="utf-8"))
    cv = Canvas(sys.argv[2], pagesize=A4, pageCompression=1)
    cv.setTitle(" — ".join(x for x in (content["title"], content.get("subtitle", "")) if x))
    cv.setAuthor(content.get("author", ""))
    frame = Frame(M, 16 * mm, CW, H - M - 16 * mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    # KeepInFrame in "error" mode raises instead of silently shrinking or dropping content.
    box = KeepInFrame(CW, frame._aH, build(content), mode="error")
    try:
        frame.addFromList([box], cv)
    except Exception as e:
        raise SystemExit(f"does not fit on one A4 page - cut the copy ({e})")
    footer(cv, content)
    cv.showPage()
    cv.save()
    print(sys.argv[2])


if __name__ == "__main__":
    main()
