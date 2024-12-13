from pdfminer.high_level import extract_text
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file):
    """Extraction du texte d'un fichier PDF."""
    try:
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction du texte du PDF: {e}")
        return ""