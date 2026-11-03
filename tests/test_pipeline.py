import unittest
import asyncio
from humanize_ai_copywriter.detector_bypass import DetectorBypassAuditor
from humanize_ai_copywriter.entropy_engine import ZeroEntropyEngine
from humanize_ai_copywriter.voice_cloner import VoiceToneCloner
from humanize_ai_copywriter.geo_seo_optimizer import GeoSeoOptimizer, ContentBrief
from humanize_ai_copywriter.pipeline import HumanizeCopyPipeline


class TestHumanizeCopywriter(unittest.TestCase):
    def test_detector_auditor_detects_cliches(self):
        text = "In today's rapidly evolving landscape, we delve into a pivotal tapestry of solutions."
        auditor = DetectorBypassAuditor()
        report = auditor.audit(text)
        self.assertGreaterEqual(len(report.ai_cliches_found), 3)
        self.assertFalse(report.is_safe_from_detectors)

    def test_detector_auditor_passes_clean_human_text(self):
        text = (
            "We build clean databases. That is the point. When connections hit twenty thousand, "
            "PostgreSQL locks your tables if your foreign key lacks an index, leading to total API failure. "
            "Fix it now."
        )
        auditor = DetectorBypassAuditor()
        report = auditor.audit(text)
        self.assertEqual(len(report.ai_cliches_found), 0)
        self.assertGreater(report.burstiness_score, 0.30)

    def test_entropy_engine_lexical_density(self):
        text = "High performance database engines require deterministic memory allocation and zero garbage collection spikes."
        engine = ZeroEntropyEngine()
        analysis = engine.analyze(text)
        self.assertGreater(analysis.lexical_density_percent, 50.0)

    def test_voice_cloner_perspective_and_cadence(self):
        samples = [
            "I test every script personally. Why? Because automated tests miss subtle memory leaks. Don't trust abstractions."
        ]
        cloner = VoiceToneCloner()
        profile = cloner.analyze_samples(samples)
        self.assertIn("first-person-singular", profile.perspective)
        self.assertGreater(profile.mean_sentence_length, 0)

    def test_full_pipeline_execution(self):
        brief = ContentBrief(
            topic="FastAPI Microservice Caching",
            target_audience="Backend Developers",
            primary_intent="commercial-sale",
            product_or_service_name="cache-pilot",
            key_pain_points=["Redis connection saturation under high load"],
        )
        pipeline = HumanizeCopyPipeline()
        res = asyncio.run(pipeline.execute(brief))
        self.assertEqual(res.status, "success")
        self.assertIn("cache-pilot", res.prompt_for_agent)
        self.assertGreaterEqual(len(res.structure.faq_schema_blueprints), 3)


if __name__ == "__main__":
    unittest.main()
