import json
import numpy as np
import logging
from collections import defaultdict
from app.core.config import settings

logger = logging.getLogger(__name__)


def load_target_words(lang="english"):
    try:
        with open(settings.target_words_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get(lang, []))
    except FileNotFoundError:
        logger.error(f"Target words file not found at {settings.target_words_path}")
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from {settings.target_words_path}")
    except Exception as e:
        logger.error(f"Unexpected error loading target words: {e}")
    return set()


def mean_word_distance(text):
    try:
        words = text.lower().split()
        word_positions = defaultdict(list)
        target_words = load_target_words()

        if not target_words:
            logger.warning("No target words loaded.")
            return {}

        for index, word in enumerate(words):
            if word in target_words:
                word_positions[word].append(index)

        mean_distances = {}
        for word, positions in word_positions.items():
            if len(positions) > 1:
                distances = np.diff(positions)
                mean_distances[word] = float(np.mean(distances))
            else:
                mean_distances[word] = None

        return mean_distances
    except Exception as e:
        logger.error(f"Error computing mean word distances: {e}")
        return {}