"""
Detector Bypass & AI-Slop Auditor
Calculates Burstiness, Perplexity proxies, identifies AI fingerprints,
and enforces human linguistic variance across English and Persian.
"""

from __future__ import annotations
import re
import math
from typing import Dict, List, Any
from pydantic import BaseModel, Field

# High-frequency AI tells and cliché blacklist (English & Persian)
AI_CLICHE_MAP: Dict[str, str] = {
    # English
    r"\bdelve(?:s|d|ing)?\b": "explore / dig into",
    r"\btapestry\b": "mix / collection",
    r"\bpivotal\b": "critical / key",
    r"\bin today'?s rapidly evolving (?:digital )?landscape\b": "today",
    r"\bin today'?s world\b": "now",
    r"\btestament to\b": "proof of",
    r"\bleverage(?:s|d|ing)?\b": "use",
    r"\butilize(?:s|d|ing)?\b": "use",
    r"\bstreamline(?:s|d|ing)?\b": "simplify",
    r"\bfoster(?:s|d|ing)?\b": "build / support",
    r"\bembark(?:s|ed|ing)? on a journey\b": "start",
    r"\bbeacon of\b": "guide for",
    r"\bgame-?changer\b": "significant shift",
    r"\bit is important to (?:note|remember|consider)\b": "[remove filler]",
    r"\bfurthermore\b": "also / plus",
    r"\bmoreover\b": "and / what's more",
    r"\bin conclusion\b": "[state point directly]",
    r"\bultimately\b": "in the end / practically",
    r"\bseamless(?:ly)?\b": "smooth / direct",
    r"\bparadigm shift\b": "major change",
    r"\bnavigat(?:e|ing) the complexities\b": "handling",

    # Persian
    r"در دنیای پرشتاب امروز": "امروز",
    r"در عصر حاضر": "امروز",
    r"نقش بسزایی دارد": "اثر مستقیم دارد / مهم است",
    r"لازم به ذکر است": "[حذف حشو - مستقیم بگو]",
    r"شایان ذکر است": "[حذف حشو]",
    r"بر کسی پوشیده نیست": "[حذف حشو]",
    r"در نهایت می‌توان گفت": "[نتیجه را مستقیم بگو]",
    r"سفری شگفت‌انگیز": "مسیر / تجربه",
    r"تلفیقی بی‌نظیر": "ترکیب",
    r"گامی نوین": "روش جدید",
    r"پنجره‌ای نو": "امکان جدید",
    r"به ارمغان می‌آورد": "می‌آورد / ایجاد می‌کند",
    r"دستخوش تغییرات": "عوض شده",
    r"در این میان": "اینجا",
    r"همواره در تلاش است": "تلاش می‌کند",
}


class AuditReport(BaseModel):
    total_words: int
    total_sentences: int
    mean_sentence_length: float
    sentence_length_std_dev: float
    burstiness_score: float = Field(
        description="Coefficient of variation (std_dev / mean). > 0.4 indicates strong human variance."
    )
    ai_cliches_found: List[Dict[str, str]]
    ai_density_percent: float
    predicted_human_score: float = Field(
        description="Estimated probability (0-100%) that detectors classify text as human-written."
    )
    is_safe_from_detectors: bool
    suggestions: List[str]


class DetectorBypassAuditor:
    """Analyzes text for AI signatures and validates human structural metrics."""

    def __init__(self, cliche_map: Dict[str, str] | None = None):
        self.cliche_map = cliche_map or AI_CLICHE_MAP

    def split_sentences(self, text: str) -> List[str]:
        # Split on sentence terminals in Latin and Persian/Arabic (. ! ? ؛ ؟)
        raw = re.split(r"[.!?؟;\n]+", text)
        sentences = [s.strip() for s in raw if len(s.strip()) > 3]
        return sentences

    def count_words(self, text: str) -> int:
        return len(re.findall(r"\b\w+\b|[\u0600-\u06FF]+", text))

    def audit(self, text: str) -> AuditReport:
        sentences = self.split_sentences(text)
        total_sentences = len(sentences) or 1
        words_per_sentence = [self.count_words(s) for s in sentences]
        total_words = sum(words_per_sentence) or 1

        mean_length = total_words / total_sentences
        variance = sum((l - mean_length) ** 2 for l in words_per_sentence) / total_sentences
        std_dev = math.sqrt(variance)
        burstiness = std_dev / mean_length if mean_length > 0 else 0.0

        # Scan for AI tells
        found_cliches: List[Dict[str, str]] = []
        for pattern, replacement in self.cliche_map.items():
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                found_cliches.append({
                    "pattern": pattern,
                    "matches_count": str(len(matches)),
                    "suggested_alternative": replacement,
                })

        cliche_count = sum(int(item["matches_count"]) for item in found_cliches)
        ai_density = (cliche_count / (total_words / 100)) if total_words > 0 else 0.0

        # Heuristic Human Score calculation
        # Baseline 100, penalize for low burstiness (flat AI sentences) and high cliché count
        score = 98.0
        if burstiness < 0.35:
            score -= (0.35 - burstiness) * 80.0
        elif burstiness > 0.55:
            score += 2.0

        score -= (ai_density * 15.0)

        # Check for excessive em-dash overuse (a classic AI signature)
        em_dash_count = text.count("—") + text.count("--")
        if em_dash_count > (total_sentences * 0.4):
            score -= 10.0

        predicted_human = max(5.0, min(100.0, score))
        is_safe = (predicted_human >= 90.0) and (cliche_count == 0) and (burstiness >= 0.35)

        suggestions: List[str] = []
        if burstiness < 0.35:
            suggestions.append(
                f"Burstiness is low ({burstiness:.2f}). Alternate between punchy 2-4 word sentences and long compound thoughts."
            )
        if cliche_count > 0:
            suggestions.append(
                f"Found {cliche_count} blacklisted AI phrases. Replace them with plain spoken language."
            )
        if em_dash_count > 3:
            suggestions.append(
                "Excessive em dashes detected. Replace them with commas or split into separate sentences."
            )

        return AuditReport(
            total_words=total_words,
            total_sentences=total_sentences,
            mean_sentence_length=round(mean_length, 2),
            sentence_length_std_dev=round(std_dev, 2),
            burstiness_score=round(burstiness, 3),
            ai_cliches_found=found_cliches,
            ai_density_percent=round(ai_density, 3),
            predicted_human_score=round(predicted_human, 1),
            is_safe_from_detectors=is_safe,
            suggestions=suggestions,
        )
