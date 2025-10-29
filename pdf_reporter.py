# pdf_reporter.py
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_ai_report(errors_text, output_path="ai_review_report.pdf"):
    """Génère un PDF clair et bien formaté listant les erreurs détectées."""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("🤖 Rapport d'Analyse IA Gemini", styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 15))
    story.append(Paragraph("🧠 Résumé des erreurs détectées :", styles["Heading2"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(errors_text.replace("\n", "<br/>"), styles["Normal"]))

    story.append(Spacer(1, 20))
    story.append(Paragraph("🔍 Analyse effectuée par l'IA Gemini 2.5 Flash", styles["Italic"]))

    doc.build(story)
    return output_path
