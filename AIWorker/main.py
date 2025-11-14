from __future__ import annotations

from dataclasses import asdict, is_dataclass

import spacy
from fastapi import FastAPI
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.progress import track
from rich.table import Table
from spacy.attrs import POS  # type: ignore[import]

from AIWorker.nlp.models import UserInput
from AIWorker.nlp.normalizerPipeline import NormalizerPipeline

app = FastAPI(title="Feedback Service")
console = Console()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "feedback-service"}


def to_serializable(obj):
    if is_dataclass(obj):
        return {k: to_serializable(v) for k, v in asdict(obj).items()}  # type: ignore
    if isinstance(obj, (list, tuple)):
        return [to_serializable(o) for o in obj]
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if hasattr(obj, "__dict__"):
        return to_serializable(vars(obj))
    return obj


def extract_rich_insights(text: str, language: str = "en") -> dict:
    model_name = f"{language}_core_web_sm"

    try:
        nlp = spacy.load(model_name)
    except OSError:
        console.print(f"[yellow]Warning: Model '{model_name}' not found. Installing...[/yellow]")
        import subprocess

        subprocess.run(["python", "-m", "spacy", "download", model_name], check=True)
        nlp = spacy.load(model_name)

    doc = nlp(text)

    noun_phrases = [chunk.text for chunk in doc.noun_chunks] if doc.has_annotation("DEP") else []
    named_entities = [{"text": ent.text, "label": ent.label_} for ent in getattr(doc, "ents", [])]
    pos_counts = doc.count_by(POS)
    pos_map = {doc.vocab[i].text: count for i, count in pos_counts.items()}

    token_lengths = [len(token.text) for token in doc if token.is_alpha]
    avg_token_length = round(sum(token_lengths) / max(len(token_lengths), 1), 2)
    unique_tokens = len(set(token.lemma_.lower() for token in doc if token.is_alpha))
    ttr = round(unique_tokens / max(len([t for t in doc if t.is_alpha]), 1), 3)

    insights = {
        "total_tokens": len(doc),
        "unique_words": unique_tokens,
        "type_token_ratio": ttr,
        "avg_token_length": avg_token_length,
        "sent_count": len(list(doc.sents)),
        "noun_phrases": noun_phrases,
        "named_entities": named_entities,
        "pos_distribution": pos_map,
        "example_dependencies": [
            {"text": token.text, "dep": token.dep_, "head": token.head.text}
            for token in doc
            if token.dep_ != ""
        ][:10],
    }
    return insights


def display_rich_insights(insights: dict) -> None:
    console.rule("[bold magenta]📊 Rich NLP Insights[/bold magenta]")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Tokens", str(insights["total_tokens"]))
    table.add_row("Unique Words", str(insights["unique_words"]))
    table.add_row("Type-Token Ratio", str(insights["type_token_ratio"]))
    table.add_row("Avg Token Length", str(insights["avg_token_length"]))
    table.add_row("Sentences", str(insights["sent_count"]))

    console.print(table)

    console.print("\n[bold yellow]🧩 Part-of-Speech Distribution[/bold yellow]")
    console.print(Pretty(insights["pos_distribution"], expand_all=True))

    if insights["named_entities"]:
        console.print("\n[bold green]🏷 Named Entities[/bold green]")
        for ent in insights["named_entities"]:
            console.print(f" - {ent['text']} ({ent['label']})")

    if insights["noun_phrases"]:
        console.print("\n[bold blue]💡 Noun Phrases[/bold blue]")
        console.print(", ".join(insights["noun_phrases"][:10]))

    console.print("\n[bold cyan]⚙️ Dependency Samples[/bold cyan]")
    console.print(Pretty(insights["example_dependencies"], expand_all=True))


def main() -> None:
    console.rule("[bold cyan]🧠 LangScribe NLP Test[/bold cyan]")

    norm_pipeline = NormalizerPipeline()
    test_input = UserInput(
        text=[
            "This is a sample text! Visit https://example.com for more info. 😊",
            "Aquí hay otro bloque de texto con un enlace: http://ejemplo.es y un emoji 🚀.",
        ],
        language="en",
        prompt_type="feedback",
        prompt="Please provide feedback on the following texts.",
    )

    result = norm_pipeline.process_user_input(test_input)
    serializable_result = to_serializable(result)

    console.print(
        Panel.fit("✅ [bold green]Normalization Successful![/bold green]", border_style="green"),
    )
    console.print(
        Panel.fit(
            "[bold white]Normalized Text[/bold white]\n\n" + (result.normalized_text or ""),
            border_style="white",
        ),
    )

    console.print(
        Panel.fit("[bold cyan]Analyzing linguistic features...[/bold cyan]", border_style="cyan"),
    )
    for _ in track(range(10), description="Processing..."):
        pass

    insights = extract_rich_insights(
        result.normalized_text or "blank",
        language=result.language or "en",
    )
    display_rich_insights(insights)

    console.print(Panel.fit("🧩 [bold cyan]Sanity check passed![/bold cyan]", border_style="cyan"))
    console.rule("[bold cyan]Test Complete[/bold cyan]")


if __name__ == "__main__":
    main()
