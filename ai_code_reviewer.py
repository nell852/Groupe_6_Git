# ai_code_reviewer.py
import os
import subprocess
import sys
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()

# Vérification des variables d'environnement
if not os.getenv("GEMINI_API_KEY"):
    print("❌ Erreur : GEMINI_API_KEY non défini.")
    sys.exit(1)
if not os.getenv("EMAIL_SENDER") or not os.getenv("EMAIL_PASSWORD"):
    print("❌ Erreur : EMAIL_SENDER ou EMAIL_PASSWORD non défini.")
    sys.exit(1)

# Configuration Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-2.5-flash"  # Corrigé : utiliser le modèle correct

# Configuration email
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def get_last_commit_files():
    """Retourne la liste des fichiers modifiés dans le dernier commit (JS et Python)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True
    )
    files = result.stdout.strip().split("\n")
    return [f for f in files if f.endswith(".js") or f.endswith(".py")]

def get_commit_author_email():
    """Récupère l'email de l'auteur du dernier commit."""
    result = subprocess.run(
        ["git", "config", "user.email"], capture_output=True, text=True
    )
    return result.stdout.strip()

def review_code_with_gemini(file_path):
    """Analyse le code via Gemini et retourne un texte avec les erreurs détectées."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
Analyse ce code et détecte les erreurs éventuelles :
{content}

Retourne uniquement une liste d'erreurs ou 'Aucune erreur détectée'.
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erreur lors de l'analyse du code : {str(e)}"

def send_email(to_email, subject, body):
    """Envoie un email via SMTP."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email envoyé à {to_email}")
    except Exception as e:
        print(f"❌ Échec de l'envoi de l'email : {str(e)}")

def main():
    files = get_last_commit_files()
    if not files:
        print("Aucun fichier pertinent pour l'analyse.")
        return

    author_email = get_commit_author_email()
    errors_detected = False
    message = ""

    for file in files:
        review = review_code_with_gemini(file)
        if review.lower() != "aucune erreur détectée":
            errors_detected = True
            message += f"\nFichier : {file}\n{review}\n"

    if errors_detected:
        print("❌ Commit annulé : l'IA a détecté des erreurs.")
        print(message)
        # Envoi email à l'auteur si email disponible
        if author_email:
            send_email(
                to_email=author_email,
                subject="Code review automatique - erreurs détectées",
                body=message
            )
        sys.exit(1)  # Annule le commit
    else:
        print("✅ Aucun problème détecté par l'IA. Commit autorisé.")

if __name__ == "__main__":
    main()