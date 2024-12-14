import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_stop_words():
    return set(stopwords.words('french') + stopwords.words('english'))

stop_words = get_stop_words()

def preprocess_text(text):
    """Prétraitement du texte : minuscules, suppression des caractères spéciaux et des stopwords."""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)