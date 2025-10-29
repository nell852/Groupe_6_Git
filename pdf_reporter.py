from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def generate_ai_report(errors, output_path="ai_review_report.pdf"):
    """
    Génère un PDF clair et coloré listant les erreurs détectées.
    `errors` doit être une liste de dictionnaires avec :
    {'line': int, 'problem': str, 'correction': str}
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    story = []

    # TITRE PRINCIPAL
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"],
        fontSize=24, textColor=colors.HexColor("#1F618D"), spaceAfter=20
    )
    story.append(Paragraph("🤖 Rapport d'Analyse Syntaxique - IA Gemini", title_style))

    # DATE
    date_style = ParagraphStyle(
        "DateStyle", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#555555"), spaceAfter=20
    )
    story.append(Paragraph(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", date_style))

    # FICHIER ANALYSÉ
    file_style = ParagraphStyle(
        "FileStyle", parent=styles["Heading2"],
        fontSize=14, textColor=colors.HexColor("#D35400"), spaceAfter=10
    )
    story.append(Paragraph("📄 Fichier : history.js", file_style))
    story.append(Spacer(1, 10))

    # POUR CHAQUE ERREUR
    for i, err in enumerate(errors, start=1):
        # Titre d'erreur
        err_title_style = ParagraphStyle(
            "ErrTitleStyle", parent=styles["Heading3"],
            fontSize=12, textColor=colors.HexColor("#C0392B"), spaceAfter=5
        )
        story.append(Paragraph(f"Erreur {i} :", err_title_style))

        # Tableau encadré pour l'erreur
        error_data = [
            ["Ligne", "Problème", "Correction"],
            [str(err["line"]), err["problem"], err["correction"]]
        ]
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2980B9")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FDFEFE")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#7F8C8D")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#7F8C8D")),
        ])
        table = Table(error_data, colWidths=[40, 300, 150])
        table.setStyle(table_style)
        story.append(KeepTogether(table))
        story.append(Spacer(1, 15))

    # FOOTER
    footer_style = ParagraphStyle(
        "FooterStyle", parent=styles["Italic"],
        fontSize=9, textColor=colors.HexColor("#7F8C8D"), spaceBefore=20
    )
    story.append(Paragraph("🔍 Analyse effectuée par l'IA Gemini 2.5 Flash", footer_style))

    doc.build(story)
    return output_path

# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    errors = [
        {
            "line": 17,
            "problem": "Il manque la parenthèse fermante `)` après le paramètre `entry` et avant l'accolade ouvrante `{` du corps de la fonction.",
            "correction": "`function addToHistory(entry) {`"
        }
    ]
    generate_ai_report(errors)
