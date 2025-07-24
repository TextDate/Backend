import logging
from nltk.corpus import stopwords
from textstat import textstat

logger = logging.getLogger(__name__)

def get_stopwords(lang: str = "english") -> set:
    try:
        return set(stopwords.words(lang))
    except (OSError, LookupError) as e:
        logger.warning(f"Stopwords not available for language '{lang}': {e}. Defaulting to empty set.")
        return set()

def stopword_ratio(text: str, lang: str = "english") -> float:
    try:
        stopword_set = get_stopwords(lang)
        if not stopword_set:
            return 0.0
        words = text.split()
        return sum(1 for word in words if word.lower() in stopword_set) / len(words) if words else 0.0
    except Exception as e:
        logger.error(f"stopword_ratio failed: {e}")
        return 0.0

def flesch_readability(text: str) -> float:
    try:
        return textstat.flesch_reading_ease(text)
    except Exception as e:
        logger.error(f"flesch_readability failed: {e}")
        return 0.0