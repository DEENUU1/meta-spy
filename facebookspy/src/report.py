from .ai import format_person_data
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from rich import print as rprint


def generate_pdf_report(person_id: str) -> None:
    """
    Generate and save PDF file with scraped data for specified person.
    """

    rprint(f"[bold green]Start generating report for person: {person_id}[/bold green]")
    rprint("[bold]Step 1 of 3 - Extract data from models[/bold]")
    data = format_person_data(person_id)
    doc = SimpleDocTemplate(f"{person_id}_report.pdf", pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]

    person_personal_info = [
        f"Full Name: {data[0].full_name}",
        f"AI Summary: {data[0].ai_summary}",
        f"Email: {data[0].email}",
        f"Phone Number: {data[0].phone_number}",
    ]

    rprint("[bold]Step 2 of 3 - Adding data to PDF file [/bold]")
    main_info_text = "\n".join(person_personal_info)
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
        story.append(Paragraph(heading, heading_style))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(content, styles["Normal"]))
        story.append(PageBreak())

    rprint("[bold]Step 3 of 3 - Saving PDF file[/bold]")
    doc.build(story)
