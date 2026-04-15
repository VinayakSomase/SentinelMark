# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from datetime import datetime

# def generate_evidence_report(asset_id, distributor_name,
#                               registered_at, detected_at,
#                               confidence, output_path):
#     c = canvas.Canvas(output_path, pagesize=letter)

#     # Header bar
#     c.setFillColorRGB(0.06, 0.09, 0.16)
#     c.rect(0, 720, 612, 120, fill=1, stroke=0)

#     c.setFillColorRGB(1, 1, 1)
#     c.setFont("Helvetica-Bold", 22)
#     c.drawString(40, 790, "SentinelMark")
#     c.setFont("Helvetica", 12)
#     c.drawString(40, 765, "Forensic Evidence Report")

#     # Content
#     c.setFillColorRGB(0.1, 0.1, 0.1)
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(40, 690, "Leak Source Identified")

#     c.setFont("Helvetica", 12)
#     fields = [
#         ("Asset ID", asset_id),
#         ("Leaked by", distributor_name),
#         ("Asset Registered", registered_at),
#         ("Leak Detected", detected_at),
#         ("Watermark Confidence", f"{confidence}%"),
#         ("Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#     ]
#     y = 660
#     for label, value in fields:
#         c.setFillColorRGB(0.4, 0.4, 0.4)
#         c.drawString(40, y, label + ":")
#         c.setFillColorRGB(0.1, 0.1, 0.1)
#         c.setFont("Helvetica-Bold", 12)
#         c.drawString(200, y, value)
#         c.setFont("Helvetica", 12)
#         y -= 30

#     # Legal note
#     c.setFillColorRGB(0.8, 0.2, 0.2)
#     c.rect(40, y-20, 530, 50, fill=1, stroke=0)
#     c.setFillColorRGB(1, 1, 1)
#     c.setFont("Helvetica", 11)
#     c.drawString(50, y+20, "This document constitutes forensic evidence of")
#     c.drawString(50, y+5, "unauthorized content redistribution.")

#     c.save()
#     print(f"PDF saved: {output_path}")

# if __name__ == "__main__":
#     generate_evidence_report(
#         asset_id="ASSET-001",
#         distributor_name="StarSports East",
#         registered_at="2026-04-12 14:00",
#         detected_at="2026-04-13 09:22",
#         confidence=97.4,
#         output_path="evidence_report.pdf"
#     )
#     print("Open evidence_report.pdf in your folder to check it")

print("RUNNING PDF FILE...")

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import uuid
import os

# ===============================
# MAIN FUNCTION
# ===============================
def generate_evidence_report(asset_id, distributor_name,
                            registered_at, detected_at,
                            confidence, output_path):

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    elements = []

    # ===== HEADER =====
    elements.append(Paragraph("<b>SentinelMark</b>", styles['Title']))
    elements.append(Paragraph("Digital Piracy Intelligence System", styles['Normal']))
    elements.append(Spacer(1, 10))

    report_id = str(uuid.uuid4())[:8].upper()
    elements.append(Paragraph(f"Report ID: <b>{report_id}</b>", styles['Normal']))
    elements.append(Spacer(1, 20))

    # ===== TITLE =====
    elements.append(Paragraph("<b>FORENSIC EVIDENCE REPORT</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # ===== STATUS BADGE =====
    status = Paragraph(
        "<font color='white'><b> LEAK CONFIRMED </b></font>",
        styles['Normal']
    )

    status_table = Table([[status]])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.darkred),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(status_table)
    elements.append(Spacer(1, 20))

    # ===== DATA TABLE =====
    data = [
        ["Asset ID", asset_id],
        ["Leaked By", f"<b>{distributor_name}</b>"],
        ["Registered At", registered_at],
        ["Detected At", detected_at],
        ["Confidence", f"{confidence}%"],
        ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    table = Table(data, colWidths=[150, 300])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ===== CONFIDENCE =====
    elements.append(Paragraph(
        f"<b>Watermark Match Confidence:</b> {confidence}%",
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # ===== LEGAL =====
    elements.append(Paragraph("<b>⚠ LEGAL WARNING</b>", styles['Heading3']))

    elements.append(Paragraph(
        "This report is generated using forensic watermarking techniques. "
        "Unauthorized redistribution of digital content is punishable by law.",
        styles['Normal']
    ))

    elements.append(Spacer(1, 30))

    # ===== FOOTER =====
    elements.append(Paragraph(
        "© 2026 SentinelMark | Digital Content Protection System",
        styles['Normal']
    ))

    # ===== BUILD PDF =====
    doc.build(elements)

    print(f"🔥 PDF GENERATED: {output_path}")


# ===============================
# RUN TEST (AUTO GENERATE)
# ===============================
if __name__ == "__main__":

    print("CALLING FUNCTION...")

    # ✅ Create unique filename
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # ✅ Save in same folder
    output_path = os.path.join(os.path.dirname(__file__), filename)

    generate_evidence_report(
        asset_id="ASSET-001",
        distributor_name="StarSports East",
        registered_at="2026-04-12 14:00",
        detected_at="2026-04-13 09:22",
        confidence=97.4,
        output_path=output_path
    )