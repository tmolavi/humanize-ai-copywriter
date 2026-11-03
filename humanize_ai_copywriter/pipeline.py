"""
Full Orchestration Pipeline
Coordinates Voice Cloning, GeoSeo Optimization, Zero-Entropy refinement,
and Detector Bypass verification into a single seamless run.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from humanize_ai_copywriter.detector_bypass import DetectorBypassAuditor, AuditReport
from humanize_ai_copywriter.entropy_engine import ZeroEntropyEngine, EntropyAnalysis
from humanize_ai_copywriter.voice_cloner import VoiceToneCloner, VoiceProfile
from humanize_ai_copywriter.geo_seo_optimizer import GeoSeoOptimizer, ContentBrief, GeoSeoStructure


class PipelineResult(BaseModel):
    brief: ContentBrief
    voice_profile: Optional[VoiceProfile] = None
    structure: GeoSeoStructure
    audit_report: Optional[AuditReport] = None
    entropy_analysis: Optional[EntropyAnalysis] = None
    prompt_for_agent: str
    status: str = "success"


class HumanizeCopyPipeline:
    """End-to-end pipeline for zero-entropy, undetectable, conversion-first content generation."""

    def __init__(self):
        self.detector_auditor = DetectorBypassAuditor()
        self.entropy_engine = ZeroEntropyEngine()
        self.voice_cloner = VoiceToneCloner()
        self.geo_seo_optimizer = GeoSeoOptimizer()

    async def execute(
        self,
        brief: ContentBrief,
        sample_urls: Optional[List[str]] = None,
        sample_texts: Optional[List[str]] = None,
        existing_draft: Optional[str] = None,
    ) -> PipelineResult:
        # Step 1: Voice Tone Extraction
        voice_profile: Optional[VoiceProfile] = None
        collected_samples: List[str] = list(sample_texts or [])

        if sample_urls:
            for url in sample_urls:
                try:
                    fetched = await self.voice_cloner.fetch_url_text(url)
                    collected_samples.append(fetched)
                except Exception:
                    pass

        if collected_samples:
            voice_profile = self.voice_cloner.analyze_samples(collected_samples, profile_name="Extracted Client Voice")

        # Step 2: Build GEO/SEO and Neuromarketing Structure
        structure = self.geo_seo_optimizer.build_structure(brief)

        # Step 3: If draft provided, run full audits
        audit_report: Optional[AuditReport] = None
        entropy_analysis: Optional[EntropyAnalysis] = None
        if existing_draft:
            audit_report = self.detector_auditor.audit(existing_draft)
            entropy_analysis = self.entropy_engine.analyze(existing_draft)

        # Step 4: Construct Universal Agent Prompt
        voice_directive = (
            voice_profile.prompt_injection_directive
            if voice_profile
            else "Write with an authentic, grounded, and unapologetically direct senior human tone."
        )

        agent_prompt = f"""
# TASK: Write a Zero-Entropy, High-Conversion Article / Landing Page
- **Topic**: {brief.topic}
- **Audience**: {brief.target_audience}
- **Primary Intent**: {brief.primary_intent} (Persuasion to buy goods/services unless user specifies otherwise)
- **Product/Service**: {brief.product_or_service_name or brief.topic}

## VOICE DIRECTIVE
{voice_directive}

## DUAL GEO & SEO BLUEPRINT
- **H1**: {structure.recommended_headings[0]['title']}
- **AEO Standalone Extraction Hook (Insert directly under H1 in blockquote)**:
  > "{structure.aeo_extraction_sentence}"
- **Meta Description**: {structure.meta_description}

## SECTIONS TO WRITE
{chr(10).join(f"- {h['level']}: {h['title']}" for h in structure.recommended_headings)}

## CONVERSION FAQS (Verified for AI Search RAG Chunks, each answer < 50 words)
{chr(10).join(f"- Q: {faq['question']} | A: {faq['answer']}" for faq in structure.faq_schema_blueprints)}

## NON-NEGOTIABLE ANTI-AI RULES
1. Strict Burstiness: drastically alternate sentence lengths (e.g. a 3-word punch, followed by a detailed 28-word explanation).
2. Ban ALL AI clichés: no 'delve', 'tapestry', 'pivotal', 'in today\'s landscape', 'seamless', 'testament to'.
3. Zero fluff: every sentence must deliver unique proof, pain diagnosis, or direct actionable outcome.
4. No fake statistics or hallucinated guarantees. Honesty beats hype.
""".strip()

        return PipelineResult(
            brief=brief,
            voice_profile=voice_profile,
            structure=structure,
            audit_report=audit_report,
            entropy_analysis=entropy_analysis,
            prompt_for_agent=agent_prompt,
            status="success",
        )
