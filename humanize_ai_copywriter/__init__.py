"""
humanize-ai-copywriter
~~~~~~~~~~~~~~~~~~~~~~
Universal Agent Skill & Framework for Zero-Entropy, Undetectable Human Copywriting,
High-Conversion Sales, and Empirical SEO/GEO Citations.

Author: Taghi Molavi (contact@molavi.pro)
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Taghi Molavi"

from humanize_ai_copywriter.detector_bypass import DetectorBypassAuditor
from humanize_ai_copywriter.entropy_engine import ZeroEntropyEngine
from humanize_ai_copywriter.voice_cloner import VoiceToneCloner
from humanize_ai_copywriter.geo_seo_optimizer import GeoSeoOptimizer
from humanize_ai_copywriter.pipeline import HumanizeCopyPipeline

__all__ = [
    "DetectorBypassAuditor",
    "ZeroEntropyEngine",
    "VoiceToneCloner",
    "GeoSeoOptimizer",
    "HumanizeCopyPipeline",
]
