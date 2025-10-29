# ai_report_generator.py
from __future__ import annotations
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from typing import List, Dict, Any


def generate_ai_report(errors: List[Dict[str, Any]], output_path: str = "ai_review_report.pdf") -> str:
    """
    Génère un rapport PDF élégant listant les erreurs détectées par l'IA Gemini.
    
    Args:
        errors (List[Dict[str, Any]]): Liste d'erreurs détectées.
            Chaque élément doit être un dictionnaire contenant :
                - line (int) : Numéro de ligne concerné
                - problem (str) : Description de l’erreur
                - correction (str) : Proposition de correction
        output_path (str): Chemin de sauvegarde du PDF. Défaut : "ai_review_report.pdf"

    Returns:
        str: Le chemin complet du fichier PDF généré.
    """
    # Création du document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story: List[Any] = []

    # === TITRE PRINCIPAL ===
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#1F618D"),
        spaceAfter=20,
    )
    story.append(Paragraph("🤖 Rapport d'Analyse Syntaxique - IA Gemini", title_style))

    # === DATE ===
    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#555555"),
        spaceAfter=20,
    )
    story.append(Paragraph(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", date_style))

    # === NOM DU FICHIER ANALYSÉ ===
    file_style = ParagraphStyle(
        "FileStyle",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#D35400"),
        spaceAfter=10,
    )
    story.append(Paragraph("📄 Fichier : history.js", file_style))
    story.append(Spacer(1, 10))

    # === LISTE DES ERREURS ===
    for i, err in enumerate(errors, start=1):
        err_title_style = ParagraphStyle(
            "ErrTitleStyle",
            parent=styles["Heading3"],
            fontSize=12,
            textColor=colors.HexColor("#C0392B"),
            spaceAfter=5,
        )
        story.append(Paragraph(f"Erreur {i} :", err_title_style))

        error_data = [
            ["Ligne", "Problème", "Correction"],
            [str(err.get("line", "?")), err.get("problem", ""), err.get("correction", "")]
        ]

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2980B9")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#FDFEFE")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#7F8C8D")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#7F8C8D")),
        ])

        table = Table(error_data, colWidths=[40, 300, 150])
        table.setStyle(table_style)
        story.append(KeepTogether(table))
        story.append(Spacer(1, 15))

    # === PIED DE PAGE ===
    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=styles["Italic"],
        fontSize=9,
        textColor=colors.HexColor("#7F8C8D"),
        spaceBefore=20,
    )
    story.append(Paragraph("🔍 Analyse effectuée par l'IA Gemini 2.5 Flash", footer_style))

    # Construction du PDF
    doc.build(story)
    return output_path


# === TEST LOCAL ===
if __name__ == "__main__":
    sample_errors: List[Dict[str, Any]] = [
        {
            "line": 17,
            "problem": "Parenthèse fermante manquante après le paramètre `entry`.",
            "correction": "`function addToHistory(entry) {`"
        },
        {
            "line": 45,
            "problem": "Point-virgule manquant après l’instruction `return`.",
            "correction": "Ajoutez `;` à la fin de la ligne."
        }
    ]
    path = generate_ai_report(sample_errors)
    print(f"✅ Rapport généré : {path}")
