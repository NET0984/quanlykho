from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PdfTableMixin:
    def build_pdf_table(self, title, headers, rows, meta=None):
        output = BytesIO()
        doc = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            leftMargin=20,
            rightMargin=20,
            topMargin=20,
            bottomMargin=20,
        )

        styles = getSampleStyleSheet()
        story = [Paragraph(title, styles['Heading1'])]

        for line in (meta or []):
            story.append(Paragraph(line, styles['Normal']))

        story.append(Spacer(1, 10))

        table_data = [headers] + rows
        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E78')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D9D9D9')),
            ])
        )
        story.append(table)

        doc.build(story)
        return output.getvalue()
