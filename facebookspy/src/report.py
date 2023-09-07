from .ai import format_person_data
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rich import print as rprint


def generate_pdf_report(person_id: str) -> None:
    """
    Generate and save PDF file with scraped data for the specified person.
    """

    rprint(
        f"[bold green]Start generating a report for person: {person_id}[/bold green]"
    )
    rprint("[bold]Step 1 of 3 - Extract data from models[/bold]")

    # Get formatet data
    data = format_person_data(person_id)

    # Add custom font to the PDF file
    pdfmetrics.registerFont(TTFont("Basica-UnicodeRegular", "font.ttf"))

    doc = SimpleDocTemplate(f"{person_id}_report.pdf", pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]

    person_personal_info = [
        f"AI Summary: {data[0].ai_summary}",
        f"Full Name: {data[0].full_name}",
        f"Email: {data[0].email}",
        f"Phone Number: {data[0].phone_number}",
    ]

    rprint("[bold]Step 2 of 3 - Adding data to the PDF file [/bold]")

    # Implement data to the PDF file
    main_info_text = "<br/>".join(person_personal_info)
    story.append(Paragraph("Main User Information", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(main_info_text, styles["Normal"]))
    story.append(PageBreak())

    headings = [
        "Events",
        "Family Members",
        "Groups",
        "Likes",
        "Places",
        "Posts",
        "Recent Places",
        "Reviews",
        "Work and Education",
    ]
    for heading, content in zip(headings, data[1:]):
        content_with_line_breaks = "<br/>".join(content.split("\n"))
        story.append(Paragraph(heading, heading_style))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(content_with_line_breaks, styles["Normal"]))

    rprint("[bold]Step 3 of 3 - Saving the PDF file[/bold]")

    # Save the PDF file
    doc.build(story)
