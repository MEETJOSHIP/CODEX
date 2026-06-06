from reportlab.pdfgen import canvas

def generate_invoice_pdf(invoice):
    
    filename = (
        f"media/invoices/"
        f"{invoice.invoice_number}.pdf"
    )

    pdf = canvas.Canvas(filename)

    pdf.drawString(
        100,
        750,
        f"Invoice {invoice.invoice_number}"
    )

    pdf.drawString(
        100,
        720,
        f"Total ₹{invoice.total_amount}"
    )

    pdf.save()

    return filename