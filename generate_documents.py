"""PDF Generation Script for Kemet Studio / DHS Graduation Project
Generates three professional, publication-quality PDFs:
1. Project Planning.pdf
2. Stakeholder Analysis.pdf
3. UI_UX Design.pdf
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ----------------------------------------------------------------------
# Paths & Assets
# ----------------------------------------------------------------------
ROOT = Path(r"F:\My Work\DEPI R5\Grad Proj\Describing-hieroglyphic-Symbols-based-on-CV-and-NLP-Techniques")
ASSETS_DIR = ROOT / "docs_assets"

IMG_DETECTOR = ASSETS_DIR / "ui_visual_detector.png"
IMG_CHAT = ASSETS_DIR / "ui_scribe_chat.png"
IMG_EXPLORER = ASSETS_DIR / "ui_symbol_explorer.png"
IMG_VOICE = ASSETS_DIR / "ui_voice_studio.png"

# ----------------------------------------------------------------------
# Color Palette (Exact Match to Kemet Studio Front-End)
# ----------------------------------------------------------------------
C_NAVY = colors.HexColor("#0A2947")          # Deep Pharaoh / Lapis Blue
C_NAVY_DARK = colors.HexColor("#05192D")     # Midnight Pharaoh Blue
C_NAVY_SURFACE = colors.HexColor("#103357")  # Header / Accent Blue
C_PAPYRUS = colors.HexColor("#F3E4C9")       # Warm Papyrus / Sand Cream
C_PAPYRUS_LIGHT = colors.HexColor("#FBF5EB") # Card Background / Pristine Cream
C_PAPYRUS_CARD = colors.HexColor("#F9F0DF")  # Alternate row background
C_PAPYRUS_DARK = colors.HexColor("#E8D3B3")  # Papyrus border
C_LIMESTONE = colors.HexColor("#D3D4C0")     # Desert Sage / Muted Limestone
C_LIMESTONE_BORDER = colors.HexColor("#B8BA9F") # Subtle border
C_TERRACOTTA = colors.HexColor("#8B5E3C")    # Nile Terracotta / Cedar Bronze
C_TERRACOTTA_HOVER = colors.HexColor("#754F32")
C_WHITE = colors.HexColor("#FFFFFF")
C_TEXT_DARK = colors.HexColor("#0A2947")
C_TEXT_MUTED = colors.HexColor("#4B5E71")
C_TEXT_BODY = colors.HexColor("#1A2530")
C_GREEN = colors.HexColor("#1E7E34")
C_GOLD = colors.HexColor("#C5A059")

PAGE_W, PAGE_H = A4
MARGIN_L = 36
MARGIN_R = 36
MARGIN_T = 44
MARGIN_B = 44
USABLE_W = PAGE_W - (MARGIN_L + MARGIN_R)  # 523.27 pt


# ----------------------------------------------------------------------
# Numbered Canvas for Two-Pass Headers and Footers
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        page_num = self._pageNumber
        doc_title = getattr(self, "doc_title", "Kemet Studio Documentation")
        doc_category = getattr(self, "doc_category", "DEPI R5 Project Specification")

        # Top Running Header (Pages 2+)
        if page_num > 1:
            self.saveState()
            # Top Navy Banner Bar
            self.setFillColor(C_NAVY)
            self.rect(MARGIN_L, PAGE_H - 32, USABLE_W, 16, fill=1, stroke=0)
            # Gold Accent Line
            self.setFillColor(C_TERRACOTTA)
            self.rect(MARGIN_L, PAGE_H - 33, USABLE_W, 1.5, fill=1, stroke=0)

            # Left running title
            self.setFillColor(C_PAPYRUS)
            self.setFont("Helvetica-Bold", 7.5)
            self.drawString(MARGIN_L + 8, PAGE_H - 24, "KEMET STUDIO  •  HIEROGLYPH CV & NLP ASSISTANT")

            # Right running document type
            self.setFillColor(C_LIMESTONE)
            self.setFont("Helvetica", 7.5)
            self.drawRightString(PAGE_W - MARGIN_R - 8, PAGE_H - 24, doc_category.upper())
            self.restoreState()

        # Bottom Running Footer (All Pages)
        self.saveState()
        # Footer dividing line
        self.setStrokeColor(C_LIMESTONE_BORDER)
        self.setLineWidth(0.75)
        self.line(MARGIN_L, 30, PAGE_W - MARGIN_R, 30)

        # Footer Left: Project and Program metadata
        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(C_NAVY)
        self.drawString(MARGIN_L, 20, "DEPI Round 5  |  Delta University for Science & Technology")
        self.setFont("Helvetica", 7)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(MARGIN_L, 11, "Supervised by Prof. Dr. Hisham Arafat Ali  •  Graduation Project 2024–2025")

        # Footer Center: Document classification
        self.setFont("Helvetica-Oblique", 7)
        self.setFillColor(C_TERRACOTTA)
        self.drawCentredString(PAGE_W / 2.0, 16, "Official Project Documentation  •  All Rights Reserved")

        # Footer Right: Page Count
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(C_NAVY)
        self.drawRightString(PAGE_W - MARGIN_R, 16, f"Page {page_num} of {total_pages}")
        self.restoreState()


# ----------------------------------------------------------------------
# Typography & Styles Factory
# ----------------------------------------------------------------------
def build_stylesheet():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverDocType",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=C_TERRACOTTA,
        alignment=0,
        spaceAfter=3,
        textTransform="uppercase",
    ))

    styles.add(ParagraphStyle(
        "CoverMainTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=C_NAVY,
        alignment=0,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        "CoverSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=C_NAVY_SURFACE,
        alignment=0,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=C_TEXT_DARK,
    ))

    styles.add(ParagraphStyle(
        "CoverMetaBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11.5,
        textColor=C_NAVY,
    ))

    styles.add(ParagraphStyle(
        "SectionHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=C_NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        "SubSectionHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=C_TERRACOTTA,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT_BODY,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=C_NAVY,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.5,
        textColor=C_TEXT_BODY,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5,
    ))

    styles.add(ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.5,
        textColor=C_NAVY,
    ))

    styles.add(ParagraphStyle(
        "CalloutBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=C_TERRACOTTA,
    ))

    styles.add(ParagraphStyle(
        "TH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=C_WHITE,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        "TD",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=C_TEXT_BODY,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        "TDBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=C_NAVY,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        "TDMuted",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9.5,
        textColor=C_TEXT_MUTED,
        alignment=0,
    ))

    styles.add(ParagraphStyle(
        "FigureCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=C_TERRACOTTA,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5,
    ))

    return styles


# ----------------------------------------------------------------------
# Reusable Flowable Helpers
# ----------------------------------------------------------------------
def create_cover_banner(doc_type: str, title: str, subtitle: str, meta_items: list[tuple[str, str]], styles):
    """Generates an executive header card styled with the Kemet Studio palette."""
    elements = []

    # Outer container table for the banner
    top_p = Paragraph(f"<b>{doc_type.upper()}</b>", styles["CoverDocType"])
    title_p = Paragraph(title, styles["CoverMainTitle"])
    subtitle_p = Paragraph(subtitle, styles["CoverSubTitle"])

    # Metadata formatted into a 2-column or 4-column grid
    meta_cells = []
    for label, val in meta_items:
        meta_cells.append([
            Paragraph(f"<b>{label}:</b>", styles["CoverMetaBold"]),
            Paragraph(val, styles["CoverMeta"])
        ])

    meta_table = Table(
        meta_cells,
        colWidths=[100, USABLE_W - 100 - 18],
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]
    )

    banner_content = [[
        top_p,
    ], [
        title_p,
    ], [
        subtitle_p,
    ], [
        HRFlowable(width="100%", thickness=1.5, color=C_TERRACOTTA, spaceBefore=2, spaceAfter=5),
    ], [
        meta_table,
    ]]

    banner_table = Table(
        banner_content,
        colWidths=[USABLE_W],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), C_PAPYRUS_LIGHT),
            ("BOX", (0, 0), (-1, -1), 1.2, C_LIMESTONE_BORDER),
            ("LINEBEFORE", (0, 0), (-1, -1), 4.0, C_NAVY),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ]
    )

    elements.append(banner_table)
    elements.append(Spacer(1, 10))
    return elements


def create_section_header(title: str, styles):
    """Renders a section title with a colored terracotta accent bar."""
    p = Paragraph(title, styles["SectionHeader"])
    hr = HRFlowable(width="100%", thickness=1.2, color=C_TERRACOTTA, spaceBefore=1, spaceAfter=6)
    return KeepTogether([p, hr])


def create_callout_box(title: str, text: str, styles, accent_color=C_TERRACOTTA):
    """Renders an informational highlight card."""
    content = [
        Paragraph(f"<b>{title.upper()}</b>", styles["CalloutBold"]),
        Spacer(1, 2),
        Paragraph(text, styles["CalloutText"])
    ]
    box = Table(
        [[content]],
        colWidths=[USABLE_W],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), C_PAPYRUS_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.8, C_LIMESTONE_BORDER),
            ("LINEBEFORE", (0, 0), (-1, -1), 3.5, accent_color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )
    return box


def style_table(headers: list[str], rows: list[list[str]], col_widths: list[float], styles, zebra=True):
    """Formats a clean tabular data view with Pharaoh Navy header and Papyrus alternate rows."""
    table_data = []

    # Format header cells
    head_row = [Paragraph(f"<b>{h}</b>", styles["TH"]) for h in headers]
    table_data.append(head_row)

    # Format body cells
    for r_idx, row in enumerate(rows):
        formatted_row = []
        for c_idx, cell in enumerate(row):
            # Check if cell has strong emphasis
            if cell.startswith("[B]"):
                formatted_row.append(Paragraph(cell[3:], styles["TDBold"]))
            elif cell.startswith("[M]"):
                formatted_row.append(Paragraph(cell[3:], styles["TDMuted"]))
            else:
                formatted_row.append(Paragraph(cell, styles["TD"]))
        table_data.append(formatted_row)

    t_style = [
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, C_LIMESTONE_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]

    if zebra:
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                t_style.append(("BACKGROUND", (0, i), (-1, i), C_PAPYRUS_CARD))
            else:
                t_style.append(("BACKGROUND", (0, i), (-1, i), C_WHITE))

    t = Table(table_data, colWidths=col_widths, style=t_style)
    return t


print("Helper functions and styling definitions initialized successfully.")
