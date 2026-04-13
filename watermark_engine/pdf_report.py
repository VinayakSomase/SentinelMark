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

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import uuid

def generate_evidence_report(asset_id, distributor_name,
                            registered_at, detected_at,
                            confidence, output_path):

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # ===== UNIQUE REPORT ID =====
    report_id = str(uuid.uuid4())[:8].upper()

    # ===== HEADER =====
    c.setFillColorRGB(0.07, 0.12, 0.22)
    c.rect(0, height - 100, width, 100, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, height - 55, "SentinelMark")

    c.setFont("Helvetica", 13)
    c.drawString(40, height - 75, "Digital Piracy Intelligence System")

    # Report ID (top right)
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 40, height - 50, f"Report ID: {report_id}")

    # ===== TITLE =====
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 140, "Forensic Evidence Report")

    # ===== STATUS BADGE =====
    c.setFillColorRGB(0.85, 0.15, 0.15)
    c.roundRect(width - 180, height - 160, 130, 30, 10, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width - 115, height - 140, "LEAK DETECTED")

    # ===== MAIN CARD =====
    c.setFillColorRGB(0.96, 0.97, 0.98)
    c.roundRect(30, height - 430, width - 60, 260, 12, fill=1)

    # ===== DATA =====
    data = [
        ("Asset ID", asset_id),
        ("Leaked By", distributor_name),
        ("Registered At", registered_at),
        ("Detected At", detected_at),
        ("Confidence", f"{confidence}%"),
        ("Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ]

    y = height - 190

    for label, value in data:
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.setFont("Helvetica", 11)
        c.drawString(50, y, label)

        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.setFont("Helvetica-Bold", 13)
        c.drawRightString(width - 50, y, value)

        # divider line
        c.setStrokeColorRGB(0.85, 0.85, 0.85)
        c.setLineWidth(1)
        c.line(50, y - 10, width - 50, y - 10)

        y -= 35

    # ===== CONFIDENCE BAR =====
    bar_x = 50
    bar_y = height - 460
    bar_width = width - 100
    bar_height = 20

    # background
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.roundRect(bar_x, bar_y, bar_width, bar_height, 10, fill=1)

    # fill (based on confidence)
    fill_width = (confidence / 100) * bar_width
    c.setFillColorRGB(0.2, 0.7, 0.3)
    c.roundRect(bar_x, bar_y, fill_width, bar_height, 10, fill=1)

    # text
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, bar_y + 5,
                        f"Watermark Match Confidence: {confidence}%")

    # ===== LEGAL WARNING BOX =====
    c.setFillColorRGB(0.9, 0.2, 0.2)
    c.roundRect(30, 120, width - 60, 60, 10, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 155, "⚠ LEGAL WARNING")

    c.setFont("Helvetica", 10)
    c.drawString(50, 140,
        "This report is generated using forensic watermark analysis.")
    c.drawString(50, 125,
        "Unauthorized redistribution of content is legally punishable.")

    # ===== FOOTER =====
    c.setFillColorRGB(0.07, 0.12, 0.22)
    c.rect(0, 0, width, 50, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, 20,
        "© 2026 SentinelMark | Secure Digital Content Tracking System")

    c.save()
    print(f"Premium PDF saved: {output_path}")


# ===== TEST RUN =====
if __name__ == "__main__":
    generate_evidence_report(
        asset_id="ASSET-001",
        distributor_name="StarSports East",
        registered_at="2026-04-12 14:00",
        detected_at="2026-04-13 09:22",
        confidence=97.4,
        output_path="premium_evidence_report.pdf"
    )

    