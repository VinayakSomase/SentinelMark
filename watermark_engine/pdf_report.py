from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import uuid
import os


# MAIN FUNCTION

def generate_evidence_report(asset_id, distributor_name,
                            registered_at, detected_at,
                            confidence, output_path):

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    elements = []

    # HEADER 
    elements.append(Paragraph("<b>SentinelMark</b>", styles['Title']))
    elements.append(Paragraph("Digital Piracy Intelligence System", styles['Normal']))
    elements.append(Spacer(1, 10))

    report_id = f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    elements.append(Paragraph(f"Report ID: <b>{report_id}</b>", styles['Normal']))
    elements.append(Spacer(1, 20))

    # TITLE 
    elements.append(Paragraph("<b>FORENSIC EVIDENCE REPORT</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # STATUS BADGE 
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

    # DATA TABLE 
    data = [
        ["Asset ID", asset_id],
        ["Leaked By", distributor_name],
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

    # CONFIDENCE
    elements.append(Paragraph(
        f"<b>Watermark Match Confidence:</b> {confidence}%",
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # LEGAL
    elements.append(Paragraph("<b>⚠ LEGAL WARNING</b>", styles['Heading3']))

    elements.append(Paragraph(
        "This report is generated using forensic watermarking techniques. "
        "Unauthorized redistribution of digital content is punishable by law.",
        styles['Normal']
    ))

    elements.append(Spacer(1, 30))

    # FOOTER
    elements.append(Paragraph(
        "© 2026 SentinelMark | Digital Content Protection System",
        styles['Normal']
    ))

    # BUILD PDF 
    doc.build(elements)

    print(f"🔥 PDF GENERATED: {output_path}")



# RUN TEST (AUTO GENERATE)

if __name__ == "__main__":

    print("CALLING FUNCTION...")

    #  Create unique filename
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    #  Save in same folder
    output_path = os.path.join(os.path.dirname(__file__), filename)

    generate_evidence_report(
        asset_id="ASSET-001",
        distributor_name="StarSports East",
        registered_at="2026-04-12 14:00",
        detected_at="2026-04-13 09:22",
        confidence=97.4,
        output_path=output_path
    )

