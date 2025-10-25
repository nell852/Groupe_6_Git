# list_models.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Charge ta clé API depuis le fichier .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

models = genai.list_models()
print("Modèles disponibles :")
for model in models:
    print(model.name)
