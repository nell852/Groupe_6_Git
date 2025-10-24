import google.generativeai as genai
import subprocess
import os
from dotenv import load_dotenv
from send_email import send_email

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_changed_files():
    """Liste les fichiers modifiés dans le dernier commit"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True
    )
    return [f for f in result.stdout.splitlines() if f.endswith(('.js', '.html', '.css'))]

def review_code_with_gemini(file_content):
    """Demande à Gemini d’analyser le code"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Tu es une IA experte en revue de code. Analyse le code suivant et dis :
    - Les erreurs critiques qui peuvent casser le déploiement.
    - Donne une évaluation finale sous la forme :
      VERDICT: APPROVE  (si le code est sûr)
      ou
      VERDICT: REJECT  (si le code est dangereux)
    Voici le code :
    {file_content}
    """
    response = model.generate_content(prompt)
    return response.text

def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("Aucun fichier modifié détecté.")
        return

    verdicts = []
    reviewer_output = ""

    for file in changed_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        review = review_code_with_gemini(content)
        reviewer_output += f"\n--- Analyse de {file} ---\n{review}\n"
        if "REJECT" in review:
            verdicts.append("REJECT")

    # Récupérer l’auteur du commit
    author_email = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%ae"],
        capture_output=True, text=True
    ).stdout.strip()

    if "REJECT" in verdicts:
        print("❌ Code rejeté par l’IA. Envoi d’un e-mail à l’auteur…")
        send_email(
            to_email=author_email,
            subject="🚫 Commit rejeté par l’IA — Erreurs critiques détectées",
            message=f"""
Bonjour,

L'IA Gemini a détecté des problèmes dans votre dernier commit pouvant casser le déploiement.

Résumé :
{reviewer_output}

Veuillez corriger les erreurs et refaire le commit.

Cordialement,
Votre IA de revue automatique 🤖
"""
        )
        exit(1)
    else:
        print("✅ IA Gemini a approuvé le commit.")

if __name__ == "__main__":
    main()
