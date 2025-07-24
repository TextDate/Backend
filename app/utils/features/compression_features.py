import math
import logging
from collections import Counter
from vomm import ppm

logger = logging.getLogger(__name__)


def shannon_entropy(text):
    try:
        if not text:
            return 0
        counts = Counter(text)
        total = len(text)
        return -sum((c / total) * math.log2(c / total) for c in counts.values())
    except Exception as e:
        logger.error(f"Error computing Shannon entropy: {e}")
        return 0


def compression_ratio_markov(text, order):
    try:
        if not text:
            return None
        data = [ord(c) for c in text]
        model = ppm()
        model.fit(data, d=order)
        compressed = -model.logpdf(data) / math.log(2)
        return compressed / (len(data) * 8) if len(data) > 0 else None
    except Exception as e:
        logger.error(f"Error computing compression ratio (order={order}): {e}")
        return None


def nrc_markov(text, order, alphabet_size=256):
    try:
        if not text:
            return None
        data = [ord(c) for c in text]
        model = ppm()
        model.fit(data, d=order)
        compressed = -model.logpdf(data) / math.log(2)
        max_bits = len(data) * math.log2(alphabet_size)
        return compressed / max_bits if max_bits > 0 else None
    except Exception as e:
        logger.error(f"Error computing NRC Markov (order={order}): {e}")
        return None


def nrc_markov_shannon(text, order):
    try:
        shannon = shannon_entropy(text)
        markov = compression_ratio_markov(text, order)
        if markov is None:
            return None
        return (markov * 8) / shannon if shannon > 0 else None
    except Exception as e:
        logger.error(f"Error computing NRC Markov Shannon (order={order}): {e}")
        return None