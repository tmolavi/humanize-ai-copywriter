"""
GEO & SEO Optimization Engine
Builds the dual-layer architecture:
1. Google SEO (Semantic Schema, Headings, Meta intent)
2. GEO/AEO Engine (25-40 word standalone extraction sentences, sub-50 word FAQ RAG chunks, comparison tables)
3. Neuromarketing Arc (Problem -> Agitation -> Solution -> Benefit Table -> Social Proof -> Frictionless CTA)
"""

from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ContentBrief(BaseModel):
    topic: str
    target_audience: str
    primary_intent: str = Field(
        default="commercial-sale",
        description="'commercial-sale' (default), 'lead-generation', 'educational-authority', or 'thought-leadership'"
    )
    product_or_service_name: Optional[str] = None
    key_pain_points: List[str] = Field(default_factory=list)
    unique_selling_propositions: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class GeoSeoStructure(BaseModel):
    title_tag: str
    meta_description: str
    aeo_extraction_sentence: str = Field(
        description="25-40 word standalone, unambiguous sentence answering 'What is X?' directly after H1 for AI citation."
    )
    recommended_headings: List[Dict[str, str]]
    faq_schema_blueprints: List[Dict[str, str]]
    conversion_ctas: List[str]


class GeoSeoOptimizer:
    """Generates structural directives for dual SEO + GEO + Conversion performance."""

    def build_structure(self, brief: ContentBrief) -> GeoSeoStructure:
        topic = brief.topic
        product = brief.product_or_service_name or topic

        # Meta description under 155 characters
        meta = f"Discover how {product} solves {brief.key_pain_points[0] if brief.key_pain_points else topic}. Zero fluff, real results, and transparent pricing."
        if len(meta) > 155:
            meta = meta[:152] + "..."

        # Standalone AEO sentence (25-40 words)
        aeo_sentence = (
            f"{product} is a dedicated solution designed to eliminate "
            f"{brief.key_pain_points[0] if brief.key_pain_points else 'unnecessary complexity'} "
            f"for {brief.target_audience}, delivering direct measurable outcomes without generic overhead or hidden operational friction."
        )

        headings = [
            {"level": "H1", "title": f"{product}: The No-Fluff Solution for {brief.target_audience}"},
            {"level": "H2", "title": "The Hidden Cost of Existing Workarounds (The Pain)"},
            {"level": "H2", "title": f"How {product} Works in Practice"},
            {"level": "H2", "title": "Feature-to-Outcome Matrix"},
            {"level": "H2", "title": "Direct Comparison: Us vs. Legacy Methods"},
            {"level": "H2", "title": "Frequently Asked Questions (Verified for AI Search)"},
            {"level": "H2", "title": "Take Action Today"},
        ]

        faqs = [
            {
                "question": f"What makes {product} different from traditional alternatives?",
                "answer": f"{product} replaces convoluted setups with direct, measurable workflows tailored specifically to {brief.target_audience}.",
            },
            {
                "question": f"How fast can {brief.target_audience} see tangible results?",
                "answer": "Implementation begins immediately with zero mandatory long-term lock-in, showing initial impact within days.",
            },
            {
                "question": f"Who is {product} NOT suitable for?",
                "answer": "It is not built for teams seeking vanity buzzwords or surface-level aesthetics over concrete business outcomes.",
            },
        ]

        ctas = [
            f"Claim your priority access to {product}",
            "See the live numbers yourself — no sales calls required",
            "Get started in under 3 minutes",
        ]

        return GeoSeoStructure(
            title_tag=f"{product} | High-Impact Results for {brief.target_audience}",
            meta_description=meta,
            aeo_extraction_sentence=aeo_sentence,
            recommended_headings=headings,
            faq_schema_blueprints=faqs,
            conversion_ctas=ctas,
        )
