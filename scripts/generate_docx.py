"""Generate a formatted DOCX from FabricPlanningDemoScenario.txt"""

import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "FabricPlanningDemoScenario.txt"
DST = REPO_ROOT / "FabricPlanningDemoScenario.docx"

doc = Document()

# --- styles -----------------------------------------------------------
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.space_before = Pt(0)

for level in range(1, 4):
    hs = doc.styles[f"Heading {level}"]
    hs.font.name = "Calibri"
    hs.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

# custom style for "Co mówisz" narrative blocks
if "Narrative" not in [s.name for s in doc.styles]:
    ns = doc.styles.add_style("Narrative", WD_STYLE_TYPE.PARAGRAPH)
    ns.font.name = "Calibri"
    ns.font.size = Pt(11)
    ns.font.italic = True
    ns.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    ns.paragraph_format.left_indent = Inches(0.3)
    ns.paragraph_format.space_before = Pt(4)
    ns.paragraph_format.space_after = Pt(8)

# custom style for important notes
if "ImportantNote" not in [s.name for s in doc.styles]:
    ins = doc.styles.add_style("ImportantNote", WD_STYLE_TYPE.PARAGRAPH)
    ins.font.name = "Calibri"
    ins.font.size = Pt(11)
    ins.font.bold = True
    ins.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
    ins.paragraph_format.left_indent = Inches(0.3)
    ins.paragraph_format.space_before = Pt(4)
    ins.paragraph_format.space_after = Pt(4)

# --- read source -------------------------------------------------------
text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

# --- parse & emit ------------------------------------------------------
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # skip blank lines
    if not stripped:
        i += 1
        continue

    # ===== title (first line with ===== underline)
    if i + 1 < len(lines) and lines[i + 1].strip().startswith("===="):
        doc.add_heading(stripped, level=0)
        i += 2
        continue

    # ----- section headers  (numbered: "1. CEL DEMO" etc.)
    if i + 1 < len(lines) and lines[i + 1].strip().startswith("----"):
        # detect heading level from numbering
        m = re.match(r"^(\d+)\.\s+(.+)", stripped)
        if m:
            doc.add_heading(f"{m.group(1)}. {m.group(2)}", level=1)
        else:
            doc.add_heading(stripped, level=1)
        i += 2
        continue

    # ETAP N. headers
    m_etap = re.match(r"^(ETAP\s+\d+)\.\s+(.+)", stripped)
    if m_etap:
        doc.add_heading(f"{m_etap.group(1)}. {m_etap.group(2)}", level=2)
        i += 1
        continue

    # Sub-headers like "Opcja A:", "Krok po kroku:", "Przekaz:", etc.
    if stripped.endswith(":") and len(stripped) < 80 and not stripped[0].isdigit() and not stripped.startswith("-"):
        if any(kw in stripped.lower() for kw in [
            "opcja", "krok po kroku", "przekaz", "co mówisz", "co pokazujesz",
            "cel tego kroku", "scenariusz narracyjny", "finał narracji",
            "dlaczego to działa", "uwaga"
        ]):
            doc.add_heading(stripped, level=3)
            i += 1
            continue

    # Narrative quotes (lines starting with ")
    if stripped.startswith('"') and stripped.endswith('"'):
        doc.add_paragraph(stripped, style="Narrative")
        i += 1
        continue

    # Important notes (NIE, UWAGA lines)
    if stripped.startswith("NIE ") or stripped.startswith("Uwaga:") or \
       stripped.startswith("Planning sheet NIE"):
        doc.add_paragraph(stripped, style="ImportantNote")
        i += 1
        continue

    # Bullet points
    if stripped.startswith("- "):
        doc.add_paragraph(stripped[2:], style="List Bullet")
        i += 1
        continue

    # Numbered steps (1. or 1) or a. or a) patterns)
    m_num = re.match(r"^(\d+[\.\)])\s+(.+)", stripped)
    m_let = re.match(r"^([a-z][\.\)])\s+(.+)", stripped)
    if m_num:
        doc.add_paragraph(stripped, style="List Number")
        i += 1
        continue
    if m_let:
        p = doc.add_paragraph(stripped, style="List Bullet 2")
        i += 1
        continue

    # Indented continuation (lines starting with spaces, like sub-items)
    if line.startswith("   "):
        # sub-bullet
        if stripped.startswith("- "):
            doc.add_paragraph(stripped[2:], style="List Bullet 2")
        elif re.match(r"^[a-z][\.\)]", stripped):
            doc.add_paragraph(stripped, style="List Bullet 2")
        else:
            doc.add_paragraph(stripped, style="List Bullet 2")
        i += 1
        continue

    # Default: normal paragraph
    doc.add_paragraph(stripped)
    i += 1

# --- save ---------------------------------------------------------------
doc.save(str(DST))
print(f"Created: {DST}")
print(f"Size: {DST.stat().st_size:,} bytes")
