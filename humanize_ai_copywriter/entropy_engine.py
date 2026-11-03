"""
Zero-Entropy Engine
Information-Theoretic Copywriting: Maximizes signal-to-noise ratio,
eliminates semantic redundancy, and compresses text towards minimal entropy H -> 0.
"""

from __future__ import annotations
import math
import re
from typing import Dict, List, Set
from pydantic import BaseModel, Field

# High-frequency filler / throat-clearing patterns to eliminate
FLUFF_PATTERNS: List[str] = [
    r"\bin this article,?\s*(?:we will|we shall|I will)\b",
    r"\bas we all know\b",
    r"\bit goes without saying that\b",
    r"\bat the end of the day\b",
    r"\bwithout further ado\b",
    r"\bدر این مقاله قصد داریم\b",
    r"\bهمانطور که می‌دانید\b",
    r"\bبدون شک می‌توان گفت\b",
    r"\bبه جرات می‌توان گفت\b",
    r"\bناگفته نماند که\b",
]


class EntropyAnalysis(BaseModel):
    shannon_entropy: float = Field(
        description="Shannon word entropy in bits. Lower values combined with high lexical diversity indicate dense, focused signal."
    )
    lexical_density_percent: float = Field(
        description="Ratio of content words (nouns, verbs, adjectives) to total words. Target > 55%."
    )
    signal_to_noise_ratio: float = Field(
        description="Estimated ratio of substantive proposition words vs syntactic fluff."
    )
    fluff_instances_found: List[str]
    is_zero_entropy_aligned: bool
    summary: str


class ZeroEntropyEngine:
    """Enforces zero-entropy principles: maximum substantive signal, zero fluff."""

    def __init__(self):
        self.stop_words: Set[str] = {
            # English common stopwords
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "is", "are", "was", "were", "be", "been", "being", "that", "this", "these", "those",
            # Persian common grammatical particles
            "و", "یا", "اما", "در", "بر", "به", "از", "تا", "با", "برای", "که", "این", "آن",
            "است", "بود", "شد", "می", "هم", "نیز", "چون", "اگر"
        }

    def compute_shannon_entropy(self, words: List[str]) -> float:
        if not words:
            return 0.0
        n = len(words)
        freqs: Dict[str, int] = {}
        for w in words:
            w_lower = w.lower()
            freqs[w_lower] = freqs.get(w_lower, 0) + 1

        entropy = 0.0
        for count in freqs.values():
            p = count / n
            entropy -= p * math.log2(p)
        return round(entropy, 3)

    def analyze(self, text: str) -> EntropyAnalysis:
        words = re.findall(r"\b\w+\b|[\u0600-\u06FF]+", text)
        total_words = len(words) or 1

        content_words = [w for w in words if w.lower() not in self.stop_words]
        lexical_density = (len(content_words) / total_words) * 100.0

        shannon = self.compute_shannon_entropy(words)

        # Detect throat-clearing fluff
        fluff_found: List[str] = []
        for pat in FLUFF_PATTERNS:
            matches = re.findall(pat, text, flags=re.IGNORECASE)
            fluff_found.extend(matches)

        fluff_count = len(fluff_found)
        snr = round((len(content_words) / (fluff_count * 10 + len(self.stop_words.intersection({w.lower() for w in words})) + 1)), 2)

        aligned = (lexical_density >= 52.0) and (fluff_count == 0)

        summary = (
            f"Lexical Density: {lexical_density:.1f}% | Fluff Count: {fluff_count} | "
            f"Shannon Entropy: {shannon} bits | Signal-to-Noise: {snr}"
        )

        return EntropyAnalysis(
            shannon_entropy=shannon,
            lexical_density_percent=round(lexical_density, 2),
            signal_to_noise_ratio=snr,
            fluff_instances_found=fluff_found,
            is_zero_entropy_aligned=aligned,
            summary=summary,
        )
