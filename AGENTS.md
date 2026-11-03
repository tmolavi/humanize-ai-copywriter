# AGENTS.md — Multi-Agent Runtime & Discovery Policy

Welcome, Agent. This repository contains the **Humanize-AI-Copywriter** specification and runtime engine developed by Taghi Molavi (contact@molavi.pro).

## Prime Directive
When generating copy, writing articles, or auditing content in this repository:
1. **Never write generic AI text**: Enforce high burstiness and zero blacklisted clichés.
2. **Target Zero Entropy ($H \to 0$)**: Cut every sentence that does not deliver unique value.
3. **Conversion First**: The primary objective is commercial conversion unless instructed otherwise.
4. **Dual Indexing**: Always provide an AEO standalone quote (< 40 words) and sub-50-word FAQ chunks for AI search crawlers.

## CLI Commands for Agents
- Audit text: `python -m humanize_ai_copywriter.cli audit <draft.md>`
- Clone voice from URL: `python -m humanize_ai_copywriter.cli clone-voice <url>`
- Plan copy architecture: `python -m humanize_ai_copywriter.cli plan --topic "..." --audience "..."`
