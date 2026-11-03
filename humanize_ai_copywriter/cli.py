"""
Command-Line Interface for humanize-ai-copywriter
Provides audit, voice cloning, and zero-entropy planning commands.
"""

from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
from typing import List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from humanize_ai_copywriter import __version__
from humanize_ai_copywriter.detector_bypass import DetectorBypassAuditor
from humanize_ai_copywriter.entropy_engine import ZeroEntropyEngine
from humanize_ai_copywriter.voice_cloner import VoiceToneCloner
from humanize_ai_copywriter.geo_seo_optimizer import ContentBrief
from humanize_ai_copywriter.pipeline import HumanizeCopyPipeline

console = Console()


@click.group()
@click.version_option(__version__, message="%(prog)s v%(version)s — Author: Taghi Molavi (molavi.pro)")
def main():
    """Universal Agent Skill & CLI for Zero-Entropy, Undetectable Human Copywriting & SEO/GEO Citations."""
    pass


@main.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json-out", is_flag=True, help="Output pure JSON format")
def audit(file_path: Path, json_out: bool):
    """Audit an existing draft for AI fingerprints, Burstiness, and Entropy."""
    text = file_path.read_text(encoding="utf-8")
    auditor = DetectorBypassAuditor()
    entropy_engine = ZeroEntropyEngine()

    rep = auditor.audit(text)
    ent = entropy_engine.analyze(text)

    if json_out:
        out = {
            "audit": rep.model_dump(),
            "entropy": ent.model_dump(),
        }
        click.echo(json.dumps(out, indent=2, ensure_ascii=False))
        return

    console.print(Panel(f"[bold cyan]Audit Results for:[/] {file_path.name}", expand=False))

    # Metric Table
    table = Table(title="Linguistic & Detection Metrics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Score / Value", style="green")
    table.add_column("Target Benchmark", style="yellow")
    table.add_column("Status", style="bold")

    b_status = "[green]PASS[/]" if rep.burstiness_score >= 0.35 else "[red]FAIL[/]"
    table.add_row("Burstiness (Sentence Variance)", f"{rep.burstiness_score:.3f}", ">= 0.350", b_status)

    h_status = "[green]PASS[/]" if rep.predicted_human_score >= 90 else "[red]FAIL[/]"
    table.add_row("Predicted Human Score", f"{rep.predicted_human_score:.1f}%", ">= 90.0%", h_status)

    c_count = sum(int(c["matches_count"]) for c in rep.ai_cliches_found)
    c_status = "[green]PASS[/]" if c_count == 0 else "[red]FAIL[/]"
    table.add_row("AI Cliché Detections", str(c_count), "0", c_status)

    ld_status = "[green]PASS[/]" if ent.lexical_density_percent >= 52.0 else "[yellow]SUB-OPTIMAL[/]"
    table.add_row("Lexical Density", f"{ent.lexical_density_percent:.1f}%", ">= 52.0%", ld_status)

    console.print(table)

    if rep.ai_cliches_found:
        console.print("\n[bold red]Flagged AI Clichés & Human Replacements:[/]")
        for item in rep.ai_cliches_found:
            console.print(f"  • [red]'{item['pattern']}'[/] ({item['matches_count']}x) ➔ [green]{item['suggested_alternative']}[/]")

    if rep.suggestions:
        console.print("\n[bold yellow]Remediation Recommendations:[/]")
        for s in rep.suggestions:
            console.print(f"  ➜ {s}")


@main.command()
@click.option("--topic", prompt=True, help="Primary topic or subject")
@click.option("--audience", prompt=True, help="Target reader / buyer audience")
@click.option("--intent", default="commercial-sale", help="Primary intent: commercial-sale, educational-authority, etc.")
@click.option("--product", help="Name of product or service (if selling)")
@click.option("--sample-url", multiple=True, help="Sample URL(s) to clone brand voice from")
@click.option("--out", type=click.Path(dir_okay=False, path_type=Path), help="Save prompt to file")
def plan(
    topic: str,
    audience: str,
    intent: str,
    product: Optional[str],
    sample_url: tuple[str, ...],
    out: Optional[Path],
):
    """Generate a Zero-Entropy, Dual SEO/GEO Agent Prompt & Architecture."""
    brief = ContentBrief(
        topic=topic,
        target_audience=audience,
        primary_intent=intent,
        product_or_service_name=product,
    )
    pipeline = HumanizeCopyPipeline()
    res = asyncio.run(pipeline.execute(brief, sample_urls=list(sample_url)))

    if out:
        out.write_text(res.prompt_for_agent, encoding="utf-8")
        console.print(f"[bold green]Saved agent prompt to:[/] {out}")
    else:
        console.print(Panel(res.prompt_for_agent, title="[bold green]Universal Agent Prompt[/]", expand=False))


@main.command(name="clone-voice")
@click.argument("source", type=str)
def clone_voice(source: str):
    """Clone brand voice from a web URL or local text file."""
    cloner = VoiceToneCloner()
    if source.startswith("http://") or source.startswith("https://"):
        console.print(f"[cyan]Fetching content from:[/] {source}")
        text = asyncio.run(cloner.fetch_url_text(source))
    else:
        path = Path(source)
        if not path.exists():
            console.print(f"[red]Error:[/] File '{source}' does not exist.")
            sys.exit(1)
        text = path.read_text(encoding="utf-8")

    profile = cloner.analyze_samples([text], profile_name="Source Profile")

    console.print(Panel(f"[bold green]Voice Profile Cloned[/]\n"
                        f"• Formality: [cyan]{profile.formality_level}[/]\n"
                        f"• Perspective: [cyan]{profile.perspective}[/]\n"
                        f"• Avg Sentence Length: [cyan]{profile.mean_sentence_length} words[/]\n"
                        f"• Top Key Words: [yellow]{', '.join(profile.top_characteristic_words[:7])}[/]\n\n"
                        f"[bold yellow]Agent Directive:[/]\n{profile.prompt_injection_directive}",
                        title="Brand Voice Card", expand=False))


if __name__ == "__main__":
    main()
