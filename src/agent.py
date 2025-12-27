from typing import List, Tuple

def agent_reason(query: str, evidence: List[Tuple[str, str]]) -> str:
    """
    Round-2 demo agent:
    - Takes a query
    - Uses evidence snippets from live store
    - Produces a clean, explainable answer (no LLM required)
    """
    if not query.strip():
        return "Ask me something. Tip: add notes into data/sample_docs/*.txt and then query keywords."

    if not evidence:
        return (
            "I couldn't find matching info in the live folder yet.\n"
            "Add/update a .txt/.md/.log file inside data/sample_docs and try again."
        )

    lines = []
    lines.append("AXION AI (Prototype Agent) — Answer")
    lines.append("")
    lines.append(f"Query: {query}")
    lines.append("")
    lines.append("What I found (live, from your updated files):")

    for i, (path, snippet) in enumerate(evidence, start=1):
        lines.append(f"{i}. Source: {path}")
        lines.append(f"   Snippet: {snippet}")
        lines.append("")

    lines.append("Draft Insight:")
    lines.append(
        "Based on the latest live notes above, the system would generate an updated response "
        "immediately when you edit/add files — demonstrating 'no stale knowledge' behavior."
    )

    return "\n".join(lines)
