from reportlab.pdfgen import canvas

print("STARTING PDF TEST")

c = canvas.Canvas("check.pdf")
c.drawString(100, 750, "Hello PDF")
c.save()

print("PDF CREATED SUCCESSFULLY")
