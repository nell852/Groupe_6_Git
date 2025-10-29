import os
import subprocess
import sys
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# === Chargement des variables d'environnement ===
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY manquant.", file=sys.stderr)
    sys.exit(1)

# === Configuration Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-2.5-flash"

# === Email ===
def send_email(to_email, subject, body, attachments=None, is_html=False):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content("Ce mail contient un rapport d'analyse.")
    if is_html:
        msg.add_alternative(body, subtype="html")

    if attachments:
        for file_path in attachments:
            with open(file_path, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(file_path))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email envoyé à {to_email}")
    except Exception as e:
        print(f"⚠️ Échec de l'envoi de l'email : {e}", file=sys.stderr)

# === PDF ===
def generate_pdf_report(errors_dict):
    pdf_path = "AI_Code_Review_Report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("🤖 Rapport d'Analyse Syntaxique - IA Gemini", styles["Title"]))
    content.append(Spacer(1, 20))

    if not errors_dict:
        content.append(Paragraph("✅ Aucun problème détecté !", styles["Normal"]))
    else:
        for file, errors in errors_dict.items():
            content.append(Paragraph(f"<b>Fichier :</b> {file}", styles["Heading3"]))
            content.append(Paragraph(errors.replace("\n", "<br/>"), styles["Normal"]))
            content.append(Spacer(1, 15))

    doc.build(content)
    return pdf_path

# === Analyse syntaxique ===
def get_staged_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return [f for f in result.stdout.split("\n") if f.endswith((".js", ".py"))]

def review_code_with_gemini(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except:
        return "⚠️ Impossible de lire le fichier."
    prompt = f"""
Analyse uniquement les **erreurs de syntaxe** dans ce code :
{code}

Retourne :
- "Aucune erreur syntaxique détectée" si c’est correct.
- Sinon, liste les erreurs détectées.
"""
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"⚠️ Erreur Gemini : {e}"

# === Badge README ===
def update_readme_badge(success):
    badge_url = (
        "https://img.shields.io/badge/AI%20Code%20Review-PASS-green"
        if success else "https://img.shields.io/badge/AI%20Code%20Review-FAIL-red"
    )
    badge_md = f"![AI Code Review]({badge_url})"
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return
    with open(readme_path, "r+", encoding="utf-8") as f:
        content = f.read()
        if "![AI Code Review]" in content:
            new_content = re.sub(r"!\[AI Code Review\]\(.*?\)", badge_md, content)
        else:
            new_content = badge_md + "\n\n" + content
        f.seek(0)
        f.write(new_content)
        f.truncate()
    subprocess.run(["git", "add", "README.md"])

# === Programme principal ===
def main():
    files = get_staged_files()
    if not files:
        print("ℹ️ Aucun fichier à analyser.")
        sys.exit(0)

    author_email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
    errors = {}
    has_error = False

    for f in files:
        res = review_code_with_gemini(f)
        if "aucune erreur syntaxique détectée" not in res.lower():
            has_error = True
            errors[f] = res

    pdf_path = generate_pdf_report(errors)
    update_readme_badge(not has_error)

    if has_error:
        print("❌ Des erreurs syntaxiques ont été détectées.")
        html_body = f"""
        <html><body style="font-family:Arial;">
        <h2 style="color:#D32F2F;">🚫 Des erreurs syntaxiques ont été détectées !</h2>
        <p>Merci de les corriger avant de recommitter.</p>
        <p><b>Fichiers affectés :</b></p>
        <pre>{'<br>'.join(errors.keys())}</pre>
        <p>Le rapport PDF est joint à cet email.</p>
        </body></html>
        """
        send_email(author_email, "🚫 Commit bloqué - Erreurs détectées", html_body, [pdf_path], True)
        sys.exit(1)
    else:
        print("✅ Aucun problème détecté. Commit autorisé.")
        html_body = """
        <html><body style="font-family:Arial;">
        <h2 style="color:#388E3C;">✅ Vérification réussie !</h2>
        <p>Aucun problème syntaxique détecté. Bravo 👏</p>
        </body></html>
        """
        send_email(author_email, "✅ Commit validé", html_body, [pdf_path], True)
        sys.exit(0)

if __name__ == "__main__":
    main()
