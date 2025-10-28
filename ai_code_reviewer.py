import os
import subprocess
import sys
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import google.generativeai as genai

# === Chargement des variables d'environnement ===
load_dotenv()

# Récupération des clés d'environnement
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not GEMINI_API_KEY:
    print("❌ Erreur : GEMINI_API_KEY non défini.", file=sys.stderr)
    sys.exit(1)
if not EMAIL_SENDER or not EMAIL_PASSWORD:
    print("❌ Erreur : EMAIL_SENDER ou EMAIL_PASSWORD non défini.", file=sys.stderr)
    sys.exit(1)

# === Configuration Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-2.5-flash"

# === Fonction d'envoi d'email ===
def send_email(to_email, subject, body):
    """Envoie un email via SMTP (Gmail)."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email envoyé à {to_email}")
    except Exception as e:
        print(f"⚠️ Échec de l'envoi de l'email : {str(e)}", file=sys.stderr)

# --- Récupère les fichiers en staging
def get_staged_files():
    """Retourne la liste des fichiers JS et Python ajoutés au staging."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f.endswith(".js") or f.endswith(".py")]
    except FileNotFoundError:
        print("❌ Git non trouvé sur le système. Vérifie ton installation Git.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("⚠️ Impossible de récupérer les fichiers du commit.", file=sys.stderr)
        return []

# --- Récupère l'email de l'auteur du commit
def get_commit_author_email():
    try:
        result = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return None

# --- Analyse uniquement la syntaxe avec Gemini
def review_code_with_gemini(file_path):
    """Analyse uniquement les erreurs de syntaxe du fichier."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except Exception as e:
            return f"⚠️ Impossible de lire {file_path} : {str(e)}"

    prompt = f"""
Tu es un **analyseur de syntaxe** pour développeurs.
Analyse ce code et détecte UNIQUEMENT les **erreurs de syntaxe** (ex : parenthèses manquantes, indentation, accolades non fermées, mot-clé invalide...).

Code :
{content}

Retourne exactement :
- "Aucune erreur syntaxique détectée" si tout est correct.
- Sinon, liste uniquement les erreurs syntaxiques détectées (sans explications logiques ni suggestions).
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Erreur lors de l'analyse de {file_path} : {str(e)}"

# --- Fonction principale
def main():
    files = get_staged_files()
    if not files:
        print("ℹ️ Aucun fichier Python ou JS détecté pour l'analyse.")
        sys.exit(0)

    author_email = get_commit_author_email()
    errors_detected = False
    message = ""

    for file in files:
        review = review_code_with_gemini(file)

        if "aucune erreur syntaxique détectée" not in review.lower():
            errors_detected = True
            message += f"\nFichier : {file}\n{review}\n"

    if errors_detected:
        print("❌ Des erreurs de syntaxe ont été détectées :")
        print(message)
        if author_email:
            send_email(
                to_email=author_email,
                subject="🚫 Erreurs de syntaxe détectées - Commit bloqué",
                body=message
            )
        sys.exit(1)  # Bloque le commit
    else:
        print("✅ Aucune erreur syntaxique détectée. Commit autorisé.")
        if author_email:
            send_email(
                to_email=author_email,
                subject="✅ Vérification syntaxique réussie - Commit validé",
                body="Aucune erreur syntaxique détectée. Votre commit a été validé."
            )
        sys.exit(0)

if __name__ == "__main__":
    main()
