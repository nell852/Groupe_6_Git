import smtplib
from email.mime.text import MIMEText

# 1️⃣ Mets ton adresse Gmail et le mot de passe d’application ici
sender_email = "nyogognell@gmail.com"
password = "fzet mlpt dxyq fpky"

# 2️⃣ Adresse de destination (tu peux t’envoyer à toi-même)
receiver_email = "nyogognell@gmail.com"

# 3️⃣ Contenu du message
msg = MIMEText("✅ Test réussi ! Ceci est un message automatique envoyé par Python.")
msg["Subject"] = "Test IA GitHub - Envoi de mail"
msg["From"] = sender_email
msg["To"] = receiver_email

# 4️⃣ Connexion au serveur SMTP de Gmail
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
    print("✅ Email envoyé avec succès ! Vérifie ta boîte Gmail 📬")
except Exception as e:
    print("❌ Erreur :", e)
