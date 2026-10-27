#!/usr/bin/env python3
"""Render the client one-pager as a single A4 PDF.

    python one_pager.py content.json out.pdf

content.json holds the words; this script holds the layout. It uses the
standard Helvetica faces, which PDF readers carry themselves, so nothing is
embedded and the file stays a few KB: small enough to attach anywhere.
Exits non-zero if the content doesn't fit on one page, because a one-pager
that spills onto a second page is the thing it exists not to be.

See one_pager.example.json for every field.
"""
import json
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Frame, KeepInFrame, Paragraph, Spacer, Table, TableStyle

INK = colors.HexColor("#16181d")
QUIET = colors.HexColor("#5b616e")
RULE = colors.HexColor("#dfe2e8")
ACCENT = colors.HexColor("#1f6feb")
TINT = colors.HexColor("#eef4ff")
GREY = colors.HexColor("#f2f3f5")

W, H = A4
M = 15 * mm
CW = W - 2 * M  # content width


def style(name, size, lead=None, font="Helvetica", color=INK, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=lead or size * 1.38, textColor=color, **kw)


S = {
    "title": style("title", 20, 22, "Helvetica-Bold"),
    "by": style("by", 8.2, 11, color=QUIET, alignment=TA_RIGHT),
    "lead": style("lead", 10, 14),
    "h2": style("h2", 7.8, 10, "Helvetica-Bold", ACCENT),
    "th": style("th", 7.6, 10, "Helvetica-Bold", QUIET),
    "cell": style("cell", 8.4, 11.2),
    "cellb": style("cellb", 8.4, 11.2, "Helvetica-Bold"),
    "body": style("body", 8.6, 11.6),
    "note": style("note", 7.8, 10.4, color=QUIET),
    "small": style("small", 7.8, 10.2, color=QUIET),
    "smallb": style("smallb", 8.2, 10.4, "Helvetica-Bold"),
    "phw": style("phw", 9.6, 12, "Helvetica-Bold"),
    "foot": style("foot", 7.4, 9.5, color=QUIET),
}


def p(text, s="body"):
    return Paragraph(text, S[s])


def h2(text):
    return p(text.upper(), "h2")


def bullets(items):
    rows = [[p("•", "body"), p(t)] for t in items]
    t = Table(rows, colWidths=[3.2 * mm, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
    ]))
    return t


def steps(items):
    rows = [[p(f'<font color="#1f6feb"><b>{i}</b></font>'), p(f"<b>{name}</b>: {text}")] for i, (name, text) in enumerate(items, 1)]
    t = Table(rows, colWidths=[4.5 * mm, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
    ]))
    return t


def boxed(flowables, bg=None, border=RULE, width=None, pad=2.4 * mm, line=0.6):
    t = Table([[flowables]], colWidths=[width])
    cmds = [("BOX", (0, 0), (-1, -1), line, border),
            ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
            ("TOPPADDING", (0, 0), (-1, -1), pad * 0.8), ("BOTTOMPADDING", (0, 0), (-1, -1), pad * 0.8),
            ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if bg:
        cmds.append(("BACKGROUND", (0, 0), (-1, -1), bg))
    t.setStyle(TableStyle(cmds))
    return t


def build(c):
    story = []

    head = Table([[p(f'{c["title"]}<br/>{c["subtitle"]}', "title"), p("<br/>".join(c["byline"]), "by")]],
                 colWidths=[CW * 0.6, CW * 0.4])
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.4, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    story += [head, Spacer(0, 3.5 * mm), p(c["lead"], "lead"), Spacer(0, 4 * mm)]

    story.append(h2(c.get("services_heading", "What we can do")))
    rows = [[p(x, "th") for x in c.get("services_columns", ["Area", "What we do", "What you get"])]]
    rows += [[p(a, "cellb"), p(b, "cell"), p(g, "cell")] for a, b, g in c["services"]]
    t = Table(rows, colWidths=[26 * mm, (CW - 26 * mm) * 0.53, (CW - 26 * mm) * 0.47], repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
        ("TOPPADDING", (0, 1), (-1, -1), 1.4 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4 * mm),
    ]))
    story += [t, Spacer(0, 4.5 * mm)]

    col = (CW - 7 * mm) / 2
    left = [h2(c.get("results_heading", "Results it can yield")), Spacer(0, 1.4 * mm), bullets(c["results"])]
    if c.get("results_note"):
        left += [Spacer(0, 1.2 * mm), p(c["results_note"], "note")]
    if c.get("example"):
        left += [Spacer(0, 2 * mm), boxed([p(c["example"], "body")], bg=TINT, border=TINT, width=col)]
    right = [h2(c.get("approach_heading", "Approach")), Spacer(0, 1.4 * mm), steps(c["approach"])]
    if c.get("team"):
        tw = col / len(c["team"])
        cells = [[p(n, "smallb"), p(d, "small")] for n, d in c["team"]]
        team = Table([cells], colWidths=[tw] * len(cells))
        team.setStyle(TableStyle([
            ("BOX", (i, 0), (i, 0), 0.6, RULE) for i in range(len(cells))
        ] + [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
             ("TOPPADDING", (0, 0), (-1, -1), 1.4 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6 * mm)]))
        right += [Spacer(0, 2.2 * mm), team]
    if c.get("gate"):
        right += [Spacer(0, 1.6 * mm), boxed([p(f"<b>{c['gate']}</b>", "smallb")], bg=GREY, border=GREY, width=col, pad=1.8 * mm)]
    two = Table([[left, right]], colWidths=[col + 7 * mm, col])
    two.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 7 * mm),
                             ("RIGHTPADDING", (1, 0), (1, 0), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    story += [two, Spacer(0, 4.5 * mm)]

    story.append(h2(c.get("timeline_heading", "Timeline")))
    story.append(Spacer(0, 1.4 * mm))
    n = len(c["timeline"])
    gap = 2.2 * mm
    pw = (CW - gap * (n - 1)) / n
    hl = c.get("timeline_highlight")
    cells = []
    for i, (when, phase, items) in enumerate(c["timeline"]):
        cells.append(boxed([p(when, "phw"), p(phase, "small"), Spacer(0, 1.6 * mm), p("<br/>".join(items), "body")],
                           bg=TINT if i == hl else None, border=ACCENT if i == hl else RULE,
                           width=pw, line=1.2 if i == hl else 0.6))
        if i < n - 1:
            cells.append("")
    widths = []
    for i in range(n):
        widths.append(pw)
        if i < n - 1:
            widths.append(gap)
    tl = Table([cells], colWidths=widths)
    tl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    story += [tl, Spacer(0, 4.5 * mm)]

    needs = Table([[p(f"<b>{c.get('needs_label', 'What we need from you')}:</b> {c['needs']}", "body")]], colWidths=[CW])
    needs.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.8, INK),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm)]))
    story.append(needs)
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
    from reportlab.pdfgen.canvas import Canvas

    cv = Canvas(sys.argv[2], pagesize=A4, pageCompression=1)
    cv.setTitle(f'{content["title"]} — {content["subtitle"]}')
    cv.setAuthor(content.get("author", ""))
    frame = Frame(M, 16 * mm, CW, H - M - 16 * mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    story = build(content)
    # KeepInFrame in "error" mode raises instead of silently shrinking or dropping content.
    box = KeepInFrame(CW, frame._aH, story, mode="error")
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
