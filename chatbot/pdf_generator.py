import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from langchain_core.messages import HumanMessage, AIMessage


def generate_pdf_report(messages, user_count):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(
        "Conversation Summary Report",
        ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=24,
            spaceAfter=30,
            alignment=1,
        ),
    )
    story.append(title)
    story.append(Spacer(1, 12))

    meta_style = ParagraphStyle(
        "Meta", parent=styles["Normal"], fontSize=12, spaceAfter=6
    )
    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            meta_style,
        )
    )
    story.append(Paragraph(f"<b>Total Messages:</b> {len(messages)}", meta_style))
    story.append(Paragraph(f"<b>User Messages:</b> {user_count}", meta_style))
    story.append(Spacer(1, 20))

    conv_title = Paragraph(
        "Conversation History",
        ParagraphStyle(
            "ConvTitle", parent=styles["Heading2"], fontSize=16, spaceAfter=12
        ),
    )
    story.append(conv_title)

    user_style = ParagraphStyle(
        "UserStyle",
        parent=styles["Normal"],
        fontSize=11,
        leftIndent=20,
        spaceAfter=8,
        textColor="blue",
    )
    ai_style = ParagraphStyle(
        "AIStyle",
        parent=styles["Normal"],
        fontSize=11,
        leftIndent=20,
        spaceAfter=8,
        textColor="green",
    )

    for message in messages:
        if isinstance(message, HumanMessage):
            story.append(Paragraph(f"<b>User:</b> {message.content}", user_style))
        elif isinstance(message, AIMessage):
            story.append(Paragraph(f"<b>Assistant:</b> {message.content}", ai_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer
