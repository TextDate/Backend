import string
import logging
from textstat import textstat

logger = logging.getLogger(__name__)

def avg_word_length(text: str) -> float:
    try:
        words = text.split()
        return sum(len(w) for w in words) / len(words) if words else 0.0
    except Exception as e:
        logger.error(f"avg_word_length failed: {e}")
        return 0.0

def lexical_richness(text: str) -> float:
    try:
        words = text.split()
        return len(set(words)) / len(words) if words else 0.0
    except Exception as e:
        logger.error(f"lexical_richness failed: {e}")
        return 0.0

def avg_sentence_length(text: str) -> float:
    try:
        sentences = text.split(".")
        words = [s.split() for s in sentences]
        return sum(len(s) for s in words) / len(words) if words else 0.0
    except Exception as e:
        logger.error(f"avg_sentence_length failed: {e}")
        return 0.0

def punctuation_density(text: str) -> float:
    try:
        return sum(1 for c in text if c in string.punctuation) / len(text) if text else 0.0
    except Exception as e:
        logger.error(f"punctuation_density failed: {e}")
        return 0.0

def syllable_per_word(text: str) -> float:
    try:
        words = text.split()
        return sum(textstat.syllable_count(w) for w in words) / len(words) if words else 0.0
    except Exception as e:
        logger.error(f"syllable_per_word failed: {e}")
        return 0.0

def uppercase_ratio(text: str) -> float:
    try:
        letters = [c for c in text if c.isalpha()]
        return sum(1 for c in letters if c.isupper()) / len(letters) if letters else 0.0
    except Exception as e:
        logger.error(f"uppercase_ratio failed: {e}")
        return 0.0

def digit_ratio(text: str) -> float:
    try:
        return sum(1 for c in text if c.isdigit()) / len(text) if text else 0.0
    except Exception as e:
        logger.error(f"digit_ratio failed: {e}")
        return 0.0

def special_character_ratio(text: str) -> float:
    try:
        return sum(1 for c in text if not c.isalnum() and not c.isspace() and c not in string.punctuation) / len(text) if text else 0.0
    except Exception as e:
        logger.error(f"special_character_ratio failed: {e}")
        return 0.0