# list_models.py
import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import Optional

def list_available_models() -> None:
    """
    Liste tous les modèles disponibles depuis l'API Gemini.

    Cette fonction charge la clé API à partir du fichier .env,
    configure l'accès à l'API Gemini, puis affiche la liste
    des modèles disponibles avec leur nom.
    """
    # Chargement des variables d'environnement
    load_dotenv()

    api_key: Optional[str] = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("❌ La clé API GEMINI_API_KEY est manquante dans le fichier .env")

    # Configuration de l'API Gemini
    genai.configure(api_key=api_key)

    try:
        models = genai.list_models()
        print("🧠 Modèles disponibles :")
        for model in models:
            print(f"• {model.name}")
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des modèles : {e}")

if __name__ == "__main__":
    list_available_models()
