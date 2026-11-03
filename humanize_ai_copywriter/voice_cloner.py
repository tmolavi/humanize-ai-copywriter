"""
Voice Tone Cloner
Analyzes sample text or fetches sample URLs to extract brand voice,
syntactic cadence, punctuation preferences, and rhetorical fingerprint.
"""

from __future__ import annotations
import re
import urllib.request
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class VoiceProfile(BaseModel):
    name: str = "Extracted Brand Voice"
    formality_level: str = Field(
        description="'colloquial', 'conversational-professional', 'authoritative-academic', or 'punchy-direct'"
    )
    mean_sentence_length: float
    punctuation_style: Dict[str, int]
    top_characteristic_words: List[str]
    perspective: str = Field(
        description="'first-person-singular (I/من)', 'first-person-plural (we/ما)', or 'second-person-direct (you/شما)'"
    )
    rhetorical_habits: List[str]
    prompt_injection_directive: str


class VoiceToneCloner:
    """Extracts voice fingerprint from sample texts or live website URLs."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    async def fetch_url_text(self, url: str) -> str:
        """Fetches and strips raw HTML tags from a URL to get core text content."""
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; TaghiMolaviVoiceCloner/1.0; +https://molavi.pro)"
        }
        try:
            import httpx
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                html = resp.text
        except ImportError:
            # Fallback to standard library urllib
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

        # Strip scripts, styles, and tags
        text = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
        text = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def analyze_samples(self, samples: List[str], profile_name: str = "Custom Profile") -> VoiceProfile:
        combined = "\n\n".join(samples)
        words = re.findall(r"\b\w+\b|[\u0600-\u06FF]+", combined)
        total_words = len(words) or 1

        raw_sentences = [s.strip() for s in re.split(r"[.!?؟;\n]+", combined) if len(s.strip()) > 3]
        total_sentences = len(raw_sentences) or 1
        mean_sentence_len = round(total_words / total_sentences, 1)

        # Perspective detection
        i_count = len(re.findall(r"\b(?:I|my|mine|me)\b|[\u0600-\u06FF]*\bمن\b", combined, re.IGNORECASE))
        we_count = len(re.findall(r"\b(?:we|our|us)\b|[\u0600-\u06FF]*\bما\b", combined, re.IGNORECASE))
        you_count = len(re.findall(r"\b(?:you|your|yours)\b|[\u0600-\u06FF]*\bشما\b", combined, re.IGNORECASE))

        if you_count >= max(i_count, we_count):
            perspective = "second-person-direct (you / شما)"
        elif i_count > we_count:
            perspective = "first-person-singular (I / من)"
        elif we_count > 0:
            perspective = "first-person-plural (we / ما)"
        else:
            perspective = "second-person-direct (you / شما)"

        # Punctuation style
        punct = {
            "question_marks": combined.count("?") + combined.count("؟"),
            "exclamation_marks": combined.count("!"),
            "colons": combined.count(":"),
            "semicolons": combined.count(";") + combined.count("؛"),
            "quotes": combined.count('"') + combined.count('«'),
        }

        # Formality estimation
        if mean_sentence_len < 12 and punct["question_marks"] > total_sentences * 0.15:
            formality = "punchy-direct"
        elif mean_sentence_len < 18:
            formality = "conversational-professional"
        else:
            formality = "authoritative-academic"

        # Rhetorical habits
        habits: List[str] = []
        if punct["question_marks"] > total_sentences * 0.1:
            habits.append("Frequently engages the reader with rhetorical or diagnostic questions.")
        if mean_sentence_len < 14:
            habits.append("Prefers short, definitive claims over extended academic clauses.")
        if "پرسش" in combined or "آیا" in combined or "?" in combined:
            habits.append("Uses problem-first diagnostic framing.")

        # Top characteristic vocabulary (simple word frequency excluding ultra-common stopwords)
        common_exclude = {
            "the", "a", "and", "in", "to", "of", "is", "for", "with", "that", "this", "on", "it",
            "و", "به", "از", "در", "که", "این", "را", "با", "است", "برای", "آن", "یک", "هم"
        }
        word_freq: Dict[str, int] = {}
        for w in words:
            wl = w.lower()
            if len(wl) > 3 and wl not in common_exclude:
                word_freq[wl] = word_freq.get(wl, 0) + 1

        top_words = sorted(word_freq.keys(), key=lambda k: word_freq[k], reverse=True)[:10]

        # Build prompt injection directive for downstream agents
        directive = (
            f"Adopt a {formality} voice using {perspective}. "
            f"Target average sentence length around {mean_sentence_len} words. "
            f"Emulate the rhetorical habits: {'; '.join(habits) if habits else 'Direct and persuasive'}. "
            f"Anchor naturally around key vocabulary themes: {', '.join(top_words[:5])}."
        )

        return VoiceProfile(
            name=profile_name,
            formality_level=formality,
            mean_sentence_length=mean_sentence_len,
            punctuation_style=punct,
            top_characteristic_words=top_words,
            perspective=perspective,
            rhetorical_habits=habits,
            prompt_injection_directive=directive,
        )
