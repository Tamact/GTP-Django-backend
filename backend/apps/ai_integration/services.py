import google.generativeai as genai
import os
import logging
from django.conf import settings
import spacy
from transformers import pipeline


logger = logging.getLogger(__name__)

# Configuration de l'API Gemini
api_key = ("AIzaSyClXnQlAqKXSdvp_jXAg82OlRow6PAVHI8")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 512,
    "top_p": 0.95,
    "top_k": 50
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def generate_questionnaire_google(profil):
    """
    Génère un questionnaire d'entretien basé sur le profil du candidat.
    """
    try:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "Génère un questionnaire de 10 questions basées sur le profil suivant :",
                        f"Profil : {profil}",
                    ],
                }
            ]
        )
        response = chat_session.send_message(
            "Crée un questionnaire de 10 questions en fonction du profil donné. Donne juste les questions, pas besoin de commenter"
        )

        questions = response.text.split("\n") if response.text else ["Aucune question générée."]
        return questions
    except Exception as e:
        logger.error(f"Erreur lors de la génération du questionnaire: {e}")
        return None

def categorize_skills_with_kano(text_offre):
    """
    Utilise Gemini AI pour catégoriser les compétences d'une fiche de poste ou d'un CV selon le modèle de Kano.
    """
    try:
        model_flash = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.5,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )
        chat_session = model_flash.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        f"Voici un extrait de l'offre : {text_offre}. "
                        "Catégorise les compétences en fonction du modèle de Kano (Indispensable, Proportionnelle, Attractive, Indifférente). "
                        "Donne juste les compétences classées sans explication ni commentaire. Enléve aussi les notes",
                    ],
                }
            ]
        )

        response = chat_session.send_message("Catégorise les compétences selon le modèle de Kano sans note ni commentaire.")
        if response.text:
            return response.text
        else:
            logger.error("Aucune réponse générée")
            return "Aucune réponse générée."
    except Exception as e:
        logger.error(f"Erreur lors de la catégorisation des compétences: {e}")
        return None


# Détecter le texte généré par une IA
def load_ai_detector():
    try:
      ai_detector = pipeline("text-classification", model="roberta-base-openai-detector")
      return ai_detector
    except Exception as e:
      logger.error(f"Erreur lors du chargement du modèle de détection IA: {e}")
      return None

ai_detector = load_ai_detector()

def detect_ai_generated_text(text):
    try:
        if ai_detector is None:
            logger.error("Le détecteur IA n'a pas été chargé.")
            return None
        result = ai_detector(text[:512])
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la détection IA: {e}")
        return None


# Analyser le style du texte
def analyze_text_style(text):
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        avg_sentence_length = sum(len(sent) for sent in doc.sents) / len(list(doc.sents)) if list(doc.sents) else 0
        unusual_words = [token.text for token in doc if token.is_alpha and len(token.text) > 12]
        num_sentences = len(list(doc.sents))
        return {
            "avg_sentence_length": avg_sentence_length,
            "unusual_words": unusual_words,
            "num_sentences": num_sentences
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse du style de texte: {e}")
        return None