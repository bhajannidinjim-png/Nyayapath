"""
pdf_exporter.py
---------------
Generates a formatted PDF report of verified actions from NyayPath.
Uses reportlab only — no paid APIs, no external services.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from datetime import datetime


# ─────────────────────────────────────────────
# COLOR PALETTE (government-friendly blues)
# ─────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a3557")
MID_BLUE    = colors.HexColor("#2e6da4")
LIGHT_BLUE  = colors.HexColor("#dce9f5")
RED_ALERT   = colors.HexColor("#c0392b")
ORANGE      = colors.HexColor("#d35400")
GREEN       = colors.HexColor("#1e8449")
LIGHT_GRAY  = colors.HexColor("#f4f6f7")
MID_GRAY    = colors.HexColor("#aab7b8")
WHITE       = colors.white
BLACK       = colors.black


def build_styles():
    """Return a dict of named Paragraph styles used throughout the report."""
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        fontSize=26,
        textColor=WHITE,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        spaceAfter=6,
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle",
        fontSize=13,
        textColor=LIGHT_BLUE,
        alignment=TA_CENTER,
        fontName="Helvetica",
        spaceAfter=4,
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading",
        fontSize=13,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
        leftIndent=8,
    )
    styles["field_label"] = ParagraphStyle(
        "field_label",
        fontSize=9,
        textColor=MID_BLUE,
        fontName="Helvetica-Bold",
        spaceAfter=1,
    )
    styles["field_value"] = ParagraphStyle(
        "field_value",
        fontSize=10,
        textColor=BLACK,
        fontName="Helvetica",
        spaceAfter=4,
    )
    styles["action_text"] = ParagraphStyle(
        "action_text",
        fontSize=9,
        textColor=BLACK,
        fontName="Helvetica",
        leading=13,
        spaceAfter=3,
    )
    styles["source_text"] = ParagraphStyle(
        "source_text",
        fontSize=8,
        textColor=colors.HexColor("#5d6d7e"),
        fontName="Helvetica-Oblique",
        leading=11,
        leftIndent=8,
        spaceAfter=2,
    )
    styles["footer"] = ParagraphStyle(
        "footer",
        fontSize=8,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        fontName="Helvetica",
    )
    styles["priority_high"] = ParagraphStyle(
        "priority_high",
        fontSize=9,
        textColor=RED_ALERT,
        fontName="Helvetica-Bold",
    )
    styles["priority_medium"] = ParagraphStyle(
        "priority_medium",
        fontSize=9,
        textColor=ORANGE,
        fontName="Helvetica-Bold",
    )
    styles["priority_low"] = ParagraphStyle(
        "priority_low",
        fontSize=9,
        textColor=GREEN,
        fontName="Helvetica-Bold",
    )
    styles["normal"] = base["Normal"]

    return styles


def section_header(title: str, styles: dict):
    """Returns a blue header bar as a Table (used as section divider)."""
    tbl = Table(
        [[Paragraph(title, styles["section_heading"])]],
        colWidths=["100%"]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    return tbl


def priority_style(priority: str, styles: dict):
    """Return the correct style for a priority label."""
    return {
        "High":   styles["priority_high"],
        "Medium": styles["priority_medium"],
        "Low":    styles["priority_low"],
    }.get(priority, styles["action_text"])


def generate_pdf_report(metadata: dict, verified_actions: list) -> bytes:
    """
    Generate a formatted A4 PDF compliance report.

    Args:
        metadata       : dict from extract_case_metadata()
        verified_actions: list of approved+edited action dicts

    Returns:
        PDF as raw bytes (for Streamlit download_button)
    """
    buffer = io.BytesIO()
    styles = build_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        title="NyayPath Compliance Report",
        author="NyayPath AI System",
    )

    story = []  # List of flowables to render
    W = A4[0] - 4*cm  # Usable width

    # ─────────────────────────────────────────
    # COVER BANNER
    # ─────────────────────────────────────────
    cover = Table(
        [
            [Paragraph("⚖ NyayPath", styles["cover_title"])],
            [Paragraph("Court Judgment Compliance Report", styles["cover_subtitle"])],
            [Paragraph(
                f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
                styles["cover_subtitle"]
            )],
        ],
        colWidths=[W]
    )
    cover.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(cover)
    story.append(Spacer(1, 0.5*cm))

    # ─────────────────────────────────────────
    # CASE INFORMATION SECTION
    # ─────────────────────────────────────────
    story.append(section_header("📋  CASE INFORMATION", styles))
    story.append(Spacer(1, 0.2*cm))

    case_fields = [
        ("Court Name",      metadata.get("court_name", "Not identified")),
        ("Case Title",      metadata.get("case_title", "Not identified")),
        ("Judgment Date",   metadata.get("judgment_date", "Not identified")),
        ("Petitioner",      metadata.get("petitioner", "Not identified")),
        ("Respondent",      metadata.get("respondent", "Not identified")),
    ]

    # Two-column metadata table
    rows = []
    for i in range(0, len(case_fields), 2):
        left  = case_fields[i]
        right = case_fields[i+1] if i+1 < len(case_fields) else ("", "")
        rows.append([
            Paragraph(left[0],  styles["field_label"]),
            Paragraph(left[1],  styles["field_value"]),
            Paragraph(right[0], styles["field_label"]),
            Paragraph(right[1], styles["field_value"]),
        ])

    meta_table = Table(rows, colWidths=[3*cm, W/2 - 3.5*cm, 3*cm, W/2 - 3.5*cm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("GRID",          (0, 0), (-1, -1), 0.3, MID_GRAY),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.4*cm))

    # ─────────────────────────────────────────
    # SUMMARY STATISTICS
    # ─────────────────────────────────────────
    story.append(section_header("📊  VERIFICATION SUMMARY", styles))
    story.append(Spacer(1, 0.2*cm))

    high   = sum(1 for a in verified_actions if a.get("priority") == "High")
    medium = sum(1 for a in verified_actions if a.get("priority") == "Medium")
    low    = sum(1 for a in verified_actions if a.get("priority") == "Low")

    stat_data = [
        [
            Paragraph("Total Verified Actions", styles["field_label"]),
            Paragraph("🔴 High Priority",        styles["field_label"]),
            Paragraph("🟡 Medium Priority",       styles["field_label"]),
            Paragraph("🟢 Low Priority",          styles["field_label"]),
        ],
        [
            Paragraph(str(len(verified_actions)), styles["field_value"]),
            Paragraph(str(high),   styles["priority_high"]),
            Paragraph(str(medium), styles["priority_medium"]),
            Paragraph(str(low),    styles["priority_low"]),
        ]
    ]
    stat_table = Table(stat_data, colWidths=[W/4]*4)
    stat_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), LIGHT_BLUE),
        ("BACKGROUND",    (0, 1), (-1, 1), WHITE),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("GRID",          (0, 0), (-1, -1), 0.5, MID_GRAY),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 0.5*cm))

    # ─────────────────────────────────────────
    # VERIFIED ACTION ITEMS
    # ─────────────────────────────────────────
    story.append(section_header("✅  VERIFIED ACTION ITEMS", styles))
    story.append(Spacer(1, 0.3*cm))

    if not verified_actions:
        story.append(Paragraph("No verified actions to display.", styles["action_text"]))
    else:
        for idx, action in enumerate(verified_actions, start=1):
            priority  = action.get("priority", "Medium")
            pstyle    = priority_style(priority, styles)

            # Action number header row
            header_row = Table(
                [[
                    Paragraph(f"Action #{idx}", styles["field_label"]),
                    Paragraph(priority, pstyle),
                    Paragraph(
                        f"Confidence: {action.get('confidence', 'Medium')}",
                        styles["field_label"]
                    ),
                ]],
                colWidths=[3*cm, 3*cm, W - 6*cm]
            )
            header_row.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BLUE),
                ("TOPPADDING",    (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                ("ALIGN",         (1, 0), (1, 0), "CENTER"),
            ]))

            # Detail rows
            detail_data = [
                [
                    Paragraph("Directive / Action", styles["field_label"]),
                    Paragraph(action.get("action", ""), styles["action_text"]),
                ],
                [
                    Paragraph("Responsible Dept.", styles["field_label"]),
                    Paragraph(action.get("department", "Not Specified"), styles["field_value"]),
                ],
                [
                    Paragraph("Deadline", styles["field_label"]),
                    Paragraph(action.get("deadline", "Not specified"), styles["field_value"]),
                ],
                [
                    Paragraph("Source Reference", styles["field_label"]),
                    Paragraph(
                        action.get("source_text", "")[:180] + "...",
                        styles["source_text"]
                    ),
                ],
            ]
            detail_table = Table(detail_data, colWidths=[3.5*cm, W - 3.5*cm])
            detail_table.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (0, -1), LIGHT_GRAY),
                ("BACKGROUND",    (1, 0), (1, -1), WHITE),
                ("TOPPADDING",    (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
                ("GRID",          (0, 0), (-1, -1), 0.3, MID_GRAY),
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ]))

            # Keep header + detail together on same page
            story.append(KeepTogether([header_row, detail_table]))
            story.append(Spacer(1, 0.35*cm))

    # ─────────────────────────────────────────
    # FOOTER NOTE
    # ─────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GRAY))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "This report was generated by NyayPath AI — Court Judgment Compliance System. "
        "All actions have been verified by a human officer before export. "
        "This document is for official compliance tracking purposes only.",
        styles["footer"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
