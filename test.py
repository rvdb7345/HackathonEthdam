from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF
import numpy as np


# Create a function to generate a line plot
def generate_line_plot():
    data = np.random.randint(1, 10, (5, 5))
    drawing = Drawing(400, 200)
    lp = LinePlot()
    lp.x = 50
    lp.y = 50
    lp.height = 125
    lp.width = 300
    lp.data = data
    lp.lines.strokeWidth = 1
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = 5
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 10

    legend = Legend()
    legend.x = 200
    legend.y = 150
    legend.dxTextSpace = 5
    legend.columnMaximum = 1
    legend.yGap = 0
    legend.colorNamePairs = [
        (lp.lines[0], "Line 1"),
        (lp.lines[1], "Line 2"),
        (lp.lines[2], "Line 3"),
        (lp.lines[3], "Line 4"),
        (lp.lines[4], "Line 5"),
    ]

    drawing.add(lp)
    drawing.add(legend)

    return drawing


# Create a function to generate the PDF
def generate_pdf():
    doc = SimpleDocTemplate("dashboard.pdf", pagesize=letter)

    # Create elements for the PDF
    elements = []

    # Add a title
    title = Paragraph(
        "PDF Dashboard", fontName="Helvetica-Bold", fontSize=20, alignment=1
    )
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Add text content
    text = "This is a sample PDF dashboard created using Python and ReportLab."
    paragraph = Paragraph(text, fontName="Helvetica", fontSize=12)
    elements.append(paragraph)
    elements.append(Spacer(1, 20))

    # Add the line plot
    line_plot = generate_line_plot()
    elements.append(line_plot)
    elements.append(Spacer(1, 20))

    # Create a table
    data = [
        ["Name", "Age", "Country"],
        ["John", "25", "USA"],
        ["Emily", "30", "Canada"],
        ["Michael", "35", "UK"],
    ]
    table = Table(
        data,
        style=[
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ],
    )
    elements.append(table)

    # Build the PDF document
    doc.build(elements)


# Generate the PDF
generate_pdf()
