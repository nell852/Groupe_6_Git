import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from typing import Optional

# Chargement des variables d'environnement
load_dotenv()

def send_email(to_email: str, subject: str, message: str) -> None:
    """
    Envoie un email simple (texte) via SMTP Gmail.

    Args:
        to_email (str): Adresse email du destinataire.
        subject (str): Sujet de l'email.
        message (str): Contenu du message.
    """
    sender_email: Optional[str] = os.getenv("EMAIL_USER")
    password: Optional[str] = os.getenv("EMAIL_PASS")

    if not sender_email or not password:
        raise ValueError("❌ Les variables EMAIL_USER ou EMAIL_PASS ne sont pas définies dans le fichier .env")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print(f"📨 Email envoyé à {to_email}")
    except Exception as e:
        print(f"⚠️ Erreur lors de l’envoi d’email : {e}")
