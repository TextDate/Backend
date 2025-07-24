from app.utils.features.compression_features import (
    compression_ratio_markov, nrc_markov, nrc_markov_shannon, shannon_entropy
)
from app.utils.features.lexical_structure_features import (
    avg_word_length, lexical_richness, avg_sentence_length,
    punctuation_density, syllable_per_word, uppercase_ratio,
    digit_ratio, special_character_ratio
)
from app.utils.features.readability_features import flesch_readability, stopword_ratio
from app.utils.features.lexical_distance_features import mean_word_distance
from app.utils.file_checks import text_trimmer
import logging

logger = logging.getLogger(__name__)

def extract_features_from_text(text_path: str, lang: str = "english") -> dict:
    try:
        text = text_trimmer(text_path)
        if not text:
            logger.warning(f"No valid text content extracted from: {text_path}")
            return {}

        features = {
            "compression_ratio_markov_order_1": compression_ratio_markov(text, 1),
            "nrc_markov_order_1": nrc_markov(text, 1),
            "nrc_markov_shannon_order_1": nrc_markov_shannon(text, 1),
            "compression_ratio_markov_order_3": compression_ratio_markov(text, 3),
            "nrc_markov_order_3": nrc_markov(text, 3),
            "nrc_markov_shannon_order_3": nrc_markov_shannon(text, 3),
            "shannon_entropy": shannon_entropy(text),
            "avg_word_length": avg_word_length(text),
            "lexical_richness": lexical_richness(text),
            "avg_sentence_length": avg_sentence_length(text),
            "punctuation_density": punctuation_density(text),
            "syllable_per_word": syllable_per_word(text),
            "uppercase_ratio": uppercase_ratio(text),
            "digit_ratio": digit_ratio(text),
            "special_character_ratio": special_character_ratio(text),
            "stopword_ratio": stopword_ratio(text, lang),
            "flesch_readability": flesch_readability(text) if lang == "english" else 0.0
        }

        distances = mean_word_distance(text)
        features.update(distances)

        return features

    except Exception as e:
        logger.exception(f"Feature extraction failed for {text_path}: {e}")
        return {}